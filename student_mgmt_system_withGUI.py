import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


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
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def search_student():
    keyword = search_var.get().strip()
    if keyword == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a name or program."
        )
        return
    # Switch to View Students page
    search_frame.pack_forget()
    view_frame.pack(fill="both", expand=True)
    # Clear old records
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute(
        """
        SELECT * FROM students
        WHERE name LIKE ? OR program LIKE ?
        """,
        ('%' + keyword + '%', '%' + keyword + '%')
    )
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            tree.insert("", tk.END, values=row)
    else:
        messagebox.showinfo(
            "Search",
            "No matching student found."
        )

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

root = tk.Tk()
root.title("Student Management System")

# Create StringVars 
name_var = tk.StringVar()
email_var = tk.StringVar()
program_var = tk.StringVar()
semester_var = tk.StringVar()
cgpa_var = tk.StringVar()
search_var = tk.StringVar()

# create frames
dashboard = tk.Frame(root)
dashboard.pack(expand=True)
add_frame = tk.Frame(root)
update_frame = tk.Frame(root)
delete_frame = tk.Frame(root)



def show_frame(frame):

    dashboard.pack_forget()
    add_frame.pack_forget()
    view_frame.pack_forget()
    search_frame.pack_forget()
    update_frame.pack_forget()
    delete_frame.pack_forget()

    frame.pack(fill="both",expand=True)


tk.Label(
    dashboard,
    text="Student Management System",
    font=("Arial",20,"bold")
).pack(pady=20)



tk.Button(dashboard,text="Add Student",width=20,
          command=lambda:show_frame(add_frame)).pack(pady=5)

tk.Button(dashboard,text="View Students",width=20,
    command=lambda:(
        show_frame(view_frame),
        view_students()
    )
).pack(pady=5)
tk.Button(dashboard,text="Search Student",width=20,
          command=lambda:show_frame(search_frame)).pack(pady=5)

tk.Button(dashboard,text="Update Student",width=20,
          command=lambda:show_frame(update_frame)).pack(pady=5)

tk.Button(dashboard,text="Delete Student",width=20,
          command=lambda:show_frame(delete_frame)).pack(pady=5)

tk.Button(dashboard,text="Exit",width=20,
          command=root.destroy).pack(pady=5)

#add student screen
add_frame = tk.Frame(root)

tk.Label(add_frame,text="Add Student",
         font=("Arial",18)).pack(pady=15)

form=tk.Frame(add_frame)
form.pack()

tk.Label(form,text="Name").grid(row=0,column=0,padx=5,pady=5)
tk.Entry(form,textvariable=name_var).grid(row=0,column=1)

tk.Label(form,text="Email").grid(row=1,column=0)
tk.Entry(form,textvariable=email_var).grid(row=1,column=1)

tk.Label(form,text="Program").grid(row=2,column=0)
tk.Entry(form,textvariable=program_var).grid(row=2,column=1)

tk.Label(form,text="Semester").grid(row=3,column=0)
tk.Entry(form,textvariable=semester_var).grid(row=3,column=1)

tk.Label(form,text="CGPA").grid(row=4,column=0)
tk.Entry(form,textvariable=cgpa_var).grid(row=4,column=1)

tk.Button(add_frame,text="Save",
          command=add_student).pack(pady=10)

tk.Button(add_frame,text="Back",
          command=lambda:[add_frame.pack_forget(),
                          dashboard.pack(expand=True)]).pack()

#view student screen
view_frame=tk.Frame(root)

tree=ttk.Treeview(
    view_frame,
    columns=("ID","Name","Email","Program","Semester","CGPA","Date"),
    show="headings"
)

for col in ("ID","Name","Email","Program","Semester","CGPA","Date"):
    tree.heading(col,text=col)

tree.pack(fill="both",expand=True)

tk.Button(
    view_frame,
    text="Back",
    command=lambda:[
        view_frame.pack_forget(),
        dashboard.pack(expand=True)
    ]
).pack(pady=10)


#search screen
search_frame=tk.Frame(root)

tk.Label(search_frame,
         text="Search Student",
         font=("Arial",18)).pack(pady=10)

tk.Entry(search_frame,
         textvariable=search_var,
         width=30).pack()

tk.Button(search_frame,
          text="Search",
          command=search_student).pack(pady=10)

tree.pack(fill="both", expand=True)

tk.Button(
    search_frame,
    text="Back",
    width=15,
    command=lambda:[
        search_frame.pack_forget(),
        dashboard.pack(expand=True)
    ]
).pack(pady=10)

#update student screen
update_frame = tk.Frame(root)

tk.Label(
    update_frame,
    text="Update Student",
    font=("Arial",18,"bold")
).pack(pady=15)

form = tk.Frame(update_frame)
form.pack()

tk.Label(form,text="Email").grid(row=0,column=0,padx=10,pady=5)
tk.Entry(form,textvariable=email_var).grid(row=0,column=1)

tk.Label(form,text="New CGPA").grid(row=1,column=0,padx=10,pady=5)
tk.Entry(form,textvariable=cgpa_var).grid(row=1,column=1)

tk.Button(
    update_frame,
    text="Update",
    width=15,
    command=update_student
).pack(pady=10)

tk.Button(
    update_frame,
    text="Back",
    width=15,
    command=lambda:[
        update_frame.pack_forget(),
        dashboard.pack(expand=True)
    ]
).pack()

#delete student screen
delete_frame = tk.Frame(root)

tk.Label(
    delete_frame,
    text="Delete Student",
    font=("Arial",18,"bold")
).pack(pady=20)

form = tk.Frame(delete_frame)
form.pack()

tk.Label(form,text="Email").grid(row=0,column=0,padx=10,pady=5)

tk.Entry(
    form,
    textvariable=email_var
).grid(row=0,column=1)

tk.Button(
    delete_frame,
    text="Delete",
    width=15,
    command=delete_student
).pack(pady=10)

tk.Button(
    delete_frame,
    text="Back",
    width=15,
    command=lambda:[
        delete_frame.pack_forget(),
        dashboard.pack(expand=True)
    ]
).pack()

root.mainloop()