import customtkinter as ctk
from modules.database_io import read_csv, write_csv
from modules.validators import validate_student

def open_student_form(app):
    form = ctk.CTkToplevel(app)
    form.title("Add New Student")
    form.geometry("450x750") # Increased height to accommodate pagination
    form.resizable(False, False)
    form.attributes("-topmost", True)

    ctk.CTkLabel(form, text="Student Registration", font=("Arial", 20, "bold")).pack(pady=15)

    # --- Basic Info ---
    id_entry = ctk.CTkEntry(form, placeholder_text="ID (e.g., 2024-0001)", width=300)
    id_entry.pack(pady=5)
    fname_entry = ctk.CTkEntry(form, placeholder_text="First Name", width=300)
    fname_entry.pack(pady=5)
    lname_entry = ctk.CTkEntry(form, placeholder_text="Last Name", width=300)
    lname_entry.pack(pady=5)

    # --- Gender & Year Level ---
    row_frame = ctk.CTkFrame(form, fg_color="transparent")
    row_frame.pack(pady=10)

    gender_var = ctk.StringVar(value="Male")
    gender_menu = ctk.CTkOptionMenu(row_frame, values=["Male", "Female", "Other"], variable=gender_var, width=140)
    gender_menu.pack(side="left", padx=5)

    year_var = ctk.StringVar(value="1")
    year_menu = ctk.CTkOptionMenu(row_frame, values=["1", "2", "3", "4"], variable=year_var, width=140)
    year_menu.pack(side="left", padx=5)

    # --- College & Program ---
    college_var = ctk.StringVar(value="CCS")
    college_menu = ctk.CTkOptionMenu(row_frame, values =["CCS","CEBA","CED","CHS","CSM","CASS","COE"], variable=college_var, width=140)
    college_menu.pack(side="",padx=5,pady=5)

  