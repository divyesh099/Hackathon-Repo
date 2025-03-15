"""
NovaStyles - Style definitions for the Nova assistant UI.
"""

class NovaStyles:
    """
    Provides style definitions for the Nova assistant UI components.
    """
    
    def __init__(self):
        """Initialize the styles with color schemes."""
        # Color schemes
        self.colors = {
            "primary": "#4A6FFF",  # Primary blue
            "primary_light": "#7B93FF",
            "primary_dark": "#3A5BE0",
            "secondary": "#6C757D",  # Gray
            "success": "#28A745",  # Green
            "danger": "#DC3545",  # Red
            "warning": "#FFC107",  # Yellow
            "info": "#17A2B8",  # Cyan
            "light": "#F8F9FA",
            "dark": "#343A40",
            "white": "#FFFFFF",
            "background": "#F8F9FA",
            "text": "#212529",
            "text_light": "#6C757D",
            "border": "#DEE2E6",
            "conversation_bg": "#FFFFFF",
            "user_message_bg": "#4A6FFF",
            "user_message_text": "#FFFFFF",
            "assistant_message_bg": "#E9ECEF",
            "assistant_message_text": "#212529"
        }
    
    def get_main_style(self):
        """Get the main application style."""
        return f"""
            QMainWindow, QWidget {{
                background-color: {self.colors["background"]};
                color: {self.colors["text"]};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            QLabel {{
                color: {self.colors["text"]};
            }}
            
            QPushButton {{
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                background-color: {self.colors["primary"]};
                color: {self.colors["white"]};
            }}
            
            QPushButton:hover {{
                background-color: {self.colors["primary_light"]};
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors["primary_dark"]};
            }}
            
            QLineEdit {{
                border: 1px solid {self.colors["border"]};
                border-radius: 4px;
                padding: 8px 12px;
                background-color: {self.colors["white"]};
                color: {self.colors["text"]};
            }}
            
            QLineEdit:focus {{
                border: 2px solid {self.colors["primary"]};
            }}
            
            QTextEdit {{
                border: 1px solid {self.colors["border"]};
                border-radius: 4px;
                padding: 8px;
                background-color: {self.colors["conversation_bg"]};
                color: {self.colors["text"]};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background-color: {self.colors["light"]};
                width: 10px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors["secondary"]};
                border-radius: 5px;
                min-height: 30px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
    
    def get_conversation_style(self):
        """Get the style for the conversation area."""
        return f"""
            QTextEdit {{
                border: 1px solid {self.colors["border"]};
                border-radius: 10px;
                padding: 15px;
                background-color: {self.colors["conversation_bg"]};
                color: {self.colors["text"]};
            }}
        """
    
    def get_voice_button_style(self):
        """Get the style for the voice input button."""
        return f"""
            QPushButton {{
                background-color: {self.colors["primary"]};
                color: {self.colors["white"]};
                border-radius: 25px;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors["primary_light"]};
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors["primary_dark"]};
            }}
        """
    
    def get_voice_button_active_style(self):
        """Get the active style for the voice input button."""
        return f"""
            QPushButton {{
                background-color: {self.colors["danger"]};
                color: {self.colors["white"]};
                border-radius: 25px;
            }}
            
            QPushButton:hover {{
                background-color: #E04756;
            }}
            
            QPushButton:pressed {{
                background-color: #BD2130;
            }}
        """
    
    def get_text_input_style(self):
        """Get the style for the text input field."""
        return f"""
            QLineEdit {{
                border: 1px solid {self.colors["border"]};
                border-radius: 25px;
                padding: 8px 16px;
                background-color: {self.colors["white"]};
                color: {self.colors["text"]};
            }}
            
            QLineEdit:focus {{
                border: 2px solid {self.colors["primary"]};
            }}
        """
    
    def get_send_button_style(self):
        """Get the style for the send button."""
        return f"""
            QPushButton {{
                background-color: {self.colors["primary"]};
                color: {self.colors["white"]};
                border-radius: 25px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors["primary_light"]};
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors["primary_dark"]};
            }}
        """
    
    def get_help_frame_style(self):
        """Get the style for the help/tips frame."""
        return f"""
            QFrame {{
                background-color: {self.colors["white"]};
                border: 1px solid {self.colors["border"]};
                border-radius: 10px;
                padding: 10px;
            }}
            
            QLabel {{
                color: {self.colors["text"]};
            }}
        """ 