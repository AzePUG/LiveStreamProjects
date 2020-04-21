package controllers

import (
	"golang_restful_api/models"
	"net/http"
)

// Update handles PUT requests to update users
func (a *Users) Update(w http.ResponseWriter, r *http.Request) {
	id := getUserID(r)
	a.l.Println("[DEBUG] get record id", id)

	// fetch the user from the context
	acc := r.Context().Value(KeyUser{}).(*models.User)
	acc.ID = id
	a.l.Println("[DEBUG] updating user with id", acc.ID)

	err := a.us.UpdateUser(acc)

	if err == models.ErrNotFound {
		a.l.Println("[ERROR] user not found", err)

		w.WriteHeader(http.StatusNotFound)
		models.ToJSON(&GenericError{Message: "User not found in database"}, w)
		return
	}

	// write the no content success header
	w.WriteHeader(http.StatusNoContent)
}
