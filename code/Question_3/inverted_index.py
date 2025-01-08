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


csv_files = ["../giannis_data.csv", "../tyrese_data.csv"]

# Build the inverted index
inverted_index = build_inverted_index(csv_files)

# Example of Boolean
query_entry = "basketball"
matching_query = query_inverted_index(inverted_index, query_entry)

if matching_query:
    print(f"Term '{query_entry}' found in:")
    for file_id, rows in matching_query.items():
        print(f"  In File: {csv_files[file_id]}")
        print(f"  Rows: {rows}")
else:
    print(f"Term '{query_entry}' was not found in any file you mentioned.")
