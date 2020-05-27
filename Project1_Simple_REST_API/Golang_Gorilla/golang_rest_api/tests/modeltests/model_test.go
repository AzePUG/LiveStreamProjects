package modeltests

import (
	"fmt"
	"github.com/jinzhu/gorm"
	"golang.org/x/crypto/bcrypt"
	"golang_rest_api/models"
	"golang_rest_api/utils"
	"log"
	"os"
	"testing"
)

var services *models.Services
var newdb *gorm.DB
var pepper string
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
	os.Exit(m.Run())
}

func refreshUserTable() error {
	err := newdb.DropTableIfExists(&models.User{}).Error
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

