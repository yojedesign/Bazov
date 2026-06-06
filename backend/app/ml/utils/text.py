"""
Text preprocessing utilities
"""

import re
import string
from typing import List, Optional, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


# Stop words for filtering
STOP_WORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", 
    "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
    'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
    'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 
    'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 
    'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 
    'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', 
    "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', 
    "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', 
    "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
])

# Common contractions mapping
CONTRACTIONS = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}


def preprocess_text(
    text: str,
    lowercase: bool = True,
    remove_punctuation: bool = True,
    remove_numbers: bool = True,
    remove_stopwords: bool = True,
    expand_contractions: bool = True,
    remove_extra_whitespace: bool = True,
    remove_urls: bool = True,
    remove_emails: bool = True,
    remove_special_chars: bool = True,
) -> str:
    """
    Comprehensive text preprocessing
    
    Args:
        text: Input text
        lowercase: Convert to lowercase
        remove_punctuation: Remove punctuation
        remove_numbers: Remove numbers
        remove_stopwords: Remove stop words
        expand_contractions: Expand contractions
        remove_extra_whitespace: Remove extra whitespace
        remove_urls: Remove URLs
        remove_emails: Remove email addresses
        remove_special_chars: Remove special characters
        
    Returns:
        str: Preprocessed text
    """
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove URLs
    if remove_urls:
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    if remove_emails:
        text = re.sub(r'\S+@\S+', '', text)
    
    # Expand contractions
    if expand_contractions:
        for contraction, expansion in CONTRACTIONS.items():
            text = text.replace(contraction, expansion)
    
    # Convert to lowercase
    if lowercase:
        text = text.lower()
    
    # Remove numbers
    if remove_numbers:
        text = re.sub(r'\d+', '', text)
    
    # Remove punctuation
    if remove_punctuation:
        text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove special characters (keep alphanumeric and basic punctuation)
    if remove_special_chars:
        text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize and remove stopwords
    if remove_stopwords:
        tokens = text.split()
        tokens = [token for token in tokens if token not in STOP_WORDS]
        text = ' '.join(tokens)
    
    # Remove extra whitespace
    if remove_extra_whitespace:
        text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def clean_text(text: str) -> str:
    """
    Basic text cleaning (lightweight preprocessing)
    
    Args:
        text: Input text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Convert to string
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def tokenize_text(
    text: str,
    lowercase: bool = True,
    remove_punctuation: bool = True,
    remove_stopwords: bool = True,
) -> List[str]:
    """
    Tokenize text into words
    
    Args:
        text: Input text
        lowercase: Convert to lowercase
        remove_punctuation: Remove punctuation
        remove_stopwords: Remove stop words
        
    Returns:
        list: List of tokens
    """
    if not text:
        return []
    
    # Preprocess
    text = preprocess_text(
        text,
        lowercase=lowercase,
        remove_punctuation=remove_punctuation,
        remove_stopwords=False,  # We'll handle stopwords separately
        remove_numbers=True,
        remove_urls=True,
        remove_emails=True,
    )
    
    # Tokenize
    tokens = text.split()
    
    # Remove stopwords
    if remove_stopwords:
        tokens = [token for token in tokens if token not in STOP_WORDS]
    
    return tokens


def normalize_text(text: str) -> str:
    """
    Normalize text (lemmatization would go here in production)
    
    Args:
        text: Input text
        
    Returns:
        str: Normalized text
    """
    # In production, use NLTK or spaCy for lemmatization
    # For now, just do basic preprocessing
    return preprocess_text(text)


def extract_keywords(
    text: str,
    top_n: int = 10,
    min_length: int = 3
) -> List[Tuple[str, int]]:
    """
    Extract top keywords from text
    
    Args:
        text: Input text
        top_n: Number of top keywords to return
        min_length: Minimum length of keywords
        
    Returns:
        list: List of (keyword, count) tuples
    """
    from collections import Counter
    
    # Tokenize
    tokens = tokenize_text(text, remove_stopwords=True)
    
    # Filter by length
    tokens = [token for token in tokens if len(token) >= min_length]
    
    # Count frequencies
    word_counts = Counter(tokens)
    
    # Get top N
    return word_counts.most_common(top_n)


def extract_phrases(
    text: str,
    ngram_range: tuple = (2, 3),
    top_n: int = 10
) -> List[Tuple[str, int]]:
    """
    Extract top phrases (n-grams) from text
    
    Args:
        text: Input text
        ngram_range: Range of n-gram sizes
        top_n: Number of top phrases to return
        
    Returns:
        list: List of (phrase, count) tuples
    """
    from collections import Counter
    from nltk import ngrams
    
    # Tokenize
    tokens = tokenize_text(text, remove_stopwords=True)
    
    # Generate n-grams
    all_phrases = []
    for n in range(ngram_range[0], ngram_range[1] + 1):
        n_grams = list(ngrams(tokens, n))
        all_phrases.extend([' '.join(gram) for gram in n_grams])
    
    # Count frequencies
    phrase_counts = Counter(all_phrases)
    
    # Get top N
    return phrase_counts.most_common(top_n)
