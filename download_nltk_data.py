import nltk

def download_data():
    """Downloads the required NLTK datasets."""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading 'stopwords' corpus...")
        nltk.download('stopwords')
    else:
        print("'stopwords' corpus is already downloaded.")

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading 'wordnet' corpus...")
        nltk.download('wordnet')
    else:
        print("'wordnet' corpus is already downloaded.")
        
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading 'punkt' corpus...")
        nltk.download('punkt')
    else:
        print("'punkt' corpus is already downloaded.")

if __name__ == '__main__':
    download_data()
