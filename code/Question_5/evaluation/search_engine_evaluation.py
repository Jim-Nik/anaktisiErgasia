import os
import numpy as np


# Function to load test queries and their expected relevant document IDs
def load_test_queries_and_relevance():
    return {
        "player": [0, 1],
        "rebounds": [0, 1],
        "game": [0, 1]
    }


# Function to evaluate precision, recall, and F1-score
def evaluate_performance(retrieved, relevant, top_n=10):
    retrieved = set(retrieved[:top_n])
    relevant = set(relevant)

    # Precision
    true_positives = len(retrieved & relevant)
    precision = true_positives / len(retrieved) if len(retrieved) > 0 else 0.0

    # Recall
    recall = true_positives / len(relevant) if len(relevant) > 0 else 0.0

    # F1-Score
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1


# Function to compute Average Precision (AP) for a query
def average_precision(retrieved, relevant, top_n=10):
    retrieved = list(retrieved)[:top_n]
    relevant = set(relevant)
    precision_at_k = []

    for k in range(1, top_n + 1):
        current_retrieved = set(retrieved[:k])  # Convert to set for intersection
        relevant_retrieved = current_retrieved & relevant
        precision_at_k.append(len(relevant_retrieved) / k if k > 0 else 0)

    return np.mean(precision_at_k)


# Main evaluation function
def evaluate_search_engine():
    queries_and_relevance = load_test_queries_and_relevance()

    all_precision = []
    all_recall = []
    all_f1 = []
    all_ap = []

    algorithms = {
        "Boolean Retrieval": run_boolean_retrieval,
        "Okapi BM25": run_okapi_bm25,
        "Vector Space Model": run_vector_space_model,
        "TF-IDF": run_tfidf,
        "Query Processing": run_query_processing,
    }

    # Iterate through each query and its relevant documents
    for query_entry, relevant_docs in queries_and_relevance.items():
        for algorithm_func in algorithms.values():
            try:
                retrieved = algorithm_func(query_entry)

                # Evaluate performance (precision, recall, F1)
                precision, recall, f1 = evaluate_performance(retrieved, relevant_docs)

                # Evaluate Average Precision (AP)
                ap = average_precision(retrieved, relevant_docs)

                # Store evaluation results
                all_precision.append(precision)
                all_recall.append(recall)
                all_f1.append(f1)
                all_ap.append(ap)

            except Exception:
                continue

    # Calculate the overall metrics across all algorithms and queries
    overall_map = np.mean(all_ap)
    overall_precision = np.mean(all_precision)
    overall_recall = np.mean(all_recall)
    overall_f1 = np.mean(all_f1)

    print(f"\nSearch Engine Evaluation (All algorithms combined):")
    print(f"Mean Average Precision (MAP): {overall_map:.4f}")
    print(f"Average Precision: {overall_precision:.4f}")
    print(f"Average Recall: {overall_recall:.4f}")
    print(f"Average F1-Score: {overall_f1:.4f}")


# Function to run Boolean Retrieval
def run_boolean_retrieval(query_entry):
    result = os.popen(
        f'python ../../Question_4/ranking/recovery_algorithms/boolean_retrieval.py "{query_entry}"').read()
    return extract_document_ids_from_output(result)


# Function to run Okapi BM25
def run_okapi_bm25(query_entry):
    result = os.popen(
        f'python ../../Question_4/ranking/recovery_algorithms/Okapi_BM25.py "{query_entry}"').read()
    return extract_document_ids_from_output(result)


# Function to run Vector Space Model
def run_vector_space_model(query_entry):
    result = os.popen(
        f'python ../../Question_4/ranking/recovery_algorithms/Vector_space_model.py "{query_entry}"').read()
    return extract_document_ids_from_output(result)


# Function to run TF-IDF
def run_tfidf(query_entry):
    result = os.popen(f'python ../../Question_4/ranking/TF-IDF.py "{query_entry}"').read()
    return extract_document_ids_from_output(result)


# Function to run Query Processing
def run_query_processing(query_entry):
    result = os.popen(f'python ../../Question_4/query_processing/query_processing.py "{query_entry}"').read()
    return extract_document_ids_from_output(result)


# Helper function to extract document IDs from the algorithm output
def extract_document_ids_from_output(output):
    doc_ids = []
    for line in output.splitlines():
        if "Document" in line:
            parts = line.split(":")
            try:
                doc_id = int(parts[0].split()[1]) - 1
                doc_ids.append(doc_id)
            except ValueError:
                pass
    return doc_ids


if __name__ == "__main__":
    evaluate_search_engine()
