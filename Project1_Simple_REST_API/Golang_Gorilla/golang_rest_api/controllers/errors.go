package controllers

const (
	// ErrInvalidUserPath is an error message when the user path is not valid
	ErrInvalidUserPath controllerError = "controllers: Invalid Path, path should be /users/[id]"
)

type controllerError string

func (e controllerError) Error() string {
	return string(e)
}
