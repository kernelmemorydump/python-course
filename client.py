import requests
from rich import print
from rich.prompt import Prompt

server_url = "http://localhost:8000"

def show_tasks():
    """Prikazuje zadatke."""
    response = requests.get(server_url)
    data = response.json()
    tasks = data["tasks"]

    print("\nZa uraditi:")
    for task in tasks:
        stanje = "\[x]" if task[2] else "[ ]"
        print(f" {stanje} {task[1]} (id: {task[0]})")
    print("\n")

def add_task():
    """Kreira novi zadatak."""
    naziv = Prompt.ask("Naziv zadatka")
    zavrseno_input = Prompt.ask("Zavrseno?", choices=["Da", "Ne"])
    zavrseno_bool = True if zavrseno_input == "Da" else False

    todo = { "name": naziv, "done": zavrseno_bool }

    requests.post(server_url, json=todo)

def edit_task():
    """Menja postojeći zadatak."""
    id_zadatka = Prompt.ask("Unesite id zadatka")
    name = Prompt.ask("Unesite novi naziv")
    done = Prompt.ask("Da li je zavrseno", choices=["Da", "Ne"])
    done_bool = True if done == "Da" else False

    todo = { "name": name, "done": done_bool }

    server_url_sa_id = f"{server_url}/?id={id_zadatka}"
    requests.put(server_url_sa_id, json=todo)

def complete_task():
    id_zadatka = Prompt.ask("Unesite id zadatka")

    server_url_sa_id = f"{server_url}/complete?id={id_zadatka}"
    requests.put(server_url_sa_id)

def delete_task():
    """Briše postojeći zadatak."""
    id_zadatka = Prompt.ask("Unesite id zadatka")
    requests.delete(f"{server_url}/?id={id_zadatka}")

while True:
    show_tasks()
    akcija = Prompt.ask("Izaberi akciju:", choices=["Zavrsi", "Dodaj", "Izmena", "Brisanje", "Izlaz"], default="Izlaz")

    if akcija == "Zavrsi":
        complete_task()
    elif akcija == "Dodaj":
        add_task()
    elif akcija == "Izmena":
        edit_task()
    elif akcija == "Brisanje":
        delete_task()
    else:
        exit()