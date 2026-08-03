from db import get_connection
from modules.complaint import ComplaintService
from utils.auth import hash_password, verify_password


class StudentService:

    def register_student(self):
        print("\n===== Student Registration =====")

        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip().lower()
        room_number = input("Enter Room Number: ").strip()
        password = input("Enter Password: ").strip()

        connection = get_connection()

        if connection is None:
            print("❌ Unable to connect to the database.")
            return

        cursor = connection.cursor()

        try:
            # Check if email already exists
            cursor.execute(
                """
                SELECT student_id
                FROM students
                WHERE email = %s
                """,
                (email,)
            )

            if cursor.fetchone():
                print("\n❌ Email already registered.")
                return

            encrypted_password = hash_password(password)

            cursor.execute(
                """
                INSERT INTO students
                (name, email, room_number, password)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    room_number,
                    encrypted_password
                )
            )

            connection.commit()

            print("\n✅ Registration Successful!")

        except Exception as e:
            connection.rollback()
            print(f"\n❌ Error: {e}")

        finally:
            cursor.close()
            connection.close()

    def login_student(self):
        print("\n===== Student Login =====")

        email = input("Enter Email: ").strip().lower()
        password = input("Enter Password: ").strip()

        connection = get_connection()

        if connection is None:
            print("❌ Unable to connect to the database.")
            return

        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT student_id, name, password
                FROM students
                WHERE email = %s
                """,
                (email,)
            )

            student = cursor.fetchone()

            if student is None:
                print("\n❌ Student not found.")
                return

            student_id, name, hashed_password = student

            if verify_password(password, hashed_password):
                print(f"\n✅ Login Successful. Welcome, {name}!")
                self.student_dashboard(student_id, name)
            else:
                print("\n❌ Incorrect password.")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        finally:
            cursor.close()
            connection.close()

    def student_dashboard(self, student_id, name):

        while True:

            print("\n===================================")
            print("        STUDENT DASHBOARD")
            print("===================================")
            print(f"Welcome, {name}")
            print("-----------------------------------")
            print("1. Report Complaint")
            print("2. View My Complaints")
            print("3. Logout")
            print("===================================")

            choice = input("Enter your choice: ")

            if choice == "1":
                complaint = ComplaintService()
                complaint.report_complaint(student_id)

            elif choice == "2":
                print("\n View My Complaints module will be implemented next.")

            elif choice == "3":
                print("\n Logged out successfully.")
                break

            else:
                print("\n Invalid choice. Please try again.")
