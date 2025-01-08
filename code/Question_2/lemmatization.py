import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

def lemmatize(giannis_data):
    tok = word_tokenize(giannis_data)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(t) for t in tok]

def process_csv(my_file):
    # Initialize an empty list to collect all the text from the file
    all_text = ""

    # Open and read the CSV file
    with open(my_file, mode="r", encoding="utf-8") as token_file:
        reader = csv.reader(token_file)

        for row in reader:
            all_text += " " + row[0]  # Add space to separate texts from
            # different rows

    lemmatized_tokens = lemmatize(all_text)

    print("Lemmatization:\n", lemmatized_tokens)


my_file = "../giannis_data.csv"
process_csv(my_file)


