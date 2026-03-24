"""
Student Grade Tracker - Main Application
"""

import csv
import re
from datetime import datetime
from custom_library import GradeCalculator 

class Person:
    """Base class demonstrating inheritance"""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_date = datetime.now()
    
    def display_info(self):
        """Method to be overridden by child classes"""
        return f"Name: {self.name}, Email: {self.email}"


class Student(Person):
    """Student class inheriting from Person"""
    
    def __init__(self, student_id, name, email):
        super().__init__(name, email)
        self.student_id = student_id
        self.grades = None 
    def add_grade(self, subject, grade):
        """Add a grade for a subject"""
        if subject not in self.grades:  
        self.grades[subject].append(grade)
    
    def get_average(self, subject=None):
        """Calculate average grade for a subject or all subjects"""
        if subject:
            return sum(self.grades[subject]) / len(self.grades[subject])
        else:
            all_grades = []
            for grades_list in self.grades.values():
                all_grades.extend(grades_list)
            return sum(all_grades) / len(all_grades)
    
    def display_info(self):
        """Override parent method"""
        avg = self.get_average()
        letter = GradeCalculator.get_letter_grade()
        return (f"Student: {self.name} (ID: {self.student_id})\n"
                f"Email: {self.email}\n"
                f"Average Grade: {avg:.2f}% ({letter})")


class GradeTracker:
    """Main application class"""
    
    def __init__(self):
        self.students = {}  
        self.filename = "students.csv"
        self.load_data()
    
    def validate_email(self, email):
        """Validate email format using regex"""
       
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$'
        return re.match(pattern, email) is not None
    
    def validate_student_id(self, student_id):
        """Validate student ID format using regex (S-YYYY-NNNN)"""
        pattern = r'^\d{4}-\d{4}$'
        return re.match(pattern, student_id) is not None
    
    def add_student(self, student_id, name, email):
        """Add a new student"""
        
        if student_id in self.students:
            print("Error: Student ID already exists")
            return False
        
        try:
            student = Student(student_id, name, email)
            self.students[student_id] = student
            print(f"Success: Student {name} added!")
            self.save_data()
            return True
        except Exception as e:
            print(f"Error adding student: {e}")
            return False
    
    def add_grade(self, student_id, subject, grade):
        """Add a grade for a student"""
        self.students[student_id].add_grade(subject, grade) 
        print(f"Success: Added {grade}% for {subject}")
        self.save_data()
        return True
    
    def display_student_report(self, student_id):
        """Display detailed report for a student"""
        student = self.students[student_id]
        print("\n" + "="*50)
        print(student.display_info())
        print("-"*50)
        
        if student.grades:
            print("Grades by Subject:")
            for subject, grades in student.grades.items():
                avg = sum(grades) / len(grades)
                letter = GradeCalculator.get_letter_grade(avg)
                print(f"  {subject}: {grades} (Avg: {avg:.1f}% - {letter})")
        else:
            print("No grades recorded yet")
        
        print("="*50 + "\n")
    
    def display_class_report(self):
        """Display report for all students"""
        if not self.students:
            print("No students in system")
            return
        
        print("\n" + "="*50)
        print("CLASS REPORT")
        print("="*50)
        
        all_averages = []
        for student in self.students.values():
            avg = student.get_average()
            all_averages.append(avg)
            print(f"{student.name}: {avg:.1f}%")
        
        if all_averages:
            class_avg = sum(self.students) / len(all_averages)
            print("-"*50)
            print(f"Class Average: {class_avg:.1f}%")
        
        print("="*50 + "\n")
    
    def save_data(self):
        """Save student data to CSV file"""
        try:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Student ID', 'Name', 'Email', 'Grades'])
                
                for student in self.students.values():
                    grades_str = str(student.grades)
                    writer.writerow([student.student_id, student.name, student.email, grades_str])
            
            print("Data saved to students.csv")
        except:
            print("Error saving data")
    
    def load_data(self):
        """Load student data from CSV file"""
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                next(reader) 
                
                for row in reader:
                    if len(row) >= 4:
                        student_id, name, email, grades_str = row[:4]
                        
                        student = Student(student_id, name, email)
                        import ast
                        student.grades = ast.literal_eval(grades_str)
                        
                        self.students[student_id] = student
            
            if self.students:
                print(f"Loaded {len(self.students)} students from file")
        except FileNotFoundError:
            print("No existing data file found. Starting fresh.")
        except:
            pass


def main():
    """Main menu function"""
    tracker = GradeTracker()
    
    while True:
        print("\n=== STUDENT GRADE TRACKER ===")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. View Student Report")
        print("4. View Class Report")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == '1':
            print("\n--- Add New Student ---")
            student_id = input("Student ID (format: S-2024-0001): ").strip()
            name = input("Student Name: ").strip()
            email = input("Student Email: ").strip()
            tracker.add_student(student_id, name, email)
        
        elif choice == '2':
            print("\n--- Add Grade ---")
            student_id = input("Student ID: ").strip()
            subject = input("Subject: ").strip()
            grade = input("Grade (0-100): ").strip()
            tracker.add_grade(student_id, subject, grade)
        
        elif choice == '3':
            print("\n--- Student Report ---")
            student_id = input("Student ID: ").strip()
            tracker.display_student_report(student_id)
        
        elif choice == '4':
            tracker.display_class_report()
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()