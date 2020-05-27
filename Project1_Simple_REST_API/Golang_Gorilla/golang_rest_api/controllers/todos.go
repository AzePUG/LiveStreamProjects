package controllers

import (
	"github.com/gorilla/mux"
	"golang_rest_api/auth"
	"golang_rest_api/models"
	"golang_rest_api/utils"
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

// Function to get the user_id from JWT token and search it in database
func (t *Todos) getTokenAndUser(w http.ResponseWriter, r *http.Request) (*models.User, error) {
	userID, err := auth.ExtractTokenID(r)
	if err != nil {
		t.l.Println("[ERROR] Something went wrong with token parsing", err)
		w.WriteHeader(http.StatusUnprocessableEntity)
		utils.Respond(w, &GenericError{Message: "Something went wrong with token parsing"})
		return nil, err
	}
	t.l.Println("[DEBUG] get record id", userID)

	acc, err := t.us.GetUserByID(userID)

	switch err {
	case nil:

	case models.ErrNotFound:
		t.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusNotFound)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return nil, err
	default:
		t.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusInternalServerError)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return nil, err
	}

	return acc, nil
}