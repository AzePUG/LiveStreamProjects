package controllers

import (
	"golang_restful_api/auth"
	"golang_restful_api/models"
	"golang_restful_api/utils"
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
		utils.Respond(w, &GenericError{Message: "User not found in database"})
		return
	}

	// write the no content success header
	w.WriteHeader(http.StatusNoContent)
}

// Update handles PUT requests to update users
func (t *Todos) Update(w http.ResponseWriter, r *http.Request) {
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
	// fetch the todos from the context
	todo := r.Context().Value(KeyTodo{}).(*models.Todo)
	todo.ID = tid
	t.l.Println("[DEBUG] updating todo with id", todo.ID)
	todo.UserID = userID
	err = t.ts.UpdateTodo(acc, todo, tid)

	if err == models.ErrNotFound {
		t.l.Println("[ERROR] todo not found", err)

		w.WriteHeader(http.StatusNotFound)
		utils.Respond(w, &GenericError{Message: "Todo not found in database"})
		return
	}

	// write the no content success header
	w.WriteHeader(http.StatusNoContent)
}
