package controllers

import (
	"golang_restful_api/models"
	"golang_restful_api/utils"
	"net/http"
)

// Delete handles DELETE requests and removes items from the database
func (a *Users) Delete(w http.ResponseWriter, r *http.Request) {
	id := getUserID(r)

	a.l.Println("[DEBUG] deleting record id", id)

	err := models.DeleteUser(id)
	if err == models.ErrUserNotFound {
		a.l.Println("[ERROR] deleting record id does not exist")

		w.WriteHeader(http.StatusNotFound)
		//models.ToJSON(&GenericError{Message: err.Error()}, w)
		utils.Respond(&GenericError{Message: err.Error()}, w)
		return
	}

	if err != nil {
		a.l.Println("[ERROR] deleting record", err)

		w.WriteHeader(http.StatusInternalServerError)
		models.ToJSON(&GenericError{Message: err.Error()}, w)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}
