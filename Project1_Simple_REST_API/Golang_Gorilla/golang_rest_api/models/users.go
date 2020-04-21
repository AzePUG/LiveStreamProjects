package models

import (
	"github.com/jinzhu/gorm"
	"golang.org/x/crypto/bcrypt"
)

// "github.com/jinzhu/gorm"
//User Json request payload is as follows,
//{
//  "id": "1",
//  "first_name": "james",
//  "last_name":  "bolt",
//  "user_name":  "james1234"
//}

// User will hold the user details
type User struct {
	gorm.Model
	FirstName    string `json:"first_name" validate:"required" gorm:"not null"`
	LastName     string `json:"last_name" validate:"required" gorm:"not null"`
	UserName     string `json:"user_name" validate:"required" gorm:"not null"`
	Email        string `json:"email" gorm:"not null;unique_index"`
	Password     string `json:"password" gorm:"-"`
	PasswordHash string `gorm:"not null;unique_index"`
}

// UserDB interface for holding all direct database related actions
type UserDB interface {
	// Methods for querying users
	GetUsers() ([]*User, error)
	GetUserByID(id uint) (*User, error)
	GetUserByEmail(email string) (*User, error)

	// Methods for altering the user
	UpdateUser(acc *User) error
	AddUser(acc *User) error
	DeleteUser(id uint) error
}

// UserDBExtra an extra actions as wrappers etc.
type UserDBExtra interface {
	// this will be type of userService
	CreateUser(acc *User) error
}

// UserService ...
type UserService interface {
	UserDB
	UserDBExtra
}

// NewUserService creating user service here
func NewUserService(db *gorm.DB, pepper string) UserService {
	ug := &userGorm{db}
	return &userService{
		UserDB: ug,
		pepper: pepper,
	}
}

var _ UserService = &userService{}

type userService struct {
	UserDB
	pepper string
}

var _ UserDB = &userGorm{}

type userGorm struct {
	db *gorm.DB
}

// first will query using the provided gorm.DB and it will get
// the first item returned and place it into dst.
// If nothing is found in the query, it will return ErrNotFound
func first(db *gorm.DB, dst interface{}) error {
	err := db.First(dst).Error
	if err == gorm.ErrRecordNotFound {
		return ErrNotFound
	}
	return err
}

func (ug *userGorm) GetUsers() ([]*User, error) {
	var user []*User
	err := ug.db.Find(&user).Error
	return user, err
}

// GetUserByEmail Looks up a user with given email address.
// returns that user.
func (ug *userGorm) GetUserByEmail(email string) (*User, error) {
	var user User
	db := ug.db.Where("email = ?", email)
	err := first(db, &user)
	return &user, err
}

// GetUserByID will look up the user by the id provided.
// 1 - user, nil
// 2 - nil, ErrNotFound
// 3 - nil, otherError
func (ug *userGorm) GetUserByID(id uint) (*User, error) {
	var user User
	db := ug.db.Where("id = ?", id)
	err := first(db, &user)
	return &user, err
}

// Update the record in user table i.e given new user model
func (ug *userGorm) UpdateUser(user *User) error {
	return ug.db.Save(user).Error
}

// bcryptPassword will hash a user's password with a predefined
// pepper (userPwPepper) and bcrypt if the
// Password is not the empty string
func (us *userService) bcryptPassword(user *User) error {
	if user.Password == "" {
		return nil
	}
	pwBytes := []byte(user.Password + us.pepper)
	hashedBytes, err := bcrypt.GenerateFromPassword(pwBytes, bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	user.PasswordHash = string(hashedBytes)
	user.Password = ""
	return nil
}

// Create will create provided user and backfill data
// like the ID, CreatedAt etc.
func (ug *userGorm) AddUser(user *User) error {
	return ug.db.Create(user).Error
}

// CreateUser hash password and then create database
func (us *userService) CreateUser(user *User) error {
	err := us.bcryptPassword(user)
	if err != nil {
		return err
	}
	return us.AddUser(user)
}

// Delete the user with provided ID
func (ug *userGorm) DeleteUser(id uint) error {
	user := User{Model: gorm.Model{ID: id}}
	return ug.db.Delete(&user).Error
}

// TODO: change the methods below to use database

// // Users for list of User objects
// type Users []*User
//
// var userList = []*User{&User{}}

// TODO: do we need it????
//
// // GetUsers function to get the reference for list of users
// func GetUsers() Users {
// 	return userList
// }
//
// func findIndexByUserID(id int) int {
// 	for i, acc := range userList {
// 		if acc.ID == id {
// 			// If the the given id found then return the index of array
// 			return i
// 		}
// 	}
// 	// Otherwise return -1
// 	return -1
// }
//
// // GetUserByID returns a single user which matches the id from the
// // array/list/slice of users
// // If there is not such user with given id return ErrUserNotFound
// func GetUserByID(id int) (*User, error) {
// 	i := findIndexByUserID(id)
// 	if i == -1 {
// 		return nil, ErrUserNotFound
// 	}
// 	return userList[i], nil
// }
//
// // UpdateUser replaces a user in the database with the given
// // item. Will update whole object
// // If a user with the given id does not exist in the database
// // this function returns a ErrUserNotFound error
// func UpdateUser(acc *User) error {
// 	i := findIndexByUserID(acc.ID)
// 	if i == -1 {
// 		return ErrUserNotFound
// 	}
// 	// update the user in the DB/array/list
// 	userList[i] = acc
//
// 	return nil
// }
//
// // AddUser adds a new user to the database
// func AddUser(acc *User) {
// 	// get the next id in sequence
// 	// implement autoincrement
// 	maxID := userList[len(userList)-1].ID
// 	acc.ID = maxID + 1
// 	userList = append(userList, acc)
// }
//
// // DeleteUser deletes an user from the database/list/array/slice
// func DeleteUser(id int) error {
// 	i := findIndexByUserID(id)
// 	if i == -1 {
// 		return ErrUserNotFound
// 	}
//
// 	// Remove the element at index i from a.
// 	userList[i] = userList[len(userList)-1] // Copy last element to index i.
// 	userList[len(userList)-1] = &User{}     // Erase last element (write zero value).
// 	userList = userList[:len(userList)-1]   // Truncate slice.
//
// 	// log.Println(userList[:i])
// 	// log.Println(userList[i+1])
// 	// userList = append(userList[:i], userList[i+1])
//
// 	return nil
// }
