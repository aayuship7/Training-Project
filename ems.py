import mysql.connector

# Connect to the database
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="EmpManage"
)

cursorObject = database.cursor()

# Function to register a new user
def register():
    full_name = input("Enter your full name: ")
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    re_password = input("Re-enter your password: ")
    mobile_number = input("Enter your mobile number: ")
    email = input("Enter your email ID: ")
    gender = input("Enter your gender (Male/Female/Other): ")

    # Check if passwords match
    if password != re_password:
        print("Passwords do not match. Please try again.")
        return

    try:
        # Insert user details into the users table
        query = """INSERT INTO users (FullName, Username, UserPassword, MobileNumber, Email, Gender) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursorObject.execute(query, (full_name, username, password, mobile_number, email, gender))
        database.commit()
        print("Registration successful! You can now log in.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Registration failed. Try a different username.")

# Function to log in an existing user
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    query = "SELECT * FROM users WHERE Username = %s AND UserPassword = %s"
    cursorObject.execute(query, (username, password))
    user = cursorObject.fetchone()

    if user:
        print(f"Welcome, {username}!")
        return True
    else:
        print("Invalid credentials. Please try again.")
        return False

# Employee Management Functions
def add_employee():
    emp_id = input("Enter Employee ID: ")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    department = input("Enter Department: ")
    position = input("Enter Position: ")
    salary = float(input("Enter Salary: "))
    hire_date = input("Enter Hire Date (YYYY-MM-DD): ")

    query = """INSERT INTO employees (EmployeeID, FirstName, LastName, Department, Position, Salary, HireDate) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    values = (emp_id, first_name, last_name, department, position, salary, hire_date)
    cursorObject.execute(query, values)
    database.commit()
    print("Employee added successfully!")

def remove_employee():
    emp_id = input("Enter Employee ID to remove: ")
    query = "DELETE FROM employees WHERE EmployeeID = %s"
    cursorObject.execute(query, (emp_id,))
    database.commit()
    print("Employee removed successfully!")

def promote_employee():
    emp_id = input("Enter Employee ID to promote: ")
    new_position = input("Enter new Position: ")
    new_salary = float(input("Enter new Salary: "))
    query = "UPDATE employees SET Position = %s, Salary = %s WHERE EmployeeID = %s"
    cursorObject.execute(query, (new_position, new_salary, emp_id))
    database.commit()
    print("Employee promoted successfully!")

def update_employee():
    emp_id = input("Enter Employee ID to update: ")
    first_name = input("Enter new First Name: ")
    last_name = input("Enter new Last Name: ")
    department = input("Enter new Department: ")
    position = input("Enter new Position: ")

    # Fetch the current salary from the database
    query = "SELECT Salary FROM employees WHERE EmployeeID = %s"
    cursorObject.execute(query, (emp_id,))
    current_salary = cursorObject.fetchone()

    if current_salary:
        current_salary_float = float(current_salary[0])  # Convert Decimal to float
        print(f"Current Salary: {current_salary_float}")
        percentage_increment = float(input("Enter the percentage increment for Salary: "))
        new_salary = current_salary_float + (current_salary_float * percentage_increment / 100)
        print(f"New Salary after {percentage_increment}% increment: {new_salary}")

        # Proceed with the update
        query = """UPDATE employees SET FirstName = %s, LastName = %s, Department = %s, 
                   Position = %s, Salary = %s WHERE EmployeeID = %s"""
        cursorObject.execute(query, (first_name, last_name, department, position, new_salary, emp_id))
        database.commit()
        print("Employee updated successfully!")
    else:
        print("Employee not found!")

def display_all_employees():
    query = "SELECT * FROM employees"
    cursorObject.execute(query)
    employees = cursorObject.fetchall()
    total_employees = len(employees)

    print("\n--- Employee List ---")
    for employee in employees:
        print(employee)

    print(f"\nTotal Number of Employees: {total_employees}")

def search_employee_by_id():
    emp_id = input("Enter Employee ID to search: ")
    query = "SELECT * FROM employees WHERE EmployeeID = %s"
    cursorObject.execute(query, (emp_id,))
    employee = cursorObject.fetchone()
    if employee:
        print(employee)
    else:
        print("Employee not found!")

def filter_employees_by_department():
    department = input("Enter department to filter by: ")
    query = "SELECT * FROM employees WHERE Department = %s"
    cursorObject.execute(query, (department,))
    employees = cursorObject.fetchall()
    for employee in employees:
        print(employee)

def sort_employees_by_joining_date():
    query = "SELECT * FROM employees ORDER BY HireDate"
    cursorObject.execute(query)
    employees = cursorObject.fetchall()
    for employee in employees:
        print(employee)

# Employee Management System Menu
def employee_management_system():
    while True:
        print("\n--- Employee Management System ---")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Promote Employee")
        print("4. Update Employee")
        print("5. Display All Employees")
        print("6. Search Employee by Employee ID")
        print("7. Filter Employees by Department")
        print("8. Sort Employees by Hire Date")
        print("9. Logout")

        choice = input("Enter the number of the action you wish to perform: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            remove_employee()
        elif choice == '3':
            promote_employee()
        elif choice == '4':
            update_employee()
        elif choice == '5':
            display_all_employees()
        elif choice == '6':
            search_employee_by_id()
        elif choice == '7':
            filter_employees_by_department()
        elif choice == '8':
            sort_employees_by_joining_date()
        elif choice == '9':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# Main Function: Login or Register
def main():
    while True:
        print("\n--- Welcome to Employee Management System ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            if login():
                employee_management_system()
        elif choice == '2':
            register()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Start the application
main()

# Close the database connection
cursorObject.close()
database.close()