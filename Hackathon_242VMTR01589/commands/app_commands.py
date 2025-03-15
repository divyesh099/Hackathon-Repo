"""
AppCommands - Handles commands related to opening and managing applications.
"""

import os
import subprocess
import re
import sys
import webbrowser
from pathlib import Path

class AppCommands:
    """
    Handles commands related to opening and managing applications.
    """
    
    def __init__(self, assistant):
        """Initialize the application commands handler."""
        self.assistant = assistant
        
        # Common application mappings (app name to executable)
        self.app_mappings = {
            # Browsers
            "chrome": {
                "path": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "alt_path": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "open_method": self._open_executable
            },
            "firefox": {
                "path": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                "alt_path": r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                "open_method": self._open_executable
            },
            "edge": {
                "path": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "alt_path": "",
                "open_method": self._open_executable
            },
            "browser": {
                "path": "",
                "alt_path": "",
                "open_method": self._open_default_browser
            },
            
            # Office applications
            "word": {
                "path": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                "alt_path": r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                "open_method": self._open_executable
            },
            "excel": {
                "path": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                "alt_path": r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
                "open_method": self._open_executable
            },
            "powerpoint": {
                "path": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                "alt_path": r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
                "open_method": self._open_executable
            },
            
            # System utilities
            "calculator": {
                "path": "calc.exe",
                "alt_path": "",
                "open_method": self._open_windows_app
            },
            "notepad": {
                "path": "notepad.exe",
                "alt_path": "",
                "open_method": self._open_windows_app
            },
            "paint": {
                "path": "mspaint.exe",
                "alt_path": "",
                "open_method": self._open_windows_app
            },
            
            # Other applications
            "spotify": {
                "path": r"C:\Users\{username}\AppData\Roaming\Spotify\Spotify.exe",
                "alt_path": "",
                "open_method": self._open_executable
            },
            "vlc": {
                "path": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                "alt_path": r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
                "open_method": self._open_executable
            }
        }
    
    def process(self, command_text, match=None):
        """
        Process application-related commands.
        Returns a response string.
        """
        # Extract the application name from the command
        app_name = self._extract_app_name(command_text, match)
        
        if not app_name:
            return "I didn't catch which application you want to open. Can you specify the application name?"
        
        # Try to open the application
        result = self._open_application(app_name)
        
        if result["success"]:
            return f"Opening {app_name}."
        else:
            return f"I couldn't open {app_name}. {result['message']}"
    
    def _extract_app_name(self, command_text, match=None):
        """Extract the application name from the command text or match object."""
        if match and 'app_name' in match.groupdict():
            return match.group('app_name').strip().lower()
        
        # If no match, try to extract using regex
        app_pattern = re.compile(r"(open|launch|start|run)\s+(?P<app_name>[\w\s]+)", re.IGNORECASE)
        match = app_pattern.search(command_text)
        
        if match and 'app_name' in match.groupdict():
            return match.group('app_name').strip().lower()
        
        # If still no match, just take everything after the command word
        for cmd in ["open", "launch", "start", "run"]:
            if cmd in command_text.lower():
                parts = command_text.lower().split(cmd, 1)
                if len(parts) > 1:
                    return parts[1].strip()
        
        return None
    
    def _open_application(self, app_name):
        """
        Open an application by name.
        Returns a dictionary with success status and message.
        """
        # Normalize app name (remove extra spaces, convert to lowercase)
        app_name = app_name.strip().lower()
        
        # Check if the app is in our mappings
        for key, app_info in self.app_mappings.items():
            if key in app_name or app_name in key:
                # Replace username in path if needed
                if "{username}" in app_info["path"]:
                    username = os.getenv("USERNAME")
                    app_info["path"] = app_info["path"].replace("{username}", username)
                
                # Open the application using the specified method
                return app_info["open_method"](app_info["path"], app_info["alt_path"])
        
        # If not in mappings, try as a Windows app or command
        try:
            subprocess.Popen(app_name, shell=True)
            return {"success": True, "message": ""}
        except Exception as e:
            return {"success": False, "message": f"Application not found or could not be opened."}
    
    def _open_executable(self, path, alt_path):
        """Open an executable file at the given path."""
        try:
            if os.path.exists(path):
                subprocess.Popen([path])
                return {"success": True, "message": ""}
            elif alt_path and os.path.exists(alt_path):
                subprocess.Popen([alt_path])
                return {"success": True, "message": ""}
            else:
                return {"success": False, "message": "Application path not found."}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def _open_windows_app(self, app_name, _):
        """Open a Windows built-in application."""
        try:
            subprocess.Popen([app_name])
            return {"success": True, "message": ""}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def _open_default_browser(self, _, __):
        """Open the default web browser."""
        try:
            webbrowser.open("https://www.google.com")
            return {"success": True, "message": ""}
        except Exception as e:
            return {"success": False, "message": str(e)} 