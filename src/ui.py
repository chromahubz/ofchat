"""
Simple GUI for OFChat using tkinter
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from typing import Optional

from .config import Config
from .orchestrator import OFChatOrchestrator


class OFChatGUI:
    """Simple GUI for OFChat auto-reply system"""

    def __init__(self, root: tk.Tk, config: Config):
        """
        Initialize GUI

        Args:
            root: Tkinter root window
            config: Application configuration
        """
        self.root = root
        self.config = config
        self.orchestrator = OFChatOrchestrator(config)

        # Set up callbacks
        self.orchestrator.on_message_received = self.on_message_received
        self.orchestrator.on_response_generated = self.on_response_generated
        self.orchestrator.on_error = self.on_error
        self.orchestrator.on_status_change = self.on_status_change

        # Setup UI
        self.setup_window()
        self.create_widgets()

        # Test connection on startup
        self.test_api_connection()

    def setup_window(self):
        """Configure main window"""
        self.root.title("OFChat - Auto Reply Assistant")
        self.root.geometry(f"{self.config.WINDOW_WIDTH}x{self.config.WINDOW_HEIGHT}")
        self.root.resizable(True, True)

        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        """Create all GUI widgets"""

        # === Header Frame ===
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(
            header_frame,
            text="OFChat Auto-Reply Assistant",
            font=("Arial", 14, "bold")
        ).pack(side="left")

        # === Control Frame ===
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=1, column=0, sticky="ew", padx=10)

        # Start/Stop Button
        self.start_stop_btn = ttk.Button(
            control_frame,
            text="Start Monitoring",
            command=self.toggle_monitoring,
            width=20
        )
        self.start_stop_btn.pack(side="left", padx=5)

        # Screenshot Button
        self.screenshot_btn = ttk.Button(
            control_frame,
            text="Capture Screenshot",
            command=self.capture_screenshot,
            width=20
        )
        self.screenshot_btn.pack(side="left", padx=5)

        # Clear History Button
        ttk.Button(
            control_frame,
            text="Clear History",
            command=self.clear_history,
            width=15
        ).pack(side="left", padx=5)

        # === Settings Frame ===
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding="10")
        settings_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Auto-copy checkbox
        self.auto_copy_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame,
            text="Auto-copy response to clipboard",
            variable=self.auto_copy_var,
            command=self.update_settings
        ).pack(side="left", padx=10)

        # Conversation history checkbox
        self.use_history_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            settings_frame,
            text="Use conversation history",
            variable=self.use_history_var,
            command=self.update_settings
        ).pack(side="left", padx=10)

        # === Main Content Frame ===
        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        self.root.grid_rowconfigure(3, weight=1)

        # Incoming Message Display
        msg_label = ttk.Label(content_frame, text="Incoming Message:", font=("Arial", 10, "bold"))
        msg_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.message_display = scrolledtext.ScrolledText(
            content_frame,
            height=6,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.message_display.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.message_display.config(state=tk.DISABLED)

        # Generated Response Display
        response_label = ttk.Label(content_frame, text="Generated Response:", font=("Arial", 10, "bold"))
        response_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.response_display = scrolledtext.ScrolledText(
            content_frame,
            height=6,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg="#e8f5e9"
        )
        self.response_display.grid(row=3, column=0, sticky="nsew")
        self.response_display.config(state=tk.DISABLED)

        # === Status Bar ===
        self.status_var = tk.StringVar(value="Ready - Click 'Start Monitoring' to begin")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="5"
        )
        status_bar.grid(row=4, column=0, sticky="ew")

    def toggle_monitoring(self):
        """Start or stop clipboard monitoring"""
        if not self.orchestrator.is_running:
            self.orchestrator.start()
            self.start_stop_btn.config(text="Stop Monitoring")
            self.status_var.set("Monitoring clipboard for new messages...")
        else:
            self.orchestrator.stop()
            self.start_stop_btn.config(text="Start Monitoring")
            self.status_var.set("Monitoring stopped")

    def capture_screenshot(self):
        """Capture and process screenshot"""
        def capture():
            self.orchestrator.capture_and_process_screenshot()

        # Run in thread to prevent UI blocking
        threading.Thread(target=capture, daemon=True).start()

    def clear_history(self):
        """Clear conversation history"""
        self.orchestrator.clear_history()
        messagebox.showinfo("History Cleared", "Conversation history has been cleared.")

    def update_settings(self):
        """Update orchestrator settings from UI"""
        self.orchestrator.auto_copy_enabled = self.auto_copy_var.get()
        self.orchestrator.use_conversation_history = self.use_history_var.get()

    def on_message_received(self, message: str):
        """
        Callback when new message is received

        Args:
            message: Incoming message text
        """
        def update():
            self.message_display.config(state=tk.NORMAL)
            self.message_display.delete(1.0, tk.END)
            self.message_display.insert(1.0, message)
            self.message_display.config(state=tk.DISABLED)

        self.root.after(0, update)

    def on_response_generated(self, response: str):
        """
        Callback when response is generated

        Args:
            response: Generated response text
        """
        def update():
            self.response_display.config(state=tk.NORMAL)
            self.response_display.delete(1.0, tk.END)
            self.response_display.insert(1.0, response)
            self.response_display.config(state=tk.DISABLED)

        self.root.after(0, update)

    def on_error(self, error: str):
        """
        Callback when error occurs

        Args:
            error: Error message
        """
        def show_error():
            messagebox.showerror("Error", error)

        self.root.after(0, show_error)

    def on_status_change(self, status: str):
        """
        Callback when status changes

        Args:
            status: New status message
        """
        def update():
            self.status_var.set(status)

        self.root.after(0, update)

    def test_api_connection(self):
        """Test Groq API connection on startup"""
        def test():
            try:
                if self.orchestrator.test_connection():
                    self.root.after(0, lambda: self.status_var.set("Ready - API connection successful"))
                else:
                    self.root.after(0, lambda: messagebox.showwarning(
                        "API Connection",
                        "Could not connect to Groq API. Please check your API key in .env file."
                    ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "API Error",
                    f"Error testing API connection: {str(e)}"
                ))

        threading.Thread(target=test, daemon=True).start()

    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()


def create_gui(config: Config) -> OFChatGUI:
    """
    Create and return GUI instance

    Args:
        config: Application configuration

    Returns:
        GUI instance
    """
    root = tk.Tk()
    gui = OFChatGUI(root, config)
    return gui
