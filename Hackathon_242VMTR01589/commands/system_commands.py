"""
SystemCommands - Handles commands related to system operations like shutdown, restart, etc.
"""

import os
import subprocess
import re
import ctypes
import time
import platform
import sys

class SystemCommands:
    """
    Handles commands related to system operations.
    """
    
    def __init__(self, assistant):
        """Initialize the system commands handler."""
        self.assistant = assistant
        
        # Command patterns and their handlers
        self.command_patterns = {
            r"(shutdown|turn off)\s+(computer|pc|system)": self._shutdown,
            r"restart\s+(computer|pc|system)": self._restart,
            r"log\s?out": self._logout,
            r"lock\s+(computer|pc|system)": self._lock,
            r"sleep\s+(computer|pc|system)": self._sleep,
            r"hibernate\s+(computer|pc|system)": self._hibernate
        }
    
    def process(self, command_text, match=None):
        """
        Process system-related commands.
        Returns a response string.
        """
        command_lower = command_text.lower()
        
        # If match is provided, use it to determine the command
        if match:
            for pattern, handler in self.command_patterns.items():
                if re.match(pattern, match.group(0), re.IGNORECASE):
                    return handler(command_text)
        
        # Otherwise, try to match the command
        for pattern, handler in self.command_patterns.items():
            if re.search(pattern, command_lower, re.IGNORECASE):
                return handler(command_text)
        
        # Check for specific keywords if no pattern matches
        if "shutdown" in command_lower or "turn off" in command_lower:
            return self._shutdown(command_text)
        elif "restart" in command_lower:
            return self._restart(command_text)
        elif "logout" in command_lower or "log out" in command_lower:
            return self._logout(command_text)
        elif "lock" in command_lower:
            return self._lock(command_text)
        elif "sleep" in command_lower:
            return self._sleep(command_text)
        elif "hibernate" in command_lower:
            return self._hibernate(command_text)
        
        # If no command is recognized
        return "I'm not sure which system command you want to execute. " \
               "Try saying 'shutdown', 'restart', 'lock', 'sleep', 'hibernate', or 'log out'."
    
    def _shutdown(self, command_text):
        """Shutdown the computer."""
        # Check for time specification
        delay = self._extract_time_delay(command_text)
        
        try:
            # Get confirmation before shutdown
            self.assistant.speak(f"I'll shut down your computer{' in ' + str(delay) + ' seconds' if delay > 0 else ' now'}. Are you sure?")
            
            # For now, just return the confirmation message
            return f"I'll shut down your computer{' in ' + str(delay) + ' seconds' if delay > 0 else ' now'} after confirmation."
            
            # if confirmation:
            #     if os.name == 'nt':  # Windows
            #         os.system(f"shutdown /s /t {delay}")
            #     else:  # Linux/Mac
            #         os.system(f"shutdown -h +{delay//60}")
            #     return f"Shutting down in {delay} seconds."
            # else:
            #     return "Shutdown cancelled."
            
        except Exception as e:
            return f"I couldn't shutdown your computer. Error: {str(e)}"
    
    def _restart(self, command_text):
        """Restart the computer."""
        # Check for time specification
        delay = self._extract_time_delay(command_text)
        
        try:
            # Get confirmation before restart
            self.assistant.speak(f"I'll restart your computer{' in ' + str(delay) + ' seconds' if delay > 0 else ' now'}. Are you sure?")
            
            # For now, just return the confirmation message
            return f"I'll restart your computer{' in ' + str(delay) + ' seconds' if delay > 0 else ' now'} after confirmation."
            
            # if confirmation:
            #     if os.name == 'nt':  # Windows
            #         os.system(f"shutdown /r /t {delay}")
            #     else:  # Linux/Mac
            #         os.system(f"shutdown -r +{delay//60}")
            #     return f"Restarting in {delay} seconds."
            # else:
            #     return "Restart cancelled."
            
        except Exception as e:
            return f"I couldn't restart your computer. Error: {str(e)}"
    
    def _logout(self, command_text):
        """Log out the current user."""
        try:
            # Get confirmation before logout
            self.assistant.speak("I'll log you out. Are you sure?")
            
            # For now, just return the confirmation message
            return "I'll log you out after confirmation."
            
            # if confirmation:
            #     if os.name == 'nt':  # Windows
            #         os.system("shutdown /l")
            #     else:  # Linux/Mac
            #         os.system("pkill -KILL -u $USER")
            #     return "Logging out now."
            # else:
            #     return "Logout cancelled."
            
        except Exception as e:
            return f"I couldn't log you out. Error: {str(e)}"
    
    def _lock(self, command_text):
        """Lock the computer."""
        try:
            if os.name == 'nt':  # Windows
                ctypes.windll.user32.LockWorkStation()
                return "Locking your computer."
            else:  # Linux/Mac
                # This is platform-dependent, might need adjustments
                if platform.system() == "Darwin":  # macOS
                    os.system("pmset displaysleepnow")
                else:  # Linux
                    os.system("xdg-screensaver lock")
                return "Locking your computer."
                
        except Exception as e:
            return f"I couldn't lock your computer. Error: {str(e)}"
    
    def _sleep(self, command_text):
        """Put the computer to sleep."""
        try:
            # Get confirmation before sleep
            self.assistant.speak("I'll put your computer to sleep. Are you sure?")
            
            # For now, just return the confirmation message
            return "I'll put your computer to sleep after confirmation."
            
            # if confirmation:
            #     if os.name == 'nt':  # Windows
            #         os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            #     elif platform.system() == "Darwin":  # macOS
            #         os.system("pmset sleepnow")
            #     else:  # Linux
            #         os.system("systemctl suspend")
            #     return "Putting your computer to sleep."
            # else:
            #     return "Sleep cancelled."
            
        except Exception as e:
            return f"I couldn't put your computer to sleep. Error: {str(e)}"
    
    def _hibernate(self, command_text):
        """Hibernate the computer."""
        try:
            # Get confirmation before hibernate
            self.assistant.speak("I'll hibernate your computer. Are you sure?")
            
            # For now, just return the confirmation message
            return "I'll hibernate your computer after confirmation."
            
            # if confirmation:
            #     if os.name == 'nt':  # Windows
            #         os.system("shutdown /h")
            #     elif platform.system() == "Darwin":  # macOS
            #         os.system("pmset hibernatemode 25")
            #         os.system("pmset sleepnow")
            #     else:  # Linux
            #         os.system("systemctl hibernate")
            #     return "Hibernating your computer."
            # else:
            #     return "Hibernate cancelled."
            
        except Exception as e:
            return f"I couldn't hibernate your computer. Error: {str(e)}"
    
    def _extract_time_delay(self, command_text):
        """Extract time delay from command text, in seconds."""
        # Look for time specifications like "in 5 minutes" or "after 10 seconds"
        command_lower = command_text.lower()
        
        # Check for seconds
        seconds_match = re.search(r"(\d+)\s+second", command_lower)
        if seconds_match:
            return int(seconds_match.group(1))
        
        # Check for minutes
        minutes_match = re.search(r"(\d+)\s+minute", command_lower)
        if minutes_match:
            return int(minutes_match.group(1)) * 60
        
        # Check for hours
        hours_match = re.search(r"(\d+)\s+hour", command_lower)
        if hours_match:
            return int(hours_match.group(1)) * 3600
        
        # Default delay (0 for immediate action)
        return 0 