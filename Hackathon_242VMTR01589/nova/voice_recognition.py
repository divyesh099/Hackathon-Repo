"""
VoiceRecognizer - Handles voice input and wake word detection.
"""

import os
import time
import threading
import queue
from collections import deque

import speech_recognition as sr

class VoiceRecognizer:
    """
    Handles voice recognition and wake word detection.
    """
    
    def __init__(self, assistant):
        """Initialize the voice recognizer."""
        self.assistant = assistant
        self.recognizer = sr.Recognizer()
        
        # Adjust for ambient noise level
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000  # Default value, will be adjusted
        self.recognizer.pause_threshold = 0.8    # Shorter pause detection
        self.recognizer.phrase_threshold = 0.3   # More sensitive phrase detection
        
        # Wake word (lowercase)
        self.wake_word = "nova"
        
        # Alternative wake words (e.g., "hey nova", "hi nova")
        self.alternative_wake_words = ["hey nova", "hi nova", "hello nova", "hey nowa", "hi nowa"]
        
        # Recent audio buffer for wake word detection
        self.audio_buffer = deque(maxlen=5)  # Keep last 5 seconds
        
        # Error counters
        self.consecutive_errors = 0
        self.max_consecutive_errors = 3
    
    def listen_for_audio(self, timeout=None):
        """Listen for audio input from the microphone."""
        with sr.Microphone() as source:
            try:
                # Adjust for ambient noise
                if self.consecutive_errors > self.max_consecutive_errors:
                    print("Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    self.consecutive_errors = 0
                    
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                return audio
                
            except sr.WaitTimeoutError:
                print("Listening timed out, no speech detected")
                return None
                
            except Exception as e:
                print(f"Error listening for audio: {e}")
                self.consecutive_errors += 1
                return None
    
    def recognize_speech(self, audio):
        """
        Convert audio to text using speech recognition.
        Returns the recognized text or None if recognition fails.
        """
        if not audio:
            return None
            
        try:
            # Try Google's speech recognition service
            text = self.recognizer.recognize_google(audio)
            self.consecutive_errors = 0  # Reset error counter on success
            return text.lower()  # Return lowercase text
            
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
            
        except sr.RequestError as e:
            print(f"Recognition service error: {e}")
            self.consecutive_errors += 1
            return None
            
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            self.consecutive_errors += 1
            return None
    
    def detect_wake_word(self, timeout=None):
        """
        Listen for the wake word.
        Returns True if the wake word is detected, False otherwise.
        """
        # Listen for audio
        audio = self.listen_for_audio(timeout)
        if not audio:
            return False
            
        # Recognize speech
        text = self.recognize_speech(audio)
        if not text:
            return False
        
        print(f"Heard: {text}")
            
        # Check if the wake word is in the recognized text
        text_lower = text.lower()
        
        # Check for the main wake word
        if self.wake_word in text_lower:
            return True
            
        # Check for alternative wake phrases
        for phrase in self.alternative_wake_words:
            if phrase in text_lower:
                return True
        
        return False
    
    def listen_for_command(self, timeout=5):
        """
        Listen for a command after the wake word is detected.
        Returns the command text or None if no command is recognized.
        """
        # Provide visual and audio feedback that wake word was detected
        self.assistant.on_wake_word_detected()
        
        # Listen for audio
        audio = self.listen_for_audio(timeout)
        if not audio:
            return None
            
        # Recognize speech
        return self.recognize_speech(audio)
        
    def detect_wake_word_and_command(self, timeout=None):
        """
        Listen for the wake word and the command in the same utterance.
        Returns the command part if the wake word is detected at the beginning,
        or None if no wake word is detected or no command follows.
        """
        # Listen for audio
        audio = self.listen_for_audio(timeout)
        if not audio:
            return None
            
        # Recognize speech
        text = self.recognize_speech(audio)
        if not text:
            return None
            
        text_lower = text.lower()
        print(f"Heard full phrase: {text_lower}")
        
        # Check if the text starts with the wake word
        if text_lower.startswith(self.wake_word):
            # Extract the command part (everything after the wake word)
            command = text_lower[len(self.wake_word):].strip()
            if command:
                return command
                
        # Check if the text starts with any alternative wake phrases
        for phrase in self.alternative_wake_words:
            if text_lower.startswith(phrase):
                # Extract the command part (everything after the wake phrase)
                command = text_lower[len(phrase):].strip()
                if command:
                    return command
        
        # If we detected just the wake word without a command, return None
        # This will trigger the system to listen for a follow-up command
        self.assistant.on_wake_word_detected()
        return None 