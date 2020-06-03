package controllertests

import (
	"bytes"
	"encoding/json"
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
		email        string
		password     string
		errorMessage string
	}{
		{
			// the expected fail due to shitty json format
			inputJSON:    `{"email": "rzayev.sehriyar@gmail.com", "password": 12345"}`,
			statusCode:   400,
			errorMessage: "",
		},
		{
			// the expected fail due to shitty json format
			inputJSON:    `{"email": rzayev.sehriyar@gmail.com, "password": "12345"}`,
			statusCode:   400,
			errorMessage: "",
		},
		{
			// the expected fail due to shitty json format
			// TODO: figure out how to deal wrong passed KEY name
			inputJSON:    `{"em": "rzayev.sehriyar@gmail.com", "password": "12345"}`,
			statusCode:   200,
			errorMessage: "",
		},
		//{
		//	inputJSON:    `{"email": "pet@gmail.com", "password": "wrong password"}`,
		//	statusCode:   422,
		//	errorMessage: "Incorrect Password",
		//},
		//{
		//	inputJSON:    `{"email": "frank@gmail.com", "password": "password"}`,
		//	statusCode:   422,
		//	errorMessage: "Incorrect Details",
		//},
		//{
		//	inputJSON:    `{"email": "kangmail.com", "password": "password"}`,
		//	statusCode:   422,
		//	errorMessage: "Invalid Email",
		//},
		//{
		//	inputJSON:    `{"email": "", "password": "password"}`,
		//	statusCode:   422,
		//	errorMessage: "Required Email",
		//},
		//{
		//	inputJSON:    `{"email": "kan@gmail.com", "password": ""}`,
		//	statusCode:   422,
		//	errorMessage: "Required Password",
		//},
		//{
		//	inputJSON:    `{"email": "", "password": "password"}`,
		//	statusCode:   422,
		//	errorMessage: "Required Email",
		//},
	}

	w := httptest.NewRecorder()
	r := mux.NewRouter()
	r.Use(controllers.CommonMiddleware)
	var apiV1 = r.PathPrefix("/api/v1/").Subrouter()
	postR := apiV1.Methods("POST").Subrouter()
	postR.HandleFunc("/users/login", ah.Login)
	postR.Use(gh.MiddlewareValidate)

	for _, v := range samples {
		t.Log(v.inputJSON)
		req := httptest.NewRequest("POST", "/api/v1/users/login", bytes.NewBufferString(v.inputJSON))
		r.ServeHTTP(w, req)

		assert.Equal(t, w.Code, v.statusCode)
		if v.statusCode == 200 {
			assert.NotEqual(t, w.Body.String(), "")
		}

		if v.statusCode == 422 && v.errorMessage != "" {
			responseMap := make(map[string]interface{})
			err = json.Unmarshal([]byte(w.Body.String()), &responseMap)
			if err != nil {
				t.Errorf("Cannot convert to json: %v", err)
			}
			assert.Equal(t, responseMap["error"], v.errorMessage)
		}
	}
}