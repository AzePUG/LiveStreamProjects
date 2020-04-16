package controllers

import (
	"golang_restful_api/models"
	"net/http"
)

// Create handles POST requests to add new users
func (a *Users) Create(w http.ResponseWriter, r *http.Request) {
	// fetch the user from the context
	acc := r.Context().Value(KeyUser{}).(*models.User)
	models.AddUser(acc)
	a.l.Printf("[DEBUG] Inserting user: %#v\n", acc)
}
