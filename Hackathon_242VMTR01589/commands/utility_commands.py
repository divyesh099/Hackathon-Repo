"""
UtilityCommands - Handles commands related to system utilities like Control Panel, Task Manager, etc.
"""

import os
import subprocess
import re
import sys
import psutil

class UtilityCommands:
    """
    Handles commands related to system utilities.
    """
    
    def __init__(self, assistant):
        """Initialize the utility commands handler."""
        self.assistant = assistant
        
        # Command patterns and their handlers
        self.command_patterns = {
            r"open\s+control\s*panel": self._open_control_panel,
            r"open\s+task\s*manager": self._open_task_manager,
            r"open\s+file\s*explorer": self._open_file_explorer,
            r"(show|list)\s+running\s*processes": self._list_processes,
            r"(show|display)\s+cpu\s*usage": self._show_cpu_usage,
            r"(show|display)\s+memory\s*usage": self._show_memory_usage,
            r"(set|adjust)\s+volume\s+(to|up|down|mute)": self._adjust_volume
        }
        
        # Utility mappings
        self.utility_mappings = {
            "control panel": {
                "command": "control",
                "description": "Control Panel"
            },
            "task manager": {
                "command": "taskmgr",
                "description": "Task Manager"
            },
            "file explorer": {
                "command": "explorer",
                "description": "File Explorer"
            },
            "settings": {
                "command": "ms-settings:",
                "description": "Windows Settings"
            },
            "device manager": {
                "command": "devmgmt.msc",
                "description": "Device Manager"
            },
            "disk management": {
                "command": "diskmgmt.msc",
                "description": "Disk Management"
            },
            "command prompt": {
                "command": "cmd",
                "description": "Command Prompt"
            },
            "powershell": {
                "command": "powershell",
                "description": "PowerShell"
            }
        }
    
    def process(self, command_text, match=None):
        """
        Process utility-related commands.
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
        
        # Check for utility keywords
        for utility_name, utility_info in self.utility_mappings.items():
            if utility_name in command_lower:
                if "open" in command_lower:
                    return self._open_utility(utility_info["command"], utility_info["description"])
        
        # Check for specific keywords if no pattern matches
        if "control panel" in command_lower:
            return self._open_control_panel(command_text)
        elif "task manager" in command_lower:
            return self._open_task_manager(command_text)
        elif "file explorer" in command_lower:
            return self._open_file_explorer(command_text)
        elif "processes" in command_lower:
            return self._list_processes(command_text)
        elif "cpu" in command_lower and ("usage" in command_lower or "load" in command_lower):
            return self._show_cpu_usage(command_text)
        elif "memory" in command_lower and ("usage" in command_lower or "load" in command_lower):
            return self._show_memory_usage(command_text)
        elif "volume" in command_lower:
            return self._adjust_volume(command_text)
        
        # If no command is recognized
        return "I'm not sure which utility command you want to execute. " \
               "Try saying 'open Control Panel', 'open Task Manager', or 'show CPU usage'."
    
    def _open_utility(self, command, description):
        """Open a utility using the specified command."""
        try:
            subprocess.Popen(command, shell=True)
            return f"Opening {description}."
        except Exception as e:
            return f"I couldn't open {description}. Error: {str(e)}"
    
    def _open_control_panel(self, command_text):
        """Open the Control Panel."""
        return self._open_utility("control", "Control Panel")
    
    def _open_task_manager(self, command_text):
        """Open the Task Manager."""
        return self._open_utility("taskmgr", "Task Manager")
    
    def _open_file_explorer(self, command_text):
        """Open File Explorer."""
        return self._open_utility("explorer", "File Explorer")
    
    def _list_processes(self, command_text):
        """List running processes."""
        try:
            # Get the top processes by CPU usage
            processes = []
            for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                              key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:10]:
                try:
                    processes.append(f"{proc.info['name']} (PID: {proc.info['pid']}, CPU: {proc.info['cpu_percent']}%)")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # Format response
            if processes:
                return "Here are the top processes by CPU usage: " + "; ".join(processes)
            else:
                return "I couldn't retrieve the process list."
                
        except Exception as e:
            return f"I couldn't list the processes. Error: {str(e)}"
    
    def _show_cpu_usage(self, command_text):
        """Show CPU usage."""
        try:
            # Get overall CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Get per-core usage
            per_cpu = psutil.cpu_percent(interval=1, percpu=True)
            
            # Format response
            response = f"Current CPU usage is {cpu_percent}% overall. "
            response += "Per-core usage: " + ", ".join([f"Core {i}: {usage}%" for i, usage in enumerate(per_cpu)])
            
            return response
            
        except Exception as e:
            return f"I couldn't retrieve CPU usage. Error: {str(e)}"
    
    def _show_memory_usage(self, command_text):
        """Show memory usage."""
        try:
            # Get memory usage
            mem = psutil.virtual_memory()
            
            # Calculate used memory in GB
            total_gb = mem.total / (1024 ** 3)
            used_gb = mem.used / (1024 ** 3)
            
            # Format response
            response = f"Memory usage: {mem.percent}%. "
            response += f"Using {used_gb:.2f} GB out of {total_gb:.2f} GB."
            
            return response
            
        except Exception as e:
            return f"I couldn't retrieve memory usage. Error: {str(e)}"
    
    def _adjust_volume(self, command_text):
        """Adjust system volume."""
        try:
            # Determine the volume action
            command_lower = command_text.lower()
            
            if "mute" in command_lower:
                # Mute volume
                if os.name == 'nt':  # Windows
                    subprocess.run(["powershell", "-c", "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"], 
                                  check=True, capture_output=True)
                    return "I've muted the volume."
            elif "up" in command_lower:
                # Increase volume
                if os.name == 'nt':  # Windows
                    # Increase volume multiple times for a more noticeable effect
                    for _ in range(5):
                        subprocess.run(["powershell", "-c", "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"], 
                                      check=True, capture_output=True)
                    return "I've increased the volume."
            elif "down" in command_lower:
                # Decrease volume
                if os.name == 'nt':  # Windows
                    # Decrease volume multiple times for a more noticeable effect
                    for _ in range(5):
                        subprocess.run(["powershell", "-c", "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"], 
                                      check=True, capture_output=True)
                    return "I've decreased the volume."
            elif "to" in command_lower:
                # Try to set volume to a specific level (requires additional parsing)
                # This is not fully implemented in this basic version
                return "I'm sorry, setting volume to a specific level is not yet implemented."
            
            # If no specific action is recognized
            return "I'm not sure how you want me to adjust the volume. Try saying 'volume up', 'volume down', or 'mute'."
            
        except Exception as e:
            return f"I couldn't adjust the volume. Error: {str(e)}" 