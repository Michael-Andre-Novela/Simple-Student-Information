import customtkinter as ctk
from tkinter import ttk
from modules.database_io import read_csv

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

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

        # Treeview Styles (to make it match Dark Mode)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.configure("Treeview", rowheight=30) # Makes rows taller and easier to read
        # Search Container
        search_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)

        # Dropdown to choose which field to search in
        search_map = {"All": "all", "ID": "id", "First Name": "firstname", "Last Name": "lastname"}
        self.search_col_var = ctk.StringVar(value="All")
        search_menu = ctk.CTkOptionMenu(search_frame, values=list(search_map.keys()), variable=self.search_col_var, width=120)
        search_menu.pack(side="left", padx=5)

        # Search Entry
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search student...", width=300)
        self.search_entry.pack(side="left", padx=5)

        # Search Button
        btn_search = ctk.CTkButton(search_frame, text="Search", width=80, 
                                   command=lambda: self.search_view_data("students", ["id", "firstname", "lastname", "program_code", "year"]))
        btn_search.pack(side="left", padx=5)
        # The Table
        columns = ("id", "firstname", "lastname", "program", "year")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        self.tree.column("id", width=120, stretch=True, anchor="w")
        self.tree.column("firstname", width=150, stretch=True, anchor="w")
        self.tree.column("lastname", width=150, stretch=True, anchor="w")
        self.tree.column("program", width=100, stretch=True, anchor="center")
        self.tree.column("year", width=80, stretch=True, anchor="center")

        for col in columns:
            self.tree.heading(col, text=col.upper())
            
        
        # show data
        data = read_csv("students")
        for s in data:
              self.tree.insert("", "end", values=(
         s.get('id'), 
         s.get('firstname'), 
         s.get('lastname'), 
         s.get('program_code'), 
         s.get('year')
          ))
        
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Bottom Buttons
        btn_add = ctk.CTkButton(self.content_frame, text="Add Student", fg_color="green", hover_color="#006400")
        btn_add.pack(side="left", padx=30, pady=20)

    def show_programs_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Program Management").pack(pady=20)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.configure("Treeview", rowheight=30) 
        
        columns = ("code", "name", "college")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        self.tree.column("code", width=120, stretch=True, anchor="w")
        self.tree.column("name", width=150, stretch=True, anchor="w")
        self.tree.column("college", width=150, stretch=True, anchor="w")
        
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

    def show_colleges_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="College Management").pack(pady=20)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.configure("Treeview", rowheight=30)

        columns = ("code", "name")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        self.tree.column("code", width=120, stretch=True, anchor="w")
        self.tree.column("name", width=150, stretch=True, anchor="w")
        
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

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()