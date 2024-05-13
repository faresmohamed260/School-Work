import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import Error


# Database connection
def connect_to_database():
    try:
        connection = sqlite3.connect("student.db")
        print("Connected to SQLite database")
        return connection
    except Error as e:
        print("Error connecting to SQLite database:", e)
        return None


# noinspection PyUnusedLocal
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student App")
        self.root.geometry("400x400")  # Set the window size to 800x600 pixels

        # Connect to SQLite database
        self.connection = connect_to_database()

        # Tab management
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both")

        # Login frame
        self.login_frame = tk.Frame(self.tab_control)
        self.tab_control.add(self.login_frame, text="Login")

        tk.Label(self.login_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()
        self.username_entry.bind("<Return>", self.on_enter_username)

        tk.Label(self.login_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()
        self.password_entry.bind("<Return>", self.on_enter_password)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

        # Main frame
        self.main_frame = tk.Frame(self.tab_control)

        self.logout_button = tk.Button(self.main_frame, text="Logout", command=self.logout, state="disabled")
        self.logout_button.pack()

        self.subjects_label = tk.Label(self.main_frame, text="Subjects:")
        self.subjects_label.pack()

        self.subjects_listbox = tk.Listbox(self.main_frame, width=50)  # Adjust the width as needed
        self.subjects_listbox.pack()

        self.cgpa_label = tk.Label(self.main_frame, text="CGPA:")
        self.cgpa_label.pack()

        self.cgpa_value = tk.StringVar()
        self.cgpa_label_value = tk.Label(self.main_frame, textvariable=self.cgpa_value)
        self.cgpa_label_value.pack()

        # Admin panel (Empty for now)
        self.admin_panel = tk.Frame(self.tab_control)
        self.tab_control.add(self.admin_panel, text="Admin")

        # Made by panel
        self.made_by_panel = tk.Frame(self.tab_control)
        self.tab_control.add(self.made_by_panel, text="Made by")

        # Display information about the team member(s)
        team_info = """Team Kawkab El Sor3a 

        Kareem Ashraf Ahmed    22030171
        Fares Mohamed Salah    22011614
        Mahmod Ahmed Bahig       2203165   """  # Add more information as needed
        tk.Label(self.made_by_panel, text=team_info).pack()

    def on_enter_username(self, event):
        self.password_entry.focus()

    def on_enter_password(self, event):
        self.login_button.invoke()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.connection:
            try:
                cursor = self.connection.cursor()
                # Check login credentials
                cursor.execute("SELECT * FROM account WHERE username = ? AND password = ?", (username, password))
                account = cursor.fetchone()

                if account:
                    # Get student ID
                    student_id = account[4]

                    # Check if a student exists
                    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
                    student = cursor.fetchone()

                    if student:
                        # Display student information
                        self.main_frame.pack()
                        self.login_frame.pack_forget()
                        self.logout_button.config(state="normal")

                        # Display subjects
                        cursor.execute("SELECT * FROM subjects WHERE student_id = ?", (student_id,))
                        subjects = cursor.fetchall()
                        self.subjects_listbox.delete(0, tk.END)
                        for subject in subjects:
                            self.subjects_listbox.insert(tk.END, f"{subject[2]}: {subject[3]} ({subject[4]} credits)")

                        # Calculate and display CGPA
                        cursor.execute("""
                                    SELECT SUM(credit_hours *
                                        CASE 
                                            WHEN grade = 'A+' THEN 4.3
                                            WHEN grade = 'A' THEN 4.0
                                            WHEN grade = 'A-' THEN 3.7
                                            WHEN grade = 'B+' THEN 3.3
                                            WHEN grade = 'B' THEN 3.0
                                            WHEN grade = 'B-' THEN 2.7
                                            WHEN grade = 'C+' THEN 2.3
                                            WHEN grade = 'C' THEN 2.0
                                            WHEN grade = 'C-' THEN 1.7
                                            WHEN grade = 'D+' THEN 1.3
                                            WHEN grade = 'D' THEN 1.0
                                            WHEN grade = 'D-' THEN 0.7
                                            WHEN grade = 'F' THEN 0.0
                                        END) / SUM(credit_hours) AS cgpa
                                    FROM subjects
                                    WHERE student_id = ?
                                """, (student_id,))
                        cgpa = cursor.fetchone()[0]
                        self.cgpa_value.set(f"{cgpa: .2f}")

                    else:
                        messagebox.showerror("Error", "Student not found")

                else:
                    messagebox.showerror("Error", "Invalid username or password")

                return "login successful"
            except Error as e:
                return f"Error logging in: {e}"
            finally:
                cursor.close()
        else:
            return "Not connected to the database"

    def logout(self):
        self.tab_control.select(self.login_frame)
        self.main_frame.pack_forget()
        self.logout_button.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
