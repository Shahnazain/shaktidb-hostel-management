from db import get_connection


class ComplaintService:

    def get_priority(self, description):
        description = description.lower()

        high_keywords = [
            "fire", "spark", "short circuit",
            "flood", "leak", "electric shock"
        ]

        medium_keywords = [
            "no water",
            "no electricity",
            "wifi",
            "internet",
            "network"
        ]

        for word in high_keywords:
            if word in description:
                return "High"

        for word in medium_keywords:
            if word in description:
                return "Medium"

        return "Low"

    def report_complaint(self, student_id):

        print("\n===== Report Complaint =====")

        print("1. Water")
        print("2. Electricity")
        print("3. WiFi")
        print("4. Plumbing")
        print("5. Other")

        category_map = {
            "1": "Water",
            "2": "Electricity",
            "3": "WiFi",
            "4": "Plumbing",
            "5": "Other"
        }

        choice = input("Choose Category: ")

        if choice not in category_map:
            print("Invalid category.")
            return

        category = category_map[choice]

        description = input("Describe the issue: ")

        priority = self.get_priority(description)

        connection = get_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO complaints
                (
                    student_id,
                    category,
                    description,
                    priority
                )
                VALUES (%s,%s,%s,%s)
                RETURNING complaint_id
                """,
                (
                    student_id,
                    category,
                    description,
                    priority
                )
            )

            complaint_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO complaint_status_history
                (
                    complaint_id,
                    old_status,
                    new_status
                )
                VALUES (%s,%s,%s)
                """,
                (
                    complaint_id,
                    None,
                    "Pending"
                )
            )

            connection.commit()

            print("\nComplaint Submitted Successfully!")
            print(f"Complaint ID : {complaint_id}")
            print(f"Priority     : {priority}")

        except Exception as e:
            connection.rollback()
            print(e)

        finally:
            cursor.close()
            connection.close()
