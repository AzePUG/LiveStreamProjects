package models

import (
	"fmt"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
)

// ServicesConfig type for holding Services function object
type ServicesConfig func(*Services) error

// WithGorm for activating databse connection
func WithGorm(dialect, connectionInfo string) ServicesConfig {
	return func(s *Services) error {
		db, err := gorm.Open(dialect, connectionInfo)
		if err != nil {
			return err
		}
		s.db = db
		return nil
	}
}

// WithUser function for activating UserService
func WithUser(pepper string) ServicesConfig {
	return func(s *Services) error {
		s.User = NewUserService(s.db, pepper)
		return nil
	}
}

// WithTodo function for activating TodoService
func WithTodo() ServicesConfig {
	return func(s *Services) error {
		s.Todo = NewTodoService(s.db)
		return nil
	}
}

// NewServices will loop through all passed services
func NewServices(cfgs ...ServicesConfig) (*Services, error) {
	var s Services
	for _, cfg := range cfgs {
		if err := cfg(&s); err != nil {
			return nil, err
		}
	}
	return &s, nil
}

// Services type for holding all kind of services
// i.e if you are going to add some new Gallery, Book or other service add it
// there
type Services struct {
	User UserService
	Todo TodoService
	db   *gorm.DB
}

// Close closes the database connection
func (s *Services) Close() error {
	return s.db.Close()
}

// DB return the db connection
func (s *Services) DB() *gorm.DB {
	fmt.Println(s.db)
	return s.db
}

// DestructiveReset drops all tables and rebuilds them
// FOR DEVELOPMENT
func (s *Services) DestructiveReset() (error, error) {
	err := s.db.DropTableIfExists(&User{}, &Todo{}).Error
	if err != nil {
		return err, nil
	}
	return s.AutoMigrateUser(), s.AutoMigrateTodo()
}

// // AutoMigrateUser will attempt automatically migrate user table
func (s *Services) AutoMigrateUser() error {
	return s.db.AutoMigrate(&User{}).Error
}

// AutoMigrateTodo will attempt automatically migrate
func (s *Services) AutoMigrateTodo() error {
	return s.db.AutoMigrate(Todo{}).AddForeignKey("user_id", "users(id)", "RESTRICT", "RESTRICT").Error
}
