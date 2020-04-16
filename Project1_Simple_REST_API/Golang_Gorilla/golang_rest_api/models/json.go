package models

import (
	"encoding/json"
	"io"
	"net/http"
)

// ToJSON serializes the given interface into a string based JSON format
func ToJSON(w http.ResponseWriter, i interface{}) error {
	e := json.NewEncoder(w)
	return e.Encode(i)
}

// FromJSON deserializes the object from JSON string
// in an io.Reader to the given interface
func FromJSON(i interface{}, r io.Reader) error {
	d := json.NewDecoder(r)
	return d.Decode(i)
}
