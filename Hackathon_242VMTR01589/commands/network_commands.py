"""
NetworkCommands - Handles commands related to network operations like WiFi, Bluetooth, etc.
"""

import os
import subprocess
import re
import socket
import platform
import sys

class NetworkCommands:
    """
    Handles commands related to network operations.
    """
    
    def __init__(self, assistant):
        """Initialize the network commands handler."""
        self.assistant = assistant
        
        # Command patterns and their handlers
        self.command_patterns = {
            r"turn\s+(on|off)\s+(wifi|wireless)": self._toggle_wifi,
            r"turn\s+(on|off)\s+bluetooth": self._toggle_bluetooth,
            r"(show|what is|what's)\s+(my)?\s*(ip address)": self._show_ip_address,
            r"(connect|disconnect)\s+(to|from)\s+(?P<network>.*)": self._manage_network_connection
        }
    
    def process(self, command_text, match=None):
        """
        Process network-related commands.
        Returns a response string.
        """
        command_lower = command_text.lower()
        
        # If match is provided, use it to determine the command
        if match:
            for pattern, handler in self.command_patterns.items():
                if re.match(pattern, match.group(0), re.IGNORECASE):
                    return handler(command_text, match)
        
        # Otherwise, try to match the command
        for pattern, handler in self.command_patterns.items():
            match = re.search(pattern, command_lower, re.IGNORECASE)
            if match:
                return handler(command_text, match)
        
        # Check for specific keywords if no pattern matches
        if "wifi" in command_lower or "wireless" in command_lower:
            # Try to determine if it's on or off
            if "on" in command_lower:
                return self._toggle_wifi(command_text, None, turn_on=True)
            elif "off" in command_lower:
                return self._toggle_wifi(command_text, None, turn_on=False)
            else:
                return "Would you like me to turn WiFi on or off?"
                
        elif "bluetooth" in command_lower:
            # Try to determine if it's on or off
            if "on" in command_lower:
                return self._toggle_bluetooth(command_text, None, turn_on=True)
            elif "off" in command_lower:
                return self._toggle_bluetooth(command_text, None, turn_on=False)
            else:
                return "Would you like me to turn Bluetooth on or off?"
                
        elif "ip" in command_lower or "ip address" in command_lower:
            return self._show_ip_address(command_text, None)
            
        elif "connect" in command_lower or "disconnect" in command_lower:
            return "Please specify the network name you want to connect to or disconnect from."
        
        # If no command is recognized
        return "I'm not sure which network command you want to execute. " \
               "Try saying 'turn on WiFi', 'turn off Bluetooth', or 'show my IP address'."
    
    def _toggle_wifi(self, command_text, match, turn_on=None):
        """Toggle WiFi on or off."""
        # Determine if we should turn on or off
        if turn_on is None:
            if match:
                action = match.group(1).lower()
                turn_on = (action == "on")
            else:
                # Try to extract from command text
                turn_on = "on" in command_text.lower() and not "off" in command_text.lower()
        
        try:
            if os.name == 'nt':  # Windows
                if turn_on:
                    # Turn WiFi on using netsh
                    subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"], 
                                  capture_output=True, text=True, check=True)
                    return "WiFi has been turned on."
                else:
                    # Turn WiFi off using netsh
                    subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "disabled"], 
                                  capture_output=True, text=True, check=True)
                    return "WiFi has been turned off."
            else:
                # This is not implemented for non-Windows systems
                return "I'm sorry, WiFi control is currently only implemented for Windows."
                
        except subprocess.CalledProcessError as e:
            return f"I couldn't toggle WiFi. Error: {e.stderr}"
        except Exception as e:
            return f"I couldn't toggle WiFi. Error: {str(e)}"
    
    def _toggle_bluetooth(self, command_text, match, turn_on=None):
        """Toggle Bluetooth on or off."""
        # Determine if we should turn on or off
        if turn_on is None:
            if match:
                action = match.group(1).lower()
                turn_on = (action == "on")
            else:
                # Try to extract from command text
                turn_on = "on" in command_text.lower() and not "off" in command_text.lower()
        
        try:
            if os.name == 'nt':  # Windows
                return f"I'm sorry, Bluetooth control is not fully implemented yet. Would {turn_on and 'enable' or 'disable'} Bluetooth if I could."
            else:
                # Not implemented for non-Windows systems
                return "I'm sorry, Bluetooth control is currently only implemented for Windows."
                
        except Exception as e:
            return f"I couldn't toggle Bluetooth. Error: {str(e)}"
    
    def _show_ip_address(self, command_text, match):
        """Show the user's IP address(es)."""
        try:
            # Get local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # Doesn't have to be reachable
                s.connect(('10.255.255.255', 1))
                local_ip = s.getsockname()[0]
            except Exception:
                local_ip = '127.0.0.1'
            finally:
                s.close()
            
            # Get hostname
            hostname = socket.gethostname()
            
            # Try to get public IP (this won't work without internet)
            public_ip = "Could not determine"
            try:
                import requests
                response = requests.get('https://api.ipify.org', timeout=3)
                if response.status_code == 200:
                    public_ip = response.text
            except:
                pass
            
            return f"Your local IP address is {local_ip}. Your hostname is {hostname}. Your public IP address is {public_ip}."
            
        except Exception as e:
            return f"I couldn't show your IP address. Error: {str(e)}"
    
    def _manage_network_connection(self, command_text, match):
        """Connect to or disconnect from a network."""
        try:
            # Determine if we're connecting or disconnecting
            is_connect = "connect" in command_text.lower() and not "disconnect" in command_text.lower()
            
            # Extract network name
            network_name = None
            if match and 'network' in match.groupdict():
                network_name = match.group('network').strip()
            else:
                # Try to extract from command
                command_parts = command_text.lower().split()
                if "to" in command_parts:
                    to_index = command_parts.index("to")
                    if to_index + 1 < len(command_parts):
                        network_name = " ".join(command_parts[to_index + 1:])
                elif "from" in command_parts:
                    from_index = command_parts.index("from")
                    if from_index + 1 < len(command_parts):
                        network_name = " ".join(command_parts[from_index + 1:])
            
            if not network_name:
                return "I didn't catch which network you want to connect to. Please specify the network name."
            
            # Remove any punctuation at the end
            network_name = re.sub(r'[.,;!?]$', '', network_name)
            
            if os.name == 'nt':  # Windows
                if is_connect:
                    # Connect to WiFi network
                    subprocess.run(["netsh", "wlan", "connect", "name=" + network_name], 
                                  capture_output=True, text=True, check=True)
                    return f"Connected to {network_name}."
                else:
                    # Disconnect from WiFi network
                    subprocess.run(["netsh", "wlan", "disconnect"], 
                                  capture_output=True, text=True, check=True)
                    return f"Disconnected from the current network."
            else:
                # Not implemented for non-Windows systems
                return "I'm sorry, network connection management is currently only implemented for Windows."
                
        except subprocess.CalledProcessError as e:
            return f"I couldn't manage the network connection. Error: {e.stderr}"
        except Exception as e:
            return f"I couldn't manage the network connection. Error: {str(e)}"
            
    def _get_network_status(self):
        """Get the status of network interfaces."""
        try:
            if os.name == 'nt':  # Windows
                # Get WiFi status
                wifi_status = subprocess.run(["netsh", "wlan", "show", "interfaces"], 
                                           capture_output=True, text=True, check=True)
                
                # Get network interfaces
                net_status = subprocess.run(["ipconfig", "/all"], 
                                          capture_output=True, text=True, check=True)
                
                # Parse the output to extract the relevant information
                # This would be more complex in a real implementation
                
                return "Network status retrieved. For detailed information, I'd need to parse the command output."
            else:
                # Not implemented for non-Windows systems
                return "I'm sorry, network status retrieval is currently only implemented for Windows."
                
        except subprocess.CalledProcessError as e:
            return f"I couldn't get network status. Error: {e.stderr}"
        except Exception as e:
            return f"I couldn't get network status. Error: {str(e)}" 