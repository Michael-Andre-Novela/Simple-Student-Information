import re
from modules.database_io import read_csv

def programs_exists(program_code):
    # Get all current programs
    programs = read_csv("programs")
    
    # Check if any program has a 'code' that matches our input
    for p in programs:
        if p['code'].upper() == program_code.upper():
            return True
            
    return False
def id_no_already_exists(id_number):

    id_number = read_csv("students")

    for i in id_number:
        if str(i['id']) == id:
            return False
        
    return True

def validate_student(student_data):
    # 1. Check ID Format (YYYY-NNNN)
    if not re.match(r'^\d{4}-\d{4}$', student_data['id']):
        return False, "ID must be in YYYY-NNNN format (e.g., 2026-0001)."

    # 2. Check Empty Fields
    if not student_data['firstname'].strip() or not student_data['lastname'].strip():
        return False, "First and Last names cannot be empty."

    # 3. Check Year Level
    try:
        year = int(student_data['year'])
        if not (1 <= year <= 5):
            return False, "Year level must be between 1 and 5."
    except ValueError:
        return False, "Year level must be a number."
    # 4. Check if the Program Code actually exists in programs.csv
    
    if not programs_exists(student_data['program_code']):
        return False, f"Program code '{student_data['program_code']}' not found in database."
    # 5. Check if the id number already exist in students.csv

    if id_no_already_exists(student_data['id']):
        return False, f"ID Number '{student_data['id']}' already exists."
    
    return True, 