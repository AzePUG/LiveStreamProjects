package modeltests

import (
	"fmt"
	"log"
	"testing"
)

func TestFindSingleUser(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		log.Fatal(err)
	}
	_, err = seedOneUser()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(services)
	users, err := services.User.GetUsers()
	if err != nil {
		log.Fatal(err)
		return
	}
	length := len(users)
	if length != 1 {
		t.Errorf("The length of user slice should be 1 but got %d", length)
	}
}

func TestFindAllUsers(t *testing.T) {
	return
}