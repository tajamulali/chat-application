import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.simpledialog import askstring
from user_database import register_user, validate_user
from utils import encrypt_message, decrypt_message

class ChatApplication:
    def __init__(self, window):
        self.window = window
        self.window.title("Peer-to-Peer Chat Application")

        self.user_login_dialog()

        # Frames for different sections
        self.left_frame = tk.Frame(self.window)
        self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")

        self.chat_frame = tk.Frame(self.window)
        self.chat_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Contacts List on the Left
        self.contact_label = tk.Label(self.left_frame, text="Contacts", font=("Arial", 12))
        self.contact_label.pack(anchor="w", pady=5)

        self.contact_list = tk.Listbox(self.left_frame, height=20, width=20, font=("Arial", 10))
        self.contact_list.pack(padx=5, pady=5, expand=True, fill="both")

        # Chat Messages Display Area
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, height=15, width=50)
        self.chat_area.grid(row=0, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")
        self.chat_area.config(state='disabled')

        # Text box for typing messages
        self.message_entry = tk.Entry(self.chat_frame, width=30)
        self.message_entry.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        self.message_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.chat_frame, text="Send", width=10, command=self.send_message)
        self.send_button.grid(column=1, row=1, padx=10, pady=5)

        self.sock = None
        self.is_server = False
        self.is_logged_in = False

    def user_login_dialog(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("User Login/Registration")

        def on_register():
            username = username_entry.get()
            password = password_entry.get()
            success, message = register_user(username, password)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)

        def on_login():
            username = username_entry.get()
            password = password_entry.get()
            success, message = validate_user(username, password)
            if success:
                messagebox.showinfo("Success", message)
                self.is_logged_in = True
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)

        username_label = tk.Label(dialog, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        password_label = tk.Label(dialog, text="Password:")
        password_label.grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        register_button = tk.Button(dialog, text="Register", command=on_register)
        register_button.grid(row=2, column=0, padx=5, pady=5)
        login_button = tk.Button(dialog, text="Login", command=on_login)
        login_button.grid(row=2, column=1, padx=5, pady=5)

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            self.message_entry.delete(0, tk.END)
            encrypted_message = encrypt_message(message)
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, f"You: {message} (Encrypted: {encrypted_message})\n")
            self.chat_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()
