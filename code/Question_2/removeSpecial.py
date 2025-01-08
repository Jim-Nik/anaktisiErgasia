import csv
import re
from nltk.tokenize import word_tokenize

def remove_special_characters(giannis_data):
    # Use regex to remove non-alphabetic characters (keeps letters and spaces)
    cleaned_text = re.sub(r'[^A-Za-z\s]', '', giannis_data)
    return cleaned_text

def process_csv(my_file):
    # Initialize an empty string to collect all the text from the file
    all_text = ""

    # Open and read the CSV file
    with open(my_file, mode="r", encoding="utf-8") as token_file:
        reader = csv.reader(token_file)

        for row in reader:
            all_text += " " + row[0]  # Add space to separate texts
            # rom different rows

    # Remove special characters from the entire concatenated text
    cleaned_text = remove_special_characters(all_text)

    tokens = word_tokenize(cleaned_text)

    print("Cleaned text's special characters :\n", tokens)

my_file = "../giannis_data.csv"
process_csv(my_file)

