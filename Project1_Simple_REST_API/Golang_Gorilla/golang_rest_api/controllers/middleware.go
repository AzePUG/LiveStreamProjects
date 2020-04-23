package controllers

import (
	"context"
	"net/http"

	"golang_restful_api/models"
	"golang_restful_api/utils"
)

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
