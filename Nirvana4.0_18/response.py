def calculate_score(answers, max_points_per_question=None):
    """
    Calculate the score based on the answers dynamically.
    
    Args:
        answers (list): List of integer values from the form
        max_points_per_question (int, optional): Maximum points possible per question.
            If None, it's determined from the highest answer value.
    
    Returns:
        tuple: (raw_score, max_possible_score, percentage)
    """
    # Ensure we have valid answers
    if not answers or len(answers) == 0:
        return 0, 0, 0
    
    # Sum the answers
    total = sum(answers)
    
    # If max_points_per_question wasn't specified, determine it from the data
    if max_points_per_question is None:
        # Find the highest value in answers to determine the scale
        # (assuming the minimum is always 0)
        if answers:
            max_points_per_question = max(answers)
        else:
            max_points_per_question = 0
    
    # Calculate maximum possible score based on number of questions
    max_score = len(answers) * max_points_per_question
    
    # Calculate percentage
    percentage = round((total / max_score) * 100) if max_score > 0 else 0
    
    return total, max_score, percentage

def get_diagnosis(percentage):
    """
    Return the status and diagnosis based on the score percentage.
    
    Args:
        percentage (int): Score as a percentage (0-100)
        
    Returns:
        tuple: (status, diagnosis_text)
    """
    if percentage >= 80:
        status = "High indication"
        diagnosis = "You are likely experiencing symptoms of the condition."
    elif percentage >= 50:
        status = "Moderate indication"
        diagnosis = "You may have some symptoms; monitoring or mild intervention is recommended."
    else:
        status = "Low indication"
        diagnosis = "You show few signs of the condition at the moment."
        
    return status, diagnosis

def get_remedies(condition):
    """
    Return remedies based on the condition.
    
    Args:
        condition (str): Name of the condition
        
    Returns:
        list: List of remedy suggestions
    """
    remedies_by_condition = {
        "depression": [
            "Consider speaking with a mental health professional",
            "Establish a regular exercise routine",
            "Practice mindfulness meditation daily",
            "Maintain a consistent sleep schedule",
            "Reach out to friends and family for social support",
            "Limit alcohol consumption and avoid recreational drugs"
        ],
        "adhd": [
            "Create structured routines for daily tasks",
            "Break large tasks into smaller, manageable steps",
            "Use timers and reminders for time management",
            "Minimize distractions in your work environment",
            "Consider professional assessment for appropriate treatment"
        ],
        "ptsd": [
            "Practice active listening techniques",
            "Develop consistent daily routines",
            "Try organizatiaon strategies like task lists",
            "Limit screen time and excessive stimulation",
            "Consider seeking professional evaluation"
        ],
        "bipolar": [
            "Establish consistent daily routines",
            "Use visual schedules and reminders",
            "Practice social interaction in structured environments",
            "Seek support from a behavioral therapist",
            "Use communication aids if needed (like apps or cards)",
            "Ensure sensory-friendly environments when possible"
        ],
        "anxiety": [
            "Practice deep breathing exercises daily",
            "Limit caffeine and alcohol intake",
            "Use journaling to identify and process anxious thoughts",
            "Try progressive muscle relaxation techniques",
            "Consider cognitive-behavioral therapy (CBT)"
        ],
        "ocd": [
            "Learn about exposure and response prevention techniques",
            "Practice mindfulness meditation daily",
            "Develop a regular exercise routine",
            "Consider cognitive-behavioral therapy (CBT)",
            "Consult with a healthcare provider about treatment options"
        ]
    }
    
    # Get remedies for the specified condition, or return a generic message if not found
    return remedies_by_condition.get(condition.lower(), ["Please consult with a healthcare professional for specific advice"])