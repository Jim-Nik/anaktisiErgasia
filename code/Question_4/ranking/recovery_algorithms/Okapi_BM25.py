import csv
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from rank_bm25 import BM25Okapi


# Function to extract documents from CSV files
def extract_documents_from_index(csv_files):
    documents = []
    for file_id, csv_file in enumerate(csv_files):
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            doc_text = " ".join([" ".join(row) for row in reader])  # Join all rows to form a single document
            documents.append(doc_text)
    return documents


# Function to tokenize documents and remove stopwords
def tokenize_with_stopwords(documents):
    stop_words = set(stopwords.words('english'))  # Load English stopwords
    tokenizer = RegexpTokenizer(r'\w+')  # Tokenize words (ignores punctuation)
    tokenized_corpus = []

    for doc in documents:
        tokens = tokenizer.tokenize(doc.lower())  # Tokenize and convert to lowercase
        tokens = [token for token in tokens if token not in stop_words]  # Remove stopwords
        tokenized_corpus.append(tokens)

    return tokenized_corpus


# BM25 Function
def bm25_model(query_entry, documents):
    # Tokenize all documents and remove stopwords
    tokenized_corpus = tokenize_with_stopwords(documents)

    # Tokenize the query and remove stopwords
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_query = tokenizer.tokenize(query_entry.lower())  # Tokenize query
    tokenized_query_no_stopwords = [token for token in tokenized_query if
                                    token not in stopwords.words('english')]  # Remove stopwords

    # Initialize BM25
    bm25 = BM25Okapi(tokenized_corpus)

    # Get BM25 scores
    scores = bm25.get_scores(tokenized_query_no_stopwords)

    # Return document IDs sorted by scorea
    return sorted(enumerate(scores), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    # Example CSV files
    csv_files = ["../../giannis_data.csv", "../../tyrese_data.csv"]

    # Extract documents for BM25
    documents = extract_documents_from_index(csv_files)

    query_entry = sys.argv[1] if len(sys.argv) > 1 else ""

    print(f"\nQuery: {query_entry}")

    bm25_results = bm25_model(query_entry, documents)

    # Display BM25 Results with the query name
    print(f"\nBM25 Results for query '{query_entry}' sorted from best to worst:")
    for doc_id, score in bm25_results:
        print(f"Document {doc_id + 1}: Score: {score}")
