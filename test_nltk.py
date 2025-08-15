#!/usr/bin/env python3
"""
Test script to verify NLTK is working properly
"""

import nltk
from nltk.tokenize import sent_tokenize

def test_nltk():
    """Test NLTK punkt tokenizer"""
    print("🧪 Testing NLTK...")
    
    # Test if punkt is available
    try:
        nltk.data.find('tokenizers/punkt')
        print("✅ NLTK punkt tokenizer is available")
    except LookupError:
        print("❌ NLTK punkt tokenizer not found, downloading...")
        nltk.download('punkt')
        print("✅ NLTK punkt tokenizer downloaded")
    
    # Test sentence tokenization
    test_text = "Hello world! This is a test. How are you doing today?"
    sentences = sent_tokenize(test_text)
    
    print(f"📝 Test text: {test_text}")
    print(f"🔤 Tokenized sentences: {sentences}")
    print(f"📊 Number of sentences: {len(sentences)}")
    
    if len(sentences) == 3:
        print("✅ NLTK is working correctly!")
        return True
    else:
        print("❌ NLTK is not working as expected")
        return False

if __name__ == "__main__":
    test_nltk() 