import os
import json
from tokenizer import Tokenizer
from inverted_index import InvertedIndex
from index_builder import IndexBuilder

def get_data_folder():
    """
    Determines the path to the data directory based on the script's location.

    Returns:
        str: The path to the 'data' directory located two levels up from the current file's directory.
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(base_path, 'data') #******
    # data_folder = os.path.join(base_path, 'test_data') #*************
    return data_folder


def get_files(data_folder):
    """
    Retrieves a list of JSON file paths from a specified directory.

    Args:
        data_folder (str): The directory from which to retrieve JSON files.

    Returns:
        list: A list of paths to JSON files found in the directory, including subdirectories.
    """
    files = []
    # Walk through the directory recursively to find and process the first three JSON files
    for root, dirs, files_in_dir in os.walk(data_folder):
        for file in files_in_dir:
            if file.endswith('.json'):
                files.append(os.path.join(root, file))
    ############ Comment these after testing ############
        #     if len(files) == 10000:  # Stop after finding three JSON files *****
        #         break
        # else:
        #     continue  # only executed if the inner loop did NOT break
        # break  # only executed if the inner loop DID break
    ############ Comment these after testing ############
    
    return files

def get_index_builder(data_folder, files):
    """
    Initializes and returns an IndexBuilder instance.

    Args:
        data_folder (str): The base directory for data files.
        files (list): A list of JSON file paths to be indexed.

    Returns:
        IndexBuilder: An instance of IndexBuilder initialized with specified files and directory settings.
    """
    index_builder = IndexBuilder(json_files=files,
                                 partial_threshold=500,
                                 partial_index_dir='partial_indexes',
                                 final_index_dir='final_index')
    return index_builder

def generate_final_report(index_builder):
    """
    Generates and saves a text report about the built index.

    Args:
        index_builder (IndexBuilder): The IndexBuilder instance that has completed building the index.

    This function retrieves the number of unique tokens and documents indexed, calculates the file size of the final index, and writes a detailed report to a text file. The report includes the number of documents, unique tokens, and the size on disk.
    """
    # Path to the final index JSON file
    final_index_dir = index_builder.final_index_dir
    final_index_path = os.path.join(final_index_dir, 'final_index.json')
    
    # Load the final index file
    with open(final_index_path, 'r') as file:
        final_index = json.load(file)

    num_tokens = index_builder.unique_token_count
    num_documents = index_builder.number_of_documents

    # Calculate file size
    index_size_kb = os.path.getsize(final_index_path) / 1024  # Size in KB

    # Create a report content
    report_content = f"""
    Final Index Report
    ------------------
    Number of Documents: {num_documents}
    Number of Unique Tokens: {num_tokens}
    Total Size on Disk: {index_size_kb:.2f} KB
    """

    # Path for the new report file
    project_base_dir = os.path.dirname(os.path.dirname(final_index_dir))  # This should navigate up to /path/to/CS121/Assignment3M1
    src_dir_path = os.path.join(project_base_dir, 'src')  # Append src to the path
    report_path = os.path.join(src_dir_path, 'report.txt')
    
    with open(report_path, 'w') as report_file:
        report_file.write(report_content)


    print("Report generated:", report_path)


def main():
    """
    Main function to execute the index building and report generation process.

    This function sets up the data folder, retrieves file paths, initializes the index builder, builds the index, and generates a final report.
    """
    data_folder = get_data_folder()
    files = get_files(data_folder)

    # Initialize the IndexBuilder with necessary parameters
    index_builder = get_index_builder(data_folder, files)

    # Build the index
    index_builder.build_index()

    # For now, just print out the location of the final index to verify it's done
    print(f"Index has been built and stored in {index_builder.final_index_dir}")

    generate_final_report(index_builder)

if __name__ == "__main__":
    main()
