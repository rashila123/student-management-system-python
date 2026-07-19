import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

root = tk.Tk()
root.title("Student Management System")
root.geometry("800x500")

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    program TEXT,
    semester INTEGER,
    cgpa REAL,
    enrollment_date DATE DEFAULT CURRENT_DATE
)
""")

def add_student():
    cursor.execute(
        "INSERT INTO students(name,email,program,semester,cgpa) VALUES(?,?,?,?,?)",
        (
            name_var.get(),
            email_var.get(),
            program_var.get(),
            int(semester_var.get()),
            float(cgpa_var.get())
        )
    )

    conn.commit()
    messagebox.showinfo("Success", "Student Added")

def view_students():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students")

    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def search_student():
    keyword = search_var.get()

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ? OR program LIKE ?",
        ('%' + keyword + '%', '%' + keyword + '%')
    )
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            tree.insert("", tk.END, values=row)
    else:
        messagebox.showinfo("Search", "No matching student found.")

def update_student():
    try:
        cursor.execute(
            "UPDATE students SET cgpa=? WHERE email=?",
            (
                float(cgpa_var.get()),
                email_var.get()
            )
        )

        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "CGPA Updated")
            view_students()
        else:
            messagebox.showerror("Error", "Student not found.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_student():
    try:
        answer = messagebox.askyesno(
            "Delete",
            "Are you sure you want to delete this student?"
        )

        if answer:
            cursor.execute(
                "DELETE FROM students WHERE email=?",
                (email_var.get(),)
            )

            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Student Deleted")
                view_students()
            else:
                messagebox.showerror("Error", "Student not found.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

root_frame = tk.Frame(root)
root_frame.pack(pady=20)

name_var = tk.StringVar()
email_var = tk.StringVar()
program_var = tk.StringVar()
semester_var = tk.StringVar()
cgpa_var = tk.StringVar()
search_var = tk.StringVar()

tk.Label(root_frame, text="Name").grid(row=0,column=0)
tk.Entry(root_frame,textvariable=name_var).grid(row=0,column=1)

tk.Label(root_frame,text="Email").grid(row=1,column=0)
tk.Entry(root_frame,textvariable=email_var).grid(row=1,column=1)

tk.Label(root_frame,text="Program").grid(row=2,column=0)
tk.Entry(root_frame,textvariable=program_var).grid(row=2,column=1)

tk.Label(root_frame,text="Semester").grid(row=3,column=0)
tk.Entry(root_frame,textvariable=semester_var).grid(row=3,column=1)

tk.Label(root_frame,text="CGPA").grid(row=4,column=0)
tk.Entry(root_frame,textvariable=cgpa_var).grid(row=4,column=1)

tk.Button(root_frame,text="Add Student",command=add_student).grid(row=5,column=0,pady=10)
tk.Button(root_frame,text="View Students",command=view_students).grid(row=5,column=1,pady=10)
tk.Button(root_frame,text="Update CGPA",command=update_student).grid(row=6,column=0,pady=10)
tk.Button(root_frame,text="Delete Student",command=delete_student).grid(row=6,column=1,pady=10)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame,text="Search (Name/Program):",font=("Arial", 11)).grid(row=0, column=0, padx=5)

tk.Entry(search_frame,textvariable=search_var,width=30).grid(row=0, column=1, padx=5)

tk.Button(search_frame,text="Search",command=search_student).grid(row=0, column=2, padx=5)

tk.Button(search_frame,text="Show All",command=view_students).grid(row=0, column=3, padx=5)

tree = ttk.Treeview(root,columns=("ID","Name","Email","Program","Semester","CGPA","Date"),show="headings")

for col in ("ID","Name","Email","Program","Semester","CGPA","Date"):
    tree.heading(col,text=col)

tree.pack(fill="both",expand=True)

root.mainloop()