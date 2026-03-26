"""
Custom Library - Grade Calculator Module
"""

class GradeCalculator:
    """Utility class for grade calculations"""
    
    @staticmethod
    def get_letter_grade(percentage=None):
        """Convert percentage to letter grade"""
        
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
        
        for grade in grades:
            letter = GradeCalculator.get_letter_grade(grade)
            distribution[letter] += 1
        
        return distribution
    
    @staticmethod
    def is_passing(grade, passing_score=60):
        """Check if a grade is passing"""
        return grade >= passing_score


import statistics

class StatisticsCalculator:
    """Advanced statistical calculations for grades"""
    
    @staticmethod
    def calculate_percentile(grades, percentile):
        """Calculate nth percentile of grades"""
        if not grades:
            return None
        sorted_grades = sorted(grades)
        index = (percentile / 100) * (len(sorted_grades) - 1)
        return sorted_grades[int(index)]
    
    @staticmethod
    def get_grade_trend(grades):
        """Analyze if grades are improving, declining, or stable"""
        if len(grades) < 2:
            return "Insufficient data"
        
        first_half = sum(grades[:len(grades)//2]) / len(grades[:len(grades)//2])
        second_half = sum(grades[len(grades)//2:]) / len(grades[len(grades)//2:])
        
        if second_half > first_half + 5:
            return " Improving"
        elif second_half < first_half - 5:
            return " Declining"
        else:
            return " Stable"