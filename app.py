from modules.student import StudentService

student = StudentService()

while True:
    print("\n====================================")
    print(" SMART HOSTEL MANAGEMENT SYSTEM ")
    print("====================================")
    print("1. Student Registration")
    print("2. Student Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        student.register_student()

    elif choice == "2":
        student.login_student()

    elif choice == "3":
        print("\nThank you for using the system!")
        break

    else:
        print("\n❌ Invalid choice.")
