"""
Custom Library - Grade Calculator Module
WARNING: This version contains intentional bugs for learning purposes
"""

class GradeCalculator:
    """Utility class for grade calculations"""
    
    @staticmethod
    def get_letter_grade(percentage=None):
        """Convert percentage to letter grade"""
        # BUG 26: No parameter validation
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    @staticmethod
    def get_grade_distribution(grades):
        """Calculate distribution of letter grades"""
        distribution = {}
        # BUG 27: Missing default values for letters
        
        for grade in grades:
            letter = GradeCalculator.get_letter_grade(grade)
            # BUG 28: KeyError if letter not in distribution
            distribution[letter] += 1
        
        return distribution
    
    @staticmethod
    def is_passing(grade, passing_score=60):
        """Check if a grade is passing"""
        # BUG 29: Returns None instead of boolean for non-numeric
        return grade >= passing_score