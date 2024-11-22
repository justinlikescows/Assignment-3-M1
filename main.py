import os
from inverted_index import build_inverted_index

def save_analytics(index, index_path, analytics_path):
    num_docs = len(index.documents)
    unique_tokens = len(index.index)
    index_size_kb = os.path.getsize(index_path) / 1024

    with open(analytics_path, 'w') as f:
        f.write(f"Number of indexed documents: {num_docs}\n")
        f.write(f"Number of unique tokens: {unique_tokens}\n")
        f.write(f"Total size of index on disk: {index_size_kb:.2f} KB\n")

def main():
    root_dir = "/Users/andrewly/Desktop/Assignment-3-M1/DEV"
    index_output_path = "inverted_index.json"
    analytics_output_path = "report.txt"
    
    # Build and save the inverted index
    inverted_index = build_inverted_index(root_dir)
    inverted_index.save_index(index_output_path)
    
    # Save analytics to a text file
    save_analytics(inverted_index, index_output_path, analytics_output_path)
    
    print(f"Index and analytics saved successfully. Check '{index_output_path}' and '{analytics_output_path}'.")

if __name__ == "__main__":
    main()