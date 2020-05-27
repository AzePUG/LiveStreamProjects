package controllers

import (
	"fmt"
	"golang_rest_api/auth"
	"golang_rest_api/models"
	"golang_rest_api/utils"
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
	accessToken, err := auth.CreateAccessToken(foundUser.ID)
	if err != nil {
		us.l.Println("[ERROR] Something went wrong with user Access token creation", err)
		w.WriteHeader(http.StatusUnprocessableEntity)
		utils.Respond(w, &GenericError{Message: "Something went wrong with user Access token creation"})
		return
	}

	refreshToken, err := auth.CreateRefreshToken(foundUser.ID)
	if err != nil {
		us.l.Println("[ERROR] Something went wrong with user Refresh token creation", err)
		w.WriteHeader(http.StatusUnprocessableEntity)
		utils.Respond(w, &GenericError{Message: "Something went wrong with user Refresh token creation"})
		return
	}
	tokens := map[string]string {
		"AccessToken": accessToken,
		"RefreshToken": refreshToken,
	}
	err = utils.Respond(w, tokens)
	if err != nil {
		us.l.Println("[ERROR] serializing tokens", err)
	}
}
