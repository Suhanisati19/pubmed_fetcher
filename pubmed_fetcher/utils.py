import re

def is_non_academic_affiliation(affiliation: str) -> bool:
    """
    Determines if the affiliation is non-academic based on keyword filtering.
    """
    academic_keywords = [
        "university", "college", "institute", "school",
        "department", "faculty", "hospital"
    ]
    return not any(word.lower() in affiliation.lower() for word in academic_keywords)

def extract_email(text: str) -> str:
    """
    Extracts the first email address found in a given text.
    """
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group() if match else ""
