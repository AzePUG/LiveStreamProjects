package modeltests

import (
	"testing"
)

func TestFindSingleUser(t *testing.T) {
	// TODO: failing test
	refreshUserTable()
	seedOneUser()
	user, _ := services.GetUsers()
	length := len(user)
	if length !=1 {
		t.Errorf("The length of user slice should be 1 but got %d", length)
	}
}