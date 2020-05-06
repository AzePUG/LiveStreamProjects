package controllers

import (
	"context"
	"net/http"
	"reflect"
	"regexp"

	"fmt"
	"golang_restful_api/models"
	"golang_restful_api/utils"
)

//type fn func(interface{}, http.Handler) http.Handler

//type usF = func(*interface{}, http.Handler) http.Handler
//type tdF = func(*interface{}, http.Handler) http.Handler

var uRLPathRegex = map[string]interface{}{
	"^/api/v1/users$": (*Users).MiddlewareValidateUser,
	"^/api/v1/users/(?P<v0>[0-9]+)/todos$": (*Todos).MiddlewareValidateTodo,
 }

// CommonMiddleware for updating default content type for our router
func CommonMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	})
}

// TODO: make single point validation middleware and call related specific validation from there
// func MiddlewareValidate(opts ...)
func MiddlewareValidate(next http.Handler) http.Handler{
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var getURLPath = r.URL.Path
		fmt.Println(getURLPath)
		fmt.Println(reflect.TypeOf(Users{}).String())
		for patt, fn := range uRLPathRegex {
			match, _ := regexp.MatchString(patt, getURLPath)
			if match {
				fmt.Println("hello", fn)
				Invoke(fn, next)
			}

		}
		next.ServeHTTP(w, r)
	})
}

func Invoke(fn interface{}, args ...interface{}) {
	//v := reflect.ValueOf(fn)
	//v.Call(reflect.Value(args[0]))

	v := reflect.ValueOf(fn)
	fmt.Println(reflect.TypeOf(v))
	fmt.Println(reflect.TypeOf(fn))
	fmt.Println(args)
	fmt.Println(reflect.TypeOf(args))
	fmt.Println(len(args))

	//rArgs := []reflect.Value{reflect.ValueOf(args)}
	//rArgs := make([]reflect.Value, 1)
	rArgs := []reflect.Value{reflect.ValueOf(args)}
	fmt.Println(rArgs)
	//for i, a := range args {
	//	rArgs[i] = reflect.ValueOf(a)
	//}
	fmt.Println(rArgs)
	//rArgs[0] = args[0]
	v.Call(rArgs)
}

// MiddlewareValidateUser validates the user in the request and calls next if ok
func (a *Users) MiddlewareValidateUser(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		acc := &models.User{}

		err := models.FromJSON(acc, r.Body)
		if err != nil {
			a.l.Println("[ERROR] deserializing user", err)

			w.WriteHeader(http.StatusBadRequest)
			utils.Respond(w, &GenericError{Message: err.Error()})
			return
		}

		// validate the user
		errs := a.v.Validate(acc)
		a.l.Println(errs.Errors())
		if len(errs) != 0 {
			a.l.Println("[ERROR] validating user", errs)

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
	})
}

// MiddlewareValidateTodo validates the todo in the request and calls next if ok
func (t *Todos) MiddlewareValidateTodo(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		todo := &models.Todo{}

		err := models.FromJSON(todo, r.Body)
		if err != nil {
			t.l.Println("[ERROR] deserializing todo", err)

			w.WriteHeader(http.StatusBadRequest)
			utils.Respond(w, &GenericError{Message: err.Error()})
			return
		}

		// validate the todo
		errs := t.v.Validate(todo)
		t.l.Println(errs.Errors())
		if len(errs) != 0 {
			t.l.Println("[ERROR] validating todo", errs)

			// return the validation messages as an array
			w.WriteHeader(http.StatusBadRequest)
			utils.Respond(w, &ValidationError{Messages: errs.Errors()})
			return
		}

		// add the todo to the context
		ctx := context.WithValue(r.Context(), KeyTodo{}, todo)
		r = r.WithContext(ctx)

		// Call the next handler, which can be another middleware in the chain, or the final handler.
		next.ServeHTTP(w, r)
	})
}
