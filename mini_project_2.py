"""
Student Grade Tracker - Main Application
Fully functional version with all features
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
        self.grades = {}  # Dictionary: subject -> list of grades
    
    def add_grade(self, subject, grade):
        """Add a grade for a subject"""
        # Validate grade
        if not isinstance(grade, (int, float)) or grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100")
        
        # Validate subject
        if not subject or len(subject.strip()) == 0:
            raise ValueError("Subject cannot be empty")
        
        # Add grade
        subject = subject.strip()
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append(grade)
    
    def get_average(self, subject=None):
        """Calculate average grade for a subject or all subjects"""
        if subject:
            # Average for specific subject
            if subject in self.grades and self.grades[subject]:
                return sum(self.grades[subject]) / len(self.grades[subject])
            return 0.0
        else:
            # Overall average across all subjects
            all_grades = []
            for grades_list in self.grades.values():
                all_grades.extend(grades_list)
            if all_grades:
                return sum(all_grades) / len(all_grades)
            return 0.0
    
    def display_info(self):
        """Override parent method"""
        avg = self.get_average()
        if avg > 0:
            letter = GradeCalculator.get_letter_grade(avg)
            return (f"Student: {self.name} (ID: {self.student_id})\n"
                    f"Email: {self.email}\n"
                    f"Average Grade: {avg:.2f}% ({letter})")
        else:
            return (f"Student: {self.name} (ID: {self.student_id})\n"
                    f"Email: {self.email}\n"
                    f"No grades recorded yet")
    
    def to_dict(self):
        """Convert student to dictionary for CSV storage"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'grades': str(self.grades)
        }


class GradeTracker:
    """Main application class"""
    
    def __init__(self):
        self.students = {}  # Dictionary: student_id -> Student object
        self.filename = "students.csv"
        self.load_data()
    
    def validate_email(self, email):
        """Validate email format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_student_id(self, student_id):
        """Validate student ID format using regex (S-YYYY-NNNN)"""
        pattern = r'^S-\d{4}-\d{4}$'
        return re.match(pattern, student_id) is not None
    
    def add_student(self, student_id, name, email):
        """Add a new student"""
        # Validate student ID format
        if not self.validate_student_id(student_id):
            print("Error: Student ID must be in format S-YYYY-NNNN (e.g., S-2024-0001)")
            return False
        
        # Validate email format
        if not self.validate_email(email):
            print("Error: Invalid email format (e.g., name@domain.com)")
            return False
        
        # Check for duplicate
        if student_id in self.students:
            print("Error: Student ID already exists")
            return False
        
        # Validate name not empty
        if not name or len(name.strip()) == 0:
            print("Error: Name cannot be empty")
            return False
        
        try:
            student = Student(student_id, name.strip(), email.strip())
            self.students[student_id] = student
            print(f"Success: Student {name} added!")
            self.save_data()
            return True
        except Exception as e:
            print(f"Error adding student: {e}")
            return False
    
    def add_grade(self, student_id, subject, grade):
        """Add a grade for a student"""
        # Check if student exists
        if student_id not in self.students:
            print("Error: Student not found")
            return False
        
        # Validate grade
        try:
            grade = float(grade)
            if grade < 0 or grade > 100:
                print("Error: Grade must be between 0 and 100")
                return False
        except ValueError:
            print("Error: Grade must be a number")
            return False
        
        # Validate subject
        if not subject or len(subject.strip()) == 0:
            print("Error: Subject cannot be empty")
            return False
        
        # Add the grade
        try:
            self.students[student_id].add_grade(subject.strip(), grade)
            print(f"Success: Added {grade}% for {subject}")
            self.save_data()
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False
    
    def display_student_report(self, student_id):
        """Display detailed report for a student"""
        # Check if student exists
        if student_id not in self.students:
            print("Error: Student not found")
            return
        
        student = self.students[student_id]
        print("\n" + "="*50)
        print(student.display_info())
        print("-"*50)
        
        if student.grades:
            print("Grades by Subject:")
            for subject, grades in student.grades.items():
                if grades:
                    avg = sum(grades) / len(grades)
                    letter = GradeCalculator.get_letter_grade(avg)
                    grades_str = ", ".join([f"{g}%" for g in grades])
                    print(f"  {subject}: [{grades_str}]")
                    print(f"    Average: {avg:.1f}% (Grade: {letter})")
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
        for student_id, student in self.students.items():
            avg = student.get_average()
            if avg > 0:
                all_averages.append(avg)
                letter = GradeCalculator.get_letter_grade(avg)
                print(f"{student.name} (ID: {student_id}): {avg:.1f}% ({letter})")
            else:
                print(f"{student.name} (ID: {student_id}): No grades yet")
        
        if all_averages:
            class_avg = sum(all_averages) / len(all_averages)
            class_letter = GradeCalculator.get_letter_grade(class_avg)
            print("-"*50)
            print(f"Class Average: {class_avg:.1f}% ({class_letter})")
            
            # Show grade distribution
            distribution = GradeCalculator.get_grade_distribution(all_averages)
            print("\nGrade Distribution:")
            for letter in ['A', 'B', 'C', 'D', 'F']:
                count = distribution.get(letter, 0)
                if count > 0:
                    print(f"  {letter}: {count} student(s)")
        
        print("="*50 + "\n")
    
    def save_data(self):
        """Save student data to CSV file"""
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Student ID', 'Name', 'Email', 'Grades'])
                
                for student in self.students.values():
                    try:
                        grades_str = str(student.grades)
                        writer.writerow([student.student_id, student.name, student.email, grades_str])
                    except Exception as e:
                        print(f"Error writing student {student.student_id}: {e}")
            
            print("Data saved to students.csv")
            return True
        except PermissionError:
            print("Error: Cannot write to file - permission denied")
            return False
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self):
        """Load student data from CSV file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Check if file has header
                try:
                    header = next(reader)
                except StopIteration:
                    print("File is empty")
                    return
                
                for row_num, row in enumerate(reader, start=2):
                    if len(row) >= 4:
                        try:
                            student_id, name, email, grades_str = row[:4]
                            
                            # Create student
                            student = Student(student_id, name, email)
                            
                            # Parse grades if present
                            if grades_str and grades_str != '{}':
                                try:
                                    import ast
                                    parsed_grades = ast.literal_eval(grades_str)
                                    if isinstance(parsed_grades, dict):
                                        student.grades = parsed_grades
                                except (ValueError, SyntaxError) as e:
                                    print(f"Error parsing grades for {student_id}: {e}")
                            
                            self.students[student_id] = student
                        except Exception as e:
                            print(f"Error loading row {row_num}: {e}")
            
            if self.students:
                print(f"Loaded {len(self.students)} students from file")
                
        except FileNotFoundError:
            print("No existing data file found. Starting fresh.")
        except Exception as e:
            print(f"Error loading data: {e}")


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
            try:
                grade = float(input("Grade (0-100): ").strip())
                tracker.add_grade(student_id, subject, grade)
            except ValueError:
                print("Error: Grade must be a number")
        
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