#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nova - AI-Powered Virtual Assistant
Main entry point for the application
"""

import sys
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Ensure we can import from our package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import the main application components
from nova.assistant import NovaAssistant
from ui.main_window import NovaUI

def main():
    """Main entry point for the Nova assistant application"""
    print("Starting Nova AI Assistant...")
    
    try:
        # Initialize the application
        from PyQt5.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        app.setApplicationName("Nova")
        app.setApplicationDisplayName("Nova AI Assistant")
        
        # Create the assistant
        assistant = NovaAssistant()
        
        # Create and show the UI
        ui = NovaUI(assistant)
        ui.show()
        
        # Start with a welcome message
        assistant.speak("Hello, I am Nova, your virtual assistant. How can I help you today?")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Error starting Nova: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 