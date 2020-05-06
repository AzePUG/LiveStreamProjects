package main

import (
	"flag"
	"golang_restful_api/controllers"
	"golang_restful_api/models"
	"log"
	"net/http"
	"os"
	"time"

	"fmt"
	"github.com/gorilla/mux"
)

func main() {
	// env.Parse()
	boolPtr := flag.Bool("prod", false, "Provide this flag in production. "+
		"This ensures that a .config file is provided before the application start.")
	flag.Parse()

	cfg := LoadConfig(*boolPtr)
	dbCfg := cfg.Database
	services, err := models.NewServices(
		models.WithGorm(dbCfg.Dialect(), dbCfg.ConnectionInfo()),
		models.WithUser(cfg.Pepper),
		models.WithTodo())
	must(err)

	defer services.Close()
	//services.DestructiveReset()
	//services.AutoMigrate()

	l := log.New(os.Stdout, "users-api -> ", log.LstdFlags)
	v := models.NewValidation()
	us := services.User

	l_todo := log.New(os.Stdout, "todos-api -> ", log.LstdFlags)
	ts := services.Todo

	// create the handler/conrollers
	ah := controllers.NewUsers(l, v, us)
	th := controllers.NewTodos(l_todo, v, ts, us)

	// Create new serve mux and register handlers
	r := mux.NewRouter()
	r.Use(controllers.CommonMiddleware)
	var apiV1 = r.PathPrefix("/api/v1/").Subrouter()

	// Routes for api
	getR := apiV1.Methods("GET").Subrouter()
	getR.HandleFunc("/users", ah.ListAll)
	getR.HandleFunc("/users/{id:[0-9]+}", ah.ListSingle)
	getR.HandleFunc("/users/{id:[0-9]+}/todos", th.ListAll)

	postR := apiV1.Methods("POST").Subrouter()
	postR.HandleFunc("/users", ah.Create)
	err = r.Walk(func(route *mux.Route, router *mux.Router, ancestors []*mux.Route) error {
		pathTemplate, err := route.GetPathTemplate()
		if err == nil {
			fmt.Println("ROUTE:", pathTemplate)
		}
		pathRegexp, err := route.GetPathRegexp()
		if err == nil {
			fmt.Println("Path regexp:", pathRegexp)
		}
		return nil
	})
	//postR.Use(ah.MiddlewareValidateUser)
	postR.HandleFunc("/users/{id:[0-9]+}/todos", th.Create)
	//postR.Use(th.MiddlewareValidateTodo)
	postR.Use(controllers.MiddlewareValidate)

	putR := apiV1.Methods("PUT").Subrouter()
	putR.HandleFunc("/users/{id:[0-9]+}", ah.Update)
	putR.Use(ah.MiddlewareValidateUser)

	deleteR := apiV1.Methods(http.MethodDelete).Subrouter()
	deleteR.HandleFunc("/users/{id:[0-9]+}", ah.Delete)

	// create a new server
	l.Println(cfg.Port)
	s := http.Server{
		Addr:         cfg.Port,          // configure the bind address
		Handler:      r,                 // set the default handler
		ErrorLog:     l,                 // set the logger for the server
		ReadTimeout:  5 * time.Second,   // max time to read request from the client
		WriteTimeout: 10 * time.Second,  // max time to write response to the client
		IdleTimeout:  120 * time.Second, // max time for connections using TCP Keep-Alive
	}

	l.Printf("Starting server on port %s", cfg.Port)
	err = s.ListenAndServe()
	if err != nil {
		l.Println("Unable to start HTTP server", err)
	}

}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
