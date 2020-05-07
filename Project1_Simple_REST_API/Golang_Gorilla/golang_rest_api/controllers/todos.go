package controllers

import (
	"github.com/gorilla/mux"
	"golang_restful_api/models"
	"log"
	"net/http"
	"strconv"
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

// Function for getting todos id from url
func getTodoID(r *http.Request) uint {
	// parse the user id from the url
	vars := mux.Vars(r)

	// convert the id into an integer and return
	tid, err := strconv.Atoi(vars["tid"])
	if err != nil {
		// should never happen
		panic(err)
	}

	return uint(tid)
}