package controllers

import (
	"golang_restful_api/models"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

// KeyUser is a key used for the User object in the context
type KeyUser struct{}

// Users handler/controller for getting and updating users
type Users struct {
	l  *log.Logger
	v  *models.Validation
	us models.UserService
}

// NewUsers returns a new users handler with the given logger
func NewUsers(l *log.Logger, v *models.Validation, us models.UserService) *Users {
	return &Users{
		l:  l,
		v:  v,
		us: us,
	}
}

// GenericError is a generic error message returned by a server
type GenericError struct {
	Message             string `json:"message"`
	http.ResponseWriter `json:"-"`
}

// ValidationError is a collection of validation error messages
type ValidationError struct {
	Messages            []string `json:"messages"`
	http.ResponseWriter `json:"-"`
}

// getUserID returns the user ID from the URL
// Panics if cannot convert the id into an integer
// this should never happen as the router ensures that
// this is a valid number
func getUserID(r *http.Request) uint {
	// parse the user id from the url
	vars := mux.Vars(r)

	// convert the id into an integer and return
	id, err := strconv.Atoi(vars["id"])
	if err != nil {
		// should never happen
		panic(err)
	}

	return uint(id)
}
