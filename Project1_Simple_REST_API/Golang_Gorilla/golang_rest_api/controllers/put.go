package controllers

import (
	"golang_rest_api/models"
	"golang_rest_api/utils"
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

// Update handles PUT requests to update todos
func (t *Todos) Update(w http.ResponseWriter, r *http.Request) {
	acc, err := t.getTokenAndUser(w, r)
	tid := getTodoID(r)
	// fetch the todos from the context
	todo := r.Context().Value(KeyTodo{}).(*models.Todo)
	todo.ID = tid
	t.l.Println("[DEBUG] updating todo with id", todo.ID)
	todo.UserID = acc.ID
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
