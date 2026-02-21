import customtkinter as ctk
from modules.database_io import read_csv, write_csv

def open_college_form(app):
    form = ctk.CTkToplevel(app)
    form.title("Add New College")
    form.geometry("400x380")
    form.attributes("-topmost", True)

    ctk.CTkLabel(form, text="College Registration", font=("Arial", 20, "bold")).pack(pady=20)

    code_entry = ctk.CTkEntry(form, placeholder_text="College Code (e.g., CCS)", width=300)
    code_entry.pack(pady=10)

    name_entry = ctk.CTkEntry(form, placeholder_text="Full College Name", width=300)
    name_entry.pack(pady=10)

    def handle_submit():
        new_college = {
            "code": code_entry.get().strip().upper(),
            "name": name_entry.get().strip()
        }
        
        all_colleges = read_csv("colleges")
        all_colleges.append(new_college)
        write_csv("colleges", all_colleges)

        # Refresh Main Window
        app.current_data = all_colleges
        app.refresh_table(["code", "name"])
        form.destroy()

    ctk.CTkButton(form, text="Save College", fg_color="green", command=handle_submit).pack(pady=25)