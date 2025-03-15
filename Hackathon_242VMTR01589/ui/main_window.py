"""
NovaUI - Main user interface for the Nova assistant.
"""

import os
import sys
import time
from datetime import datetime
import threading

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                             QLineEdit, QFrame, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, pyqtSlot, QThread, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPalette, QMovie

from ui.styles import NovaStyles

class NovaUI(QMainWindow):
    """
    Main window for the Nova assistant.
    """
    
    def __init__(self, assistant):
        """Initialize the main UI window."""
        super().__init__()
        
        # Store reference to the assistant
        self.assistant = assistant
        
        # Connect assistant events to UI
        self.assistant.on_listening_started = self.on_listening_started
        self.assistant.on_listening_stopped = self.on_listening_stopped
        self.assistant.on_processing_started = self.on_processing_started
        self.assistant.on_processing_stopped = self.on_processing_stopped
        self.assistant.on_speaking_started = self.on_speaking_started
        self.assistant.on_speaking_stopped = self.on_speaking_stopped
        self.assistant.on_wake_word_detected = self.on_wake_word_detected
        
        # Set up the UI
        self.init_ui()
        
        # Animation properties
        self.wave_animation = None
        self.wave_timer = QTimer()
        self.wave_timer.timeout.connect(self.stop_wave_animation)
        
        # Start the assistant
        QTimer.singleShot(1000, self.assistant.start)
    
    def get_icon_path(self, icon_name):
        """Get the path to an icon file, with fallback for missing files."""
        # Check if the icon exists in the assets directory
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        icon_path = os.path.join(assets_dir, icon_name)
        
        # If the icon exists, return its path
        if os.path.exists(icon_path):
            return icon_path
        
        # If the icon doesn't exist, return None (which will use a default)
        return None
    
    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("Nova AI Assistant")
        
        # Try to set the window icon
        icon_path = self.get_icon_path("nova_icon.png")
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        
        self.setMinimumSize(600, 700)
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Apply styles
        self.styles = NovaStyles()
        self.setStyleSheet(self.styles.get_main_style())
        
        # Create header with logo and title
        header_layout = QHBoxLayout()
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(64, 64)
        # placeholder for the logo - in real app, replace with actual logo
        self.logo_label.setStyleSheet("background-color: #4A6FFF; border-radius: 32px;")
        
        title_label = QLabel("Nova AI Assistant")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #4A6FFF;")
        
        # header_layout.addWidget(self.logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        
        # Status indicator
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setStyleSheet("color: #6C757D;")
        
        # Conversation history
        self.conversation_area = QTextEdit()
        self.conversation_area.setReadOnly(True)
        self.conversation_area.setFont(QFont("Segoe UI", 11))
        self.conversation_area.setStyleSheet(self.styles.get_conversation_style())
        self.conversation_area.setMinimumHeight(300)
        
        # Input area
        input_layout = QHBoxLayout()
        
        # Voice input button
        self.voice_button = QPushButton()
        self.voice_button.setFixedSize(50, 50)
        self.voice_button.setStyleSheet(self.styles.get_voice_button_style())
        
        # Try to set the mic icon
        mic_icon_path = self.get_icon_path("mic_icon.png")
        if mic_icon_path:
            self.voice_button.setIcon(QIcon(mic_icon_path))
            self.voice_button.setIconSize(QSize(30, 30))
        else:
            # If no icon is available, use text instead
            self.voice_button.setText("🎤")
            self.voice_button.setFont(QFont("Segoe UI", 16))
        
        self.voice_button.clicked.connect(self.toggle_voice_input)
        
        # Text input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type a command or say 'Nova' to activate voice...")
        self.text_input.setFont(QFont("Segoe UI", 11))
        self.text_input.setStyleSheet(self.styles.get_text_input_style())
        self.text_input.setMinimumHeight(50)
        self.text_input.returnPressed.connect(self.send_text_command)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(80, 50)
        self.send_button.setStyleSheet(self.styles.get_send_button_style())
        self.send_button.clicked.connect(self.send_text_command)
        
        input_layout.addWidget(self.voice_button)
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.send_button)
        
        # Help/tips section
        self.help_frame = QFrame()
        self.help_frame.setStyleSheet(self.styles.get_help_frame_style())
        self.help_frame.setMinimumHeight(100)
        
        help_layout = QVBoxLayout(self.help_frame)
        help_title = QLabel("Example Commands:")
        help_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        help_commands = QLabel(
            "• 'Nova, open Chrome'\n"
            "• 'Nova, what time is it?'\n"
            "• 'Nova, show my IP address'\n"
            "• 'Nova, search for prime minister of India'"
        )
        help_commands.setFont(QFont("Segoe UI", 10))
        
        help_layout.addWidget(help_title)
        help_layout.addWidget(help_commands)
        
        # Add all components to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.conversation_area)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.help_frame)
        
        # Set the central widget
        self.setCentralWidget(central_widget)
        
        # Add initial greeting to conversation
        self.add_assistant_message("Hello! I'm Nova, your virtual assistant. Say my name or type a command to get started.")
    
    def toggle_voice_input(self):
        """Toggle voice input on/off."""
        if not self.assistant.is_listening:
            self.voice_button.setStyleSheet(self.styles.get_voice_button_active_style())
            self.add_system_message("Listening for command...")
            self.status_label.setText("Listening...")
            self.status_label.setStyleSheet("color: #28A745;")
            
            # Start listening for a command directly (without wake word)
            threading.Thread(target=self.listen_for_direct_command).start()
        else:
            self.voice_button.setStyleSheet(self.styles.get_voice_button_style())
            self.assistant.stop()
    
    def listen_for_direct_command(self):
        """Listen for a command directly (without wake word)."""
        try:
            command = self.assistant.recognizer.listen_for_command(timeout=5)
            if command:
                self.add_user_message(command)
                self.assistant.process_command(command)
            else:
                self.add_system_message("I didn't hear a command. Please try again.")
                self.reset_ui_state()
        except Exception as e:
            self.add_system_message(f"Error listening: {str(e)}")
            self.reset_ui_state()
    
    def send_text_command(self):
        """Send a text command from the input field."""
        command = self.text_input.text().strip()
        if not command:
            return
            
        self.text_input.clear()
        self.add_user_message(command)
        self.assistant.process_command(command)
    
    def add_user_message(self, message):
        """Add a user message to the conversation area."""
        timestamp = datetime.now().strftime("%H:%M")
        html = f'<div style="margin-bottom: 10px; text-align: right;">'
        html += f'<span style="background-color: #4A6FFF; color: white; padding: 8px 12px; border-radius: 15px; display: inline-block; max-width: 70%; text-align: left;">{message}</span>'
        html += f'<div style="font-size: 10px; color: #6C757D; margin-top: 2px;">{timestamp}</div>'
        html += '</div>'
        
        self.conversation_area.append(html)
        self.conversation_area.verticalScrollBar().setValue(
            self.conversation_area.verticalScrollBar().maximum()
        )
    
    def add_assistant_message(self, message):
        """Add an assistant message to the conversation area."""
        timestamp = datetime.now().strftime("%H:%M")
        html = f'<div style="margin-bottom: 10px;">'
        html += f'<span style="background-color: #E9ECEF; color: #212529; padding: 8px 12px; border-radius: 15px; display: inline-block; max-width: 70%;">{message}</span>'
        html += f'<div style="font-size: 10px; color: #6C757D; margin-top: 2px;">{timestamp}</div>'
        html += '</div>'
        
        self.conversation_area.append(html)
        self.conversation_area.verticalScrollBar().setValue(
            self.conversation_area.verticalScrollBar().maximum()
        )
    
    def add_system_message(self, message):
        """Add a system message to the conversation area."""
        html = f'<div style="margin: 5px 0; text-align: center;">'
        html += f'<span style="font-size: 11px; color: #6C757D;">{message}</span>'
        html += '</div>'
        
        self.conversation_area.append(html)
        self.conversation_area.verticalScrollBar().setValue(
            self.conversation_area.verticalScrollBar().maximum()
        )
    
    def reset_ui_state(self):
        """Reset the UI to its default state."""
        self.voice_button.setStyleSheet(self.styles.get_voice_button_style())
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("color: #6C757D;")
        
        # Stop any animations
        if self.wave_animation and self.wave_animation.state() == QPropertyAnimation.Running:
            self.wave_animation.stop()
            self.logo_label.setStyleSheet("background-color: #4A6FFF; border-radius: 32px;")
    
    def start_wave_animation(self):
        """Start the waving animation on the logo."""
        # Create a pulsing animation for the logo
        self.wave_animation = QPropertyAnimation(self.logo_label, b"styleSheet")
        self.wave_animation.setDuration(800)  # Animation duration in ms
        self.wave_animation.setLoopCount(3)   # Repeat 3 times
        
        # Define the animation keyframes
        self.wave_animation.setStartValue("background-color: #4A6FFF; border-radius: 32px;")
        self.wave_animation.setEndValue("background-color: #FF4A6F; border-radius: 32px;")
        
        # Set easing curve for smooth animation
        self.wave_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Start the animation
        self.wave_animation.start()
        
        # Add label text to show "Listening..."
        self.add_system_message("I heard you! Now tell me what you need...")
        
        # Set a timer to stop the animation after a few seconds if no command is received
        self.wave_timer.start(5000)  # 5 seconds
    
    def stop_wave_animation(self):
        """Stop the waving animation."""
        # Stop the timer
        self.wave_timer.stop()
        
        # Reset the logo if animation is still running
        if self.wave_animation and self.wave_animation.state() == QPropertyAnimation.Running:
            self.wave_animation.stop()
            self.logo_label.setStyleSheet("background-color: #4A6FFF; border-radius: 32px;")
    
    # Event handlers for assistant states
    
    def on_listening_started(self):
        """Called when the assistant starts listening."""
        self.voice_button.setStyleSheet(self.styles.get_voice_button_active_style())
        self.status_label.setText("Listening...")
        self.status_label.setStyleSheet("color: #28A745;")
    
    def on_listening_stopped(self):
        """Called when the assistant stops listening."""
        self.voice_button.setStyleSheet(self.styles.get_voice_button_style())
        # Stop wave animation if it's still running
        self.stop_wave_animation()
    
    def on_processing_started(self):
        """Called when the assistant starts processing a command."""
        self.status_label.setText("Processing...")
        self.status_label.setStyleSheet("color: #FFC107;")
    
    def on_processing_stopped(self):
        """Called when the assistant finishes processing a command."""
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("color: #6C757D;")
    
    def on_speaking_started(self, text):
        """Called when the assistant starts speaking."""
        self.add_assistant_message(text)
        self.status_label.setText("Speaking...")
        self.status_label.setStyleSheet("color: #17A2B8;")
    
    def on_speaking_stopped(self):
        """Called when the assistant stops speaking."""
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("color: #6C757D;")
    
    def on_wake_word_detected(self):
        """Called when the wake word is detected."""
        # Start the waving animation
        self.start_wave_animation()
        
        # Update status label
        self.status_label.setText("Listening...")
        self.status_label.setStyleSheet("color: #FF4A6F;")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop the assistant before closing
        self.assistant.stop()
        event.accept() 