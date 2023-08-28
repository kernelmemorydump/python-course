import uvicorn
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel

"""
# Kreiraj databazu
db_cursor.execute("create database todo")

# Kreiraj table
db_cursor.execute("CREATE TABLE `todo_tasks` (`id` INT NOT NULL AUTO_INCREMENT, `name` VARCHAR(255), `done` BOOLEAN, PRIMARY KEY (`id`));")

# Pokazi od cega se sastoji table todo_tasks
db_cursor.execute("SELECT * FROM todo_tasks")
result = db_cursor.fetchall()
for row in result:
    print(row)
"""

db_config = {
    "host": "localhost",
    "user": "mysql",
    "password": "mysql",
    "database": "todo"
}


class TodoItem(BaseModel):
    id: int
    name: str
    done: bool

class CreateTodoItem(BaseModel):
    name: str
    done: bool

class EditTodoItem(BaseModel):
    name: str
    done: bool

app = FastAPI()

@app.get("/")
async def prikazi_todos():
    """Prikazuje sve postojeće todo zadatke."""
    try:
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM todo_tasks")

        tasks = db_cursor.fetchall()

        db_cursor.close()
        db_connection.close()

        return { "tasks": tasks }
    except mysql.connector.Error as err:
        return { "error": str(err) }

@app.post("/")
async def novi_todo(todo: CreateTodoItem):
    """Kreira novi todo zadatak."""
    name = todo.name
    done = 1 if todo.done else 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()

        db_cursor.execute(f"INSERT INTO todo_tasks (id, name, done) VALUES (0, '{name}', {done})")
        db_connection.commit()

        db_cursor.close()
        db_connection.close()
    except mysql.connector.Error as err:
        return { "error": str(err) }

    return { "message": "Novi todo je napravljen uspesno" }

@app.put("/")
async def izmeni_todo(id: int, todo: EditTodoItem):
    """Menja već postojeći todo zadatak."""
    is_done = 1 if todo.done else 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()

        update_query = f"UPDATE todo_tasks SET name = '{todo.name}', done = {is_done} WHERE id = {id}"
        db_cursor.execute(update_query)
        db_connection.commit()

        db_cursor.close()
        db_connection.close()
    except mysql.connector.Error as err:
        return { "error": str(err) }

    return { "message": f"Uspesno izmenjen todo {id}" }

@app.put("/complete")
async def zavrsi_todo(id: int):
    """Završava postojeći todo zadatak."""
    try:
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()

        complete_query = f"UPDATE todo_tasks SET done = 1 WHERE id = {id}"
        db_cursor.execute(complete_query)
        db_connection.commit()

        db_cursor.close()
        db_connection.close()
    except mysql.connector.Error as err:
        return { "error": str(err) }

    return { "message": f"Uspesno izmenjen todo {id}" }
    
@app.delete("/")
async def obrisi_todo(id: int):
    """Briše već postojeći todo zadatak."""
    try:
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()

        delete_query = f"DELETE FROM todo_tasks WHERE id = {id}"
        db_cursor.execute(delete_query)
        db_connection.commit()

        db_cursor.close()
        db_connection.close()
    except mysql.connector.Error as err:
        return { "error": str(err) }

    return { "message": f"Todo {id} je uspesno obrisan." }


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')