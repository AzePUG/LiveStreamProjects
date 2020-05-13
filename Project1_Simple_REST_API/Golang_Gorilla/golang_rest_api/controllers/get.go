package controllers

import (
	"golang_restful_api/auth"
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
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	default:
		a.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusInternalServerError)
		utils.Respond(w, &GenericError{Message: err.Error()})
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
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	default:
		a.l.Println("[ERROR] fetching user", err)

		w.WriteHeader(http.StatusInternalServerError)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}

	err = utils.Respond(w, acc)
	if err != nil {
		// we should never be here but log the error just incase
		a.l.Println("[ERROR] serializing user", err)
	}
}

// ListAll handles GET requests and returns all current todos for a given user
func (t *Todos) ListAll(w http.ResponseWriter, r *http.Request) {
	t.l.Println("[DEBUG] get all records")

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

	todos, err := t.ts.GetTodos(acc)
	if err != nil {
		// TODO: do better error checking
		t.l.Println("[ERROR] fetching todos", err)
		w.WriteHeader(http.StatusInternalServerError)
		utils.Respond(w, &GenericError{Message: err.Error()})
	}

	err = utils.Respond(w, todos)
	if err != nil {
		// we should never be here but log the error just incase
		t.l.Println("[ERROR] serializing todos", err)
	}
}

// ListSingle handles GET requests
func (t *Todos) ListSingle(w http.ResponseWriter, r *http.Request) {
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
	todo, err := t.ts.GetTodoByID(acc, tid)
	switch err {
	case nil:

	case models.ErrNotFound:
		t.l.Println("[ERROR] fetching todo", err)

		w.WriteHeader(http.StatusNotFound)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	default:
		t.l.Println("[ERROR] fetching todo", err)

		w.WriteHeader(http.StatusInternalServerError)
		utils.Respond(w, &GenericError{Message: err.Error()})
		return
	}
	err = utils.Respond(w, todo)
	if err != nil {
		// we should never be here but log the error just incase
		t.l.Println("[ERROR] serializing todos", err)
	}
}