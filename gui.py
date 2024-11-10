# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import password_manager

class PasswordManagerGUI:
    def __init__(self, root):
        # Set window title and default size
        root.title("Password Manager")
        root.geometry("270x90")
        root.update_idletasks()  # Update "requested size" to get true width and height

        # Center the window on the screen
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coord = int((screen_width / 2) - (window_width / 2))
        y_coord = int((screen_height / 2) - (window_height / 2))
        root.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

        # Main frame with padding
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Buttons for 'Create User Key' and 'Login with Key'
        self.create_key_button = tk.Button(self.main_frame, text="Create User Key", command=self.create_user_key)
        self.create_key_button.grid(row=0, column=0, padx=10, pady=10)

        self.login_key_button = tk.Button(self.main_frame, text="Login with Key", command=self.login_with_key)
        self.login_key_button.grid(row=0, column=1, padx=10, pady=10)

        # Variables to store paths and state
        self.key_path = None
        self.logged_in = False
        self.copy_button = None

    def create_user_key(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".key", title="Save Key File", filetypes=[("Key Files", "*.key")])
        if file_path:
            password_manager.create_user_key(file_path)
            self.key_path = file_path
            messagebox.showinfo("Success", "User key created successfully! Please log in with the key.")

    def login_with_key(self):
        file_path = filedialog.askopenfilename(title="Open Key File", filetypes=[("Key Files", "*.key")])
        if file_path:
            self.key_path = file_path
            self.logged_in = True
            messagebox.showinfo("Login Successful", "Key loaded successfully! Now you can save and retrieve passwords.")
            self.load_save_retrieve_screen()

    def load_save_retrieve_screen(self):
        root.geometry("340x270")
        # Clear the main frame for the new screen
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Labels and entries for application, username, and password
        tk.Label(self.main_frame, text="Application:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.app_name_entry = tk.Entry(self.main_frame, width=30)
        self.app_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="Username:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(self.main_frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(self.main_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Save Password button
        self.save_button = tk.Button(self.main_frame, text="Save Password", command=self.save_password)
        self.save_button.grid(row=3, column=0, padx=10, pady=20, columnspan=2)

        # Retrieve Password button
        self.retrieve_button = tk.Button(self.main_frame, text="Retrieve Password", command=self.retrieve_password)
        self.retrieve_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

    def save_password(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bin", title="Save Password File", filetypes=[("Binary Files", "*.bin")])
        if file_path and self.logged_in and self.key_path:
            app_name = self.app_name_entry.get()
            username = self.username_entry.get()
            password = self.password_entry.get()
            password_manager.save_password(self.key_path, file_path, app_name, username, password)
            messagebox.showinfo("Success", "Password saved successfully!")

    def retrieve_password(self):
        file_path = filedialog.askopenfilename(title="Open Password File", filetypes=[("Binary Files", "*.bin")])
        if file_path and self.logged_in and self.key_path:
            app_name = self.app_name_entry.get()
            decrypted_password = password_manager.retrieve_password(self.key_path, file_path, app_name)
            if decrypted_password:
                # Display password in an entry widget (without hiding it)
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, decrypted_password)
                # Create a "Copy to Clipboard" button
                if not self.copy_button:
                    self.copy_button = tk.Button(self.main_frame, text="Copy Retrieved Password", command=self.copy_password)
                    self.copy_button.grid(row=5, column=0, padx=10, pady=20, columnspan=2)
                root.geometry("340x330")
                messagebox.showinfo("Password Retrieved", f"Password for {app_name}: {decrypted_password}")
            else:
                messagebox.showwarning("Error", "Password not found or incorrect key.")
    
    def copy_password(self):
        """Copies the displayed password to the clipboard."""
        password = self.password_entry.get()
        root.clipboard_clear()  # Clear current clipboard content
        root.clipboard_append(password)  # Add the password to clipboard
        root.update()  # Update clipboard content
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
