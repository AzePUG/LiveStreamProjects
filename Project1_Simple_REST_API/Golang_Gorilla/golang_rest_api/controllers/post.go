package controllers

import (
	"golang_restful_api/models"
	"golang_restful_api/utils"
	"net/http"
)

// Create handles POST requests to add new users
func (a *Users) Create(w http.ResponseWriter, r *http.Request) {
	// fetch the user from the context
	acc := r.Context().Value(KeyUser{}).(*models.User)
	err := a.us.CreateUser(acc)
	if err != nil {
		a.l.Println("[ERROR] Something went wrong with user creation", err)
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: "Something went wrong with user creation"})
		return
	}
	w.WriteHeader(http.StatusCreated)
	a.l.Printf("[DEBUG] Inserting user: %#v\n", acc)
}
