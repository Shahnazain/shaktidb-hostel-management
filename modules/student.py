from db import get_connection
from utils.auth import hash_password, verify_password


class StudentService:

    def register_student(self):
        print("\n===== Student Registration =====")

        name = input("Enter Name: ")
        email = input("Enter Email: ")
        room_number = input("Enter Room Number: ")
        password = input("Enter Password: ")

        connection = get_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT student_id
                FROM students
                WHERE email=%s
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
                (name,email,room_number,password)
                VALUES (%s,%s,%s,%s)
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
            print(e)

        finally:
            cursor.close()
            connection.close()
