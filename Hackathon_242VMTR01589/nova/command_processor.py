"""
CommandProcessor - Parses and routes commands to appropriate handlers.
"""

import re
import importlib
import os
from datetime import datetime
import sys

# Import command modules
from commands.app_commands import AppCommands
from commands.system_commands import SystemCommands
from commands.network_commands import NetworkCommands
from commands.utility_commands import UtilityCommands

class CommandProcessor:
    """
    Processes user commands and routes them to the appropriate handler.
    """
    
    def __init__(self, assistant):
        """Initialize the command processor with command handlers."""
        self.assistant = assistant
        
        # Initialize command handlers
        self.command_handlers = {
            "app": AppCommands(assistant),
            "system": SystemCommands(assistant),
            "network": NetworkCommands(assistant),
            "utility": UtilityCommands(assistant)
        }
        
        # Built-in commands handled directly by the processor
        self.builtin_commands = {
            "hello": self.handle_hello,
            "hi": self.handle_hello,
            "hey": self.handle_hello,
            "time": self.handle_time,
            "date": self.handle_date,
            "help": self.handle_help,
            "who are you": self.handle_who_are_you,
            "what can you do": self.handle_what_can_you_do,
            "thank you": self.handle_thank_you,
            "thanks": self.handle_thank_you,
            "exit": self.handle_exit,
            "quit": self.handle_exit,
            "stop listening": self.handle_stop_listening
        }
        
        # Command patterns for each category
        self.command_patterns = {
            "app": [
                r"open\s+(?P<app_name>.*)",
                r"launch\s+(?P<app_name>.*)",
                r"start\s+(?P<app_name>.*)",
                r"run\s+(?P<app_name>.*)"
            ],
            "system": [
                r"(shutdown|turn off)\s+(computer|pc|system)",
                r"restart\s+(computer|pc|system)",
                r"lock\s+(computer|pc|system)",
                r"sleep\s+(computer|pc|system)",
                r"hibernate\s+(computer|pc|system)",
                r"log\s?out"
            ],
            "network": [
                r"turn\s+(on|off)\s+(wifi|wireless|bluetooth)",
                r"(show|what is|what's)\s+(my)?\s*(ip address)",
                r"(connect|disconnect)\s+(to|from)\s+(?P<network>.*)"
            ],
            "utility": [
                r"open\s+(control panel|task manager|file explorer)",
                r"(show|list)\s+(running processes|cpu usage|memory usage)",
                r"(set|adjust)\s+volume\s+(to|up|down|mute)"
            ]
        }
    
    def process(self, command_text):
        """
        Process a command and return a response.
        """
        if not command_text:
            return "I didn't catch that. Can you please repeat?"
        
        # Remove the wake word if present
        command_text = self._remove_wake_word(command_text)
        
        # Try built-in commands first
        for key, handler in self.builtin_commands.items():
            if key in command_text.lower():
                return handler(command_text)
        
        # Try to categorize the command
        category, match = self._categorize_command(command_text)
        
        if category and match:
            # Route to the appropriate handler
            return self.command_handlers[category].process(command_text, match)
        
        # If we can't categorize, try a more flexible approach
        # Check for key phrases that might indicate the category
        if any(app_key in command_text.lower() for app_key in ["open", "launch", "start", "run"]):
            return self.command_handlers["app"].process(command_text, None)
            
        if any(sys_key in command_text.lower() for sys_key in ["shutdown", "restart", "lock", "sleep", "hibernate", "log out"]):
            return self.command_handlers["system"].process(command_text, None)
            
        if any(net_key in command_text.lower() for net_key in ["wifi", "wireless", "bluetooth", "ip address", "network"]):
            return self.command_handlers["network"].process(command_text, None)
            
        if any(util_key in command_text.lower() for util_key in ["control panel", "task manager", "file explorer", "processes", "volume"]):
            return self.command_handlers["utility"].process(command_text, None)
        
        # If all else fails
        return f"I'm not sure how to handle '{command_text}'. Try asking for help to see what I can do."
    
    def _remove_wake_word(self, command_text):
        """Remove the wake word from the beginning of the command."""
        wake_word = self.assistant.wake_word.lower()
        if command_text.lower().startswith(wake_word):
            # Remove wake word and any following spaces/commas
            return re.sub(f"^{wake_word}[,\\s]*", "", command_text, flags=re.IGNORECASE).strip()
        return command_text
    
    def _categorize_command(self, command_text):
        """
        Categorize a command based on patterns.
        Returns the category and the match object, or (None, None) if no match.
        """
        command_lower = command_text.lower()
        
        for category, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command_lower, re.IGNORECASE)
                if match:
                    return category, match
        
        return None, None
    
    # Built-in command handlers
    
    def handle_hello(self, command_text):
        """Handle greeting commands."""
        return self.assistant.get_random_greeting()
    
    def handle_time(self, command_text):
        """Handle time requests."""
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."
    
    def handle_date(self, command_text):
        """Handle date requests."""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}."
    
    def handle_help(self, command_text):
        """Handle help requests."""
        return ("I can help you with various tasks. Try commands like:\n"
                "- Open Chrome\n"
                "- What time is it?\n"
                "- Shutdown my computer\n"
                "- Turn off WiFi\n"
                "- Show my IP address\n"
                "- Open Task Manager")
    
    def handle_who_are_you(self, command_text):
        """Handle identity questions."""
        return ("I'm Nova, your personal AI assistant. I'm designed to help you "
                "control your computer, open applications, and provide information through voice commands.")
    
    def handle_what_can_you_do(self, command_text):
        """Handle capability questions."""
        return ("I can help you with various tasks on your computer. I can open applications, "
                "control system functions like shutdown or restart, manage network settings, "
                "and open system utilities. Just tell me what you need!")
    
    def handle_thank_you(self, command_text):
        """Handle thank you messages."""
        responses = [
            "You're welcome!",
            "Happy to help!",
            "No problem at all!",
            "Anytime!",
            "Glad I could assist!"
        ]
        import random
        return random.choice(responses)
    
    def handle_exit(self, command_text):
        """Handle exit commands."""
        self.assistant.stop()
        return "Goodbye! Nova is shutting down."
    
    def handle_stop_listening(self, command_text):
        """Handle stop listening commands."""
        self.assistant.stop()
        return "I'll stop listening now. Call my name if you need me again." 