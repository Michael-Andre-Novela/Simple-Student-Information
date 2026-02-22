import customtkinter as ctk
from modules.database_io import read_csv, write_csv
from modules.validators import validate_student

# Palette
BG_BASE     = "#0d1117"
BG_FORM     = "#1c2230"
BG_INPUT    = "#21262d"
ACCENT_CYAN = "#00d4ff"
ACCENT_GREEN= "#10b981"
ACCENT_RED  = "#ef4444"
TEXT_PRIMARY= "#e6edf3"
TEXT_MUTED  = "#8b949e"
BORDER      = "#30363d"

def styled_label(parent, text, size=12, color=TEXT_MUTED):
    return ctk.CTkLabel(parent, text=text,
                        font=ctk.CTkFont(size=size),
                        text_color=color)

def styled_entry(parent, placeholder, width=340):
    return ctk.CTkEntry(parent, placeholder_text=placeholder,
                        width=width, height=38, corner_radius=8,
                        border_color=BORDER, fg_color=BG_INPUT,
                        text_color=TEXT_PRIMARY,
                        placeholder_text_color=TEXT_MUTED)

def styled_option(parent, values, variable, width=340, accent=ACCENT_CYAN):
    return ctk.CTkOptionMenu(parent, values=values, variable=variable,
                             width=width, height=38, corner_radius=8,
                             fg_color=BG_INPUT, button_color=accent,
                             button_hover_color="#0d1117",
                             text_color=TEXT_PRIMARY,
                             dropdown_fg_color="#21262d",
                             dropdown_text_color=TEXT_PRIMARY)

def open_student_form(app, edit_data=None):
    is_edit = edit_data is not None

    form = ctk.CTkToplevel(app)
    form.title("Edit Student" if is_edit else "Add Student")
    form.geometry("420x700")
    form.resizable(False, False)
    form.configure(fg_color=BG_FORM)
    form.attributes("-topmost", True)

    # Header
    header = ctk.CTkFrame(form, fg_color=BG_BASE, corner_radius=0, height=64)
    header.pack(fill="x")
    header.pack_propagate(False)
    accent_bar = ctk.CTkFrame(header, width=4, fg_color=ACCENT_CYAN,
                               corner_radius=0)
    accent_bar.pack(side="left", fill="y")
    ctk.CTkLabel(header,
                 text="  Edit Student" if is_edit else "  Add Student",
                 font=ctk.CTkFont(size=18, weight="bold"),
                 text_color=TEXT_PRIMARY).pack(side="left", padx=16)

    body = ctk.CTkFrame(form, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=28, pady=16)

    def field(label_text, widget_fn, *args, **kwargs):
        styled_label(body, label_text).pack(anchor="w", pady=(8, 2))
        w = widget_fn(body, *args, **kwargs)
        w.pack(anchor="w")
        return w

    id_entry = field("Student ID", styled_entry,
                     placeholder="e.g.  2024-0001")
    fname_entry = field("First Name", styled_entry,
                        placeholder="First name")
    lname_entry = field("Last Name", styled_entry,
                        placeholder="Last name")

    gender_var = ctk.StringVar(value="Male")
    year_var   = ctk.StringVar(value="1")

    row2 = ctk.CTkFrame(body, fg_color="transparent")
    row2.pack(fill="x", pady=(10, 0))
    styled_label(body, "Gender  /  Year Level").pack(anchor="w", pady=(0, 4))

    gender_menu = styled_option(row2, ["Male", "Female", "Other"],
                                gender_var, width=162)
    gender_menu.pack(side="left", padx=(0, 16))
    year_menu = styled_option(row2, ["1", "2", "3", "4", "5"],
                              year_var, width=162)
    year_menu.pack(side="left")

    # College dropdown
    colleges_data = read_csv("colleges")
    college_codes = [c['code'] for c in colleges_data] if colleges_data else ["N/A"]
    college_var = ctk.StringVar(value=college_codes[0])
    field("College", styled_option, college_codes, college_var)

    # Program dropdown (filtered)
    program_var = ctk.StringVar(value="")
    styled_label(body, "Program").pack(anchor="w", pady=(8, 2))
    program_menu = styled_option(body, [""], program_var)
    program_menu.pack(anchor="w")

    def update_programs(*_):
        all_programs = read_csv("programs")
        filtered = [p['code'] for p in all_programs
                    if p.get('college_code') == college_var.get()]
        if not filtered:
            filtered = ["No programs available"]
        program_menu.configure(values=filtered)
        program_var.set(filtered[0])

    college_var.trace_add("write", update_programs)
    update_programs()

    # Error label
    error_label = ctk.CTkLabel(body, text="", text_color=ACCENT_RED,
                               wraplength=340, font=ctk.CTkFont(size=12))
    error_label.pack(anchor="w", pady=(6, 0))

    # Pre-fill
    if is_edit:
        id_entry.insert(0, str(edit_data[0]))
        id_entry.configure(state="disabled")
        fname_entry.insert(0, str(edit_data[1]))
        lname_entry.insert(0, str(edit_data[2]))
        year_var.set(str(edit_data[4]))
        gender_var.set(str(edit_data[5]))
        college_code = str(edit_data[6])
        if college_code in college_codes:
            college_var.set(college_code)
            update_programs()
        program_var.set(str(edit_data[3]))

    # Save
    def handle_save():
        student_data = {
            "id":           str(edit_data[0]) if is_edit else id_entry.get().strip(),
            "firstname":    fname_entry.get().strip(),
            "lastname":     lname_entry.get().strip(),
            "program_code": program_var.get(),
            "year":         year_var.get(),
            "gender":       gender_var.get()
        }
        is_valid, *msg = validate_student(student_data, skip_id_check=is_edit)
        if not is_valid:
            error_label.configure(text=msg[0] if msg else "Invalid input.")
            return
        all_students = read_csv("students")
        if is_edit:
            updated = [student_data if s['id'] == student_data['id'] else s
                       for s in all_students]
        else:
            updated = all_students + [student_data]
        write_csv("students", updated)
        app.current_data = updated
        app.refresh_table(app.current_display_keys)
        form.destroy()

    # Delete confirm
    def handle_delete():
        confirm = ctk.CTkToplevel(form)
        confirm.title("Confirm Delete")
        confirm.geometry("340x180")
        confirm.configure(fg_color=BG_FORM)
        confirm.attributes("-topmost", True)
        confirm.resizable(False, False)

        ctk.CTkLabel(confirm,
                     text=f"Delete student {edit_data[0]}?",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(pady=(24, 4))
        ctk.CTkLabel(confirm, text="This cannot be undone.",
                     text_color=TEXT_MUTED).pack()

        bf = ctk.CTkFrame(confirm, fg_color="transparent")
        bf.pack(pady=20)

        def confirm_delete():
            all_s = read_csv("students")
            updated = [s for s in all_s if s['id'] != str(edit_data[0])]
            write_csv("students", updated)
            app.current_data = updated
            app.refresh_table(app.current_display_keys)
            confirm.destroy()
            form.destroy()

        ctk.CTkButton(bf, text="Yes, Delete", fg_color=ACCENT_RED,
                      hover_color="#b91c1c", width=120, height=36,
                      corner_radius=8, command=confirm_delete).pack(side="left", padx=8)
        ctk.CTkButton(bf, text="Cancel", fg_color=BG_INPUT,
                      hover_color=BORDER, width=100, height=36,
                      corner_radius=8, command=confirm.destroy).pack(side="left", padx=8)

    # Buttons
    btn_row = ctk.CTkFrame(body, fg_color="transparent")
    btn_row.pack(fill="x", pady=(12, 0))

    ctk.CTkButton(
        btn_row,
        text="Save Changes" if is_edit else "Save Student",
        fg_color=ACCENT_GREEN, hover_color="#059669",
        height=40, corner_radius=8,
        font=ctk.CTkFont(size=13, weight="bold"),
        command=handle_save
    ).pack(side="left", padx=(0, 10))

    if is_edit:
        ctk.CTkButton(
            btn_row, text="Delete",
            fg_color=ACCENT_RED, hover_color="#b91c1c",
            height=40, corner_radius=8, width=100,
            font=ctk.CTkFont(size=13),
            command=handle_delete
        ).pack(side="left")