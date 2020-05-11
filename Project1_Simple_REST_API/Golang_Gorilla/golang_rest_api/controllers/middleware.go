package controllers

import (
	"context"
	"errors"
	"net/http"
	"regexp"

	"fmt"
	"golang_restful_api/models"
	"golang_restful_api/utils"
	"golang_restful_api/auth"

)

//type genF = func(*GenHandler, http.Handler) http.Handler

//type tdF  func(*Todos, http.Handler) http.Handler
type GenHandler struct {
	*Users
	*Todos
}

//var uRLPathRegex = map[string]interface{}{
//	"^/api/v1/users$": (*GenHandler).MiddlewareValidateUser,
//	//"^/api/v1/users/(?P<v0>[0-9]+)/todos$": (*GenHandler).MiddlewareValidateTodo,
// }

var uRLPathRegex = map[string]string{
	"^/api/v1/users$":                      "users",
	"^/api/v1/users/(?P<v0>[0-9]+)$":		"users",
	"^/api/v1/users/(?P<v0>[0-9]+)/todos$": "todos",
	"^/api/v1/users/(?P<v0>[0-9]+)/todos/(?P<v0>[0-9]+)$": "todos",
}

// CommonMiddleware for updating default content type for our router
func CommonMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	})
}

// SetMiddlewareAuthentication ...
func SetMiddlewareAuthentication(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		err := auth.TokenValid(r)
		if err != nil {
			w.WriteHeader(http.StatusUnauthorized)
			utils.Respond(w, &GenericError{Message: err.Error()})
			return
		}
		next.ServeHTTP(w, r)
	})
}

// MiddlewareValidate general middleware method for calling specific validations based on path.
func (g *GenHandler) MiddlewareValidate(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var getURLPath = r.URL.Path
		for patt, val := range uRLPathRegex {
			match, _ := regexp.MatchString(patt, getURLPath)
			if match && val == "users" {
				g.MiddlewareValidateUser(next, w, r)
				break
			} else {
				g.MiddlewareValidateTodo(next, w, r)
				break
			}
		}
	})
}

// MiddlewareValidateUser validates the user in the request and calls next if ok
func (a *GenHandler) MiddlewareValidateUser(next http.Handler, w http.ResponseWriter, r *http.Request) error {
	acc := &models.User{}
	err := models.FromJSON(acc, r.Body)
	if err != nil {
		a.Users.l.Println("[ERROR] deserializing user", err)

		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return err
	}

	// validate the user
	errs := a.Users.v.Validate(acc)
	a.Users.l.Println("Here: ", errs.Errors())
	if len(errs) != 0 {
		a.Users.l.Println("[ERROR] validating user", errs)

		// return the validation messages as an array
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &ValidationError{Messages: errs.Errors()})
		return err
	}

	// add the user to the context
	ctx := context.WithValue(r.Context(), KeyUser{}, acc)
	r = r.WithContext(ctx)
	fmt.Println(r)
	// Call the next handler, which can be another middleware in the chain, or the final handler.
	next.ServeHTTP(w, r)
	//})
	return nil
}

// MiddlewareValidateTodo validates the todos in the request and calls next if ok
func (g *GenHandler) MiddlewareValidateTodo(next http.Handler, w http.ResponseWriter, r *http.Request) error {
	todo := &models.Todo{}
	err := models.FromJSON(todo, r.Body)
	if err != nil {
		g.Todos.l.Println("[ERROR] deserializing todo", err)

		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return err
	}

	// validate the todos
	errs := g.Todos.v.Validate(todo)
	if len(errs) != 0 {
		g.Todos.l.Println("[ERROR] validating todo", errs)

		// return the validation messages as an array
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &ValidationError{Messages: errs.Errors()})
		return err
	}

	// add the todos to the context
	ctx := context.WithValue(r.Context(), KeyTodo{}, todo)
	r = r.WithContext(ctx)

	// Call the next handler, which can be another middleware in the chain, or the final handler.
	next.ServeHTTP(w, r)
	return nil
}
