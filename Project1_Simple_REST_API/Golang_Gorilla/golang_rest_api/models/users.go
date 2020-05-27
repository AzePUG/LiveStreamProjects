package models

import (
	"github.com/jinzhu/gorm"
	"golang.org/x/crypto/bcrypt"
)

// User will hold the user details
type User struct {
	gorm.Model
	FirstName    string `json:"first_name" validate:"required,min=3,max=15" gorm:"type:varchar(15);not null;default:null"`
	LastName     string `json:"last_name" validate:"required,min=3,max=20" gorm:"type:varchar(20);not null;default:null"`
	UserName     string `json:"user_name" validate:"required,min=3,max=10" gorm:"type:varchar(10);not null;default:null"`
	Email        string `json:"email" validate:"required,email" gorm:"type:varchar(30);not null;unique_index;default:null"`
	Password     string `json:"password" validate:"required,min=5,max=15" gorm:"-"`
	PasswordHash string `json:"-" gorm:"not null;unique_index;default:null"`
}

type Login struct {
	Email    string `json:"email" validation:"required,email"`
	Password string `json:"password" validation:"required,min=5,max=15"`
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
	Authenticate(email, password string) (*User, error)
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

// Authenticate Can be used to authenticate the user with the
// provided email address and password.
func (us *userService) Authenticate(email, password string) (*User, error) {
	foundUser, err := us.GetUserByEmail(email)
	if err != nil {
		return nil, err
	}
	err = bcrypt.CompareHashAndPassword([]byte(foundUser.PasswordHash),
		[]byte(password+us.pepper))
	if err != nil {
		switch err {
		case bcrypt.ErrMismatchedHashAndPassword:
			return nil, ErrPasswordIncorrect
		default:
			return nil, err
		}
	}
	return foundUser, nil
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
	if email == "" {
		return nil, ErrEmailEmpty
	}
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
		return ErrPasswordEmpty
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

// AddUser will call actual db command to create the user
func (ug *userGorm) AddUser(user *User) error {
	return ug.db.Create(user).Error
}

// CreateUser hash password and then create user
func (us *userService) CreateUser(user *User) error {
	err := us.bcryptPassword(user)
	if err != nil {
		return err
	}
	return us.AddUser(user)
}

// Delete the user with provided ID
func (ug *userGorm) DeleteUser(id uint) error {
	user, err := ug.GetUserByID(id)
	if err != nil {
		return err
	}
	// user := User{Model: gorm.Model{ID: id}}
	ug.db.Delete(&user)
	return nil
}
