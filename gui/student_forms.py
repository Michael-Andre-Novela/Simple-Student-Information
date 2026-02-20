import customtkinter as ctk
from modules.database_io import read_csv, write_csv
from modules.validators import validate_student

def open_student_form(app):
    #pop-up window
    form = ctk.CTkToplevel(app)
    form.title("Add New Student")
    form.geometry("400x550")
    form.attributes("-topmost", True)  # Keeps form in front of main window

    # Title
    ctk.CTkLabel(form, text="Student Registration", font=("Arial", 20, "bold")).pack(pady=20)

    # Input Fields
    id_entry = ctk.CTkEntry(form, placeholder_text="ID (e.g., 2024-0001)", width=300)
    id_entry.pack(pady=10)

    fname_entry = ctk.CTkEntry(form, placeholder_text="First Name", width=300)
    fname_entry.pack(pady=10)

    lname_entry = ctk.CTkEntry(form, placeholder_text="Last Name", width=300)
    lname_entry.pack(pady=10)

    # Program Dropdown (Fetches list from programs.csv)
    programs_data = read_csv("programs")
    program_list = [p['code'] for p in programs_data] if programs_data else ["N/A"]
    
    ctk.CTkLabel(form, text="Select Program:").pack(pady=(10, 0))
    program_var = ctk.StringVar(value=program_list[0])
    program_menu = ctk.CTkOptionMenu(form, values=program_list, variable=program_var, width=300)
    program_menu.pack(pady=10)

    ctk.CTkLabel(form, text="Year Level:").pack(pady=(10, 0))
    year_var = ctk.StringVar(value="1")
    year_menu = ctk.CTkOptionMenu(form, values=["1", "2", "3", "4"], variable=year_var, width=300)
    year_menu.pack(pady=10)

    # Error Label (Hidden by default)
    error_label = ctk.CTkLabel(form, text="", text_color="red")
    error_label.pack(pady=5)

    def handle_submit():
        # 1. Collect Data
        new_student = {
            "id": id_entry.get().strip(),
            "firstname": fname_entry.get().strip(),
            "lastname": lname_entry.get().strip(),
            "program_code": program_var.get(),
            "year": year_var.get()
        }

        # 2. Validate using  module
        is_valid, error_msg = validate_student(new_student)

        if not is_valid:
            error_label.configure(text=error_msg)
            return

        # 3. Save to Database
        all_students = read_csv("students")
        all_students.append(new_student)
        write_csv("students", all_students)

        # 4. Update Main Window UI immediately
        app.current_data = all_students # Sync the buffer
        app.refresh_table(["id", "firstname", "lastname", "program_code", "year"])
        
        form.destroy()

    # Submit Button
    btn_save = ctk.CTkButton(form, text="Save Student", fg_color="green", hover_color="#006400", command=handle_submit)
    btn_save.pack(pady=20)