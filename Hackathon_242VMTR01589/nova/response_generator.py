"""
ResponseGenerator - Generates verbal responses for the assistant.
"""

import random
import json
import os
from datetime import datetime

class ResponseGenerator:
    """
    Generates appropriate verbal responses for the assistant.
    """
    
    def __init__(self, assistant):
        """Initialize the response generator."""
        self.assistant = assistant
        
        # Response templates
        self.success_templates = [
            "Done! {action}.",
            "I've {action} for you.",
            "Task complete. {action}.",
            "That's done. {action}.",
            "All set. {action}."
        ]
        
        self.error_templates = [
            "I'm sorry, I couldn't {action}. {reason}",
            "I encountered an issue while trying to {action}. {reason}",
            "I wasn't able to {action}. {reason}",
            "There was a problem: {reason}",
            "I couldn't complete that task. {reason}"
        ]
        
        self.clarification_templates = [
            "I'm not sure I understood. Did you want to {action}?",
            "Could you clarify if you want me to {action}?",
            "I didn't quite catch that. Do you want me to {action}?",
            "I need more information. Are you asking me to {action}?",
            "To confirm, would you like me to {action}?"
        ]
        
        # Affirmation phrases
        self.affirmations = [
            "I'll do that for you.",
            "Working on it now.",
            "Right away.",
            "Consider it done.",
            "Getting that for you now."
        ]
    
    def generate_success_response(self, action_description):
        """Generate a success response with the given action description."""
        template = random.choice(self.success_templates)
        return template.format(action=action_description)
    
    def generate_error_response(self, action_description, reason=""):
        """Generate an error response with the given action and reason."""
        template = random.choice(self.error_templates)
        return template.format(action=action_description, reason=reason)
    
    def generate_clarification_response(self, action_description):
        """Generate a clarification response with the given action."""
        template = random.choice(self.clarification_templates)
        return template.format(action=action_description)
    
    def generate_affirmation(self):
        """Generate a random affirmation phrase."""
        return random.choice(self.affirmations)
        
    def format_system_status(self, status_dict):
        """Format a system status dictionary into a verbal response."""
        lines = []
        for key, value in status_dict.items():
            # Format the key by replacing underscores with spaces and capitalizing
            formatted_key = key.replace('_', ' ').capitalize()
            lines.append(f"{formatted_key}: {value}")
        
        return ". ".join(lines) + "."
    
    def format_list_items(self, items, intro="Here's what I found:"):
        """Format a list of items into a verbal response."""
        if not items:
            return "I didn't find any items."
        
        if len(items) == 1:
            return f"{intro} {items[0]}."
        
        formatted_items = ", ".join(items[:-1]) + ", and " + items[-1]
        return f"{intro} {formatted_items}."
    
    def format_time_duration(self, seconds):
        """Format seconds into a human-readable time duration."""
        if seconds < 60:
            return f"{seconds} second{'s' if seconds != 1 else ''}"
        
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        
        hours = minutes // 60
        minutes %= 60
        
        if minutes == 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        return f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"