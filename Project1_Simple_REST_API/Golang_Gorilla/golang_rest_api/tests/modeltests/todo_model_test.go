package modeltests

import (
	"github.com/stretchr/testify/assert"
	"golang_rest_api/models"
	"testing"
)


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

func TestGetTodoByID(t *testing.T) {
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

	todo, err := seedOneTodo()
	if err != nil {
		t.Fatal(err)
	}
	todoReturned, err := services.Todo.GetTodoByID(&user, todo.ID)
	// As we have inserted only one to-do here it should have id 1
	assert.Equal(t, uint(1), todoReturned.ID)

	// Get to-do by non-existing ID
	// It should raise error models: resource not found
	_, err = services.Todo.GetTodoByID(&user, 85)
	assert.EqualError(t, err, "models: resource not found")
}

func TestDeleteTodo(t *testing.T) {
	err := refreshUserTable()
	if err != nil {
		t.Fatal(err)
	}

	err = refreshTodoTable()
	if err != nil {
		t.Fatal(err)
	}

	// Try to delete with empty user and to-do ID
	todo := models.Todo{}
	user := models.User{}
	err = services.Todo.DeleteTodo(&user, todo.ID)
	assert.EqualError(t, err, "models: resource not found")

	user, err = seedOneUser()
	if err != nil {
		t.Fatal(err)
	}

	todo, err = seedOneTodo()
	if err != nil {
		t.Fatal(err)
	}

	_ = services.Todo.DeleteTodo(&user, todo.ID)
	// If delete succeeded searching for to-do id 1 should fail.
	_, err = services.Todo.GetTodoByID(&user, 1)
	assert.EqualError(t, err, "models: resource not found")
}

func TestUpdateTodo(t *testing.T) {
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

	_, err = seedOneTodo()
	if err != nil {
		t.Fatal(err)
	}

	todo, err := services.Todo.GetTodoByID(&user, 1)
	todo.Title = "Updated Todo"
	err = services.Todo.UpdateTodo(&user, todo, 1)
	assert.Equal(t, nil, err)
	todoUpdated, err := services.Todo.GetTodoByID(&user, 1)
	assert.Equal(t, "Updated Todo", todoUpdated.Title)

	todo.ID = 5
	err = services.Todo.UpdateTodo(&user, todo, 1)
	assert.Equal(t, nil, err)
	todoUpdated, err = services.Todo.GetTodoByID(&user, 5)
	assert.Equal(t, uint(5), todoUpdated.ID)
}
