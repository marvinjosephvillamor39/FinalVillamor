import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# -------------------- MySQL Connection --------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   
    port=3307  # change if XAMPP uses a different port
)

cursor = conn.cursor()
print("✅ Connected to MySQL/MariaDB!")

# -------------------- Create Database if Not Exists --------------------
cursor.execute("CREATE DATABASE IF NOT EXISTS shs_registration")
cursor.execute("USE shs_registration")  # Switch to the new database

# -------------------- Create Table --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    grade_level TEXT,
    guardian TEXT,
    gender TEXT,
    age INT,
    strand TEXT
)
""")
conn.commit()


# -------------------- Helper Functions --------------------
def center_window(win, w, h):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w / 2) - (w / 2))
    y = int((screen_h / 2) - (h / 2))
    win.geometry(f"{w}x{h}+{x}+{y}")

# -------------------- Tkinter Windows --------------------
def open_student_registration():
    reg_win = tk.Toplevel(root)
    reg_win.title("Student Registration Form")
    center_window(reg_win, 500, 350)

    tk.Label(reg_win, text="Step 1: Fill Out Registration Form",
             font=("Arial", 12, "bold")).pack(pady=10)

    entries = {}
    fields = ["First Name", "Last Name", "Grade Level", "Guardian", "Gender", "Age"]

    for f in fields:
        frame = tk.Frame(reg_win)
        frame.pack(pady=5)
        tk.Label(frame, text=f + ":", width=15, anchor="e").pack(side="left")
        if f == "Grade Level":
            entry = ttk.Combobox(frame, values=["Grade 11", "Grade 12"], width=18)
        else:
            entry = tk.Entry(frame, width=20)
        entry.pack(side="left")
        entries[f] = entry

    def next_step():
        data = {k: v.get() for k, v in entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return
        reg_win.destroy()
        open_strand_selection(data)

    tk.Button(reg_win, text="Next", command=next_step).pack(pady=20)

def open_strand_selection(student_data):
    strand_win = tk.Toplevel(root)
    strand_win.title("Strand Selection")
    center_window(strand_win, 400, 300)

    tk.Label(strand_win, text="Step 2: Choose Your Strand",
             font=("Arial", 12, "bold")).pack(pady=20)

    strand_var = tk.StringVar()
    for s in ["STEM", "ABM", "HUMSS", "TVL"]:
        tk.Radiobutton(strand_win, text=s, variable=strand_var, value=s).pack(anchor="w", padx=100)

    def next_step():
        if not strand_var.get():
            messagebox.showwarning("Warning", "Please select a strand!")
            return
        student_data["Strand"] = strand_var.get()
        strand_win.destroy()
        open_confirmation(student_data)

    tk.Button(strand_win, text="Next", command=next_step).pack(pady=20)

def open_confirmation(student_data):
    confirm_win = tk.Toplevel(root)
    confirm_win.title("Confirm Details")
    center_window(confirm_win, 400, 350)

    tk.Label(confirm_win, text="Step 3: Confirm Your Details",
             font=("Arial", 12, "bold")).pack(pady=10)

    for k, v in student_data.items():
        tk.Label(confirm_win, text=f"{k}: {v}").pack(anchor="w", padx=50)

    def register():
        try:
            cursor.execute(
                "INSERT INTO students (first_name, last_name, grade_level, guardian, gender, age, strand) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    student_data["First Name"],
                    student_data["Last Name"],
                    student_data["Grade Level"],
                    student_data["Guardian"],
                    student_data["Gender"],
                    int(student_data["Age"]),
                    student_data["Strand"]
                )
            )
            conn.commit()
            messagebox.showinfo("Success", "Student registered successfully!")
            confirm_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register student.\n{e}")

    tk.Button(confirm_win, text="Register", command=register).pack(pady=20)

# -------------------- Main Window --------------------
root = tk.Tk()
root.title("SHS Students Registration System")
center_window(root, 400, 250)

tk.Label(root, text="Welcome to SHS Registration System",
         font=("Arial", 12, "bold"), wraplength=300).pack(pady=20)

tk.Button(root, text="Student Portal", width=25, command=open_student_registration).pack(pady=10)
tk.Button(root, text="Administrator", width=25, command=lambda: messagebox.showinfo("Admin", "Admin Panel Coming Soon")).pack(pady=10)
tk.Button(root, text="Track Payments", width=25, command=lambda: messagebox.showinfo("Payments", "Payment Tracking Coming Soon")).pack(pady=10)

root.mainloop()
