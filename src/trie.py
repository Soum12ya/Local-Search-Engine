class TrieNode:
    """A single node in the Trie structure."""
    def __init__(self):
        # Dictionary to hold children nodes, keyed by character
        self.children = {}
        # Flag to mark if this node completes a valid indexed term
        self.is_end_of_word = False
        # Optional: Store the actual term for easier retrieval (for debugging/simplicity)
        self.term = None 

class Trie:
    """The Prefix Tree structure for fast autocomplete lookup."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        """Adds a word to the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.term = word

    def search_prefix(self, prefix: str) -> list[str]:
        """Returns all complete words matching the given prefix."""
        node = self.root
        
        # 1. Traverse to the end of the prefix
        for char in prefix:
            if char not in node.children:
                # If the prefix doesn't exist, return empty list
                return []
            node = node.children[char]
        
        # 2. Collect all words beneath this node
        suggestions = []
        self._collect_words(node, suggestions)
        
        return suggestions

    def _collect_words(self, node: TrieNode, suggestions: list[str], max_suggestions=10):
        """Helper function to perform Depth First Search (DFS) from a given node."""
        if len(suggestions) >= max_suggestions:
            return

        if node.is_end_of_word:
            suggestions.append(node.term)

        # Iterate over children in a sorted manner for clean output
        for char in sorted(node.children.keys()):
            self._collect_words(node.children[char], suggestions, max_suggestions)

# Example Usage:
#trie = Trie()
#trie.insert("running")
#trie.insert("run")
#trie.insert("runner")
#print(trie.search_prefix("ru")) # Output: ['run', 'runner', 'running']