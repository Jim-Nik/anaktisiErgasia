import csv
from nltk.tokenize import word_tokenize


def build_inverted_index(csv_files):
    inverted_index = {}
    for file_id, csv_file in enumerate(csv_files):
        # Open and read the current CSV file
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                # Gather the text from all columns in one row
                row_text = " ".join(row)
                tokens = word_tokenize(row_text)

                # Add tokens to the inverted index
                for token in tokens:

                    token_lower = token.lower()  # Converting to lowercase
                    # Checks if token exists in inverted_index dictionary
                    if token_lower not in inverted_index:
                        # if it's not, it's added as a new key with {} as its value
                        inverted_index[token_lower] = {}

                    # Checks whether the file_id is already a key under the token's
                    # entry in the inverted_index.
                    if file_id not in inverted_index[token_lower]:
                        # Adds the file_id as a key with an empty list [] as its value.
                        inverted_index[token_lower][file_id] = []

                    # Checks if the current row_index is already in the list of
                    # row indices for this token and file.
                    if row_index not in inverted_index[token_lower][file_id]:
                        # Adds the row_index to the list for the token under
                        # the current file_id
                        inverted_index[token_lower][file_id].append(row_index)

    return inverted_index


# Function to query the inverted index
def query_inverted_index(inverted_index, term):
    term_lower = term.lower()
    return inverted_index.get(term_lower, {})


def boolean_query_processor(inverted_index, query):
    def get_docs_for_term(term):
        # Retrieve document IDs
        return set(inverted_index.get(term.lower(), {}).keys())

    def handle_and(terms):
        # For AND
        result = get_docs_for_term(terms[0])
        for term in terms[1:]:
            result &= get_docs_for_term(term)
        return result

    def handle_or(terms):
        # For OR
        result = set()
        for term in terms:
            result |= get_docs_for_term(term)
        return result

    def handle_not(term, universe):
        # For OR
        return universe - get_docs_for_term(term)

    # Tokenize and removing parentheses
    query = query.replace('(', '').replace(')', '')
    tokens = query.split()

    universe = set()  # Include all documents
    for term in inverted_index:
        universe.update(inverted_index[term].keys())

    # Boolean
    if 'AND' in tokens:
        terms = [t for t in tokens if t not in ['AND']]
        return handle_and(terms)
    elif 'OR' in tokens:
        terms = [t for t in tokens if t not in ['OR']]
        return handle_or(terms)
    elif 'NOT' in tokens:
        term = tokens[-1]  # Assume NOT is for last term
        return handle_not(term, universe)
    else:
        return get_docs_for_term(tokens[0])


if __name__ == "__main__":
    csv_files = ["../../giannis_data.csv", "../../tyrese_data.csv"]

    # Build the inverted index
    inverted_index = build_inverted_index(csv_files)

    # Example of Boolean
    queries = [
        "Haliburton AND February",
        "brother OR olympic",
        "NOT season",
        "consecutive"
    ]

    for q in queries:
        print(f"\nTerm: {q}")
        result = boolean_query_processor(inverted_index, q)
        if result:
            for file_id in result:
                if 'NOT' not in q:
                    rows = []
                    for term in q.split():
                        term_rows = inverted_index.get(term.lower(), {}).get(file_id, [])
                        rows.extend(term_rows)
                    print(f"  File: {csv_files[file_id]} Rows: {sorted(set(rows))}")
                else:
                    print(f"  File: {csv_files[file_id]}")
        else:
            print(f"  Term was not found!")
