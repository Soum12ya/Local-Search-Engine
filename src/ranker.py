import pickle
from pathlib import Path
from collections import defaultdict
import math

from .processor import TextProcessor 
from .trie import Trie

class SearchEngine:
    """Manages index loading, querying, retrieval, and ranking."""
    
    def __init__(self, index_path='output/search_index_data.pkl'):
        self.inverted_index = defaultdict(list)
        self.document_store = {}
        self.index_path = index_path
        self.autocomplete_trie = Trie()
        self._load_index()


    def _load_index(self):
        """Loads the Inverted Index and Document Store from the pickle file."""
        try:
            with open(self.index_path, 'rb') as f:
                # We saved both the index and store in a single tuple
                loaded_index, loaded_store, loaded_trie = pickle.load(f)
                self.inverted_index.update(loaded_index)
                self.document_store.update(loaded_store)
                self.autocomplete_trie = loaded_trie
            
            print(f"Successfully loaded index from {self.index_path}. Total documents: {len(self.document_store)}")
            
        except FileNotFoundError:
            print(f"Error: Index file not found at {self.index_path}. Run indexer.py first.")
        except Exception as e:
            print(f"Error loading index: {e}")


    def get_suggestions(self, prefix: str) -> list[str]:
        """Provides stemmed term suggestions for a raw prefix.""" 
        # 1. Pre-process the prefix (must be stemmed/lowercased just like the terms in the index)
        # Note: We only take the first token if the user types multiple words
        processed_prefix = TextProcessor.preprocess(prefix)
        if not processed_prefix:
            return []
        
        stemmed_prefix = processed_prefix[0]
        # 2. Search the Trie
        return self.autocomplete_trie.search_prefix(stemmed_prefix)
    

    def _phrase_search(self, terms: list[str]) -> set[int]:
        """ Finds documents where the terms appear as an exact contiguous phrase. """
        if not terms:
            return set()

        # Get the Posting list for the first term
        first_term = terms[0]
        if first_term not in self.inverted_index:
            return set()

        candidate_docs = set(posting['doc_id'] for posting in self.inverted_index[first_term])
    
        # Iterate through each subsequent term
        for i, next_term in enumerate(terms[1:], start=1):
            if next_term not in self.inverted_index:
                return set()

            # Perform a merge/intersection and check position
            new_candidates = {}
            next_term_postings = {p['doc_id']: p['positions'] for p in self.inverted_index[next_term]}

            for doc_id in candidate_docs.copy():
                if doc_id in next_term_postings:
                    # Find the intersection of positions (core positional logic)
                    current_term_postings = next((p for p in self.inverted_index[terms[i-1]] if p['doc_id'] == doc_id), None)
                
                    # Check the current term's positions against the next term's positions
                    # We are looking for (Current Pos + 1) == Next Pos

                    match_found = False
                    if current_term_postings:
                        for pos_prev in current_term_postings['positions']:
                            for pos_curr in next_term_postings[doc_id]:
                                if pos_curr == pos_prev + 1:
                                    match_found = True
                                    break
                            if match_found:
                                break
                
                    if not match_found:
                        # If the phrase breaks in this document, remove it from candidates
                        candidate_docs.discard(doc_id)         
                else:
                    # If the subsequent term isn't in the document, discard it
                    candidate_docs.discard(doc_id)             
        
        return candidate_docs


# --- Update the main search method to use this ---        

    def search(self, raw_query: str) -> list:
        """Processes the query, retrieves documents, and returns ranked results."""
        # Check for phrase search (query enclosed in quotes)
        is_phrase_search = raw_query.startswith('"') and raw_query.endswith('"')
        if is_phrase_search:
            # Remove quotes and process the internal terms
            clean_query = raw_query.strip('"')
            stemmed_query_terms = TextProcessor.preprocess(clean_query)

            # New Phrase Retrieval
            candidate_docs = self._phrase_search(stemmed_query_terms)

        else:
            # Standard Boolean Retrieval (existing logic)
            stemmed_query_terms = TextProcessor.preprocess(raw_query)
            candidate_docs = self._retrieve_candidates(stemmed_query_terms)

        if not candidate_docs:
            return []    
        
        # RANK THE RESULTS (Same as before)
        ranked_results = self._rank_documents(stemmed_query_terms, candidate_docs)
        
        return ranked_results

    # --- Implement these methods next! ---

    def _retrieve_candidates(self, terms: list[str]) -> set[int]:
        """Finds the intersection of documents containing all query terms."""
        # Placeholder for the set of DocIDs containing the first term
        candidate_set = None 
        
        for term in terms:
            if term in self.inverted_index:
                # Get the set of DocIDs for the current term
                current_doc_ids = {posting['doc_id'] for posting in self.inverted_index[term]}
                
                if candidate_set is None:
                    # Initialize the set with the first term's DocIDs
                    candidate_set = current_doc_ids
                else:
                    # Perform set intersection (AND logic)
                    candidate_set.intersection_update(current_doc_ids)
            else:
                # If any term is not found, the intersection is empty
                return set()
        
        return candidate_set if candidate_set is not None else set()

    def _rank_documents(self, terms: list[str], doc_ids: set[int]) -> list:
        """Calculates TF-IDF scores and sorts the results."""
        # N is the total number of documents in the collection
        N = len(self.document_store)
        doc_scores = defaultdict(float)
        
        for doc_id in doc_ids:
            score = 0.0
            doc_info = self.document_store[doc_id]
            doc_length = doc_info['content_length'] # Stored during indexing
            
            for term in terms:
                # 1. Calculate IDF (Inverse Document Frequency)
                df = len(self.inverted_index.get(term, [])) # Document Frequency (number of documents containing the term)
                # Avoid log(0) if df is 0, though retrieval should prevent this
                # idf = math.log(N / (df + 1)) 
                idf = math.log(1 + (N / df))

                # 2. Calculate TF (Term Frequency)
                # Find the specific posting for the current doc_id
                posting = next((p for p in self.inverted_index[term] if p['doc_id'] == doc_id), None)
                
                if posting:
                    term_count = len(posting['positions'])
                    tf = term_count / doc_length # Raw count divided by doc length
                    
                    # 3. Calculate TF-IDF
                    score += tf * idf
                    
            doc_scores[doc_id] = score
        
        # 4. Sort and Format Results
        ranked_list = []
        for doc_id, score in doc_scores.items():
            ranked_list.append({
                'title': self.document_store[doc_id]['title'],
                'score': score,
                'path': self.document_store[doc_id]['path'],
                'doc_id': doc_id, # <--- ADD THIS LINE
            })
            
        # Sort by score in descending order
        ranked_list.sort(key=lambda x: x['score'], reverse=True)
        
        return ranked_list

# --- Execution ---

if __name__ == "__main__":
    search_engine = SearchEngine()
    
    # Example search query
    query = input("Enter your search query: ")
    
    if search_engine.document_store: # Check if index loaded successfully
        results = search_engine.search(query)
        
        print("\n--- Search Results ---")
        if results:
            for i, result in enumerate(results):
                # Format score to 4 decimal places
                print(f"{i+1}. {result['title']} (Score: {result['score']:.4f})")
                
        else:
            print("No documents matched all search terms.")