from flask import Flask, render_template, request, redirect, url_for
import sys
import os
from flask import jsonify

# Ensure the project root is in the path for proper module imports
# This is a good practice for running the app directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the core search engine logic
from src.ranker import SearchEngine 

# --- Initialization ---
app = Flask(__name__)

# Initialize the search engine once when the app starts
try:
    search_engine = SearchEngine(index_path='output/search_index_data.pkl')
except Exception as e:
    # If the index is missing or fails to load, stop the app initialization
    print(f"FATAL ERROR: Could not load SearchEngine. {e}")
    sys.exit(1)


# --- Web Routes ---

@app.route('/', methods=['GET', 'POST'])
def search_page():
    query = ""
    results = []
    
    if request.method == 'POST':
        # 1. Get query from the form input
        query = request.form.get('query', '').strip()
        
        if query:
            # 2. Call the core search logic
            # The search() method handles pre-processing, retrieval, and ranking
            results = search_engine.search(query)
            
    # Render the search results template
    return render_template('search.html', query=query, results=results)


@app.route('/suggest', methods=['GET'])
def get_suggestions_api():
    # Get the user's partial input from the URL query parameters (?prefix=...)
    prefix = request.args.get('prefix', '').strip()
    
    if prefix:
        # Call the Trie logic
        suggestions = search_engine.get_suggestions(prefix)
        # Return the results as JSON
        return jsonify(suggestions)
    
    return jsonify([])


@app.route('/document/<int:doc_id>')
def view_document(doc_id):
    # This route is a placeholder for showing the full document content later
    doc_info = search_engine.document_store.get(doc_id)
    if doc_info:
        return f"<h1>Viewing Document: {doc_info['title']}</h1><p>Full content would go here...</p>"
    return "Document not found", 404


# --- Execution ---
if __name__ == '__main__':
    # Flask needs a 'templates' directory to find HTML files
    print("Starting Flask web server...")
    app.run(debug=True)