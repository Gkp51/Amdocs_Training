import mysql.connector
import hashlib
import csv

# Connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",    
        user="root",         
        password="G#ayatri#09",      
        database="student_management",
        port=3307
    )

# Register a new user
def register_user(email, username, password, phone_no, role):
    db = connect_db()
    cursor = db.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "INSERT INTO users (email, username, password, phone_no, role) VALUES (%s, %s, %s, %s, %s)"
    val = (email, username, hashed_password, phone_no, role)
    try:
        cursor.execute(sql, val)
        db.commit()
        print("{} '{}' registered successfully!".format(role.capitalize(), username))
    except mysql.connector.errors.IntegrityError:
        print("Username or email already exists.")
    cursor.close()
    db.close()

# Login user
def login_user(username, password):
    db = connect_db()
    cursor = db.cursor()    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()   
    sql = "SELECT role FROM users WHERE username = %s AND password = %s"
    val = (username, hashed_password)  
    cursor.execute(sql, val)      
    result = cursor.fetchone()
    cursor.close()
    db.close()    
    if result:
        print("Login successful! Logged in as {}.".format(result[0].capitalize()))
        return result[0]
    else:
        print("Invalid username or password.")
        return None

# Add a student record
def add_student(name, age, contact, gender, email, dob, address):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO students (name, age, contact, gender, email, dob, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (name, age, contact, gender, email, dob, address)
    cursor.execute(sql, val)
    db.commit()
    print("Student {} added successfully!".format(name))
    cursor.close()
    db.close()

# Display all student records
def display_students():
    db = connect_db()
    cursor = db.cursor()
    sql = "SELECT * FROM students"
    cursor.execute(sql) 
    results = cursor.fetchall()    
    if len(results) == 0:
        print("No students data found in the database.")
    else:
        print("Roll No | Name | Age | Contact | Gender | Email | DOB | Address")
        print("---------------------------------------------------------------")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]}")    
    cursor.close()
    db.close()

# Search for a student by roll number
def search_student(roll_no):
    db = connect_db()
    cursor = db.cursor()
    sql = "SELECT * FROM students WHERE roll_no = %s"
    val = (roll_no,)  
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        print("Roll No | Name | Age | Contact | Gender | Email | DOB | Address")
        print("-------------------------------------------------------------")
        print(f"{result[0]} | {result[1]} | {result[2]} | {result[3]} | {result[4]} | {result[5]} | {result[6]} | {result[7]}")
    else:
        print("Student not found.")
    cursor.close()
    db.close()

# Update a student record
def update_student(roll_no, name=None, age=None, contact=None, gender=None, email=None, dob=None, address=None):
    db = connect_db()
    cursor = db.cursor()
    updates = []
    params = []
    
    if name:
        updates.append("name = %s")
        params.append(name)
    if age:
        updates.append("age = %s")
        params.append(age)
    if contact:
        updates.append("contact = %s")
        params.append(contact)
    if gender:
        updates.append("gender = %s")
        params.append(gender)
    if email:
        updates.append("email = %s")
        params.append(email)
    if dob:
        updates.append("dob = %s")
        params.append(dob)
    if address:
        updates.append("address = %s")
        params.append(address)

    sql = f"UPDATE students SET {', '.join(updates)} WHERE roll_no = %s"
    params.append(roll_no)
    cursor.execute(sql, params)
    db.commit()
    print(f"Student Roll No {roll_no} updated successfully!")
    cursor.close()
    db.close()

# Delete a student record
def delete_student(roll_no):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE roll_no = %s", (roll_no,))
    db.commit()
    print(f"Student Roll No {roll_no} deleted successfully!")
    cursor.close()
    db.close()

# Export all student data to CSV
def export_data():
    db = connect_db()
    cursor = db.cursor()
    sql="SELECT * FROM students"
    cursor.execute(sql)
    results = cursor.fetchall()
    with open("students_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Roll No", "Name", "Age", "Contact", "Gender", "Email", "DOB", "Address"])
        writer.writerows(results)
    print("Data exported to students_data.csv successfully!")
    cursor.close()
    db.close()

def reset_password(email, username):
    db = connect_db()
    cursor = db.cursor()
    sql = "SELECT email FROM users WHERE email = %s AND username = %s"
    val=(email, username)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    
    if result:
        new_password = input("Enter your new password: ")
        confirm_password = input("Confirm your new password: ")
        
        if new_password == confirm_password:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            sql = "UPDATE users SET password = %s WHERE email = %s AND username = %s"
            val = (hashed_password, email, username)
            cursor.execute(sql, val)
            db.commit()
            print("Password reset successful!")
        else:
            print("Passwords do not match.")
    else:
        print("Email and username do not match our records.")
    
    cursor.close()
    db.close()

# Admin menu
def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Search Student by Roll No")
        print("4. Update Student by Roll No")
        print("5. Delete Student by Roll No")
        print("6. Export Data to CSV")
        print("7. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            contact = input("Enter contact number: ")
            gender = input("Enter gender (M/F/Other): ")
            email = input("Enter email: ")
            dob = input("Enter date of birth (YYYY-MM-DD): ")
            address = input("Enter address: ")
            add_student(name, age, contact, gender, email, dob, address)
        elif choice == '2':
            display_students()
        elif choice == '3':
            roll_no = int(input("Enter roll number to search: "))
            search_student(roll_no)
        elif choice == '4':
            roll_no = int(input("Enter roll number to update: "))
            name = input("Enter new name (leave blank to skip): ")
            age = input("Enter new age (leave blank to skip): ")
            contact = input("Enter new contact (leave blank to skip): ")
            gender = input("Enter new gender (leave blank to skip): ")
            email = input("Enter new email (leave blank to skip): ")
            dob = input("Enter new date of birth (leave blank to skip): ")
            address = input("Enter new address (leave blank to skip): ")
            update_student(roll_no, name or None, int(age) if age else None, contact or None, gender or None, email or None, dob or None, address or None)
        elif choice == '5':
            roll_no = int(input("Enter roll number to delete: "))
            delete_student(roll_no)
        elif choice == '6':
            export_data()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

# Faculty menu
def faculty_menu():
    while True:
        print("\nFaculty Menu")
        print("1. Display All Students")
        print("2. Search Student")
        print("3. Export Data")
        print("4. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            display_students()
        elif choice == '2':
            roll_no = int(input("Enter roll number to search: "))
            search_student(roll_no)
        elif choice == '3':
            export_data()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Student menu
def student_menu():
    while True:
        print("\nStudent Menu")
        print("1. View My Record")
        print("2. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            roll_no = int(input("Enter roll number to view your record: "))
            search_student(roll_no)
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    while True:
        print("\n                                            Student Management System                                     ")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            email = input("Enter email: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            phone_no = input("Enter phone number: ")
            role = input("Enter role (admin, faculty, student): ").lower()
            if role in ['admin', 'faculty', 'student']:
                register_user(email, username, password, phone_no, role)
            else:
                print("Invalid role.")
        
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = login_user(username, password)
            if role == 'admin':
                admin_menu()
            elif role == 'faculty':
                faculty_menu()
            elif role == 'student':
                student_menu()
        
        elif choice == '3':
            email = input("Enter your registered email: ")
            username = input("Enter your username: ")
            reset_password(email, username)
        
        elif choice == '4':
            break

if __name__ == "__main__":
    main()
