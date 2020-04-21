package controllers

import (
	"golang_restful_api/models"
	"golang_restful_api/utils"
	"net/http"
)

// ListAll handles GET requests and returns all current users
func (a *Users) ListAll(w http.ResponseWriter, r *http.Request) {
	a.l.Println("[DEBUG] get all records")

	accs, err := a.us.GetUsers()
	switch err {
	case nil:

	case models.ErrNotFound:
		a.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusNotFound)
		models.ToJSON(&GenericError{Message: err.Error()}, w)
		return
	default:
		a.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusInternalServerError)
		models.ToJSON(&GenericError{Message: err.Error()}, w)
		return
	}
	//err := models.ToJSON(accs, w)
	err = utils.Respond(w, accs)
	if err != nil {
		// we should never be here but log the error just incase
		a.l.Println("[ERROR] serializing user", err)
	}
}

// ListSingle handles GET requests
func (a *Users) ListSingle(w http.ResponseWriter, r *http.Request) {
	// Get the id from request -> URL
	id := getUserID(r)

	a.l.Println("[DEBUG] get record id", id)

	acc, err := a.us.GetUserByID(id)

	switch err {
	case nil:

	case models.ErrNotFound:
		a.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusNotFound)
		models.ToJSON(&GenericError{Message: err.Error()}, w)
		return
	default:
		a.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusInternalServerError)
		models.ToJSON(&GenericError{Message: err.Error()}, w)
		return
	}

	err = utils.Respond(w, acc)
	if err != nil {
		// we should never be here but log the error just incase
		a.l.Println("[ERROR] serializing user", err)
	}
}
