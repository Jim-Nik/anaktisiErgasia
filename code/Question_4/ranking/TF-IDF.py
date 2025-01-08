import csv
from nltk.tokenize import word_tokenize
from math import log
import sys

# Function to build the inverted index
def build_inverted_index(csv_files):
    inverted_index = {}
    doc_lengths = {}  # To store document lengths for TF-IDF normalization
    for file_id, csv_file in enumerate(csv_files):
        doc_lengths[file_id] = 0
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                row_text = " ".join(row)
                tokens = word_tokenize(row_text)

                for token in tokens:
                    token_lower = token.lower()
                    doc_lengths[file_id] += 1  # Count total terms in the document

                    if token_lower not in inverted_index:
                        inverted_index[token_lower] = {}

                    if file_id not in inverted_index[token_lower]:
                        inverted_index[token_lower][file_id] = []

                    if row_index not in inverted_index[token_lower][file_id]:
                        inverted_index[token_lower][file_id].append(row_index)

    return inverted_index, doc_lengths

# Function to compute TF-IDF rankings
def compute_tfidf_ranking(inverted_index, doc_lengths, query, num_docs):
    query_terms = word_tokenize(query.lower())
    tfidf_scores = {}

    for term in query_terms:
        if term in inverted_index:
            doc_occurrences = inverted_index[term]
            idf = log((num_docs + 1) / (len(doc_occurrences) + 1)) + 1  # Compute IDF

            for doc_id, rows in doc_occurrences.items():
                tf = len(rows) / doc_lengths[doc_id]  # Compute TF
                tfidf = tf * idf

                if doc_id not in tfidf_scores:
                    tfidf_scores[doc_id] = 0
                tfidf_scores[doc_id] += tfidf

    return sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

# Function to query the inverted index
def query_inverted_index(inverted_index, term):
    term_lower = term.lower()
    return inverted_index.get(term_lower, {})

# Main block for execution when the script is run directly
if __name__ == "__main__":
    # Get the query entry from command-line arguments (if provided)
    if len(sys.argv) > 1:
        query_entry = " ".join(sys.argv[1:])  # Combine arguments into a single query string
    else:
        query_entry = "basketball"  # Default query if no arguments are passed

    csv_files = ["../../giannis_data.csv", "../../tyrese_data.csv"]

    # Build the inverted index
    inverted_index, doc_lengths = build_inverted_index(csv_files)
    num_docs = len(csv_files)

    # Perform TF-IDF query using the provided or default query
    tfidf_results = compute_tfidf_ranking(inverted_index, doc_lengths, query_entry, num_docs)

    print(f"\nTF-IDF Rankings for query entry: '{query_entry}'")
    for doc_id, score in tfidf_results:
        print(f"  File: {csv_files[doc_id]} Score: {score:.4f}")
