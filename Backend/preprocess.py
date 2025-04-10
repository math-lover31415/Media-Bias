from newspaper import Article
from transformers import BertTokenizerFast

import torch
from torch.utils.data import Dataset

class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        # Ensure texts are strings
        texts = [str(text) for text in texts]
        
        # Tokenize inputs
        self.encodings = tokenizer(
            texts, 
            truncation=True, 
            padding=True, 
            max_length=max_length, 
            return_tensors='pt'
        )
        
        # Encode labels
        self.labels = torch.tensor(labels)
    
    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item
    
    def __len__(self):
        return len(self.labels)


def get_article(html=None,url=''):
    article = Article(url)
    if html:
        article.set_html(html)
        article.download(input_html=html)
    else:
        article.download()
    article.parse()
    article.nlp()
    return {
        'title': article.title,
        'text': article.text,
        'authors': article.authors,
        'publish_date': article.publish_date,
        'top_image': article.top_image,
        'movies': article.movies,
        'summary': article.summary
    }

import nltk
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources (run this once)
nltk.download('punkt', quiet=True)

def get_tokens(text):
    """
    Tokenize text using NLTK's word_tokenize method.
    
    Args:
        text (str): Input text to tokenize
    
    Returns:
        list: List of tokens
    """
    # Tokenize the text
    tokens = word_tokenize(text)
    
    return tokens