package modeltests

import (
	"fmt"
	"github.com/stretchr/testify/assert"
	"golang_rest_api/models"
	"testing"
)

func TestIfSingleUserExists(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}
	fmt.Println(services)
	users, err := services.User.GetUsers()
	if err != nil {
		t.Fatal(err)
		return
	}
	length := len(users)
	if length != 1 {
		t.Errorf("The length of user slice should be 1 but got %d", length)
	}
}

func TestCreateUserWithDuplicateEmail(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
			FirstName: "Shahriyar",
			LastName:    "Rzayev",
			UserName: "shako",
			Email: "rzayev.sehriyar@gmail.com",
			Password: "12345",
	}
	err = services.User.CreateUser(&user)
	// Expecting unique constraint fail error message
	assert.EqualErrorf(t, err, "pq: duplicate key value violates unique constraint \"uix_users_email\"",
		"error message %s", err)
}

func TestCreateUserWithDuplicateUserName(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
		FirstName: "Shahriyar",
		LastName:    "Rzayev",
		UserName: "shako",
		Email: "rzayev.sehriyarrr@gmail.com",
		Password: "12345",
	}
	err = services.User.CreateUser(&user)
	// Expecting nil from err as we don't require the username to be unique
	assert.Nil(t, err)
}

func TestUserTableColumnsLength(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
		FirstName: "Sjsdaksdajsdlajdlaksjdaljdssaljdsaljdlajsljdaldjsaldjalsjdalksj",
		LastName:    "Rzayev",
		UserName: "shako",
		Email: "rzayev.sehriyarrr@gmail.com",
		Password: "12345",
	}
	err = services.User.CreateUser(&user)
	assert.EqualErrorf(t, err, "pq: value too long for type character varying(15)",
		"error message %s", err)

	// Cehcking LastName length
	err = refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user.LastName = "Sjsdaksdajsdlajdlaksjdaljdssaljdsaljdlajsljdaldjsaldjalsjdalksj"
	user.FirstName = "Shahriyar"
	user.Password = "12345"
	err = services.User.CreateUser(&user)
	assert.EqualErrorf(t, err, "pq: value too long for type character varying(20)",
		"error message %s", err)

	// Checking email length
	err = refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user.LastName = "Rzayev"
	user.Email = "asjdhajsdjabsdjabsdjabsjdbasjbdjasbdjasdb"
	user.Password = "12345"
	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "pq: value too long for type character varying(30)")

	// Checking username length
	err = refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user.Email = "rzayev.sehriyar@box.az"
	user.UserName = "asdsadasda2323423dkasdjnasdnaasd"
	user.Password = "12345"
	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "pq: value too long for type character varying(10)")

}

func TestCreateUserWithEmptyPassword(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
		FirstName: "Shahriyar",
		LastName:   "Rzayev",
		UserName: "shako",
		Email: "rzayev.sehriyar@gmail.com",
		Password: "",
	}
	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "models: empty password provided")
}

func TestAddUserWithEmptyPasswordHash(t *testing.T) {
	// PasswordHash must not be empty at db level.
	// But keep in mind that database does not care the algorithm or some kind of type of our hash.
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
		FirstName: "Shahriyar",
		LastName:   "Rzayev",
		UserName: "shako",
		Email: "rzayev.sehriyar@gmail.com",
		Password: "12345",
	}
	err = bcryptPassword(&user)
	if err != nil {
		t.Fatal(err)
	}
	// Resetting PasswordHash it should fail to add user with empty PasswordHash.
	user.PasswordHash = ""
	err = services.User.AddUser(&user)
	assert.EqualError(t, err, "pq: null value in column \"password_hash\" violates not-null constraint")
}

func TestCreateUserWithEmptyEmail(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
		FirstName: "Shahriyar",
		LastName:   "Rzayev",
		UserName: "shako",
		Email: "",
		Password: "12345",
	}

	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "pq: null value in column \"email\" violates not-null constraint")
}

func TestCreateUserWithEmptyUserName(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
		FirstName: "Shahriyar",
		LastName:   "Rzayev",
		UserName: "",
		Email: "rzayev.sehriyar@gmail.com",
		Password: "12345",
	}

	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "pq: null value in column \"user_name\" violates not-null constraint")
}

func TestCreateUserWithEmptyFirstName(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
		FirstName: "",
		LastName:   "Rzayev",
		UserName: "shako",
		Email: "rzayev.sehriyar@gmail.com",
		Password: "12345",
	}

	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "pq: null value in column \"first_name\" violates not-null constraint")
}

func TestCreateUserWithEmptyLastName(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	user := models.User{
		FirstName: "Shahriyar",
		LastName:   "",
		UserName: "shako",
		Email: "rzayev.sehriyar@gmail.com",
		Password: "12345",
	}

	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "pq: null value in column \"last_name\" violates not-null constraint")
}

func TestFindAllUsers(t *testing.T) {
	return
}