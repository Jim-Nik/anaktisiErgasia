import csv
import sys
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Build the inverted index
def build_inverted_index(csv_files):
    inverted_index = {}
    for file_id, csv_file in enumerate(csv_files):
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                row_text = " ".join(row)
                tokens = word_tokenize(row_text)

                for token in tokens:
                    token_lower = token.lower()
                    if token_lower not in inverted_index:
                        inverted_index[token_lower] = {}

                    if file_id not in inverted_index[token_lower]:
                        inverted_index[token_lower][file_id] = []

                    if row_index not in inverted_index[token_lower][file_id]:
                        inverted_index[token_lower][file_id].append(row_index)

    return inverted_index

# Function to query the inverted index
def query_inverted_index(inverted_index, term):
    term_lower = term.lower()
    return inverted_index.get(term_lower, {})

# Extract documents from CSV files
def extract_documents_from_index(inverted_index, csv_files):
    documents = []
    for file_id, csv_file in enumerate(csv_files):
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            doc_text = " ".join([" ".join(row) for row in reader])
            documents.append(doc_text)
    return documents

# Vector Space Model implementation
def vector_space_model(query_entry, documents):
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Transform the query into the TF-IDF space
    query_vector = vectorizer.transform([query_entry])

    # Compute cosine similarity between the query and each document
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Rank documents by similarity score
    ranked_documents = sorted(enumerate(cosine_similarities), key=lambda x: x[1], reverse=True)

    return ranked_documents

# Main code
if __name__ == "__main__":
    csv_files = ["../../giannis_data.csv", "../../tyrese_data.csv"]

    # Build the inverted index
    inverted_index = build_inverted_index(csv_files)

    # Extract documents from the CSV files
    documents = extract_documents_from_index(inverted_index, csv_files)

    # Get query from command-line arguments
    query_entry = sys.argv[1] if len(sys.argv) > 1 else ""

    # Apply Vector Space Model
    vsm_results = vector_space_model(query_entry, documents)

    # Display results with the query included
    print(f"\nVSM results for query '{query_entry}' sorted from best to worst:")
    for doc_id, score in vsm_results:
        print(f"Document {doc_id + 1}: Score: {score:.4f}")
