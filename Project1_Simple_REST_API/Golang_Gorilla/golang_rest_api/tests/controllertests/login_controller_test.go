package controllertests

import (
	"bytes"
	"github.com/gorilla/mux"
	"github.com/stretchr/testify/assert"
	"golang_rest_api/controllers"
	"net/http/httptest"
	"testing"
)

// Reference blog post
// https://levelup.gitconnected.com/crud-restful-api-with-go-gorm-jwt-postgres-mysql-and-testing-460a85ab7121

func TestLoginWithValidationPassWrongJSONFormat(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}

	samples := []struct {
		inputJSON    string
		statusCode   int
	}{
		{
			// the expected fail due to shitty json format
			inputJSON:    `{"email": "rzayev.sehriyar@gmail.com", "password": 12345"}`,
			statusCode:   400,
		},
		{
			// the expected fail due to shitty json format
			inputJSON:    `{"email": rzayev.sehriyar@gmail.com, "password": "12345"}`,
			statusCode:   400,
		},
		{
			// the expected fail due to shitty json format
			inputJSON:    `{"em": "rzayev.sehriyar@gmail.com", "password": "12345"}`,
			statusCode:   400,
		},
	}

	w := httptest.NewRecorder()
	r := mux.NewRouter()
	r.Use(controllers.CommonMiddleware)
	var apiV1 = r.PathPrefix("/api/v1/").Subrouter()
	postR := apiV1.Methods("POST").Subrouter()
	postR.HandleFunc("/users/login", ah.Login)
	postR.Use(gh.MiddlewareValidate)

	for _, v := range samples {
		req := httptest.NewRequest("POST", "/api/v1/users/login", bytes.NewBufferString(v.inputJSON))
		r.ServeHTTP(w, req)
		assert.Equal(t, w.Code, v.statusCode)
	}
}

func TestLoginWithValidationEmptyInvalidEmail(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}

	samples := []struct {
		inputJSON    string
		statusCode   int
	}{
		{
			// wrong email format
			inputJSON:    `{"email": "rzayevsehriyargmailcom", "password": "12345"}`,
			statusCode:   400,
		},
		{
			// empty email address
			inputJSON:    `{"email": "", "password": 12345"}`,
			statusCode:   400,
		},

	}

	w := httptest.NewRecorder()
	r := mux.NewRouter()
	r.Use(controllers.CommonMiddleware)
	var apiV1 = r.PathPrefix("/api/v1/").Subrouter()
	postR := apiV1.Methods("POST").Subrouter()
	postR.HandleFunc("/users/login", ah.Login)
	postR.Use(gh.MiddlewareValidate)

	for _, v := range samples {
		req := httptest.NewRequest("POST", "/api/v1/users/login", bytes.NewBufferString(v.inputJSON))
		r.ServeHTTP(w, req)
		assert.Equal(t, w.Code, v.statusCode)
	}
}