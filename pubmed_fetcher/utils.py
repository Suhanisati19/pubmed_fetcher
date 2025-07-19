import re

def is_non_academic_affiliation(affiliation: str) -> bool:
    academic_keywords = ["university", "college", "institute", "school", "department", "faculty", "hospital"]
    return not any(word.lower() in affiliation.lower() for word in academic_keywords)

def extract_email(text: str) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group() if match else ""