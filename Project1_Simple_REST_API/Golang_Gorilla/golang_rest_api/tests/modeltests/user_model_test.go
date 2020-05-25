package modeltests

import (
	"fmt"
	"github.com/stretchr/testify/assert"
	"golang_restful_api/models"
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

	// LastName related case
	user.LastName = "Sjsdaksdajsdlajdlaksjdaljdssaljdsaljdlajsljdaldjsaldjalsjdalksj"
	user.FirstName = "Shahriyar"
	err = services.User.CreateUser(&user)
	assert.EqualErrorf(t, err, "pq: value too long for type character varying(20)",
		"error message %s", err)

	// Checking email length
	user.LastName = "Rzayev"
	user.Email = "asjdhajsdjabsdjabsdjabsjdbasjbdjasbdjasdb"
	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "pq: value too long for type character varying(30)")

	// Checking username length
	user.Email = "rzayev.sehriyar@box.az"
	user.UserName = "asdsadasda2323423dkasdjnasdnaasd"
	err = services.User.CreateUser(&user)
	assert.EqualError(t, err, "pq: value too long for type character varying(10)")

}

func TestCreateUserWithEmptyPasswordHash(t *testing.T) {
	// PasswordHash must not be empty at db level.
	// But keep in mind that database does not care the algorithm or some kind of type of our hash.
	return
}

func TestFindAllUsers(t *testing.T) {
	return
}