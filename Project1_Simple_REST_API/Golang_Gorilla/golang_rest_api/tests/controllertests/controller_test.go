package controllertests
// Duplicated code with model_test.go file

import (
"fmt"
"github.com/jinzhu/gorm"
"golang.org/x/crypto/bcrypt"
	"golang_rest_api/controllers"
	"golang_rest_api/models"
"golang_rest_api/utils"
"log"
"os"
"testing"
)

var services *models.Services
var newdb *gorm.DB
var pepper string
var ah  *controllers.Users
var th  *controllers.Todos
var gh controllers.GenHandler
type testError string

func (e testError) Error() string {
	return string(e)
}

const (
	ErrPasswordEmpty testError = "testError: empty password provided"
)

func TestMain(m *testing.M)  {
	var err error
	cfg := utils.LoadTestConfig()
	dbCfg := cfg.Database
	services, err = models.NewServices(
		models.WithGorm(dbCfg.Dialect(), dbCfg.ConnectionInfo()),
		models.WithUser(cfg.Pepper),
		models.WithTodo(),
	)
	if err != nil {
		fmt.Println("[ERROR] Something went wrong with test initialization", err)
	}
	newdb = services.DB()
	pepper = cfg.Pepper

	l := log.New(os.Stdout, "users-api -> ", log.LstdFlags)
	v := models.NewValidation()
	us := services.User

	l_todo := log.New(os.Stdout, "todos-api -> ", log.LstdFlags)
	ts := services.Todo
	// create the handler/conrollers
	ah = controllers.NewUsers(l, v, us)
	th = controllers.NewTodos(l_todo, v, ts, us)
	gh = controllers.GenHandler{
		ah,
		th,
	}

	os.Exit(m.Run())
}

func refreshUserTable() error {
	// Dropping using SQL statement as it fails otherwise to handle
	err := newdb.Exec("DROP TABLE IF EXISTS users CASCADE").Error
	//err := newdb.Set("gorm:table_options", "CASCADE").DropTableIfExists(&models.User{}).Error
	//err := newdb.DropTableIfExists(&models.User{}).Error
	if err != nil {
		return err
	}

	err = newdb.AutoMigrate(&models.User{}).Error
	if err != nil {
		return err
	}
	log.Printf("Successfully refreshed table")
	return nil
}

func refreshTodoTable() error {
	err := newdb.Set("gorm:table_options", "CASCADE").DropTableIfExists(&models.Todo{}).Error
	if err != nil {
		return err
	}

	err = newdb.AutoMigrate(&models.Todo{}).AddForeignKey("user_id", "users(id)", "CASCADE", "CASCADE").Error
	if err != nil {
		return err
	}
	log.Printf("Successfully refreshed table")
	return nil
}

func bcryptPassword(user *models.User) error {
	if user.Password == "" {
		return ErrPasswordEmpty
	}
	pwBytes := []byte(user.Password + pepper)
	hashedBytes, err := bcrypt.GenerateFromPassword(pwBytes, bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	user.PasswordHash = string(hashedBytes)
	user.Password = ""
	return nil
}

func seedOneUser() (models.User, error) {
	user := models.User{
		FirstName: "Shahriyar",
		LastName:    "Rzayev",
		UserName: "shako",
		Email: "rzayev.sehriyar@gmail.com",
		Password: "12345",
	}
	bcryptPassword(&user)

	err := newdb.Model(&models.User{}).Create(&user).Error
	if err != nil {
		log.Fatalf("cannot seed users table: %v", err)
		return models.User{}, err
	}
	log.Printf("Successfully inserted the user")
	return user, nil
}

func seedTwoUser() ([]models.User, error) {
	users := []models.User{
		{
			FirstName: "Shahriyar",
			LastName:    "Rzayev",
			UserName: "shako",
			Email: "rzayev.sehriyar@gmail.com",
			Password: "12345",
		},
		{
			FirstName: "Tural",
			LastName:    "Yek",
			UserName: "T_Yek",
			Email: "tural_yek@gmail.com",
			Password: "12345",
		},
	}
	for _, user := range(users) {
		bcryptPassword(&user)
		err := newdb.Model(&models.User{}).Create(&user).Error
		if err != nil {
			log.Fatalf("cannot seed users table: %v", err)
			return nil, err
		}
	}
	log.Printf("Successfully inserted the users")
	return users, nil
}


func seedOneTodo() (models.Todo, error){
	// We assume that seedOneUser() function will be called prior to this function call.
	// due to this UserID will be updated to 1 every time.

	todo := models.Todo{
		Title: "Dummy Todo",
		Description: "My dummy Todo for tests",
		UserID: 1,
	}
	err := newdb.Model(&models.Todo{}).Create(&todo).Error
	if err != nil {
		log.Fatalf("cannot seed todo table: %v", err)
		return models.Todo{}, err
	}
	log.Printf("Successfully inserted the todo")
	return todo, nil
}

func seedTwoTodos() ([]models.Todo, error){
	// We assume that seedOneUser() function will be called prior to this function call.
	// due to this UserID will be updated to 1 every time.
	todos := []models.Todo{
		{
			Title: "Dummy Todo",
			Description: "My dummy Todo for tests",
			UserID: 1,
		},
		{
			Title: "Dummy Todo 2 ",
			Description: "My dummy Todo for tests 2",
			UserID: 1,
		},
	}
	for _, todo := range todos {
		err := newdb.Model(&models.Todo{}).Create(&todo).Error
		if err != nil {
			log.Fatalf("cannot seed todo table: %v", err)
			return []models.Todo{}, err
		}
	}
	log.Printf("Successfully inserted the todos")
	return todos, nil
}