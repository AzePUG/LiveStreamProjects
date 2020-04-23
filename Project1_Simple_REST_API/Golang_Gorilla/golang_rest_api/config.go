package main

import (
	"encoding/json"
	"fmt"
	"os"
)

// PostgresConfig struct for holding DB connection information
type PostgresConfig struct {

	//host = "localhost"
	Host     string `json:"host"`
	Port     int    `json:"port"`
	User     string `json:"user"`
	Password string `json:"password"`
	//password = ""
	DBName string `json:"dbname"`
}

// Dialect returnin for DB dialect
func (c PostgresConfig) Dialect() string {
	return "postgres"
}

// ConnectionInfo connection string for postgres
func (c PostgresConfig) ConnectionInfo() string {
	if c.Password == "" {
		return fmt.Sprintf("host=%s port=%d user=%s  dbname=%s sslmode=disable",
			c.Host, c.Port, c.User, c.DBName)
	}

	return fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		c.Host, c.Port, c.User, c.Password, c.DBName)

}

// DefaultsPostgresConfig if there is no config file
func DefaultsPostgresConfig() PostgresConfig {
	return PostgresConfig{
		Host:     "localhost",
		Port:     5432,
		User:     "restapi",
		Password: "12345",
		//password = "",
		DBName: "restapi_dev",
	}
}

// Config overall config struct for our project
type Config struct {
	Port     string         `json:"port"`
	Env      string         `json:"env"`
	Pepper   string         `json:"pepper"`
	Database PostgresConfig `json:"database"`
}

// IsProd check if the environment is production or not
func (c Config) IsProd() bool {
	return c.Env == "prod"
}

// DefaultConfig for project level config
func DefaultConfig() Config {
	return Config{
		Port:     ":9090",
		Env:      "dev",
		Pepper:   "secret-random-string",
		Database: DefaultsPostgresConfig(),
	}
}

// LoadConfig openning and loading the config file.
// if there is no .config file then use DefaultConfig
func LoadConfig(configreq bool) Config {
	f, err := os.Open(".config")
	if err != nil {
		if configreq {
			panic(err)
		}
		fmt.Println("Using the default config...")
		return DefaultConfig()
	}
	var c Config
	dec := json.NewDecoder(f)
	err = dec.Decode(&c)
	if err != nil {
		panic(err)
	}
	fmt.Println("Successfully loaded .config")
	return c
}
