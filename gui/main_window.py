from tkinter import ttk
import customtkinter as ctk
from modules.database_io import read_csv, sort
from gui.student_forms import open_student_form
from gui.programs_forms import open_program_form
from gui.college_forms import open_college_form

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_data = [] # Buffer for search/sort results

        self.title("Student Information System")
        self.geometry("1100x650")

        # Configure Grid Layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Admin", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_students = ctk.CTkButton(self.sidebar_frame, text="Students", command=self.show_students_view)
        self.btn_students.grid(row=1, column=0, padx=20, pady=10)

        self.btn_programs = ctk.CTkButton(self.sidebar_frame, text="Programs", command=self.show_programs_view)
        self.btn_programs.grid(row=2, column=0, padx=20, pady=10)

        self.btn_colleges = ctk.CTkButton(self.sidebar_frame, text="Colleges", command=self.show_colleges_view)
        self.btn_colleges.grid(row=3, column=0, padx=20, pady=10)

        # --- Main Content Area ---
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    
        # Default view
        self.show_students_view()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_common_controls(self, title, search_options, sort_options, file_key, display_keys, add_command=None):
        """Creates the header, search bar, and sort bar used across all views."""
        self.clear_content()
        label = ctk.CTkLabel(self.content_frame, text=title, font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)

        # --- Top Control Bar ---
        top_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_container.pack(fill="x", padx=20, pady=(10, 0))

        # Primary Action (Left side)
        btn_text = f"+ Add {title.split()[0]}"
        btn_add = ctk.CTkButton(top_container, text=btn_text, width=120, fg_color="green", hover_color="#006400", command=add_command)
        btn_add.pack(side="left", padx=5)
        
        # 1. Search Entry
        self.search_entry = ctk.CTkEntry(top_container, placeholder_text=f"Search {title.lower()}...", width=250)
        self.search_entry.pack(side="left", padx=10)

        # 3. Dropdown
        self.search_var = ctk.StringVar(value=list(search_options.keys())[0])
        search_menu = ctk.CTkOptionMenu(top_container, values=list(search_options.keys()), variable=self.search_var, width=140)
        search_menu.pack(side="left", padx=5)

        # 4. Search Button
        btn_search = ctk.CTkButton(
            top_container, 
            text="Search", 
            width=80, 
            command=lambda: self.search_view_data(file_key, search_options, display_keys)
        )
        btn_search.pack(side="left", padx=7)

        # Sorting Controls (Right side)
        self.sort_var = ctk.StringVar(value=list(sort_options.keys())[0])

        btn_sort = ctk.CTkButton(
            top_container, 
            text="Sort", 
            width=80,
            command=lambda: self.sort_view_data(file_key, sort_options[self.sort_var.get()], display_keys)
        )
        btn_sort.pack(side="right", padx=5)

        sort_menu = ctk.CTkOptionMenu(top_container, values=list(sort_options.keys()), variable=self.sort_var, width=140)
        sort_menu.pack(side="right", padx=5)

        sort_label = ctk.CTkLabel(top_container, text="Sort by:")
        sort_label.pack(side="right", padx=2)

    def setup_treeview(self, columns):
        """Sets up the standardized dark-mode Treeview."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, rowheight=45)
        style.map("Treeview", background=[('selected', '#1f538d')])
        
        container = ctk.CTkFrame(self.content_frame)
        container.pack(expand=True, fill="both", padx=20, pady=10)

        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")

        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=150, anchor="center")

    def show_students_view(self):
        search_opts = {"ID": "id", 
                       "First Name": "firstname", 
                       "Last Name": "lastname", 
                       "Program Code": "program_code", 
                       "Year": "year", 
                       "Gender":"gender", 
                       "College":"college"}
        
        sort_opts = search_opts.copy()

        display_keys = ["id", "firstname", "lastname", "program_code", "year", "gender", "college"]
        
        self.create_common_controls("Student Records", search_opts, sort_opts, "students", display_keys, lambda: open_student_form(self))

        self.setup_treeview(("id", "firstname", "lastname", "program", "year", "gender", "college"))

        self.tree.column("firstname", width=200) # Custom width
        
        self.current_data = read_csv("students")

        self.refresh_table(display_keys)

    def show_programs_view(self):

        search_opts = {"Code": "code", 
                       "Name": "name", 
                       "College": "college"}
        
        sort_opts = search_opts.copy()

        display_keys = ["code", "name", "college"]

        self.create_common_controls("Program Management", search_opts, sort_opts, "programs", display_keys)

        self.setup_treeview(("code", "name", "college"))

        self.tree.column("name", width=400) # Programs have long names

        self.current_data = read_csv("programs")

        self.refresh_table(display_keys)

        self.create_common_controls("Program Management", search_opts, sort_opts, "programs", display_keys, lambda: open_program_form(self))
        self.setup_treeview(("code", "name", "college"))
        self.tree.column("name", width=400)

        self.current_data = read_csv("programs")
        self.refresh_table(display_keys)

    def show_colleges_view(self):
        search_opts = {"Code": "code", "Name": "name"}

        sort_opts = search_opts.copy()

        display_keys = ["code", "name"]

        self.create_common_controls("College Management", search_opts, sort_opts, "colleges", display_keys)

        self.setup_treeview(("code", "name"))
        self.tree.column("name", width=500)

        self.current_data = read_csv("colleges")
        self.refresh_table(display_keys)
        
        self.create_common_controls("College Management", search_opts, sort_opts, "colleges", display_keys, lambda: open_college_form(self))
        self.setup_treeview(("code", "name"))
        self.tree.column("name", width=500)

        self.current_data = read_csv("colleges")
        self.refresh_table(display_keys)
   
    def sort_view_data(self, file_key, sort_col, display_keys):
        if not hasattr(self, 'current_data') or not self.current_data:
            self.current_data = read_csv(file_key)

        if sort_col == "college" and file_key == "students":
            programs_list = read_csv("programs")
            prog_to_col = {p['code']: p.get('college', 'N/A') for p in programs_list}
            self.current_data.sort(key=lambda x: str(prog_to_col.get(x.get('program_code'), "")).lower())
        else:
            self.current_data.sort(key=lambda x: str(x.get(sort_col, "")).lower())

        self.refresh_table(display_keys)
   
    def search_view_data(self, file_key, search_map, display_keys):
        query = self.search_entry.get().strip().lower()
        column_to_search = search_map[self.search_var.get()]
        all_data = read_csv(file_key)
        
        if not query:
            self.current_data = all_data
        else:
            self.current_data = []
            # Handle student college search specifically since it's a virtual column
            if column_to_search == "college" and file_key == "students":
                progs = read_csv("programs")
                mapping = {p['code']: p.get('college', '').lower() for p in progs}
                for row in all_data:
                    if query in mapping.get(row.get('program_code', ''), ''):
                        self.current_data.append(row)
            else:
                for row in all_data:
                    cell_value = str(row.get(column_to_search, "")).lower()
                    if cell_value.startswith(query):
                        self.current_data.append(row)

        self.refresh_table(display_keys)
   
    def refresh_table(self, display_keys):
        #college lookup mapping
        programs_list = read_csv("programs")
        prog_to_col = {p['code']: p.get('college', 'N/A') for p in programs_list}

        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Re-populate with filtered/sorted data
        for s in self.current_data:
            row_values = []
            for key in display_keys:
                if key == "college" and "program_code" in s: # Only for student table
                    val = prog_to_col.get(s.get('program_code',"Unassigned"))
                else:
                    val = s.get(key, "")
                row_values.append(val)
            self.tree.insert("", "end", values=row_values)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()