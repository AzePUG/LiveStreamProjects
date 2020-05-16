package controllers

import (
	"golang_restful_api/auth"
	"golang_restful_api/models"
	"golang_restful_api/utils"
	"net/http"
)

// Delete handles DELETE requests and removes items from the database
func (a *Users) Delete(w http.ResponseWriter, r *http.Request) {
	id := getUserID(r)

	a.l.Println("[DEBUG] deleting record id", id)

	err := a.us.DeleteUser(id)
	if err == models.ErrNotFound {
		a.l.Println("[ERROR] deleting record id does not exist")

		w.WriteHeader(http.StatusNotFound)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}

	if err != nil {
		a.l.Println("[ERROR] deleting record", err)

		w.WriteHeader(http.StatusInternalServerError)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// Delete handles DELETE requests and removes items from the database
func (t *Todos) Delete(w http.ResponseWriter, r *http.Request) {
	userID, err := auth.ExtractTokenID(r)
	if err != nil {
		t.l.Println("[ERROR] Something went wrong with token parsing", err)
		w.WriteHeader(http.StatusUnprocessableEntity)
		utils.Respond(w, &GenericError{Message: "Something went wrong with token parsing"})
		return
	}
	t.l.Println("[DEBUG] get record id", userID)

	acc, err := t.us.GetUserByID(userID)

	switch err {
	case nil:

	case models.ErrNotFound:
		t.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusNotFound)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	default:
		t.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusInternalServerError)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}

	tid := getTodoID(r)
	t.l.Println("[DEBUG] deleting record id", tid)

	err = t.ts.DeleteTodo(acc, tid)
	if err == models.ErrNotFound {
		t.l.Println("[ERROR] deleting record id does not exist")

		w.WriteHeader(http.StatusNotFound)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}

	if err != nil {
		t.l.Println("[ERROR] deleting record", err)

		w.WriteHeader(http.StatusInternalServerError)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}

	w.WriteHeader(http.StatusNoContent)
}