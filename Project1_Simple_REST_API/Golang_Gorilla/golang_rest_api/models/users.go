package models

import (
	"fmt"
)

//User Json request payload is as follows,
//{
//  "id": "1",
//  "first_name": "james",
//  "last_name":  "bolt",
//  "user_name":  "james1234"
//}

// ErrUserNotFound raised when the user not found
var ErrUserNotFound = fmt.Errorf("User not found")

// User will hold the user details
type User struct {
	ID        int    `json:"id"`
	FirstName string `json:"first_name" validate:"required"`
	LastName  string `json:"last_name" validate:"required"`
	UserName  string `json:"user_name" validate:"required"`
}

// Users for list of User objects
type Users []*User

var userList = []*User{&User{}}

// GetUsers function to get the reference for list of users
func GetUsers() Users {
	return userList
}

func findIndexByUserID(id int) int {
	for i, acc := range userList {
		if acc.ID == id {
			// If the the given id found then return the index of array
			return i
		}
	}
	// Otherwise return -1
	return -1
}

// GetUserByID returns a single user which matches the id from the
// array/list/slice of users
// If there is not such user with given id return ErrUserNotFound
func GetUserByID(id int) (*User, error) {
	i := findIndexByUserID(id)
	if i == -1 {
		return nil, ErrUserNotFound
	}
	return userList[i], nil
}

// UpdateUser replaces a user in the database with the given
// item. Will update whole object
// If a user with the given id does not exist in the database
// this function returns a ErrUserNotFound error
func UpdateUser(acc *User) error {
	i := findIndexByUserID(acc.ID)
	if i == -1 {
		return ErrUserNotFound
	}
	// update the user in the DB/array/list
	userList[i] = acc

	return nil
}

// AddUser adds a new user to the database
func AddUser(acc *User) {
	// get the next id in sequence
	// implement autoincrement
	maxID := userList[len(userList)-1].ID
	acc.ID = maxID + 1
	userList = append(userList, acc)
}

// DeleteUser deletes an user from the database/list/array/slice
func DeleteUser(id int) error {
	i := findIndexByUserID(id)
	if i == -1 {
		return ErrUserNotFound
	}

	// Remove the element at index i from a.
	userList[i] = userList[len(userList)-1] // Copy last element to index i.
	userList[len(userList)-1] = &User{}     // Erase last element (write zero value).
	userList = userList[:len(userList)-1]   // Truncate slice.

	// log.Println(userList[:i])
	// log.Println(userList[i+1])
	// userList = append(userList[:i], userList[i+1])

	return nil
}
