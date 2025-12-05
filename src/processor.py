import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict
import re

# Initialize NLP tools
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

class TextProcessor:
    """Handles tokenization, stop word removal, and stemming."""

    @staticmethod
    def preprocess(text: str) -> list[str]:
        # 1. Lowercase and Tokenize
        # Use regex to find all word tokens (better than simple split)
        tokens = re.findall(r'\b\w+\b', text.lower())

        processed_tokens = []
        for token in tokens:
            # 2. Stop Word Removal
            if token not in stop_words:
                # 3. Stemming
                stemmed_token = stemmer.stem(token)
                processed_tokens.append(stemmed_token)

        return processed_tokens

    @staticmethod
    def get_token_positions(text: str) -> dict[str, list[int]]:
        """Returns a dictionary mapping stemmed tokens to their positions in the text."""
        # This is a more complex version for positional indexing
        
        token_map = defaultdict(list)
        
        # We need the original, non-stemmed tokens to count positions correctly
        original_tokens = re.findall(r'\b\w+\b', text.lower())
        
        for i, token in enumerate(original_tokens):
            if token not in stop_words:
                stemmed_token = stemmer.stem(token)
                token_map[stemmed_token].append(i + 1) # Position starts at 1
                
        return token_map

# Example Usage:
# text = "The running fox jumps quickly over the lazy dog."
# positions = TextProcessor.get_token_positions(text)
# print(positions) 
# Output: {'run': [2], 'fox': [3], 'jump': [4], 'quickli': [5], 'lazi': [8], 'dog': [9]}