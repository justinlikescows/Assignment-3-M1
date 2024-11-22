import os
import json
import re
from collections import defaultdict
import html
class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)
        self.documents = {}
    
    def add_document(self, doc_id, content):
        words = self.tokenize(content)
        term_freq = defaultdict(int)
        for word in words:
            term_freq[word] += 1
        self.documents[doc_id] = len(words)
        for word, freq in term_freq.items():
            self.index[word].append({'doc_id': doc_id, 'term_frequency': freq})

    def tokenize(self, text):
        text = html.unescape(text)  # Handle HTML entities
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        words = re.findall(r'\b\w+\b', text.lower())  # Extract words
        return words
    
    def save_index(self, filepath):
        with open(filepath, 'w') as f:
            json.dump({'index': self.index, 'documents': self.documents}, f)
    
    def load_index(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.index = defaultdict(list, data['index'])
            self.documents = data['documents']

def build_inverted_index(root_dir):
    inverted_index = InvertedIndex()
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    print(f'Opened {file_path}')
                    data = json.load(f)
                    doc_id = os.path.relpath(file_path, root_dir)
                    content = data.get('content', '')
                    inverted_index.add_document(doc_id, content)
                    print(f'Closed {file_path}')

    return inverted_index
