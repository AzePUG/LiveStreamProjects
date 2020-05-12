package controllers

import (
	"fmt"
	"golang_restful_api/auth"
	"golang_restful_api/models"
	"golang_restful_api/utils"
	"net/http"
)

type KeyLogin struct{}

func (us *Users) Login(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Inside Login handler")
	login := r.Context().Value(KeyLogin{}).(*models.Login)
	foundUser, err := us.us.Authenticate(login.Email, login.Password)
	if err != nil {
		us.l.Println("[ERROR] Something went wrong with user authentication", err)
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: "Something went wrong with user authentication"})
		return
	}
	token, err := auth.CreateToken(foundUser.ID)
	if err != nil {
		us.l.Println("[ERROR] Something went wrong with user token creation", err)
		w.WriteHeader(http.StatusUnprocessableEntity)
		utils.Respond(w, &GenericError{Message: "Something went wrong with user token creation"})
		return
	}

	err = utils.Respond(w, token)
	if err != nil {
		us.l.Println("[ERROR] serializing token", err)
	}
}
