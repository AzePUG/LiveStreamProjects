package modeltests

import (
	"github.com/stretchr/testify/assert"
	"golang_rest_api/models"
	"testing"
)

func TestCreateEmptyTodo(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	err = refreshTodoTable()
	if err != nil {
		t.Fatal(err)
	}

	todo := models.Todo{}
	// It should violate foreign key constraint and as usual should fail at db level.
	err = services.Todo.AddTodo(&todo)
	assert.EqualError(t, err, "pq: insert or update on table \"todos\" violates foreign key constraint \"todos_user_id_users_id_foreign\"")
}

func TestCreateTodoWithNonExistingUserID(t  *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	err = refreshTodoTable()
	if err != nil {
		t.Fatal(err)
	}

	todo := models.Todo{
		Title: "Dummy Todo",
		Description: "My dummy Todo for tests",
		UserID: 85,
	}
	err = services.Todo.AddTodo(&todo)
	assert.EqualError(t, err, "pq: insert or update on table \"todos\" violates foreign key constraint \"todos_user_id_users_id_foreign\"")

}

func TestCreateTodoWithExistingUserID(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	err = refreshTodoTable()
	if err != nil {
		t.Fatal(err)
	}

	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}

	todo, err := seedOneTodo()
	if err != nil {
		t.Fatal(err)
	}
	assert.Equal(t, "Dummy Todo", todo.Title)
}

func TestTodoTableColumnLengths(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	err = refreshTodoTable()
	if err != nil {
		t.Fatal(err)
	}

	todo := models.Todo{
		Title: "Dummy Todoakjdaksdjaklsjdajsdjajdalkdjalksdjalkdjaldjalkdjalsjdaldjalsdkjaslkdj",
		Description: "My dummy Todo for tests",
		UserID: 85,
	}
	err = services.Todo.AddTodo(&todo)
	assert.EqualError(t, err, "pq: value too long for type character varying(20)")

	todo.Title = "My Todo"
	todo.Description = "DummyTodoakjdaksdjaklsjdajsdjajdalkdjalksdjalkdjaldjalkdjalsjdaldjalsdkjaslkdjasdadaddasdasdada" +
		"asdasdadsdsadadsaaaaaaaaaaaaaaaaaaasdadadadadadsadadadadasdadadasdasdadadadasdasdasdasd"

	err = services.Todo.AddTodo(&todo)
	assert.EqualError(t, err, "pq: value too long for type character varying(100)")
}

func TestCreateTodoWithEmptyValues(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	err = refreshTodoTable()
	if err != nil {
		t.Fatal(err)
	}

	_, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}

	todo := models.Todo{
		Title: "",
		Description: "My dummy Todo for tests",
		UserID: 1,
	}
	err = services.Todo.AddTodo(&todo)
	assert.EqualError(t, err, "pq: null value in column \"title\" violates not-null constraint")

	todo = models.Todo{
		Title: "My dummy Todo",
		Description: "",
		UserID: 1,
	}
	err = services.Todo.AddTodo(&todo)
	assert.EqualError(t, err, "pq: null value in column \"description\" violates not-null constraint")
}

func TestGetTodos(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	err = refreshTodoTable()
	if err != nil {
		t.Fatal(err)
	}

	user, err := seedOneUser()
	if err != nil {
		t.Fatal(err)
	}
	// Get directly
	todos, err := seedTwoTodos()
	length := len(todos)
	assert.Equal(t, 2, length)

	// Get todos using user object
	todosSlice, err := services.Todo.GetTodos(&user)
	length = len(todosSlice)
	assert.Equal(t, 2, length)

	// Get todos with empty user
	var emptyUser models.User
	todosSlice, err = services.Todo.GetTodos(&emptyUser)
	// it should return empty list
	assert.Equal(t, 0, len(todosSlice))

}
