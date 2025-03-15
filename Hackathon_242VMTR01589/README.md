# Nova - AI-Powered Virtual Assistant

## Overview
Nova is an advanced AI-powered virtual assistant for Windows that responds to voice commands and performs various system operations seamlessly. Named after the brightness of a new star, Nova is designed to be your intelligent companion for everyday computing tasks.

## Features
- 🎤 **Voice Recognition**: Understands natural language voice commands
- 🔊 **Voice Response**: Provides verbal feedback and confirmation
- 🖥️ **Application Control**: Opens and manages various applications
- 🔄 **System Control**: Handles system operations (shutdown, restart, lock)
- 🌐 **Network Management**: Controls WiFi, Bluetooth, and displays network information
- ⚙️ **System Utilities**: Quick access to Control Panel, Task Manager, etc.
- 🎨 **Modern UI**: Clean, intuitive interface with visual feedback
- ✨ **Visual Cues**: Waving animation when wake word is detected

## Usage Examples
- "Nova, open Chrome"
- "Nova, what time is it?"
- "Nova, shutdown my computer"
- "Nova, turn off WiFi"
- "Nova, show me my IP address"
- "Nova, open Task Manager"

## Wake Word Detection
Nova responds to the following wake phrases:
- "Nova"
- "Hey Nova"
- "Hi Nova"
- "Hello Nova"

When Nova detects a wake word:
1. Nova provides a brief verbal acknowledgment
2. Nova then listens for your command

You can also combine the wake word and command in a single phrase: "Nova, open Chrome"

## Installation
1. Ensure you have Python 3.8+ installed
2. Clone this repository
3. cd Hackathon_242VMTR01589
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python main.py`

## Project Structure
- `main.py`: Entry point for the application
- `nova/`: Core assistant module
- `commands/`: Implementation of various command categories
- `ui/`: User interface components
- `utils/`: Utility functions and helpers

## Dependencies
- SpeechRecognition for voice input
- pyttsx3 for text-to-speech
- PyQt5 for the user interface
- pywin32 for Windows system operations
- Additional libraries for enhanced functionality

## Development
Created by divyesh savaliya, for the PyHackathon competition.
This project follows best practices in code organization, performance optimization, and user experience design.
