import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.simpledialog import askstring

# ------------------------------------ GUI Chat Application ------------------------------------
class ChatApplication:
    def __init__(self, window):
        self.window = window
        self.window.title("Peer-to-Peer Chat Application")

        # Frames for different sections
        self.left_frame = tk.Frame(self.window)
        self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")
        
        self.chat_frame = tk.Frame(self.window)
        self.chat_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        # ----------- Contacts List on the Left -----------
        self.contact_label = tk.Label(self.left_frame, text="Contacts", font=("Arial", 12))
        self.contact_label.pack(anchor="w", pady=5)

        self.contact_list = tk.Listbox(self.left_frame, height=20, width=20, font=("Arial", 10))
        self.contact_list.pack(padx=5, pady=5, expand=True, fill="both")
        
        # ----------- Chat Messages Display Area -----------
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, height=15, width=50)
        self.chat_area.grid(row=0, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")
        self.chat_area.config(state='disabled')  # Disable input in chat area

        # ----------- Text box for typing messages -----------
        self.message_entry = tk.Entry(self.chat_frame, width=30)
        self.message_entry.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        self.message_entry.bind("<Return>", self.send_message)  # Send message on Enter

        # ----------- Send button -----------
        self.send_button = tk.Button(self.chat_frame, text="Send", width=10, command=self.send_message)
        self.send_button.grid(column=1, row=1, padx=10, pady=5)

        # Network-related attributes
        self.sock = None
        self.is_server = False

        # Start the connection dialog
        self.connect_dialog()

    def connect_dialog(self):
        """Dialog to choose whether to host or connect to a chat"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Connection Setup")

        # Server mode
        server_button = tk.Button(dialog, text="Host Chat", width=20, command=lambda: self.setup_server(dialog))
        server_button.pack(pady=10)

        # Client mode
        client_button = tk.Button(dialog, text="Join Chat", width=20, command=lambda: self.setup_client(dialog))
        client_button.pack(pady=10)

    def setup_server(self, dialog):
        """Set up the server socket"""
        dialog.destroy()
        self.is_server = True

        # Start server socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 12345))  # Bind to any available network interface and port 12345
        self.sock.listen(5)

        # Accept client connections
        threading.Thread(target=self.accept_connections).start()
        self.append_message("Server started, waiting for connections...")

    def setup_client(self, dialog):
        """Set up the client socket and connect to the server"""
        dialog.destroy()
        self.is_server = False

        # Dialog to ask for server address
        server_ip = askstring("Server IP", "Enter Server IP Address:", parent=self.window)

        # Connect to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((server_ip, 12345))
            threading.Thread(target=self.receive_messages).start()
            self.append_message(f"Connected to server at {server_ip}")
        except Exception as e:
            messagebox.showerror("Connection Failed", str(e))

    def accept_connections(self):
        """Accept connections from other peers"""
        client_sock, client_addr = self.sock.accept()
        self.append_message(f"Client {client_addr} connected")
        threading.Thread(target=self.handle_client, args=(client_sock,)).start()

    def handle_client(self, client_sock):
        """Handle messages from connected client"""
        while True:
            try:
                message = client_sock.recv(1024).decode()
                if message:
                    self.append_message(message)
                else:
                    break
            except:
                break

    def receive_messages(self):
        """Receive messages from the server or peer"""
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    self.append_message(message)
                else:
                    break
            except:
                break

    def send_message(self, event=None):
        """Send message to the connected peer"""
        message = self.message_entry.get()
        if message:
            self.message_entry.delete(0, tk.END)
            formatted_message = f"You: {message}"
            self.append_message(formatted_message)

            # Send message to connected peer or server
            if self.is_server:
                self.sock.sendto(message.encode(), ('127.0.0.1', 12345))
            else:
                self.sock.send(message.encode())

    def append_message(self, message):
        """Append message to chat area"""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)


# --------------- Main Code -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()
