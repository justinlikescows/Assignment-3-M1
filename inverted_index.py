from posting import Posting 
class InvertedIndex:
    def __init__(self):
        self.index = {}

    def add_posting(self, token, doc_id):
        """
        Adds a posting to the inverted index for a specific token and document ID.

        Args:
            token (str): The token for which the posting needs to be added or updated.
            doc_id (int): The document ID where the token was found.
        """
        if token not in self.index:
            self.index[token] = []
        posting = next((p for p in self.index[token] if p.doc_id == doc_id), None)
        if posting:
            posting.term_freq += 1  # Increment term frequency
        else:
            new_posting = Posting(doc_id, term_freq=1)
            self.index[token].append(new_posting)

    def serialize_to_file(self, filename):
        """
        Serializes the entire inverted index to a JSON file.

        Args:
            filename (str): The name of the file where the index should be saved.

        """
        import json
        # Convert Posting objects to a serializable format
        serializable_index = {
            token: [
                {'doc_id': p.doc_id, 'term_freq': p.term_freq}
                for p in postings
            ]
            for token, postings in self.index.items()
        }
        with open(filename, 'w') as file:
            json.dump(serializable_index, file)
