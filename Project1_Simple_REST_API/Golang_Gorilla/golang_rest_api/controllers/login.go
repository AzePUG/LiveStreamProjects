package controllers

import (
	"context"
	"fmt"
	"golang_restful_api/auth"
	"golang_restful_api/models"
	"golang_restful_api/utils"
	"net/http"
)

type KeyLogin struct{}
type KeyToken struct{}

func (us *Users) Login(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
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
		ctx := context.WithValue(r.Context(), KeyToken{}, token)
		r = r.WithContext(ctx)
		next.ServeHTTP(w, r)
	})

}

// TODO: currently fails to compile uncomment and fix this to read Login credentials
// This function should be called only after middleware validation check
//func (us *Users) Login(w http.ResponseWriter, r *http.Request) {
//	body, err := ioutil.ReadAll(r.Body)
//	if err != nil {
//		responses.ERROR(w, http.StatusUnprocessableEntity, err)
//		return
//	}
//	user := models.User{}
//	err = json.Unmarshal(body, &user)
//	if err != nil {
//		responses.ERROR(w, http.StatusUnprocessableEntity, err)
//		return
//	}
//
//	user.Prepare()
//	err = user.Validate("login")
//	if err != nil {
//		responses.ERROR(w, http.StatusUnprocessableEntity, err)
//		return
//	}
//	token, err := server.SignIn(user.Email, user.Password)
//	if err != nil {
//		formattedError := formaterror.FormatError(err.Error())
//		responses.ERROR(w, http.StatusUnprocessableEntity, formattedError)
//		return
//	}
//	responses.JSON(w, http.StatusOK, token)
//}