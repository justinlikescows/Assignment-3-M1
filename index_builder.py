import os
import json
from tokenizer import Tokenizer
from inverted_index import InvertedIndex
from posting import Posting

class IndexBuilder:
    def __init__(self, json_files, partial_threshold=500, partial_index_dir='partial_indexes', final_index_dir='final_index'):
        """
        Initializes the IndexBuilder class with the specified configurations.

        Args:
            json_files (list): A list of paths to JSON files that contain the documents to be indexed.
            partial_threshold (int, optional): The number of documents to process before creating a partial index. Defaults to 500.
            partial_index_dir (str, optional): The directory where partial indexes are stored. Defaults to 'partial_indexes'.
            final_index_dir (str, optional): The directory where the final consolidated index is stored. Defaults to 'final_index'.
        """
        self.json_files = json_files
        self.index = InvertedIndex()
        self.tokenizer = Tokenizer()
        self.partial_threshold = partial_threshold
        self.partial_index_count = 0
        self.partial_index_dir = partial_index_dir
        self.final_index_dir = final_index_dir

        self.unique_token_count = 0
        self.number_of_documents = 0

        # Ensure directories for partial and final indexes exist
        os.makedirs(self.partial_index_dir, exist_ok=True)
        os.makedirs(self.final_index_dir, exist_ok=True)

    def save_partial_index(self):
        """
        Saves the current in-memory index as a partial index file on the disk.
        """
        filename = os.path.join(self.partial_index_dir, f'partial_index_{self.partial_index_count}.json')
        self.index.serialize_to_file(filename)  # Ensure this method is called
        self.partial_index_count += 1
        # Clear the in-memory index
        self.index.index = {}

    def merge_indexes(self, index_files):
        """
        Merges multiple partial index files into a final comprehensive index.

        Args:
            index_files (list): A list of file paths to the partial index files that need to be merged.
        """
        final_index = {}
        for index_file in index_files:
            with open(index_file, 'r') as file:
                partial_index = json.load(file)
                for token, postings in partial_index.items():
                    if token not in final_index.keys():
                        self.unique_token_count += 1
                        final_index[token] = postings
                    else:
                        final_index[token].extend(postings)
        # Save the final index to disk
        final_filename = os.path.join(self.final_index_dir, 'final_index.json')
        with open(final_filename, 'w') as file:
            json.dump(final_index, file)
        print(f"file {self.partial_index_count} Unique tokens after merging: {self.unique_token_count}")
        return final_index

    def build_index(self):
        """
        Builds the inverted index from the provided JSON files, incorporating periodic offloading of partial indexes to disk.
        """
        for doc_id, json_file in enumerate(self.json_files):
            tokens = self.tokenizer.process_html_file(json_file)  # Assume this returns a list of tokens
            for token in tokens:
                self.index.add_posting(token, doc_id)
            self.number_of_documents += 1
            # Offload to disk if the index reaches the partial threshold
            if len(self.index.index) >= self.partial_threshold:
                self.save_partial_index()
        # Final offloading after processing all documents
        self.save_partial_index()
        index_files = [os.path.join(self.partial_index_dir, f'partial_index_{i}.json') for i in range(self.partial_index_count)]
        self.merge_indexes(index_files)
