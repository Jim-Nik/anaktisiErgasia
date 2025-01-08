import csv
import sys
from nltk.tokenize import word_tokenize

# Build the inverted index
def build_inverted_index(csv_files):
    inverted_index = {}
    logical_operators = {'and', 'or', 'not'}  # Logical operators to ignore
    for file_id, csv_file in enumerate(csv_files):
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                row_text = " ".join(row)
                tokens = word_tokenize(row_text)

                for token in tokens:
                    token_lower = token.lower()

                    if token_lower in logical_operators:
                        continue

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

def boolean_query_processor(inverted_index, query_entry):
    query_entry = query_entry.replace('(', ' ( ').replace(')', ' ) ')  # Add spaces around parentheses
    tokens = query_entry.split()

    logical_operators = {'and', 'or', 'not'}

    result = None
    operator = None

    all_docs = set(range(len(csv_files)))

    i = 0
    while i < len(tokens):
        token = tokens[i]
        term_docs = query_inverted_index(inverted_index, token)

        if operator == 'NOT':
            if result is None:
                if term_docs:
                    result = all_docs - set(term_docs.keys())
                else:
                    result = all_docs
            else:
                result -= set(term_docs.keys())
        else:
            if result is None:
                result = set(term_docs.keys())
            elif operator == 'AND':
                result &= set(term_docs.keys())
            elif operator == 'OR':
                result |= set(term_docs.keys())

        i += 1
        if i < len(tokens):
            operator = tokens[i].upper() if tokens[i].lower() in logical_operators else None
            i += 1
        else:
            operator = None

    if result == set():
        return "Term was not found!"
    return result


if __name__ == "__main__":
    csv_files = ["../../giannis_data.csv", "../../tyrese_data.csv"]

    # Build the inverted index
    inverted_index = build_inverted_index(csv_files)

    # Get query from command-line arguments
    query_entry = sys.argv[1] if len(sys.argv) > 1 else ""

    print(f"\nQuery: {query_entry}")
    result = boolean_query_processor(inverted_index, query_entry)

    if isinstance(result, set):
        print(f"  Boolean Search Results: {result}")
        print(f"  Terms in the query:")
        for term in query_entry.split():
            term_lower = term.lower()
            if term_lower in inverted_index:
                print(f"    '{term_lower}': {inverted_index[term_lower]}")
    else:
        print(f"  {result}")
