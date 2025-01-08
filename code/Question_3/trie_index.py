import csv
from nltk.tokenize import word_tokenize

class TrieNode:
    def __init__(self):
        # Each node contains a dictionary of children and
        # end_word indicates the end of a word
        self.children = {}
        self.end_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.end_word


def build_trie_index(csv_files):
    trie = Trie()

    for csv_file in csv_files:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                # Combine all columns into one string
                row_text = " ".join(row)
                tokens = word_tokenize(row_text)
                for token in tokens:
                    token_lower = token.lower()  # Converting to lowercase
                    trie.insert(token_lower)

    return trie

def query_trie_index(trie, term):
    term_lower = term.lower()
    return trie.search(term_lower)

# Example
if __name__ == "__main__":
    csv_files = ["../giannis_data.csv", "../tyrese_data.csv"]

    # Build the Trie index
    trie_index = build_trie_index(csv_files)

    # Query the Trie index
    query_term = "basketball"
    if query_trie_index(trie_index, query_term):
        print(f"Term '{query_term}' was found in the CSV files.")
    else:
        print(f"Term '{query_term}' was not found in any file you mentioned.")
