package modeltests

import (
	"testing"
)

func TestFindSingleUser(t *testing.T) {
	refreshUserTable()
	seedOneUser()
}