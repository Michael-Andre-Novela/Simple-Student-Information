import re
from datetime import datetime
from modules.database_io import read_csv

CURRENT_YEAR = datetime.now().year
MIN_YEAR = 2000  # Earliest valid enrollment year


# ── Helpers ────────────────────────────────────────────────────────────────

def is_blank(value):
    return not str(value).strip()

def has_invalid_chars(value, allow_spaces=True, allow_hyphen=False):
    """Returns True if value contains non-alphabetic characters."""
    pattern = r"^[a-zA-Z"
    if allow_spaces:
        pattern += r"\s"
    if allow_hyphen:
        pattern += r"\-"
    pattern += r"]+$"
    return not re.match(pattern, str(value).strip())

def id_already_exists(id_number, exclude_id=None):
    """Check if a student ID already exists. Optionally exclude one (for edits)."""
    students = read_csv("students")
    for s in students:
        if str(s['id']) == str(id_number):
            if exclude_id and str(id_number) == str(exclude_id):
                continue
            return True
    return False

def program_exists(program_code):
    programs = read_csv("programs")
    return any(p['code'].upper() == program_code.upper() for p in programs)

def college_exists(college_code):
    colleges = read_csv("colleges")
    return any(c['code'].upper() == college_code.upper() for c in colleges)

def program_code_exists(code, exclude_code=None):
    programs = read_csv("programs")
    for p in programs:
        if p['code'].upper() == code.upper():
            if exclude_code and code.upper() == exclude_code.upper():
                continue
            return True
    return False

def college_code_exists(code, exclude_code=None):
    colleges = read_csv("colleges")
    for c in colleges:
        if c['code'].upper() == code.upper():
            if exclude_code and code.upper() == exclude_code.upper():
                continue
            return True
    return False


# ── Student Validator ──────────────────────────────────────────────────────

def validate_student(student_data, skip_id_check=False):
    sid       = str(student_data.get('id', '')).strip()
    firstname = str(student_data.get('firstname', '')).strip()
    lastname  = str(student_data.get('lastname', '')).strip()
    program   = str(student_data.get('program_code', '')).strip()
    year      = str(student_data.get('year', '')).strip()
    gender    = str(student_data.get('gender', '')).strip()

    # 1. ID format: YYYY-NNNN
    if not re.match(r'^\d{4}-\d{4}$', sid):
        return False, "ID must be in YYYY-NNNN format (e.g. 2024-0001)."

    # 2. ID year must be realistic
    id_year = int(sid.split('-')[0])
    if id_year < MIN_YEAR or id_year > CURRENT_YEAR:
        return False, f"ID year must be between {MIN_YEAR} and {CURRENT_YEAR}."

    # 3. First name checks
    if is_blank(firstname):
        return False, "First name cannot be empty."
    if len(firstname) < 2:
        return False, "First name must be at least 2 characters."
    if len(firstname) > 64:
        return False, "First name must be under 64 characters."
    if re.search(r'[0-9@#$%^&*()_+=\[\]{};:\'",.<>?/\\|`~]', firstname):
        return False, "First name must not contain numbers or special characters."

    # 4. Last name checks
    if is_blank(lastname):
        return False, "Last name cannot be empty."
    if len(lastname) < 2:
        return False, "Last name must be at least 2 characters."
    if len(lastname) > 64:
        return False, "Last name must be under 64 characters."
    if re.search(r'[0-9@#$%^&*()_+=\[\]{};:\'",.<>?/\\|`~]', lastname):
        return False, "Last name must not contain numbers or special characters."

    # 5. Year level
    if is_blank(year):
        return False, "Year level cannot be empty."
    try:
        year_int = int(year)
        if not (1 <= year_int <= 5):
            return False, "Year level must be between 1 and 5."
    except ValueError:
        return False, "Year level must be a number."

    # 6. Gender
    if gender not in ("Male", "Female", "Other"):
        return False, "Gender must be Male, Female, or Other."

    # 7. Program code exists
    if is_blank(program):
        return False, "Program code cannot be empty."
    if not program_exists(program):
        return False, f"Program code '{program}' does not exist."

    # 8. Program is not unassigned
    if program.lower() == "unassigned":
        return False, "Please select a valid program."

    # 9. Duplicate ID check
    if not skip_id_check:
        if id_already_exists(sid):
            return False, f"ID '{sid}' already exists."

    return True, "Valid."


# ── Program Validator ──────────────────────────────────────────────────────

def validate_program(program_data, is_edit=False):
    code    = str(program_data.get('code', '')).strip()
    name    = str(program_data.get('name', '')).strip()
    college = str(program_data.get('college_code', '')).strip()

    # 1. Code empty
    if is_blank(code):
        return False, "Program code cannot be empty."

    # 2. Code length
    if len(code) > 32:
        return False, "Program code must be under 32 characters."

    # 3. Code format — only letters, numbers, hyphens, spaces
    if not re.match(r'^[a-zA-Z0-9\s\-]+$', code):
        return False, "Program code can only contain letters, numbers, hyphens, and spaces."

    # 4. Name empty
    if is_blank(name):
        return False, "Program name cannot be empty."

    # 5. Name length
    if len(name) < 5:
        return False, "Program name must be at least 5 characters."
    if len(name) > 128:
        return False, "Program name must be under 128 characters."

    # 6. Name must not be numbers only
    if re.match(r'^\d+$', name):
        return False, "Program name cannot be numbers only."

    # 7. College must exist
    if is_blank(college) or college.lower() == "unassigned":
        return False, "Please select a valid college."
    if not college_exists(college):
        return False, f"College '{college}' does not exist."

    # 8. Duplicate code check (skip for edits)
    if not is_edit:
        if program_code_exists(code):
            return False, f"Program code '{code}' already exists."

    return True, "Valid."


# ── College Validator ──────────────────────────────────────────────────────

def validate_college(college_data, is_edit=False):
    code = str(college_data.get('code', '')).strip()
    name = str(college_data.get('name', '')).strip()

    # 1. Code empty
    if is_blank(code):
        return False, "College code cannot be empty."

    # 2. Code length
    if len(code) > 16:
        return False, "College code must be under 16 characters."

    # 3. Code format — letters only
    if not re.match(r'^[a-zA-Z]+$', code):
        return False, "College code can only contain letters (no spaces or symbols)."

    # 4. Name empty
    if is_blank(name):
        return False, "College name cannot be empty."

    # 5. Name length
    if len(name) < 5:
        return False, "College name must be at least 5 characters."
    if len(name) > 128:
        return False, "College name must be under 128 characters."

    # 6. Name must not be numbers only
    if re.match(r'^\d+$', name):
        return False, "College name cannot be numbers only."

    # 7. Duplicate code check (skip for edits)
    if not is_edit:
        if college_code_exists(code):
            return False, f"College code '{code}' already exists."

    return True, "Valid."