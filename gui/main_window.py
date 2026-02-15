import customtkinter as ctk
from tkinter import ttk
from modules.database_io import read_csv, sort

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
        
        
        # The Table
        columns = ("id", "firstname", "lastname", "program", "year")
        container = ctk.CTkFrame(self.content_frame)
        container.pack(expand=True, fill="both", padx=20, pady=10)

        # 2. The Table (Inside the container)
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # 3. The Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 4. Pack side-by-side
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")
        
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
        # Button Container for better alignment
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=30, pady=20)

        btn_add = ctk.CTkButton(btn_frame, text="Add Student", fg_color="green", hover_color="#006400")
        btn_add.pack(side="left", padx=5)

        # Dropdown to choose which column to sort
        sort_options = {
                 "ID":"id",
                 "First Name": "firstname", 
                 "Last Name":"lastname", 
                 "Progam Code":"program_code", 
                 "Year":"year"}
        
        self.sort_var = ctk.StringVar(value="ID") # Default value
        
        sort_menu = ctk.CTkOptionMenu(btn_frame, values=list(sort_options.keys()), variable=self.sort_var)
        sort_menu.pack(side="left", padx=10)

        # The Sort Button now uses the variable from the menu
        btn_sort = ctk.CTkButton(
            btn_frame, 
            text="Sort", 
            command=lambda: self.sort_view_data(
                "students", 
                sort_options[self.sort_var.get()], 
                ["id", "firstname", "lastname", "program_code", "year"]
            )
        )
        btn_sort.pack(side="left", padx=5)


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
        
        # 2. The Table (Inside the container)
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # 3. The Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 4. Pack side-by-side
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

        # 2. The Table (Inside the container)
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # 3. The Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 4. Pack side-by-side
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
        data = read_csv(file_key)
        sorted_data=sort(file_key, sort_col)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for s in sorted_data:
            row_values = [s.get(k, "") for k in display_keys]
            self.tree.insert("", "end", values=row_values)
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()