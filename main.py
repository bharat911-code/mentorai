

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import requests
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import nltk
from nltk.tokenize import sent_tokenize


try:
    nltk.data.find('tokenizers/punkt')
    print("✅ NLTK punkt tokenizer already available")
except LookupError:
    print("📥 Downloading NLTK punkt tokenizer...")
    nltk.download('punkt')
    print("✅ NLTK punkt tokenizer downloaded")

app = FastAPI(title="Yapper RAG Server", version="1.0.0")

PERSONALITIES = {
    "naval": {
        "name": "Naval Ravikant",
        "description": "a philosopher and entrepreneur",
        "style": "Be authentic, thoughtful, and speak in Naval's style.",
        "folder": "js/naval",
        "key": "naval"
    },
    "peter": {
        "name": "Peter Thiel",
        "description": "a venture capitalist and author",
        "style": "Be contrarian, analytical, and speak in Peter's style.",
        "folder": "peter",
        "key": "peter"
    },
    "paul": {
        "name": "Paul Graham",
        "description": "a programmer, writer, and venture capitalist",
        "style": "Be insightful, clear, and speak in Paul's style.",
        "folder": "paul",
        "key": "paul"
    },
    "sama": {
        "name": "Sam Altman",
        "description": "CEO of OpenAI and former president of Y Combinator",
        "style": "Be optimistic about technology, pragmatic about AI safety, and speak with Sam's characteristic clarity and forward-thinking vision.",
        "folder": "sama",
        "key": "sama"
    },
    "charlie": {
        "name": "Charlie Munger",
        "description": "Investor, vice chairman of Berkshire Hathaway, and renowned for his wisdom and wit.",
        "style": "Be practical, witty, and speak with Charlie's characteristic directness and multidisciplinary insight.",
        "folder": "charlie",
        "key": "charlie"
    }
}

# Store embeddings and chunks for each personality
personality_data = {}

# Global variables
model_initialized = False
embedding_model: SentenceTransformer | None = None

class QueryRequest(BaseModel):
    question: str
    personality: str = "naval"  # Default to naval

class QueryResponse(BaseModel):
    answer: str
    status: str

def load_texts_from_folder(folder_path):
    """Load all .txt files from a folder"""
    texts = []
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return texts
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                    texts.append(f.read())
                    print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return texts

def chunk_text_by_sentences(text, max_chunk_len=500):
    """Split text into chunks by sentences"""
    sentences = sent_tokenize(text)
    chunks, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) < max_chunk_len:
            current += " " + sentence
        else:
            if current.strip():
                chunks.append(current.strip())
            current = sentence
    if current.strip():
        chunks.append(current.strip())
    return chunks

def ask_huggingface(prompt):
    """Send prompt to HuggingFace Inference API"""
    HF_TOKEN = os.getenv('HF_TOKEN')
    if not HF_TOKEN:
        raise Exception("HF_TOKEN environment variable not set")
    
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Format prompt for Mistral
    formatted_prompt = f"<s>[INST] {prompt} [/INST]"
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.95,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', '').replace(formatted_prompt, '').strip()
        else:
            return str(result)
    except Exception as e:
        print(f"Error calling HuggingFace API: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

def search_similar_chunks(query, personality_key, k=3):
    """Search for similar chunks using FAISS"""
    if personality_key not in personality_data:
        raise Exception(f"Personality '{personality_key}' not initialized")
    
    if embedding_model is None:
        raise Exception("Embedding model not initialized")
    
    
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
    
    # Get FAISS index and chunks for this personality
    faiss_index = personality_data[personality_key]['faiss_index']
    chunks = personality_data[personality_key]['chunks']
    
    # Search using FAISS
    similarities, indices = faiss_index.search(query_embedding, k)
    
    # Return the chunks
    return [chunks[i] for i in indices[0]]

def build_prompt(query, chunks, personality_info):
    """Build prompt with context"""
    context_parts = []
    total_length = 0
    max_context_length = 2000
    
    for chunk in chunks:
        chunk_text = chunk.strip()
        if total_length + len(chunk_text) < max_context_length:
            context_parts.append(chunk_text)
            total_length += len(chunk_text)
        else:
            break
    
    context = "\n\n".join(context_parts)
    
    prompt = (
        f"You are {personality_info['name']}, {personality_info['description']}. "
        f"Answer the following question using the context provided. "
        f"{personality_info['style']} If the context doesn't provide enough information, "
        f"try to go through the given context again and again, until you find the answer from within the context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"{personality_info['name'].split()[0]}:"
    )
    return prompt

@app.on_event("startup")
async def startup_event():
    """Initialize embeddings on startup"""
    global model_initialized, embedding_model, personality_data
    print("🚀 Starting Yapper RAG Server with HuggingFace API...")
    
    # Load embedding model (much lighter than full LLM)
    print("📥 Loading embedding model...")
    try:
        # Use a smaller model 
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Loaded all-MiniLM-L6-v2 (smaller model)")
    except Exception as e:
        print(f"❌ Failed to load embedding model: {e}")
    
    if embedding_model is None:
        print("❌ No embedding model loaded")
        model_initialized = False
        return
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    all_success = True
    
    for key, meta in PERSONALITIES.items():
        folder_path = os.path.join(current_dir, meta["folder"])
        print(f"📁 Processing personality '{key}' at: {folder_path}")
        
        if not os.path.exists(folder_path):
            print(f"❌ Folder not found for personality '{key}': {folder_path}")
            all_success = False
            continue
        
        try:
            # Load and chunk texts
            texts = load_texts_from_folder(folder_path)
            if not texts:
                print(f"❌ No texts loaded for '{key}'")
                all_success = False
                continue
            
            chunks = []
            for text in texts:
                chunks.extend(chunk_text_by_sentences(text))
            
            print(f"📝 Created {len(chunks)} chunks for '{key}'")
            
            # Create embeddings
            print(f"🔢 Creating embeddings for '{key}'...")
            embeddings = embedding_model.encode(chunks, convert_to_numpy=True).astype('float32')
            
            # Create FAISS index
            print(f"🔍 Creating FAISS index for '{key}'...")
            dimension = embeddings.shape[1]
            faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            faiss_index.add(embeddings.astype('float32'))
            
            # Store data
            personality_data[key] = {
                'chunks': chunks,
                'embeddings': embeddings,
                'faiss_index': faiss_index
            }
            
            print(f"✅ Personality '{key}' initialized!")
            
        except Exception as e:
            print(f"❌ Error processing '{key}': {e}")
            all_success = False
    
    model_initialized = all_success
    print(f"🎯 Server ready! Initialized: {model_initialized}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Yapper RAG Server with HuggingFace API is running!",
        "model_initialized": model_initialized,
        "personalities": list(PERSONALITIES.keys()),
        "endpoints": {
            "ask": "/ask",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_initialized": model_initialized,
        "personalities_loaded": len(personality_data)
    }

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """Ask a question to the RAG system"""
    global model_initialized, personality_data
    
    if not model_initialized:
        raise HTTPException(status_code=503, detail="System not initialized yet")

    personality = request.personality
    if personality not in PERSONALITIES:
        raise HTTPException(status_code=400, detail=f"Unknown personality: {personality}")
    
    if personality not in personality_data:
        raise HTTPException(status_code=503, detail=f"Personality '{personality}' not loaded")

    try:
        print(f"🤔 Received question: {request.question} (personality: {personality})")
        
        # Search for relevant chunks
        relevant_chunks = search_similar_chunks(request.question, personality, k=3)
        print(f"📚 Found {len(relevant_chunks)} relevant chunks")
        
        # Build prompt
        prompt = build_prompt(request.question, relevant_chunks, PERSONALITIES[personality])
        print(f"📝 Prompt length: {len(prompt)} characters")
        
        # Get response from HuggingFace API
        answer = ask_huggingface(prompt)
        print(f"💬 Generated answer: {answer[:100]}...")
        
        return QueryResponse(
            answer=answer,
            status="success"
        )
    except Exception as e:
        print(f"❌ Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

if __name__ == "__main__":
    # Use PORT environment variable for Render, fallback to 8000
    port = int(os.getenv("PORT", 8000))
    print(f"🎯 Starting Yapper RAG Server with HuggingFace API on port {port}...")
    uvicorn.run(
        "yapper_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
