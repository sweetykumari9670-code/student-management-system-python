import json
import os

DATA_FILE = "students.json"


def load_students():
    """Load student records from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read student data.")
        return []


def save_students(students):
    """Save student records to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError:
        print("Error: Could not save student data.")
        return False


def get_student_id():
    """Read and validate a student ID."""
    while True:
        student_id = input("Enter student ID: ").strip()

        if student_id:
            return student_id

        print("Student ID cannot be empty.")


def get_marks():
    """Read marks between 0 and 100."""
    while True:
        try:
            marks = float(input("Enter marks (0-100): "))

            if 0 <= marks <= 100:
                return marks

            print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


def get_grade(marks):
    """Calculate a grade from student marks."""
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


def find_student(students, student_id):
    """Find a student using their ID."""
    for student in students:
        if student["id"].lower() == student_id.lower():
            return student

    return None


def add_student(students):
    """Add a new student record."""
    print("\n--- Add Student ---")

    student_id = get_student_id()

    if find_student(students, student_id):
        print("A student with this ID already exists.")
        return

    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    age = None
    while age is None:
        try:
            entered_age = int(input("Enter age: "))
            if 1 <= entered_age <= 120:
                age = entered_age
            else:
                print("Enter an age between 1 and 120.")
        except ValueError:
            print("Please enter a valid age.")

    course = input("Enter course name: ").strip()
    if not course:
        print("Course name cannot be empty.")
        return

    marks = get_marks()

    student = {
        "id": student_id,
        "name": name,
        "age": age,
        "course": course,
        "marks": marks,
        "grade": get_grade(marks)
    }

    students.append(student)

    if save_students(students):
        print("Student added successfully!")


def view_students(students):
    """Display all student records."""
    print("\n--- Student Records ---")

    if not students:
        print("No student records found.")
        return

    print("-" * 85)
    print(
        f"{'ID':<12}{'Name':<22}{'Age':<8}"
        f"{'Course':<20}{'Marks':<10}{'Grade':<8}"
    )
    print("-" * 85)

    for student in students:
        print(
            f"{student['id']:<12}"
            f"{student['name'][:20]:<22}"
            f"{student['age']:<8}"
            f"{student['course'][:18]:<20}"
            f"{student['marks']:<10.2f}"
            f"{student['grade']:<8}"
        )

    print("-" * 85)
    print("Total students:", len(students))


def search_student(students):
    """Search by student ID or name."""
    print("\n--- Search Student ---")

    if not students:
        print("No student records available.")
        return

    query = input("Enter student ID or name: ").strip().lower()

    if not query:
        print("Search query cannot be empty.")
        return

    results = [
        student for student in students
        if query in student["id"].lower()
        or query in student["name"].lower()
    ]

    if not results:
        print("No matching student found.")
        return

    for student in results:
        print("\nStudent Details")
        print("ID:", student["id"])
        print("Name:", student["name"])
        print("Age:", student["age"])
        print("Course:", student["course"])
        print("Marks:", student["marks"])
        print("Grade:", student["grade"])


def update_student(students):
    """Update an existing student record."""
    print("\n--- Update Student ---")

    student_id = get_student_id()
    student = find_student(students, student_id)

    if student is None:
        print("Student not found.")
        return

    print("Press Enter to keep the current value.")

    new_name = input(
        f"Name [{student['name']}]: "
    ).strip()

    new_course = input(
        f"Course [{student['course']}]: "
    ).strip()

    if new_name:
        student["name"] = new_name

    if new_course:
        student["course"] = new_course

    change_marks = input("Update marks? (y/n): ").strip().lower()

    if change_marks == "y":
        student["marks"] = get_marks()
        student["grade"] = get_grade(student["marks"])

    if save_students(students):
        print("Student record updated successfully!")


def delete_student(students):
    """Delete a student after confirmation."""
    print("\n--- Delete Student ---")

    student_id = get_student_id()
    student = find_student(students, student_id)

    if student is None:
        print("Student not found.")
        return

    print("Student:", student["name"])
    confirmation = input(
        "Are you sure you want to delete this record? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Deletion cancelled.")
        return

    students.remove(student)

    if save_students(students):
        print("Student record deleted successfully!")


def show_statistics(students):
    """Display basic student performance statistics."""
    print("\n--- Student Statistics ---")

    if not students:
        print("No records available for statistics.")
        return

    total = len(students)
    average = sum(s["marks"] for s in students) / total
    highest = max(students, key=lambda s: s["marks"])
    lowest = min(students, key=lambda s: s["marks"])
    passed = sum(1 for s in students if s["marks"] >= 40)

    print("Total students:", total)
    print(f"Average marks: {average:.2f}")
    print("Students scoring 40 or above:", passed)
    print("Students scoring below 40:", total - passed)
    print(
        f"Highest scorer: {highest['name']} "
        f"({highest['marks']:.2f})"
    )
    print(
        f"Lowest scorer: {lowest['name']} "
        f"({lowest['marks']:.2f})"
    )


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 45)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Student Statistics")
    print("7. Exit")
    print("=" * 45)


def main():
    """Run the student management application."""
    students = load_students()

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_student(students)

        elif choice == "2":
            view_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            update_student(students)

        elif choice == "5":
            delete_student(students)

        elif choice == "6":
            show_statistics(students)

        elif choice == "7":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice. Please select from 1 to 7.")


if __name__ == "__main__":
    main()
