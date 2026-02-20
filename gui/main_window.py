from tkinter import ttk
import customtkinter as ctk
from modules.database_io import read_csv, sort
from gui.student_forms import open_student_form

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_data = read_csv("students")

        self.title("Student Information System")
        self.geometry("1100x600")

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

    def show_students_view(self):
        self.clear_content()
        label = ctk.CTkLabel(self.content_frame, text="Student Records", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)
        # --- Top Control Bar ---
        top_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_container.pack(fill="x", padx=20, pady=(10, 0)) # Added top padding for breathing room

        # Primary Action (Left side)
        btn_add = ctk.CTkButton(top_container, text="+ Add Student", width=120, fg_color="green", hover_color="#006400", command= lambda: open_student_form(self))
        btn_add.pack(side="left", padx=5)
        
         #search bar (Left side, next to Add button)

# 1. Search Entry
        self.search_entry = ctk.CTkEntry(top_container, placeholder_text="Search students...", width=250)
        self.search_entry.pack(side="left", padx=10)

        # 2. Search Options Mapping
        search_options = {
            "ID": "id",
            "First Name": "firstname", 
            "Last Name": "lastname", 
            "Program Code": "program_code", 
            "Year": "year",
            "Gender":"gender",
            "College":"college"
        }

        # 3. Dropdown (Variable must be created BEFORE the button uses it in lambda)
        self.search_var = ctk.StringVar(value="ID")
        search_menu = ctk.CTkOptionMenu(top_container, values=list(search_options.keys()), variable=self.search_var, width=140)
        search_menu.pack(side="left", padx=5)

        # 4. Search Button (Now passing search_options)
        btn_search = ctk.CTkButton(
            top_container, 
            text="Search", 
            width=80, 
            command=lambda: self.search_view_data(
                "students", 
                search_options, # Pass the dictionary here!
                ["id", "firstname", "lastname", "program_code", "year", "gender","college"]
            )
        )
        btn_search.pack(side="left", padx=7)
        # Sorting Controls (Right side)
        # Defining sort_options locally here is fine
        sort_options = {
            "ID": "id",
            "First Name": "firstname", 
            "Last Name": "lastname", 
            "Program Code": "program_code", 
            "Year": "year",
            "Gender":"gender",
            "College": "college"
        }
        
        self.sort_var = ctk.StringVar(value="ID")

        # Sort Button - Placed on the far right
        btn_sort = ctk.CTkButton(
            top_container, 
            text="Sort", 
            width=80,
            command=lambda: self.sort_view_data(
                "students", 
                sort_options[self.sort_var.get()], 
                ["id", "firstname", "lastname", "program_code", "year", "gender", "college"]
            )
        )
        btn_sort.pack(side="right", padx=5)

        # Dropdown - Placed next to the Sort button
        sort_menu = ctk.CTkOptionMenu(top_container, values=list(sort_options.keys()), variable=self.sort_var, width=140)
        sort_menu.pack(side="right", padx=5)

        # Label for clarity
        sort_label = ctk.CTkLabel(top_container, text="Sort by:")
        sort_label.pack(side="right", padx=2)
                        
        # Treeview Styles (to make it match Dark Mode)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.configure("Treeview", rowheight=45) # Makes rows taller and easier to read
        
        
        # The Table
        columns = ("id", "firstname", "lastname", "program", "year", "gender", "college")
        container = ctk.CTkFrame(self.content_frame)
        container.pack(expand=True, fill="both", padx=20, pady=10)

        # The Table (Inside the container)
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # The Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack side-by-side
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")

        # Define specific widths for each column
        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column("firstname", width=200, minwidth=150)
        programs_list = read_csv("programs")
        prog_to_col = {p['code']: p.get('college', 'N/A') for p in programs_list}


        data = read_csv("students")
        for s in data:
              student_college = prog_to_col.get(s.get('program_code'), "Unassigned")

              self.tree.insert("", "end", values=(
         s.get('id'), 
         s.get('firstname'), 
         s.get('lastname'), 
         s.get('program_code'), 
         s.get('year'),
         s.get('gender'),
         student_college
        ))
              
        
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

    def show_programs_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Program Management").pack(pady=20)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.configure("Treeview", rowheight=30)
        
        columns = ("code", "name", "college")

        container = ctk.CTkFrame(self.content_frame)
        container.pack(expand=True, fill="both", padx=20, pady=10)
        
        # The Table (Inside the container)
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # The Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack side-by-side
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")

        for col in columns:
            self.tree.heading(col, text=col.upper())
            
        #show data
        data = read_csv("programs")
        for s in data:
              self.tree.insert("", "end", values=(
         s.get('code'), 
         s.get('name'), 
         s.get('college') 
          ))
        
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Bottom Buttons
        btn_add = ctk.CTkButton(self.content_frame, text="Add Program", fg_color="green", hover_color="#006400")
        btn_add.pack(side="left", padx=30, pady=20)

        btn_sort = ctk.CTkButton(
    self.content_frame, 
    text="Sort", 
    fg_color="green", 
    hover_color="#006400",
    command=lambda: self.sort_view_data(
        "programs", 
        "name", 
        ["code", "name", "college"]
    )
)
        btn_sort.pack(side="left", padx=35,pady=20)

    def show_colleges_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="College Management").pack(pady=20)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.configure("Treeview", rowheight=30)

        columns = ("code", "name")
        container = ctk.CTkFrame(self.content_frame)
        container.pack(expand=True, fill="both", padx=20, pady=10)

        # The Table (Inside the container)
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # The Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack side-by-side
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")
        
        
        for col in columns:
            self.tree.heading(col, text=col.upper())
            
        
        #show data
        data = read_csv("colleges")
        for s in data:
              self.tree.insert("", "end", values=(
         s.get('code'), 
         s.get('name') 
          ))
        
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)
    
        # Bottom Buttons
        btn_add = ctk.CTkButton(self.content_frame, text="Add College", fg_color="green", hover_color="#006400")
        btn_add.pack(side="left", padx=30, pady=20)
        
        btn_sort = ctk.CTkButton(
    self.content_frame, 
    text="Sort", 
    fg_color="green", 
    hover_color="#006400",
    command=lambda: self.sort_view_data(
        "colleges", 
        "name", 
        ["code", "name"]
    )
)
        btn_sort.pack(side="left", padx=35,pady=20)
   
    def sort_view_data(self, file_key, sort_col, display_keys):
        # Ensure we have a data buffer to sort. Prefer the current search buffer
        # (so sorting respects an active search); otherwise load fresh data.
        if not hasattr(self, 'current_data') or not self.current_data:
            self.current_data = read_csv(file_key)
        # for college header since it's not in the students.csv

        if sort_col == "college":
            programs_list = read_csv("programs")
            prog_to_col = {p['code']: p.get('college', 'N/A') for p in programs_list}
            
            # Sort based on the looked-up college value
            self.current_data.sort(key=lambda x: str(prog_to_col.get(x.get('program_code'), "")).lower())
        else:
            # 2. Otherwise, sort by the standard keys (id, name, year, etc.)
            self.current_data.sort(key=lambda x: str(x.get(sort_col, "")).lower())
        # Sort the current buffer by the requested column

        # Push sorted results to UI
        self.refresh_table(display_keys)
   
    def search_view_data(self, file_key, search_map, display_keys):
        # 1. Clean up the input
        query = self.search_entry.get().strip().lower()
        column_to_search = search_map[self.search_var.get()]

        # 2. Get fresh data from the file
        all_data = read_csv(file_key)
        
        if not query:
            self.current_data = all_data
        else:
            self.current_data = []
            for row in all_data:
                # Convert cell to string safely
                cell_value = str(row.get(column_to_search, "")).lower()
                
                # CHANGED: Use .startswith() for "First Letter" basis
                if cell_value.startswith(query):
                    self.current_data.append(row)

        # 3. Update the display
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
                if key == "college":
                    val = prog_to_col.get(s.get('program_code',"Unassigned"))
                else:
                    val = s.get(key, "")
                row_values.append(val)
            self.tree.insert("", "end", values=row_values)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()