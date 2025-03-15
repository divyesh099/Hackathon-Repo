"""
System information utilities for the Nova assistant.
"""

import os
import sys
import platform
import socket
import psutil
import datetime
import uuid
import time

def get_system_info():
    """
    Get comprehensive system information.
    Returns a dictionary of system information.
    """
    info = {}
    
    # OS Information
    info["os_name"] = platform.system()
    info["os_version"] = platform.version()
    info["os_release"] = platform.release()
    
    # CPU Information
    info["cpu_count"] = psutil.cpu_count(logical=False)
    info["cpu_logical_count"] = psutil.cpu_count(logical=True)
    info["cpu_percent"] = psutil.cpu_percent(interval=1)
    
    # Memory Information
    memory = psutil.virtual_memory()
    info["memory_total"] = format_bytes(memory.total)
    info["memory_available"] = format_bytes(memory.available)
    info["memory_used"] = format_bytes(memory.used)
    info["memory_percent"] = memory.percent
    
    # Disk Information
    disk = psutil.disk_usage('/')
    info["disk_total"] = format_bytes(disk.total)
    info["disk_free"] = format_bytes(disk.free)
    info["disk_used"] = format_bytes(disk.used)
    info["disk_percent"] = disk.percent
    
    # Network Information
    info["hostname"] = socket.gethostname()
    try:
        info["ip_address"] = socket.gethostbyname(socket.gethostname())
    except:
        info["ip_address"] = "127.0.0.1"
    
    # Machine Information
    info["machine_type"] = platform.machine()
    info["processor"] = platform.processor()
    
    # System Uptime
    uptime_seconds = int(time.time() - psutil.boot_time())
    info["system_uptime"] = format_time_delta(uptime_seconds)
    
    # User Information
    info["user"] = os.getlogin()
    
    return info

def get_battery_status():
    """
    Get battery status information.
    Returns a dictionary of battery information, or None if no battery is present.
    """
    if not hasattr(psutil, "sensors_battery") or psutil.sensors_battery() is None:
        return None
    
    battery = psutil.sensors_battery()
    info = {}
    
    info["percent"] = battery.percent
    info["power_plugged"] = battery.power_plugged
    info["charging"] = "Yes" if battery.power_plugged else "No"
    
    # Estimated time remaining (if discharging)
    if battery.secsleft != -1 and not battery.power_plugged:
        info["time_left"] = format_time_delta(battery.secsleft)
    else:
        info["time_left"] = "N/A"
    
    return info

def get_network_connections():
    """
    Get information about network connections.
    Returns a list of dictionaries with connection information.
    """
    connections = []
    
    for conn in psutil.net_connections(kind='inet'):
        connection_info = {}
        
        if conn.laddr:
            connection_info["local_address"] = f"{conn.laddr.ip}:{conn.laddr.port}"
        
        if conn.raddr:
            connection_info["remote_address"] = f"{conn.raddr.ip}:{conn.raddr.port}"
        
        connection_info["status"] = conn.status
        
        try:
            connection_info["process"] = psutil.Process(conn.pid).name() if conn.pid else "Unknown"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            connection_info["process"] = "Access Denied"
        
        connections.append(connection_info)
    
    return connections

def format_bytes(bytes_value):
    """Format bytes into a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"

def format_time_delta(seconds):
    """Format seconds into a human-readable time string."""
    if seconds < 60:
        return f"{seconds} seconds"
    
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} minutes, {seconds} seconds"
    
    hours, minutes = divmod(minutes, 60)
    if hours < 24:
        return f"{hours} hours, {minutes} minutes"
    
    days, hours = divmod(hours, 24)
    return f"{days} days, {hours} hours, {minutes} minutes"

def get_mac_address():
    """Get the MAC address of the machine."""
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                   for elements in range(0, 2*6, 8)][::-1])
    return mac

def get_public_ip():
    """Get the public IP address of the machine."""
    try:
        import requests
        response = requests.get('https://api.ipify.org', timeout=3)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return "Could not determine" 