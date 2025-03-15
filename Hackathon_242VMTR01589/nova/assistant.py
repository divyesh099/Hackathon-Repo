"""
NovaAssistant - Core assistant class that handles voice recognition,
command processing, and response generation.
"""

import os
import sys
import time
import threading
import queue
import json
import random
from datetime import datetime

import speech_recognition as sr
import pyttsx3

from nova.voice_recognition import VoiceRecognizer
from nova.command_processor import CommandProcessor
from nova.response_generator import ResponseGenerator

class NovaAssistant:
    """
    Main assistant class that coordinates all Nova functionality.
    """
    
    def __init__(self):
        """Initialize the Nova assistant with all required components."""
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Set voice properties
        voices = self.engine.getProperty('voices')
        # Try to find a female voice
        female_voice = next((voice for voice in voices if 'female' in voice.name.lower()), None)
        if female_voice:
            self.engine.setProperty('voice', female_voice.id)
        
        # Set speech rate and volume
        self.engine.setProperty('rate', 180)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Initialize components
        self.recognizer = VoiceRecognizer(self)
        self.command_processor = CommandProcessor(self)
        self.response_generator = ResponseGenerator(self)
        
        # Status flags
        self.is_listening = False
        self.is_processing = False
        self.is_speaking = False
        self.wake_word_detected = False
        
        # Command queue for processing
        self.command_queue = queue.Queue()
        
        # Greeting messages
        self.greetings = [
            "Hello! I'm Nova, your virtual assistant.",
            "Hi there! Nova at your service.",
            "Greetings! Nova is ready to assist you.",
            "Hello! Nova is listening.",
            "Hi! I'm Nova, how can I help you today?"
        ]
        
        # Wake word acknowledgments
        self.wake_word_responses = [
            "Yes?",
            "I'm listening",
            "How can I help?",
            "What can I do for you?",
            "I'm here"
        ]
        
        # Wake word
        self.wake_word = "nova"
        
        # Start listening thread
        self.listening_thread = None
        self.stop_listening = threading.Event()
    
    def start(self):
        """Start the assistant services."""
        if self.listening_thread is None or not self.listening_thread.is_alive():
            self.stop_listening.clear()
            self.listening_thread = threading.Thread(target=self.listen_continuously)
            self.listening_thread.daemon = True
            self.listening_thread.start()
            
    def stop(self):
        """Stop the assistant services."""
        if self.listening_thread and self.listening_thread.is_alive():
            self.stop_listening.set()
            self.listening_thread.join(timeout=2.0)
    
    def listen_continuously(self):
        """Listen continuously for the wake word followed by commands."""
        while not self.stop_listening.is_set():
            try:
                # Listen for the wake word
                print("Listening for wake word...")
                
                # Try to detect wake word and command in the same utterance
                command = self.recognizer.detect_wake_word_and_command()
                
                if command and not self.stop_listening.is_set():
                    # If we got both wake word and command, process it directly
                    print(f"Recognized wake word and command: {command}")
                    self.process_command(command)
                    continue
                
                # Otherwise, listen for wake word only
                wake_word_detected = self.recognizer.detect_wake_word()
                
                if wake_word_detected and not self.stop_listening.is_set():
                    # Wake word was detected, now listen for the command
                    self.is_listening = True
                    self.wake_word_detected = True
                    
                    # Notify UI or any observers
                    self.on_listening_started()
                    
                    # Provide feedback that we heard the wake word
                    self.on_wake_word_detected()
                    
                    # Listen for the command
                    print("Listening for command...")
                    command = self.recognizer.listen_for_command()
                    
                    if command:
                        print(f"Recognized: {command}")
                        self.process_command(command)
                    
                    # Done listening
                    self.is_listening = False
                    self.wake_word_detected = False
                    self.on_listening_stopped()
            
            except Exception as e:
                print(f"Error in listen_continuously: {e}")
                time.sleep(1)  # Prevent tight loop on error
    
    def process_command(self, command_text):
        """Process a recognized command."""
        self.is_processing = True
        self.on_processing_started()
        
        try:
            # Queue the command for processing
            self.command_queue.put(command_text)
            
            # Process the command
            response = self.command_processor.process(command_text)
            
            # Generate a response
            if response:
                self.speak(response)
            
        except Exception as e:
            print(f"Error processing command: {e}")
            self.speak("I'm sorry, I encountered an error while processing your request.")
        
        finally:
            self.is_processing = False
            self.on_processing_stopped()
    
    def speak(self, text):
        """Convert text to speech and speak it."""
        if not text:
            return
            
        self.is_speaking = True
        self.on_speaking_started(text)
        
        # Speak in a separate thread to avoid blocking
        def speak_thread():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Error in speak: {e}")
            finally:
                self.is_speaking = False
                self.on_speaking_stopped()
        
        threading.Thread(target=speak_thread).start()
    
    def get_random_greeting(self):
        """Return a random greeting message."""
        return random.choice(self.greetings)
    
    def get_random_wake_word_response(self):
        """Return a random wake word acknowledgment."""
        return random.choice(self.wake_word_responses)
    
    def on_wake_word_detected(self):
        """Called when the wake word is detected."""
        self.wake_word_detected = True
        # Play a soft sound or speak a brief response
        wake_response = self.get_random_wake_word_response()
        self.speak(wake_response)
        # This is where the UI would show the waving animation
        pass
    
    # Event callbacks for UI updates
    def on_listening_started(self):
        """Called when the assistant starts listening."""
        pass
    
    def on_listening_stopped(self):
        """Called when the assistant stops listening."""
        pass
    
    def on_processing_started(self):
        """Called when the assistant starts processing a command."""
        pass
    
    def on_processing_stopped(self):
        """Called when the assistant finishes processing a command."""
        pass
    
    def on_speaking_started(self, text):
        """Called when the assistant starts speaking."""
        pass
    
    def on_speaking_stopped(self):
        """Called when the assistant stops speaking."""
        pass 