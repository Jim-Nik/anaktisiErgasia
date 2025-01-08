import csv
import nltk
from nltk.tokenize import word_tokenize
# nltk.download('punkt_tab')

my_file = "../giannis_data.csv"

# Open and read the CSV file
with open(my_file, mode="r", encoding="utf-8") as token_file:
    reader = csv.reader(token_file)

    # Initialize lists to collect tokens
    split_tokens_list = []
    word_tokenize_list = []

    # Process the file
    for row in reader:
        for cell in row:
            # Split method
            split_tokens_list.extend(cell.split())

            # Word Tokenize method
            word_tokenize_list.extend(word_tokenize(cell))

    # Print results once for the entire file
    print("Split Method:", split_tokens_list)
    print("Word Tokenize:", word_tokenize_list)

