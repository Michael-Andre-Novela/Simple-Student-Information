
from modules.database_io import initialize_storage, read_csv, write_csv
from modules.validators import validate_student


def test_add_student():
    # 1. Initialize our CSVs
    initialize_storage()
    
    print("--- Add New Student ---")
    
    # 2. Collect Input
    new_student = {
        'id': input("Enter ID (YYYY-NNNN): "),
        'firstname': input("First Name: "),
        'lastname': input("Last Name: "),
        'program_code': input("Program Code: "),
        'year': input("Year Level: "),
        'gender': input("Gender: ")
    }

    # 3. Use your "Security Guard"
    is_valid, message = validate_student(new_student)
    

    if is_valid:
        # 4. Use your "Muscles" to save
        data = read_csv("students")
        data.append(new_student)
        write_csv("students", data)
        print(f"\n✅ Success")
    else:
        # 5. Report the failure
        print(f"\n❌ Error: {message}")

if __name__ == "__main__":
    test_add_student()

