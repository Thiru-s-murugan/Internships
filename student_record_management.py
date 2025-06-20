import json
import os
from tabulate import tabulate

class Student:
    """Class to represent a student record"""
    def __init__(self, student_id, name, branch, year, marks):
        self.student_id = student_id
        self.name = name
        self.branch = branch
        self.year = year
        self.marks = marks
    
    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'branch': self.branch,
            'year': self.year,
            'marks': self.marks
        }

class StudentManager:
    """Class to manage student records"""
    def __init__(self, file_path='students.json'):
        self.file_path = file_path
        self.students = []
        self.load_students()
    
    def load_students(self):
        """Load student data from JSON file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.students = [Student(**student) for student in data]
        else:
            self.students = []
    
    def save_students(self):
        """Save student data to JSON file"""
        with open(self.file_path, 'w') as file:
            json.dump([student.to_dict() for student in self.students], file, indent=4)
    
    def add_student(self, student):
        """Add a new student record"""
        if any(s.student_id == student.student_id for s in self.students):
            print(f"Student with ID {student.student_id} already exists!")
            return False
        self.students.append(student)
        self.save_students()
        print("Student added successfully!")
        return True
    
    def view_all_students(self):
        """Display all student records in tabular format"""
        if not self.students:
            print("No student records found!")
            return
        
        headers = ["Student ID", "Name", "Branch", "Year", "Marks"]
        table_data = []
        
        for student in self.students:
            table_data.append([
                student.student_id,
                student.name,
                student.branch,
                student.year,
                student.marks
            ])
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def update_student(self, student_id, new_data):
        """Update an existing student record"""
        for student in self.students:
            if student.student_id == student_id:
                student.name = new_data.get('name', student.name)
                student.branch = new_data.get('branch', student.branch)
                student.year = new_data.get('year', student.year)
                student.marks = new_data.get('marks', student.marks)
                self.save_students()
                print("Student record updated successfully!")
                return True
        
        print(f"Student with ID {student_id} not found!")
        return False
    
    def delete_student(self, student_id):
        """Delete a student record"""
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                del self.students[i]
                self.save_students()
                print("Student record deleted successfully!")
                return True
        
        print(f"Student with ID {student_id} not found!")
        return False

def display_menu():
    """Display the main menu"""
    print("\nStudent Record Management System")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

def get_student_input():
    """Get student details from user input"""
    student_id = input("Enter Student ID: ")
    name = input("Enter Name: ")
    branch = input("Enter Branch: ")
    year = input("Enter Year: ")
    marks = input("Enter Marks: ")
    return Student(student_id, name, branch, year, marks)

def get_update_data():
    """Get updated student details from user input"""
    print("Enter new details (leave blank to keep current value):")
    name = input("Name: ")
    branch = input("Branch: ")
    year = input("Year: ")
    marks = input("Marks: ")
    
    update_data = {}
    if name: update_data['name'] = name
    if branch: update_data['branch'] = branch
    if year: update_data['year'] = year
    if marks: update_data['marks'] = marks
    
    return update_data

def main():
    manager = StudentManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            student = get_student_input()
            manager.add_student(student)
        elif choice == '2':
            manager.view_all_students()
        elif choice == '3':
            student_id = input("Enter Student ID to update: ")
            update_data = get_update_data()
            manager.update_student(student_id, update_data)
        elif choice == '4':
            student_id = input("Enter Student ID to delete: ")
            manager.delete_student(student_id)
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()