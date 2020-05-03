package models

import "github.com/jinzhu/gorm"

type Todo struct {
	gorm.Model
	Title       string `json:"title" validate:"required,min=5,max=20" gorm:"not null"`
	Description string `json:"description" validate:"required,min=10,max=100" gorm:"not null"`
	UserID      uint   `json:"-"`
}

// TodoDB interface for holding all direct database related actions

type TodoDB interface {
	// Methods for querying todos
	GetTodos() ([]*Todo, error)
	GetTodoByID(id uint) (*Todo, error)

	// Methods for altering the todos
	UpdateTodo(td *Todo) error
	AddTodo(td *Todo) error
	DeleteTodo(id uint) error
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

func (tg *todoGorm) GetTodos() ([]*Todo, error) {
	var todo []*Todo
	err := tg.db.Find(&todo).Error
	return todo, err
}

func (tg *todoGorm) GetTodoByID(id uint) (*Todo, error) {
	var todo Todo
	db := tg.db.Where("id = ?", id)
	err := first(db, &todo)
	return &todo, err
}

// Update the record in todo table i.e given new todo model
func (tg *todoGorm) UpdateTodo(todo *Todo) error {
	return tg.db.Save(todo).Error
}

// Create will create provided todo and backfill data
// like the ID, CreatedAt etc.
func (tg *todoGorm) AddTodo(todo *Todo) error {
	return tg.db.Create(todo).Error
}

// Delete the user with provided ID
func (tg *todoGorm) DeleteTodo(id uint) error {
	todo, err := tg.GetTodoByID(id)
	if err != nil {
		return err
	}
	tg.db.Delete(&todo)
	return nil
}
