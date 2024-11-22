import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
from PIL import Image, ImageTk  # Requires pillow library for image handling
import os

# Main application window
root = tk.Tk()
root.title("Northern Railway - Travelling Allowance Journal")
root.geometry("1000x1000")
root.configure(bg="skyblue")

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Admin Login Frame
login_frame = tk.Frame(root, bg="skyblue")
login_frame.grid(row=0, column=0, sticky="nsew")

# Home Frame
home_frame = tk.Frame(root, bg="skyblue")
home_frame.grid(row=0, column=0, sticky="nsew")

# Top Section Frame
top_section_frame = tk.Frame(root, bg="skyblue")
top_section_frame.grid(row=0, column=0, sticky="nsew")

# Table Section Frame
table_section_frame = tk.Frame(root, bg="skyblue")
table_section_frame.grid(row=0, column=0, sticky="nsew")

# Certification Section Frame
certification_section_frame = tk.Frame(root, bg="skyblue")
certification_section_frame.grid(row=0, column=0, sticky="nsew")

# --- Admin Login Page ---
def login():
    if username_entry.get() == "sarvesh9119" and password_entry.get() == "sarvesh@9119":
        show_frame(home_frame)
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

login_label = tk.Label(login_frame, text="Admin Login", font=("Arial", 18, "bold"), bg="skyblue")
login_label.pack(pady=20)

tk.Label(login_frame, text="Username", font=("Arial", 12), bg="skyblue").pack()
username_entry = tk.Entry(login_frame, width=30)
username_entry.pack(pady=5)

tk.Label(login_frame, text="Password", font=("Arial", 12), bg="skyblue").pack()
password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=login, font=("Arial", 12, "bold"), bg="navy", fg="white")
login_button.pack(pady=20)

# --- Home Frame with Logo ---
home_label = tk.Label(home_frame, text="Northern Railway - Travelling Allowance Journal", font=("Arial", 20, "bold"), fg="red", bg="skyblue")
home_label.pack(pady=20)

# Load and display Indian Railway logo
try:
    logo_image = Image.open("/mnt/data/logo.png")  # Replace with correct path
    logo_image = logo_image.resize((150, 150), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(home_frame, image=logo_photo, bg="skyblue")
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)
except Exception as e:
    print("Error loading logo:", e)

# Navigation buttons
buttons = [
    ("Main Page", lambda: show_frame(top_section_frame), "lightgreen"),
    ("Employee", lambda: show_frame(table_section_frame), "lightblue"),
    ("Certification", lambda: show_frame(certification_section_frame), "lightcoral"),
]

for text, command, color in buttons:
    btn = tk.Button(home_frame, text=text, command=command, font=("Arial", 12, "bold"), width=20, pady=5, bg=color)
    btn.pack(pady=10)

# --- Top Section ---
def submit_data():
    print("Top Section data submitted.")

tk.Label(top_section_frame, text="Main Page", font=("Arial", 14, "bold"), bg="skyblue").pack(pady=10)

labels = ["Dept.", "PF NO.", "BILL UNIT NO.", "Headquarters", "Journal of duties performed by:", 
          "Designation", "Pay in Level", "of 7th CPC", "Date of Appointment", "Rules by which governed"]

entries_top = {}

frame_top = tk.Frame(top_section_frame, bg="skyblue")
frame_top.pack(pady=10, padx=10, fill="x")

for i, text in enumerate(labels):
    tk.Label(frame_top, text=text, font=("Arial", 10), bg="skyblue").grid(row=i, column=0, sticky="w")
    entry = tk.Entry(frame_top, width=30)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entries_top[text] = entry

tk.Button(top_section_frame, text="Submit", command=submit_data, font=("Arial", 12, "bold"), bg="navy", fg="white").pack(pady=10)
tk.Button(top_section_frame, text="Back to Home", command=lambda: show_frame(home_frame), font=("Arial", 12, "bold"), bg="gray").pack()

# --- Table Section (Scrollable) ---
table_headers = ["Month & Date", "Employee Name", "Train no.", "Time left", "Time arrived", "Station (from)", 
                 "Station (to)", "Kilometer", "Day/Night", "Object of Journey", "Rate (Rs.)", "Rate (P.)"]

table_entries = []

def add_row():
    row_entries = []
    for j in range(len(table_headers)):
        entry = tk.Entry(table_inner_frame, width=12)
        entry.grid(row=len(table_entries) + 1, column=j, pady=2)
        row_entries.append(entry)
    table_entries.append(row_entries)

def delete_row():
    if len(table_entries) > 1:
        row = table_entries.pop()
        for entry in row:
            entry.grid_forget()
    else:
        messagebox.showwarning("Warning", "At least one row is required.")

def save_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.append(table_headers)
    for row_entries in table_entries:
        row_data = [entry.get() for entry in row_entries]
        ws.append(row_data)
    save_path = os.path.join(os.getcwd(), "TravelAllowanceData.xlsx")
    wb.save(save_path)
    messagebox.showinfo("Save to Excel", f"Data saved successfully to {save_path}")

tk.Label(table_section_frame, text="Table Section", font=("Arial", 14, "bold"), bg="skyblue").pack(pady=10)

table_frame = tk.Frame(table_section_frame, bg="skyblue")
table_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Create a canvas for the table and attach both vertical and horizontal scrollbars
canvas = tk.Canvas(table_frame, bg="skyblue")
canvas.pack(side="left", fill="both", expand=True)

# Vertical scrollbar (for rows)
scrollbar_y = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
scrollbar_y.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar_y.set)

# Horizontal scrollbar (for columns)
scrollbar_x = tk.Scrollbar(table_frame, orient="horizontal", command=canvas.xview)
scrollbar_x.pack(side="bottom", fill="x")
canvas.configure(xscrollcommand=scrollbar_x.set)

# Create the inner frame that will hold the table rows and columns
table_inner_frame = tk.Frame(canvas, bg="skyblue")
canvas.create_window((0, 0), window=table_inner_frame, anchor="nw")

# Bind the inner frame to the canvas to make the scroll region dynamic
table_inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

# Add table headers to the table
for j, header in enumerate(table_headers):
    tk.Label(table_inner_frame, text=header, borderwidth=1, relief="solid", width=12, font=("Arial", 10, "bold"), bg="lightgray").grid(row=0, column=j)

# Start with one row in the table
add_row()

row_control_frame = tk.Frame(table_section_frame, bg="skyblue")
row_control_frame.pack(pady=5)

# Buttons for row management
tk.Button(row_control_frame, text="Add Row", command=add_row, font=("Arial", 10, "bold"), bg="green", fg="white").grid(row=0, column=0, padx=5)
tk.Button(row_control_frame, text="Delete Row", command=delete_row, font=("Arial", 10, "bold"), bg="red", fg="white").grid(row=0, column=1, padx=5)
tk.Button(row_control_frame, text="Save to Excel", command=save_to_excel, font=("Arial", 10, "bold"), bg="purple", fg="white").grid(row=0, column=2, padx=5)

tk.Button(table_section_frame, text="Back to Home", command=lambda: show_frame(home_frame), font=("Arial", 12, "bold"), bg="gray").pack()

# --- Certification Section (Fillable) ---
certification_labels = [
    "The T.A claimed by me has not been claimed before and will not be claimed hereafter.",
    "Conveyance charges claimed have actually been spent by me and according to local municipal rates.",
    "Cheapest mode of conveyance was utilized for travel.",
    "I hereby declare that I have followed the prescribed rules for the reimbursement."
]

# Create a dictionary to store the entry widgets for certification responses
certification_entries = {}

tk.Label(certification_section_frame, text="Certification", font=("Arial", 14, "bold"), bg="skyblue").pack(pady=10)

for i, text in enumerate(certification_labels):
    # Create a label for each certification statement
    tk.Label(certification_section_frame, text=text, font=("Arial", 10), bg="skyblue").pack(pady=5)
    
    # Create an entry widget for each certification statement to allow user input
    entry = tk.Entry(certification_section_frame, width=50)  # Adjust width as needed
    entry.pack(pady=5)
    certification_entries[text] = entry

tk.Button(certification_section_frame, text="Back to Home", command=lambda: show_frame(home_frame), font=("Arial", 12, "bold"), bg="gray").pack(pady=20)

# Start the application with the login frame
show_frame(login_frame)

root.mainloop()
