from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import json


class Tokenizer:
    def __init__(self):
        """
        Initializes the Tokenizer with a Porter Stemmer.
        """
        self.stemmer = PorterStemmer()

    def parse_html(self, html_content):
        """
        Extracts all text from HTML content.

        Args:
            html_content (str): HTML content from which to extract text.

        Returns:
            str: The textual content extracted from the HTML, with elements separated by spaces.

        """
        # Extract alphanumeric tokens
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ')
        return text
    
    def tokenize(self, text):
        """
        Splits text into alphanumeric tokens using regular expressions.

        Args:
            text (str): The text to tokenize.

        Returns:
            list: A list of lowercase, alphanumeric tokens extracted from the input text.
        """
        return re.findall(r'\b\w+\b', text.lower())
    
    def stem(self, token):
        """
        Reduces a token to its stem using a Porter Stemmer.

        Args:
            token (str): The token to stem.

        Returns:
            str: The stemmed version of the token.
        """
        return self.stemmer.stem(token)
    
    def process_html_file(self, json_file):
        """
        Processes an HTML file from a JSON source to extract, tokenize, and stem its content.

        Args:
            json_file (str): The file path to the JSON file containing the HTML content.

        Returns:
            list: A list of stemmed tokens extracted from the HTML content within the JSON file.

        """
        with open(json_file, 'r') as file:
            data = json.load(file)
        html_content = data.get('content', '')
        raw_text = self.parse_html(html_content)
        tokens = self.tokenize(raw_text)
        return [self.stem(token) for token in tokens]
