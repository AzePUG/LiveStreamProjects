package controllers

import (
	"fmt"
	"net/http"
)

type KeyLogin struct{}
type KeyToken struct{}

func (us *Users) Login(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Success")
	fmt.Println(r.Context().Value("KeyLogin"))
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