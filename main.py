import json
import csv
import os
import datetime

# Файлы для хранения заметок в JSON и CSV форматах
json_notes_file = "notes.json"
csv_notes_file = "notes.csv"


def load_notes(file_name):
    try:
        with open(file_name, "r") as file:
            if file_name.endswith(".json"):
                return json.load(file)
            elif file_name.endswith(".csv"):
                notes = []
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    notes.append(row)
                return notes
    except FileNotFoundError:
        return []


def save_notes(notes, file_name):
    with open(file_name, "w", newline='') as file:
        if file_name.endswith(".json"):
            json.dump(notes, file, indent=4)
        elif file_name.endswith(".csv"):
            fieldnames = ["id", "title", "body", "timestamp"]
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(notes)


def add_note(title, body):
    notes = load_notes(json_notes_file)
    note_id = len(notes) + 1
    timestamp = datetime.datetime.now().isoformat()
    new_note = {"id": note_id, "title": title, "body": body, "timestamp": timestamp}
    notes.append(new_note)
    save_notes(notes, json_notes_file)
    save_notes(notes, csv_notes_file)
    print("Заметка добавлена успешно!")


def list_notes():
    notes = load_notes(json_notes_file)
    if not notes:
        print("Заметок нет.")
    else:
        for note in notes:
            print(f"ID: {note['id']}")
            print(f"Заголовок: {note['title']}")
            print(f"Содержание: {note['body']}")
            print(f"Дата/время создания: {note['timestamp']}")
            print("-" * 20)


def edit_note(note_id, title, body):
    notes = load_notes(json_notes_file)
    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["body"] = body
            note["timestamp"] = datetime.datetime.now().isoformat()
            save_notes(notes, json_notes_file)
            save_notes(notes, csv_notes_file)
            print("Заметка отредактирована успешно!")
            return
    print("Заметка с указанным ID не найдена.")


def delete_note(note_id):
    notes = load_notes(json_notes_file)
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            save_notes(notes, json_notes_file)
            save_notes(notes, csv_notes_file)
            print("Заметка удалена успешно!")
            return
    print("Заметка с указанным ID не найдена.")


def search_notes(query):
    notes = load_notes(json_notes_file)
    matching_notes = []
    for note in notes:
        if query.lower() in note["title"].lower() or query.lower() in note["body"].lower():
            matching_notes.append(note)
    if not matching_notes:
        print("Совпадений не найдено.")
    else:
        for note in matching_notes:
            print(f"ID: {note['id']}")
            print(f"Заголовок: {note['title']}")
            print(f"Содержание: {note['body']}")
            print(f"Дата/время создания: {note['timestamp']}")
            print("-" * 20)


while True:
    print("\nКоманды:")
    print("1. Добавить заметку")
    print("2. Список заметок")
    print("3. Редактировать заметку")
    print("4. Удалить заметку")
    print("5. Поиск заметок")
    print("6. Выйти из программы")

    choice = input("Выберите команду: ")

    if choice == "1":
        title = input("Введите заголовок заметки: ")
        body = input("Введите текст заметки: ")
        add_note(title, body)
    elif choice == "2":
        list_notes()
    elif choice == "3":
        note_id = int(input("Введите ID заметки для редактирования: "))
        title = input("Введите новый заголовок: ")
        body = input("Введите новое содержание: ")
        edit_note(note_id, title, body)
    elif choice == "4":
        note_id = int(input("Введите ID заметки для удаления: "))
        delete_note(note_id)
    elif choice == "5":
        query = input("Введите текст для поиска: ")
        search_notes(query)
    elif choice == "6":
        break
    else:
        print("Неверная команда. Пожалуйста, выберите существующую команду.")