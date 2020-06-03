package controllers

import (
	"context"
	"net/http"
	"regexp"

	"golang_rest_api/auth"
	"golang_rest_api/models"
	"golang_rest_api/utils"
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
	"^/api/v1/users$":                                     "users",
	"^/api/v1/users/(?P<v0>[0-9]+)$":                      "users",
	"^/api/v1/users/todos$":                			   "todos",
	"^/api/v1/users/todos/(?P<v0>[0-9]+)$": 			   "todos",
	"^/api/v1/users/login$":                               "login",
}

// CommonMiddleware for updating default content type for our router
func CommonMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	})
}

// SetMiddlewareAuthentication ...
func (g *GenHandler) SetMiddlewareAuthentication(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, err := auth.TokenValid(r)
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
			} else if match && val == "todos" {
				// TODO: seems to be the first check does not work.
				g.SetMiddlewareAuthentication(next)
				g.MiddlewareValidateTodo(next, w, r)
				break
			} else if match && val == "login" {
				// Matching /login then
				g.MiddlewareValidateLogin(next, w, r)
				break
			}
		}
	})
}

func (g *GenHandler) MiddlewareValidateLogin(next http.Handler, w http.ResponseWriter, r *http.Request)  {
	login := &models.Login{}
	err := models.FromJSON(login, r.Body)
	if err != nil {
		g.Users.l.Println("[ERROR] deserialize user login credentials", err)
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}
	g.Users.l.Println("Pre-Validation: ", login)


	// validate the user
	errs := g.Users.v.Validate(login)
	if len(errs) != 0 {
		g.Users.l.Println("[ERROR] validating user login credentials", errs)
		// return the validation messages as an array
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &ValidationError{Messages: errs.Errors()})
		return
	}
	// Add login credentials to the context.
	g.Users.l.Println("Post-Validation: ", login)
	ctx := context.WithValue(r.Context(), KeyLogin{}, login)
	r = r.WithContext(ctx)
	// Call the next handler, which can be another middleware in the chain, or the final handler.
	// TODO: this will fail
	next.ServeHTTP(w, r)
	return
}

// MiddlewareValidateUser validates the user in the request and calls next if ok
func (g *GenHandler) MiddlewareValidateUser(next http.Handler, w http.ResponseWriter, r *http.Request) {
	acc := &models.User{}
	err := models.FromJSON(acc, r.Body)
	if err != nil {
		g.Users.l.Println("[ERROR] deserializing user", err)

		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}

	// validate the user
	errs := g.Users.v.Validate(acc)
	if len(errs) != 0 {
		g.Users.l.Println("[ERROR] validating user", errs)

		// return the validation messages as an array
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &ValidationError{Messages: errs.Errors()})
		return
	}

	// add the user to the context
	ctx := context.WithValue(r.Context(), KeyUser{}, acc)
	r = r.WithContext(ctx)
	// Call the next handler, which can be another middleware in the chain, or the final handler.
	next.ServeHTTP(w, r)

}

// MiddlewareValidateTodo validates the todos in the request and calls next if ok
func (g *GenHandler) MiddlewareValidateTodo(next http.Handler, w http.ResponseWriter, r *http.Request)  {
	todo := &models.Todo{}
	err := models.FromJSON(todo, r.Body)
	if err != nil {
		g.Todos.l.Println("[ERROR] deserializing todo", err)

		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}

	// validate the todos
	errs := g.Todos.v.Validate(todo)
	if len(errs) != 0 {
		g.Todos.l.Println("[ERROR] validating todo", errs)

		// return the validation messages as an array
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &ValidationError{Messages: errs.Errors()})
		return
	}

	// add the todos to the context
	ctx := context.WithValue(r.Context(), KeyTodo{}, todo)
	r = r.WithContext(ctx)

	// Call the next handler, which can be another middleware in the chain, or the final handler.
	next.ServeHTTP(w, r)
}
