"""
Test Module - Tests all functionality
"""

import unittest
import os
from mini_project_2 import Student, GradeTracker
from custom_library import GradeCalculator


class TestStudent(unittest.TestCase):
    """Test Student class"""
    
    def setUp(self):
        """Set up test data"""
        self.student = Student("S-2024-0001", "John Doe", "john@email.com")
    
    def test_add_grade(self):
        """Test adding grades"""
        self.student.add_grade("Math", 85)
        self.assertEqual(len(self.student.grades["Math"]), 1)
        self.assertEqual(self.student.grades["Math"][0], 85)
    
    def test_add_multiple_grades(self):
        """Test adding multiple grades to same subject"""
        self.student.add_grade("Math", 85)
        self.student.add_grade("Math", 90)
        self.assertEqual(len(self.student.grades["Math"]), 2)
    
    def test_subject_average(self):
        """Test calculating average for a subject"""
        self.student.add_grade("Math", 80)
        self.student.add_grade("Math", 100)
        self.assertEqual(self.student.get_average("Math"), 90)
    
    def test_overall_average(self):
        """Test calculating overall average across subjects"""
        self.student.add_grade("Math", 80)
        self.student.add_grade("Math", 100)
        self.student.add_grade("Science", 90)
        self.assertEqual(self.student.get_average(), 90)
    
    def test_empty_average(self):
        """Test average with no grades"""
        self.assertEqual(self.student.get_average(), 0)
    
    def test_invalid_grade(self):
        """Test adding invalid grade"""
        with self.assertRaises(ValueError):
            self.student.add_grade("Math", 105)
        with self.assertRaises(ValueError):
            self.student.add_grade("Math", -10)


class TestGradeCalculator(unittest.TestCase):
    """Test GradeCalculator utility"""
    
    def test_letter_grades(self):
        """Test letter grade conversion"""
        self.assertEqual(GradeCalculator.get_letter_grade(95), 'A')
        self.assertEqual(GradeCalculator.get_letter_grade(85), 'B')
        self.assertEqual(GradeCalculator.get_letter_grade(75), 'C')
        self.assertEqual(GradeCalculator.get_letter_grade(65), 'D')
        self.assertEqual(GradeCalculator.get_letter_grade(55), 'F')
        self.assertEqual(GradeCalculator.get_letter_grade(90), 'A')
        self.assertEqual(GradeCalculator.get_letter_grade(89), 'B')
    
    def test_grade_distribution(self):
        """Test grade distribution calculation"""
        grades = [95, 85, 75, 65, 55]
        dist = GradeCalculator.get_grade_distribution(grades)
        self.assertEqual(dist['A'], 1)
        self.assertEqual(dist['B'], 1)
        self.assertEqual(dist['C'], 1)
        self.assertEqual(dist['D'], 1)
        self.assertEqual(dist['F'], 1)
    
    def test_is_passing(self):
        """Test passing grade check"""
        self.assertTrue(GradeCalculator.is_passing(75))
        self.assertTrue(GradeCalculator.is_passing(60))
        self.assertFalse(GradeCalculator.is_passing(59))
        self.assertFalse(GradeCalculator.is_passing("invalid"))


class TestGradeTracker(unittest.TestCase):
    """Test GradeTracker functionality"""
    
    def setUp(self):
        """Set up test tracker"""
        self.tracker = GradeTracker()
        self.tracker.students = {}  # Clear any loaded data
        # Use a test file
        self.tracker.filename = "test_students.csv"
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists("test_students.csv"):
            os.remove("test_students.csv")
    
    def test_validate_email(self):
        """Test email validation with regex"""
        # Valid emails
        self.assertTrue(self.tracker.validate_email("test@email.com"))
        self.assertTrue(self.tracker.validate_email("test.name@domain.co.uk"))
        
        # Invalid emails
        self.assertFalse(self.tracker.validate_email("invalid-email"))
        self.assertFalse(self.tracker.validate_email("test@"))
        self.assertFalse(self.tracker.validate_email("@domain.com"))
    
    def test_validate_student_id(self):
        """Test student ID validation with regex"""
        # Valid IDs
        self.assertTrue(self.tracker.validate_student_id("S-2024-0001"))
        self.assertTrue(self.tracker.validate_student_id("S-2023-1234"))
        
        # Invalid IDs
        self.assertFalse(self.tracker.validate_student_id("2024-0001"))
        self.assertFalse(self.tracker.validate_student_id("S-2024-001"))
        self.assertFalse(self.tracker.validate_student_id("S-24-0001"))
    
    def test_add_student(self):
        """Test adding students"""
        result = self.tracker.add_student("S-2024-0001", "John Doe", "john@email.com")
        self.assertTrue(result)
        self.assertIn("S-2024-0001", self.tracker.students)
    
    def test_add_duplicate_student(self):
        """Test adding duplicate student"""
        self.tracker.add_student("S-2024-0001", "John Doe", "john@email.com")
        result = self.tracker.add_student("S-2024-0001", "Jane Doe", "jane@email.com")
        self.assertFalse(result)
    
    def test_add_grade_valid(self):
        """Test adding valid grades"""
        self.tracker.add_student("S-2024-0001", "John Doe", "john@email.com")
        result = self.tracker.add_grade("S-2024-0001", "Math", 85)
        self.assertTrue(result)
    
    def test_add_grade_invalid_range(self):
        """Test adding invalid grade values"""
        self.tracker.add_student("S-2024-0001", "John Doe", "john@email.com")
        result = self.tracker.add_grade("S-2024-0001", "Math", 105)
        self.assertFalse(result)
        
        result = self.tracker.add_grade("S-2024-0001", "Math", -10)
        self.assertFalse(result)
    
    def test_add_grade_nonexistent_student(self):
        """Test adding grade for non-existent student"""
        result = self.tracker.add_grade("S-9999-9999", "Math", 85)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)