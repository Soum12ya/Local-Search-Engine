import os
import pickle
from collections import defaultdict
from pathlib import Path

from .processor import TextProcessor 
from .trie import Trie

# Initialize NLP tools (Add this section to your indexer.py if not already there)
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
# (Paste your TextProcessor class implementation here)

autocomplete_trie = Trie()

# Inverted Index structure: 
# { 'stemmed_term': [ {'doc_id': 1, 'positions': [pos1, pos2]}, {'doc_id': 3, 'positions': [posA, posB]} ] }
inverted_index = defaultdict(list) 
document_store = {} # To map DocID to Title/Path for easy retrieval later

# --- Indexing Functions ---

def build_index(data_dir: str):
    """Builds the Inverted Index and Document Store from text files in data_dir."""
    global inverted_index, document_store, autocomplete_trie
    inverted_index = defaultdict(list)
    document_store = {}
    autocomplete_trie = Trie()
    
    doc_id = 0
    
    # Ensure data_dir path is correct relative to where the script is run
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Data directory not found: {data_dir}. Run the script from the root project directory.")

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            doc_id += 1
            file_path = os.path.join(data_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Store document info
            document_store[doc_id] = {"title": filename, "path": file_path, "content_length": len(content.split())}
            
            # 2. Get processed tokens and their positions (Assuming TextProcessor is imported/defined)
            token_positions = TextProcessor.get_token_positions(content)
            
            # --- START DUMMY TOKEN POSITIONS FOR TESTING ---
            # Replace the above line with real logic later. Using dummy for now:
            # token_positions = {"data": [1, 5], "structure": [2], "search": [3, 6]} 
            # --- END DUMMY TOKEN POSITIONS FOR TESTING ---
            

            # 3. Build the Inverted Index and Trie for autocomplete
            for term, positions in token_positions.items():

                if not inverted_index[term]: # Only insert if this is the first document for this term
                    autocomplete_trie.insert(term)

                # Create the Posting (a dictionary here for simplicity)
                posting = {'doc_id': doc_id, 'positions': positions}

                # Append the posting to the term's list
                inverted_index[term].append(posting)

    print(f"Indexing complete. {len(document_store)} documents indexed.")

def save_index(output_dir: str = 'output', filename: str = "inverted_index.pkl"):
    """
    Saves the index, document store, and the Trie.
    """
    # 1. Create the output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 2. Define the full path for the pickle file
    full_path = Path(output_dir) / filename
    
    # 3. Save the data
    with open(full_path, 'wb') as f:
        # Save the Trie along with the other data
        pickle.dump((dict(inverted_index), document_store, autocomplete_trie), f)
        
    print(f"Index successfully saved to {full_path}")


# --- Execution ---
if __name__ == "__main__":
    # Ensure you are running this from the root directory (one level above 'src')
    
    # Pass the location of the data folder and the desired output folder
    build_index('data') 
    save_index(output_dir='output', filename='search_index_data.pkl')