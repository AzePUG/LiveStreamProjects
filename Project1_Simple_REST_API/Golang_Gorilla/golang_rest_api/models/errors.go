package models

const (
	// ErrNotFound is returned when a resource can not be found in database
	ErrNotFound modelError = "models: resource not found"
	// ErrPasswordIncorrect is returned when an invalid password
	// is used when attempting to authenticate a user.
	ErrPasswordIncorrect modelError = "models: incorrect password provided"
	// The errors below are primarily used in unit tests.
	// ErrPasswordEmpty
	ErrPasswordEmpty modelError = "models: empty password provided"
	ErrEmailEmpty modelError = "models: empty email address provided"
)

type modelError string

func (e modelError) Error() string {
	return string(e)
}
