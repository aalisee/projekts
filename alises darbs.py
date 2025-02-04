import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import json

# Datu saglabāšanas un ielādes funkcijas
DATA_FILE = "students_data.json"

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(students_data, file)

def load_data():
    global students_data
    try:
        with open(DATA_FILE, "r") as file:
            students_data = json.load(file)
    except FileNotFoundError:
        students_data = {}

# Sākotnējie dati
students_data = {}
books_data = {
    'Matemātika 101': None,
    'Vēstures Pamati': None,
    'Dabaszinības': None,
    'Programēšanas Ievads': None,
    'Literatūras Klasiķi': None
}

load_data()  # Ielādējam iepriekš saglabātos datus

# Skolēna reģistrācija
def register_student():
    name = name_entry.get().strip().lower()
    surname = surname_entry.get().strip()
    grade = grade_entry.get().strip()

    if name and surname and grade:
        students_data[name] = {
            'surname': surname,
            'grade': grade,
            'books': {}
        }
        save_data()
        messagebox.showinfo("Success", "Reģistrācija veiksmīga!")
    else:
        messagebox.showerror("Error", "Lūdzu aizpildiet visus laukus!")

def borrow_book():
    name = name_entry.get().strip().lower()
    book = book_entry.get().strip()

    if name in students_data:
        if book in books_data:
            if book not in students_data[name]['books']:
                due_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
                students_data[name]['books'][book] = due_date
                save_data()
                messagebox.showinfo("Success", f"Grāmata '{book}' paņemta! Atgriezt līdz {due_date}.")
            else:
                messagebox.showerror("Error", "Šī grāmata jau ir aizņemta!")
        else:
            messagebox.showerror("Error", "Norādītā grāmata neeksistē!")
    else:
        messagebox.showerror("Error", "Skolēns nav reģistrēts!")

def return_book():
    name = name_entry.get().strip().lower()
    book = book_entry.get().strip()

    if name in students_data:
        if book in students_data[name]['books']:
            del students_data[name]['books'][book]
            save_data()
            messagebox.showinfo("Success", f"Grāmata '{book}' veiksmīgi atgriezta!")
        else:
            messagebox.showerror("Error", "Skolēns nav aizņēmies šo grāmatu!")
    else:
        messagebox.showerror("Error", "Skolēns nav reģistrēts!")

def open_student_page():
    name = name_entry.get().strip().lower()

    if name in students_data:
        student = students_data[name]
        student_window = tk.Toplevel(root)
        student_window.title(f"{name.capitalize()} - Bibliotēka")
        
        tk.Label(student_window, text=f"Vārds: {name.capitalize()} {student['surname']}", font=("Helvetica", 12)).pack()
        tk.Label(student_window, text=f"Klase: {student['grade']}", font=("Helvetica", 12)).pack()
        tk.Label(student_window, text="Paņemtās grāmatas:", font=("Helvetica", 14, "bold")).pack(pady=10)

        if student['books']:
            for book, due_date in student['books'].items():
                tk.Label(student_window, text=f"{book} - jānodod līdz {due_date}", font=("Helvetica", 12)).pack()
        else:
            tk.Label(student_window, text="Nav paņemtu grāmatu.", font=("Helvetica", 12)).pack()
    else:
        messagebox.showerror("Error", "Skolēns nav reģistrēts!")

# Galvenais logs
root = tk.Tk()
root.title("Skolas Bibliotēka")

# Reģistrācijas sadaļa
register_frame = tk.Frame(root)
register_frame.pack(pady=20)

tk.Label(register_frame, text="Vārds:").grid(row=0, column=0)
name_entry = tk.Entry(register_frame)
name_entry.grid(row=0, column=1)

tk.Label(register_frame, text="Uzvārds:").grid(row=1, column=0)
surname_entry = tk.Entry(register_frame)
surname_entry.grid(row=1, column=1)

tk.Label(register_frame, text="Klase:").grid(row=2, column=0)
grade_entry = tk.Entry(register_frame)
grade_entry.grid(row=2, column=1)

tk.Button(register_frame, text="Reģistrēt", command=register_student).grid(row=3, columnspan=2)

# Grāmatu aizņemšanas sadaļa
borrow_frame = tk.Frame(root)
borrow_frame.pack(pady=20)

tk.Label(borrow_frame, text="Norādiet grāmatu, kuru vēlaties paņemt:").grid(row=0, column=0)
book_entry = tk.Entry(borrow_frame)
book_entry.grid(row=0, column=1)

tk.Button(borrow_frame, text="Paņemt", command=borrow_book).grid(row=1, column=0)
tk.Button(borrow_frame, text="Atgriezt", command=return_book).grid(row=1, column=1)

# Skolēna informācijas poga
tk.Button(root, text="Skatīt skolēna info", command=open_student_page).pack(pady=10)

library_frame = tk.Frame(root)
library_frame.pack(pady=20)

tk.Label(library_frame, text="Pieejamās grāmatas:", font=("Helvetica", 14, "bold")).pack()
for book in books_data.keys():
    tk.Label(library_frame, text=book, font=("Helvetica", 12)).pack()
