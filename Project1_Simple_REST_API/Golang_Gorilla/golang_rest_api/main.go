package main

import (
	"golang_restful_api/controllers"
	"golang_restful_api/models"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
	"github.com/nicholasjackson/env"
)

var bindAddress = env.String("BIND_ADDRESS", false, ":9090", "Bind address for the server")

func main() {
	env.Parse()

	l := log.New(os.Stdout, "users-api -> ", log.LstdFlags)
	v := models.NewValidation()

	// create the user handler/conroller
	ah := controllers.NewUsers(l, v)

	// Create new serve mux and register handlers
	r := mux.NewRouter()
	var apiV1 = r.PathPrefix("/api/v1/").Subrouter()

	// Routes for api
	getR := apiV1.Methods("GET").Subrouter()
	getR.HandleFunc("/users", ah.ListAll)
	getR.HandleFunc("/users/{id:[0-9]+}", ah.ListSingle)

	postR := apiV1.Methods("POST").Subrouter()
	postR.HandleFunc("/users", ah.Create)
	postR.Use(ah.MiddlewareValidateUser)

	putR := apiV1.Methods("PUT").Subrouter()
	putR.HandleFunc("/users/{id:[0-9]+}", ah.Update)
	putR.Use(ah.MiddlewareValidateUser)

	deleteR := apiV1.Methods(http.MethodDelete).Subrouter()
	deleteR.HandleFunc("/users/{id:[0-9]+}", ah.Delete)

	// create a new server
	s := http.Server{
		Addr:         *bindAddress,      // configure the bind address
		Handler:      r,                 // set the default handler
		ErrorLog:     l,                 // set the logger for the server
		ReadTimeout:  5 * time.Second,   // max time to read request from the client
		WriteTimeout: 10 * time.Second,  // max time to write response to the client
		IdleTimeout:  120 * time.Second, // max time for connections using TCP Keep-Alive
	}

	l.Println("Starting server on port 9090")
	s.ListenAndServe()

}

// func createUserHandler(w http.ResponseWriter, r *http.Request) {
// 	log.Print("Request received to create an User")
//
// 	var user User
// 	json.NewDecoder(r.Body).Decode(&user)
// 	id := string(user.ID)
// 	userMap[id] = user
// 	log.Print("Successfully created the User ", user)
//
// 	w.Header().Add("Content-Type", "application/json")
// 	w.WriteHeader(http.StatusCreated)
//
// 	json.NewEncoder(w).Encode(user)
// }
//
// func getUserHandler(w http.ResponseWriter, r *http.Request) {
// 	params := mux.Vars(r)
// 	id, _ := params["id"]
//
// 	log.Print("Request received to get an user by user id: ", id)
// 	user, key := userMap[id]
//
// 	w.Header().Add("Content-Type", "application/json")
//
// 	if key {
// 		log.Println("Successfully retrieved the user ", user, " for user id: ", id)
// 		log.Println(userMap)
// 		w.WriteHeader(http.StatusOK)
// 		json.NewEncoder(w).Encode(user)
// 	} else {
// 		log.Println("Requested user is not found for user id: ", id)
// 		log.Println(userMap)
// 		w.WriteHeader(http.StatusNotFound)
// 		json.NewEncoder(w)
// 	}
// }
//
// func deleteUserHandler(w http.ResponseWriter, r *http.Request) {
// 	log.Print("Request received to delete an User by user id")
// 	//add your own flavor to this function :)
// }
