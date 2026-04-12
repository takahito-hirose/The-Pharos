import random
from models.schemas import CategoryScore
from typing import Dict

def perform_static_analysis(code: str) -> Dict[str, CategoryScore]:
    """
    (Dummy Implementation)
    Performs a mock static analysis on the given code and returns initial scores.
    This simulates finding some potential issues and deducting points.
    """
    # Start with perfect scores
    security_score = 100
    maintainability_score = 100
    performance_score = 100

    security_issues = []
    maintainability_issues = []
    performance_issues = []

    # Dummy logic: randomly find "issues"
    if "password" in code.lower() or "secret" in code.lower():
        security_score -= random.randint(20, 40)
        security_issues.append("Potential hardcoded secret detected.")
    
    if len(code.splitlines()) > 50: # Arbitrary length check
        maintainability_score -= random.randint(10, 25)
        maintainability_issues.append("Code is long, potentially impacting maintainability.")

    if "sleep" in code: # Arbitrary performance check
        performance_score -= random.randint(10, 20)
        performance_issues.append("Use of 'sleep' can cause performance bottlenecks.")

    return {
        "security": CategoryScore(score=security_score, issues=security_issues, suggestions=[]),
        "maintainability": CategoryScore(score=maintainability_score, issues=maintainability_issues, suggestions=[]),
        "performance": CategoryScore(score=performance_score, issues=performance_issues, suggestions=[]),
    }