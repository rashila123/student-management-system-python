import sqlite3
# Connect to database
conn = sqlite3.connect("college.db")
cursor = conn.cursor()

# Create table
sql_create_table="""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    program VARCHAR(20),
    semester INTEGER,
    cgpa REAL,
    enrollment_date DATE DEFAULT CURRENT_DATE
)
"""
conn.execute(sql_create_table)
conn.commit()
'''
sql_insert="INSERT INTO students(name,email,program,semester,cgpa) VALUES (?,?,?,?,?)"
record=[
    ('Ram Sharma','ram11@gmail.com','BIM',5,3.6),
    ('Sita Karki','5','BCA',4,3.25),
    ('Hari Thapa','hari56@gmail.com','BBA',6,2.95),
    ('Suman KC','suman22@gmail.com','BCA',2,2.75),
    ('Ramesh Adhikari','ramesh55@gmail.com','BBA',8,3.45),
    ('Priya Shrestha','priya76@gmail.com','BIM',1,3.15)
]
cursor.executemany(sql_insert,record)
conn.commit()
'''
# Add Student
def add_student():
    try:
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        program = input("Enter Program: ")
        semester = int(input("Enter Semester: "))
        cgpa = float(input("Enter CGPA: "))

        cursor.execute(
            "INSERT INTO students(name,email,program,semester,cgpa) VALUES(?,?,?,?,?)",
            (name, email, program, semester, cgpa)
        )
        conn.commit()
        print("Student added successfully.")

    except sqlite3.IntegrityError:
        print("Email already exists!")

    except Exception as e:
        print("Error:", e)


# View Students
def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No records found.")


# Search Student
def search_student():
    key = input("Enter Name or Email: ")

    cursor.execute(
        "SELECT * FROM students WHERE name=? OR email=?",
        (key, key)
    )

    row = cursor.fetchone()

    if row:
        print(row)
    else:
        print("Student not found.")


# Update Student
def update_student():
    email = input("Enter Student Email: ")

    print("1. Update CGPA")
    print("2. Update Semester")
    choice = input("Enter choice: ")

    if choice == "1":
        cgpa = float(input("Enter New CGPA: "))
        cursor.execute(
            "UPDATE students SET cgpa=? WHERE email=?",
            (cgpa, email)
        )

    elif choice == "2":
        semester = int(input("Enter New Semester: "))
        cursor.execute(
            "UPDATE students SET semester=? WHERE email=?",
            (semester, email)
        )

    else:
        print("Invalid choice.")
        return

    conn.commit()

    if cursor.rowcount:
        print("Record updated successfully.")
    else:
        print("Student not found.")


# Delete Student
def delete_student():
    email = input("Enter Student Email: ")

    cursor.execute(
        "DELETE FROM students WHERE email=?",
        (email,)
    )
    conn.commit()

    if cursor.rowcount:
        print("Student deleted successfully.")
    else:
        print("Student not found.")


# Top Performers
def top_performers():
    cursor.execute(
        "SELECT * FROM students WHERE cgpa>?",
        (3.0,)
    )

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No top performers found.")


# Main Menu
while True:

    print("\n===== Student Management System =====")
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student by name or email")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Show Top Performers")
    print("7. Exit")

    choice = input("Enter your choice: ")

    match choice:

        case "1":
            add_student()

        case "2":
            view_students()

        case "3":
            search_student()

        case "4":
            update_student()

        case "5":
            delete_student()

        case "6":
            top_performers()

        case "7":
            print("Thank you!")
            cursor.close()
            conn.close()
            break

        case _:
            print("Invalid choice.")


