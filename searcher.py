import streamlit as st
import json
from collections import defaultdict
import time  # Import the time module
import os

class Searcher:
    def __init__(self, index_file):
        self.index = self.load_index(index_file)
        self.document_urls = self.index['documents']  # Mapping of document IDs to their URLs

    def load_index(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)

    def search(self, query):
        """
        Perform an AND search on the query.
        Returns the top 5 document URLs containing all query terms.
        """
        start_time = time.time()  # Record start time

        query_terms = query.lower().split()  # Split query into terms
        postings_lists = [self.index['index'].get(term, []) for term in query_terms]

        if not all(postings_lists):  # If any term has no postings, return empty result
            end_time = time.time()  # Record end time
            print(f"Search took {round((end_time - start_time) * 1000, 2)} ms")
            return []

        # Intersect postings lists to get documents containing all query terms
        doc_ids = set(post['doc_id'] for post in postings_lists[0])
        for postings in postings_lists[1:]:
            doc_ids &= set(post['doc_id'] for post in postings)

        # Collect results with term frequency for sorting
        results = [
            {
                'doc_id': doc_id,
                'term_frequency': sum(
                    post['term_frequency'] for post in postings if post['doc_id'] == doc_id
                )
            }
            for doc_id in doc_ids
            for postings in postings_lists
        ]

        # Sort results by term frequency (descending) and get top 5
        sorted_results = sorted(results, key=lambda x: x['term_frequency'], reverse=True)[:5]

        # Map doc_id to URLs
        top_5_file_paths = [result['doc_id'] for result in sorted_results]
        top_5_urls = []
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_folder = os.path.join(base_path, 'ASSIGNMENT-3-M3/DEV')

        for file_path in top_5_file_paths:
            with open(f'{data_folder}/{file_path}', 'r') as file:
                data = json.load(file)
                top_5_urls.append(data['url'])

        end_time = time.time()  # Record end time
        print(f"Search took {round((end_time - start_time) * 1000, 2)} ms")
        print(f"Documents searched: {len(doc_ids)}")  # Print additional performance metric

        return top_5_urls


# Cache the searcher instance
@st.cache_resource
def get_searcher(index_file):
    return Searcher(index_file)


def main():
    st.title("Search Engine Interface")

    index_file = "inverted_index.json"
    searcher = get_searcher(index_file)  # Cached instance

    query = st.text_input("Enter your query:", "")
    if st.button("Search"):
        if not query.strip():
            st.warning("Please enter a valid query.")
        else:
            results = searcher.search(query)
            if results:
                st.subheader("Top 5 Results:")
                for i, url in enumerate(results, start=1):
                    st.write(f"{i}. ({url})")
            else:
                st.info("No results found. Try another query.")

if __name__ == "__main__":
    main()