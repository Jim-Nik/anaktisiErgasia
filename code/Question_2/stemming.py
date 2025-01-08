import csv
import nltk
from nltk.tokenize import word_tokenize
# nltk.download('punkt')

def stemming(giannis_data):
    tok = word_tokenize(giannis_data)
    porter = nltk.PorterStemmer()
    return [porter.stem(t) for t in tok]

def process_csv(my_file):
    # Initialize an empty list to collect all the text from the file
    all_text = ""

    # Open and read the CSV file
    with open(my_file, mode="r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            all_text += " " + row[0]  # Add space to separate texts from
            # different rows

    stemmed_tokens = stemming(all_text)

    print("Stemming:\n", stemmed_tokens)


# Provide the path to your CSV file
my_file = "../giannis_data.csv"  # Change this to the correct path
process_csv(my_file)


