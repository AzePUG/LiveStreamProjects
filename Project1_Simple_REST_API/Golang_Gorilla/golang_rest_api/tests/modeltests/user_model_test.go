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

func TestIfTwoUsersExist(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}
	_, err = seedTwoUser()
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
	if length != 2 {
		t.Errorf("The length of user slice should be 2 but got %d", length)
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

func TestGetUserByEmail(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	// Trying to get user with empty email address
	// It should fail with ErrEmailEmpty models error.
	_, err = services.User.GetUserByEmail("")
	assert.EqualError(t, err, "models: empty email address provided")

	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}

	// Trying to get user with non-existing email address.
	// It should fail with ErrNotFound models error
	_, err = services.User.GetUserByEmail("rzayev@box.az")
	assert.EqualError(t, err, "models: resource not found")

	// Trying to get user with existing email address.
	// It should return the found user. I will check if returned user's email is equal to passed email.
	user, err := services.User.GetUserByEmail("rzayev.sehriyar@gmail.com")
	assert.Equal(t, "rzayev.sehriyar@gmail.com", user.Email)
}

func TestGetUserByID(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}

	// Trying to get user with non-existing ID
	// Should return an ErrNotFound
	_, err = services.User.GetUserByID(222)
	assert.EqualError(t, err, "models: resource not found")

	// Trying to get user with existing ID
	// Should return found user from DB and I will check if ID is equal 1 or not.
	user, err := services.User.GetUserByID(1)
	assert.Equal(t, uint(1), user.ID)
}

func TestDeleteUser(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	_, err = seedTwoUser()
	if err != nil {
		t.Fatal(err)
	}

	users, err := services.User.GetUsers()
	assert.Equal(t,2,  len(users))

	// Trying to delete user with non-existing id
	// Expecting error here
	err = services.User.DeleteUser(85)
	assert.EqualError(t, err, "models: resource not found")

	// Trying to delete first user.
	// The delete function should return nil if the user is deleted successfully.
	err = services.User.DeleteUser(1)
	assert.Equal(t,nil, err)
}