package models

const (
	// ErrNotFound is returned when a resource can not be found in database
	ErrNotFound modelError = "models: resource not found"
)

type modelError string

func (e modelError) Error() string {
	return string(e)
}
