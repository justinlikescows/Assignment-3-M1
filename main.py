import os
from inverted_index import build_inverted_index


# DEV file w JSON Data is stored in root directory, i.e., alongside main.py, 
# inverted_index.py, report.txt, and searcher.py
# Removed DEV file for submission purposes - folder too large


def save_analytics(index, index_path, analytics_path):
    num_docs = len(index.documents)
    unique_tokens = len(index.index)
    index_size_kb = os.path.getsize(index_path) / 1024

    with open(analytics_path, 'w') as f:
        f.write(f"Number of indexed documents: {num_docs}\n")
        f.write(f"Number of unique tokens: {unique_tokens}\n")
        f.write(f"Total size of index on disk: {index_size_kb:.2f} KB\n")

def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(base_path, 'ASSIGNMENT-3-M3/DEV')
    index_output_path = "inverted_index.json"
    analytics_output_path = "report.txt"
    
    # Build and save the inverted index
    inverted_index = build_inverted_index(data_folder)
    inverted_index.save_index(index_output_path)
    
    # Save analytics to a text file
    save_analytics(inverted_index, index_output_path, analytics_output_path)
    
    print(f"Index and analytics saved successfully. Check '{index_output_path}' and '{analytics_output_path}'.")
    


if __name__ == "__main__":
    main()