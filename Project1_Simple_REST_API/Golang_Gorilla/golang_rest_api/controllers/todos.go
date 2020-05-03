package controllers

import (
	"golang_restful_api/models"
	"log"
)

// KeyUser is a key used for the Todo object in the context
type KeyTodo struct{}

// Users handler/controller for getting and updating users
type Todos struct {
	l  *log.Logger
	v  *models.Validation
	ts models.TodoService
	us models.UserService
}

// NewUsers returns a new users handler with the given logger
func NewTodos(l *log.Logger, v *models.Validation,
	ts models.TodoService, us models.UserService) *Todos {
	return &Todos{
		l:  l,
		v:  v,
		ts: ts,
		us: us,
	}
}
