"""
SearchCommands - Handles commands related to web searches.
"""

import webbrowser
import urllib.parse
import requests
from bs4 import BeautifulSoup

class SearchCommands:
    """
    Handles commands related to web searches (Google, etc).
    """
    
    def __init__(self, assistant):
        """Initialize the search commands handler."""
        self.assistant = assistant
        
    def process(self, command_text, match=None):
        """
        Process search-related commands.
        Returns a response string.
        """
        # Extract the search query
        search_query = self._extract_search_query(command_text)
        
        if not search_query:
            return "I'm not sure what you want me to search for. Can you please be more specific?"
        
        # Perform the search
        result = self.search_google(search_query)
        
        if result:
            return result
        else:
            # If we couldn't get a direct answer, just open the browser with the search
            self.open_browser_search(search_query)
            return f"I've opened a Google search for '{search_query}'."
    
    def _extract_search_query(self, command_text):
        """Extract the search query from the command text."""
        # List of common search prefixes
        search_prefixes = [
            "search for",
            "search",
            "google",
            "look up",
            "find information about",
            "find info on",
            "find information on",
            "who is",
            "what is",
            "where is",
            "when is",
            "why is",
            "how to"
        ]
        
        command_lower = command_text.lower()
        
        # Try each prefix and see if it's in the command
        for prefix in search_prefixes:
            if prefix in command_lower:
                # Extract everything after the prefix
                query_parts = command_lower.split(prefix, 1)
                if len(query_parts) > 1 and query_parts[1].strip():
                    return query_parts[1].strip()
        
        # If no specific prefix is found, but the command seems like a search query
        # (e.g., "nova, prime minister of india")
        if "who" in command_lower or "what" in command_lower or "where" in command_lower or \
           "when" in command_lower or "why" in command_lower or "how" in command_lower:
            return command_lower
        
        # If still no match, and it doesn't look like any other type of command,
        # assume the entire text after the wake word is the search query
        return command_lower
    
    def open_browser_search(self, query):
        """Open a web browser with the given search query."""
        # URL encode the query
        encoded_query = urllib.parse.quote_plus(query)
        
        # Build the Google search URL
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        # Open the URL in the default browser
        webbrowser.open(search_url)
        
        return True
    
    def search_google(self, query):
        """
        Perform a Google search and try to extract a direct answer.
        Returns a string with the answer or None if no direct answer is found.
        """
        try:
            # URL encode the query
            encoded_query = urllib.parse.quote_plus(query)
            
            # Create the search URL
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            # Set a user agent to mimic a browser
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            # Send the request
            response = requests.get(search_url, headers=headers, timeout=5)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try to extract the Google Featured Snippet (direct answer)
                # This is just a simple example; actual implementation might need more sophistication
                featured_snippet = soup.select_one('.kp-header')
                if featured_snippet:
                    answer = featured_snippet.get_text().strip()
                    return f"According to Google: {answer}"
                
                # Try to extract the "People also ask" questions and answers
                paa_questions = soup.select('.related-question-pair')
                if paa_questions and len(paa_questions) > 0:
                    for question in paa_questions[:1]:  # Just get the first one
                        answer_text = question.get_text().strip()
                        if answer_text:
                            return f"I found this related information: {answer_text}"
                
                # If no featured snippet or PAA, try to get the first search result
                first_result = soup.select_one('.g .yuRUbf')
                if first_result:
                    title_element = first_result.select_one('h3')
                    link_element = first_result.select_one('a')
                    snippet_element = soup.select_one('.g .IsZvec')
                    
                    if title_element and link_element and snippet_element:
                        title = title_element.get_text().strip()
                        link = link_element.get('href', '')
                        snippet = snippet_element.get_text().strip()
                        
                        return f"Here's what I found: {title}\n{snippet}\n\nI've opened the web page for more information."
            
            # If we couldn't extract a direct answer, return None
            # This will cause the function caller to open a browser search instead
            return None
                
        except Exception as e:
            print(f"Error in search_google: {str(e)}")
            return None 