import customtkinter as ctk
from modules.database_io import read_csv, write_csv

def open_program_form(app):
    form = ctk.CTkToplevel(app)
    form.title("Add New Program")
    form.geometry("400x480")
    form.attributes("-topmost", True)

    ctk.CTkLabel(form, text="Program Registration", font=("Arial", 20, "bold")).pack(pady=20)

    code_entry = ctk.CTkEntry(form, placeholder_text="Program Code (e.g., BSCS)", width=300)
    code_entry.pack(pady=10)

    name_entry = ctk.CTkEntry(form, placeholder_text="Program Name", width=300)
    name_entry.pack(pady=10)

    # Fetch dynamic list of colleges
    colleges_data = read_csv("colleges")
    college_list = [c['code'] for c in colleges_data] if colleges_data else ["N/A"]
    
    ctk.CTkLabel(form, text="Select College:").pack(pady=(10, 0))
    college_var = ctk.StringVar(value=college_list[0])
    college_menu = ctk.CTkOptionMenu(form, values=college_list, variable=college_var, width=300)
    college_menu.pack(pady=10)

    def handle_submit():
        new_prog = {
            "code": code_entry.get().strip().upper(),
            "name": name_entry.get().strip(),
            "college": college_var.get()
        }
        
        all_programs = read_csv("programs")
        all_programs.append(new_prog)
        write_csv("programs", all_programs)

        # Refresh Main Window
        app.current_data = all_programs
        app.refresh_table(["code", "name", "college"])
        form.destroy()

    ctk.CTkButton(form, text="Save Program", fg_color="green", command=handle_submit).pack(pady=25)