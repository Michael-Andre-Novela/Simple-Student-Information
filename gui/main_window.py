import customtkinter as ctk
from tkinter import ttk
from modules.database_io import read_csv

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Student Information System v2.0")
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

        # The Table
        columns = ("id", "firstname", "lastname", "program", "year")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=150)
        
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Bottom Buttons
        btn_add = ctk.CTkButton(self.content_frame, text="Add Student", fg_color="green", hover_color="#006400")
        btn_add.pack(side="left", padx=30, pady=20)

    def show_programs_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Program Management").pack(pady=20)

    def show_colleges_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="College Management").pack(pady=20)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()