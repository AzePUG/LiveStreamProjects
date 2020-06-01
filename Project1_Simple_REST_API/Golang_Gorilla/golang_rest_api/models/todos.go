package models

import (
	"github.com/jinzhu/gorm"
)

type Todo struct {
	gorm.Model
	Title       string `json:"title" validate:"required,min=5,max=20" gorm:"type:varchar(20);not null;default:null"`
	Description string `json:"description" validate:"required,min=10,max=100" gorm:"type:varchar(100);not null;default:null"`
	UserID      uint   `json:"-" gorm:"not null"`
}

// TodoDB interface for holding all direct database related actions

type TodoDB interface {
	// Methods for querying todos
	GetTodos(user *User) ([]*Todo, error)
	GetTodoByID(user *User, id uint) (*Todo, error)

	// Methods for altering the todos
	UpdateTodo(user *User, todo *Todo, id uint) error
	AddTodo(td *Todo) error
	DeleteTodo(user *User, id uint) error
}

type TodoService interface {
	TodoDB
}

// NewTodoService creating todo service here
func NewTodoService(db *gorm.DB) TodoService {
	tg := &todoGorm{db}
	return &todoService{
		TodoDB: tg,
	}
}

var _ TodoService = &todoService{}

type todoService struct {
	TodoDB
}

var _ TodoDB = &todoGorm{}

type todoGorm struct {
	db *gorm.DB
}

func (tg *todoGorm) GetTodos(user *User) ([]*Todo, error) {
	var todos []*Todo
	err := tg.db.Model(&user).Related(&todos).Error
	return todos, err
}

func (tg *todoGorm) GetTodoByID(user *User, id uint) (*Todo, error) {
	var todo Todo
	var todos []*Todo
	db := tg.db.Model(&user).Related(&todos).Where("id = ?", id)
	//db := tg.db.Where("id = ?", id)
	err := first(db, &todo)
	return &todo, err
}

// Update the record in todo table i.e given new todo model
func (tg *todoGorm) UpdateTodo(user *User, todo *Todo, id uint) error {
	todos, err := tg.GetTodoByID(user, id)
	if err != nil {
		return err
	}
	todos = todo
	return tg.db.Save(todos).Error
}

// Create will create provided todo and backfill data
// like the ID, CreatedAt etc.
func (tg *todoGorm) AddTodo(todo *Todo) error {
	return tg.db.Create(todo).Error
}

// Delete the user with provided ID
func (tg *todoGorm) DeleteTodo(user *User, id uint) error {
	todo, err := tg.GetTodoByID(user, id)
	if err != nil {
		return err
	}
	tg.db.Delete(&todo)
	return nil
}
