package modeltests

import (
	"fmt"
	"os"
	"testing"
	"golang_restful_api/main"
	"golang_restful_api/models"
)

// TODO: figure out the way to initialize necessary things at very beginning of the test
func TestMain(m *testing.M)  {
	cfg := main.LoadTestConfig()
	dbCfg := cfg.Database
	fmt.Println(dbCfg)
	os.Exit(m.Run())
}



