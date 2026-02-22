import customtkinter as ctk
from modules.database_io import read_csv, write_csv
from modules.validators import validate_college

BG_BASE      = "#0d1117"
BG_FORM      = "#1c2230"
BG_INPUT     = "#21262d"
ACCENT_GREEN = "#10b981"
ACCENT_RED   = "#ef4444"
TEXT_PRIMARY = "#e6edf3"
TEXT_MUTED   = "#8b949e"
BORDER       = "#30363d"

def styled_label(parent, text):
    return ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=12),
                        text_color=TEXT_MUTED)

def styled_entry(parent, placeholder, width=340):
    return ctk.CTkEntry(parent, placeholder_text=placeholder,
                        width=width, height=38, corner_radius=8,
                        border_color=BORDER, fg_color=BG_INPUT,
                        text_color=TEXT_PRIMARY,
                        placeholder_text_color=TEXT_MUTED)

def open_college_form(app, edit_data=None):
    is_edit = edit_data is not None

    form = ctk.CTkToplevel(app)
    form.title("Edit College" if is_edit else "Add College")
    form.geometry("420x360")
    form.resizable(False, False)
    form.configure(fg_color=BG_FORM)
    form.attributes("-topmost", True)

    # Header
    header = ctk.CTkFrame(form, fg_color=BG_BASE, corner_radius=0, height=64)
    header.pack(fill="x")
    header.pack_propagate(False)
    ctk.CTkFrame(header, width=4, fg_color=ACCENT_GREEN,
                 corner_radius=0).pack(side="left", fill="y")
    ctk.CTkLabel(header,
                 text="  Edit College" if is_edit else "  Add College",
                 font=ctk.CTkFont(size=18, weight="bold"),
                 text_color=TEXT_PRIMARY).pack(side="left", padx=16)

    body = ctk.CTkFrame(form, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=28, pady=16)

    styled_label(body, "College Code").pack(anchor="w", pady=(8, 2))
    code_entry = styled_entry(body, "e.g.  CCS")
    code_entry.pack(anchor="w")

    styled_label(body, "College Name").pack(anchor="w", pady=(10, 2))
    name_entry = styled_entry(body, "Full college name")
    name_entry.pack(anchor="w")

    error_label = ctk.CTkLabel(body, text="", text_color=ACCENT_RED,
                               wraplength=340, font=ctk.CTkFont(size=12))
    error_label.pack(anchor="w", pady=(8, 0))

    if is_edit:
        code_entry.insert(0, str(edit_data[0]))
        code_entry.configure(state="disabled")
        name_entry.insert(0, str(edit_data[1]))

    def handle_save():
        code = str(edit_data[0]) if is_edit else code_entry.get().strip().upper()
        name = name_entry.get().strip()
        college_data = {"code": code, "name": name}

        is_valid, msg = validate_college(college_data, is_edit=is_edit)
        if not is_valid:
            error_label.configure(text=msg)
            return

        all_colleges = read_csv("colleges")
        if is_edit:
            updated = [college_data if c['code'] == code else c for c in all_colleges]
        else:
            updated = all_colleges + [college_data]

        write_csv("colleges", updated)
        app.current_data = updated
        app.refresh_table(app.current_display_keys)
        form.destroy()

    def handle_delete():
        code = str(edit_data[0])
        all_programs = read_csv("programs")
        affected_programs = [p for p in all_programs if p.get('college_code') == code]
        all_students = read_csv("students")
        affected_codes = {p['code'] for p in affected_programs}
        affected_students = [s for s in all_students if s.get('program_code') in affected_codes]

        confirm = ctk.CTkToplevel(form)
        confirm.title("Confirm Delete")
        confirm.geometry("360x210")
        confirm.configure(fg_color=BG_FORM)
        confirm.attributes("-topmost", True)
        confirm.resizable(False, False)

        ctk.CTkLabel(confirm, text=f"Delete college '{code}'?",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(pady=(24, 4))
        if affected_programs:
            msg = (f"⚠  {len(affected_programs)} program(s) → Unassigned\n"
                   f"⚠  {len(affected_students)} student(s) affected")
            ctk.CTkLabel(confirm, text=msg, text_color="#f59e0b").pack()
        else:
            ctk.CTkLabel(confirm, text="This cannot be undone.",
                         text_color=TEXT_MUTED).pack()

        bf = ctk.CTkFrame(confirm, fg_color="transparent")
        bf.pack(pady=20)

        def confirm_delete():
            all_c = read_csv("colleges")
            updated_c = [c for c in all_c if c['code'] != code]
            write_csv("colleges", updated_c)
            if affected_programs:
                all_p = read_csv("programs")
                updated_p = []
                for p in all_p:
                    if p.get('college_code') == code:
                        p['college_code'] = "Unassigned"
                    updated_p.append(p)
                write_csv("programs", updated_p)
            if affected_students:
                all_s = read_csv("students")
                updated_s = []
                for s in all_s:
                    if s.get('program_code') in affected_codes:
                        s['program_code'] = "Unassigned"
                    updated_s.append(s)
                write_csv("students", updated_s)
            app.current_data = updated_c
            app.refresh_table(app.current_display_keys)
            confirm.destroy()
            form.destroy()

        ctk.CTkButton(bf, text="Yes, Delete", fg_color=ACCENT_RED,
                      hover_color="#b91c1c", width=120, height=36,
                      corner_radius=8, command=confirm_delete).pack(side="left", padx=8)
        ctk.CTkButton(bf, text="Cancel", fg_color=BG_INPUT,
                      hover_color=BORDER, width=100, height=36,
                      corner_radius=8, command=confirm.destroy).pack(side="left", padx=8)

    btn_row = ctk.CTkFrame(body, fg_color="transparent")
    btn_row.pack(fill="x", pady=(12, 0))

    ctk.CTkButton(btn_row,
                  text="Save Changes" if is_edit else "Save College",
                  fg_color=ACCENT_GREEN, hover_color="#059669",
                  height=40, corner_radius=8,
                  font=ctk.CTkFont(size=13, weight="bold"),
                  command=handle_save).pack(side="left", padx=(0, 10))

    if is_edit:
        ctk.CTkButton(btn_row, text="Delete", fg_color=ACCENT_RED,
                      hover_color="#b91c1c", height=40, corner_radius=8,
                      width=100, font=ctk.CTkFont(size=13),
                      command=handle_delete).pack(side="left")