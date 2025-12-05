# 🔎 Local Search & Ranking Engine

This project is a highly performant, custom-built search engine prototype developed in Python. It demonstrates foundational Computer Science concepts, including Information Retrieval (IR) algorithms, advanced data structures (Trie, Inverted Index), and modern full-stack integration (Python/Flask/AJAX).

---

## 🚀 Project Goal & Technical Focus

The primary goal of this project was to move beyond simple CRUD applications and build a system that solves a complex, core engineering problem: **efficiently retrieving and ranking relevant information**.

The project showcases mastery in three key areas:

- **Algorithms**: Implementation of the TF-IDF (Term Frequency-Inverse Document Frequency) relevance scoring algorithm.
- **Data Structures**: Custom implementation and integration of the Inverted Index and the Trie (Prefix Tree).
- **System Design**: Building a scalable pipeline with separated Indexing, Searching, and Ranking modules.

---

## ⚙️ Architecture and Data Flow

**Project Architecture Diagram:**  
<!-- Add your architecture diagram image here: -->
<img width="1273" height="703" alt="architecture" src="https://github.com/user-attachments/assets/39d844eb-8017-4e8c-84aa-7a7c7429b0b1" />

The system employs a classic pipeline architecture to separate the heavy, offline Indexing Phase from the fast, real-time Searching Phase.

### Core Components

| Component          |      Files              | Purpose                                                                   |
|--------------------|------------------------|---------------------------------------------------------------------------|
| **data/**          | `.txt` files           | Stores raw, unstructured input documents to be indexed.                   |
| **src/processor.py**| `TextProcessor` class  | Data Cleaning: Handles Tokenization, Stop Word Removal (NLTK), Stemming.  |
| **src/indexer.py** | `build_index` function | Indexing: Builds Inverted Index & Trie, saves to disk.                    |
| **src/ranker.py**  | `SearchEngine` class   | Search Logic: Retrieval & relevance score calculation.                    |
| **src/main.py**    | Flask App              | Web Interface and API endpoints.                                          |
| **output/**        | `.pkl` files           | Persistence for serialized (pickled) Index & Document Store.              |

---

## 🌟 Advanced Features Implemented

### Application Preview  
<!-- Add project output screenshot here: -->
<img width="1912" height="947" alt="LSE_1" src="https://github.com/user-attachments/assets/5b8f2cc3-e08e-4c5c-bdeb-1be596bc1547" />
<img width="1917" height="1002" alt="LSE_2" src="https://github.com/user-attachments/assets/1e25f6a7-4411-46fa-997b-ae1d00ec37a0" />
<img width="1918" height="1001" alt="LSE_3" src="https://github.com/user-attachments/assets/e507bc00-4bfe-4189-bb1b-38dbeb469563" />


The final application features a centered, modern interface with real-time Autocomplete functionality.

### 1. Inverted Index with Positional Data
- Records the specific position(s) of each term.
- Enables accurate phrase searching.

### 2. Positional / Phrase Searching (Boolean Logic)
- When queries are wrapped in quotes (e.g., `"running fox"`), performs strict positional checks.
- Complex merging/intersection logic for accurate matches.

### 3. TF-IDF Ranking Algorithm
- Determines relevance by weighting terms based on frequency and rarity.
- Includes smoothed IDF to prevent division-by-zero errors.

### 4. Autocomplete via Trie Data Structure
- Custom Trie (Prefix Tree) built at indexing.
- AJAX frontend calls Trie for real-time suggestions.
- Search time: $O(\text{length of prefix})$.

### 5. Full-Stack Demonstration (Python & Flask)
- Backend exposed via clean web API (`src/main.py`).
- Frontend uses JavaScript for AJAX requests, yielding fast user experience.

---

## 🛠️ Setup & Installation Guide

### Prerequisites
- Python 3.8+
- pip package manager

### A. Environment Setup

```bash
git clone your-repo-link search_engine_project
cd search_engine_project
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
pip install Flask nltk
```

**Download NLTK Data (Required):**

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

### B. Indexing Phase (Building Search Data)

1. **Add `.txt` files** to the `data/` directory.
2. **Build Index & Trie**:
   ```bash
   python -m src.indexer
   ```
   - Generates `search_index_data.pkl` in `output/`

### C. Running the Web Application

```bash
python src/main.py
```
Open your browser to: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## ✍️ Development History

- **Phase 1**: Core Data Structures (`indexer.py`, `processor.py`)
  - Inverted Index, TextProcessor (Tokenization, Stopword removal, Stemming using NLTK)
- **Phase 2**: Retrieval & Ranking (`ranker.py`)
  - Boolean retrieval, TF-IDF formula (with IDF smoothing)
- **Phase 3**: Web Integration (`main.py`, `templates/search.html`)
  - Flask backend, frontend HTML/CSS structure
- **Phase 4**: Advanced Algorithms (Phrase Search, Trie)
  - Positional search, accurate phrase matching, custom Trie structure
- **Phase 5**: UX/UI Polish
  - AJAX/JS for Autocomplete, modern search interface look

---

## 📁 Project Structure

```
search_engine_project/
│
├── data/                 # Input .txt documents  
├── output/               # Serialized index (.pkl) files  
├── src/
│   ├── processor.py      # TextProcessor class  
│   ├── indexer.py        # build_index function  
│   ├── ranker.py         # SearchEngine class  
│   └── main.py           # Flask entry point  
└── README.md             # Project documentation
```

---

## 💡 Contributing & License

Feel free to fork, clone, and contribute by submitting pull requests!

---

## 📬 Contact

For questions or feedback, open an issue or reach out directly.

```
Soum12ya
```

---
