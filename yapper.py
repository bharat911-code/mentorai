import os
import nltk
nltk.download('punkt')

llm_dict = {}
model_dict = {}
index_dict = {}
all_chunks_dict = {}

def initialize_model_and_index(folder_path, hf_token=None, personality_key=None):
    print(f"Initializing model and index with folder: {folder_path} (personality_key={personality_key})")
    
    try:
        from huggingface_hub import hf_hub_download
        from llama_cpp import Llama
        from sentence_transformers import SentenceTransformer
        import faiss
        import numpy as np
        from nltk.tokenize import sent_tokenize
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False

    try:
        print("Downloading model...")
        model_path = hf_hub_download(
            repo_id="TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF",
            filename="capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
            token=hf_token
        )
        
        print("Loading Llama model...")
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=8,
            n_gpu_layers=35,
            temperature=0.7,
            max_tokens=1024,
        )
        print("Llama model loaded successfully.")
        if personality_key:
            llm_dict[personality_key] = llm
        else:
            llm_dict[folder_path] = llm
    except Exception as e:
        print(f"Error loading Llama model: {e}")
        return False

    def load_texts_from_folder(folder_path):
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

    print("Loading texts...")
    all_texts = load_texts_from_folder(folder_path)
    if not all_texts:
        print("No texts loaded!")
        return False
    
    all_chunks = []
    for text in all_texts:
        all_chunks.extend(chunk_text_by_sentences(text))
    print(f"Total chunks created: {len(all_chunks)}")
    if personality_key:
        all_chunks_dict[personality_key] = all_chunks
    else:
        all_chunks_dict[folder_path] = all_chunks

    try:
        print("Encoding chunks...")
        model = SentenceTransformer('all-mpnet-base-v2', use_auth_token=hf_token)
        embeddings = model.encode(all_chunks, convert_to_numpy=True).astype('float32')
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        print("FAISS index built successfully.")
        if personality_key:
            model_dict[personality_key] = model
            index_dict[personality_key] = index
        else:
            model_dict[folder_path] = model
            index_dict[folder_path] = index
        # Debug: print keys after each initialization
        print(f"llm_dict keys: {list(llm_dict.keys())}")
        print(f"model_dict keys: {list(model_dict.keys())}")
        print(f"index_dict keys: {list(index_dict.keys())}")
        print(f"all_chunks_dict keys: {list(all_chunks_dict.keys())}")
        return True
    except Exception as e:
        print(f"Error creating embeddings/index: {e}")
        return False

def search(query, k=5, personality_key=None):
    if personality_key is None:
        raise Exception("Personality key must be provided.")
    model = model_dict.get(personality_key)
    index = index_dict.get(personality_key)
    all_chunks = all_chunks_dict.get(personality_key)
    if model is None or index is None or all_chunks is None:
        raise Exception(f"Model and index not initialized for personality '{personality_key}'.")
    import numpy as np
    query_vec = model.encode([query], convert_to_numpy=True).astype('float32')
    if query_vec.ndim == 1:
        query_vec = query_vec.reshape(1, -1)
    D, I = index.search(query_vec, k * 2)  # over-fetch
    raw_results = [(all_chunks[i], D[0][idx]) for idx, i in enumerate(I[0])]
    sorted_results = sorted(raw_results, key=lambda x: x[1])  # sort by closeness
    return [chunk for chunk, _ in sorted_results[:k]]

def build_prompt(query, chunks, personality_info):
    # Limit context length to avoid overflow
    context_parts = []
    total_length = 0
    max_context_length = 2000  # Limit context to avoid token overflow
    
    for chunk in chunks:
        chunk_text = chunk.strip()
        if total_length + len(chunk_text) < max_context_length:
            context_parts.append(chunk_text)
            total_length += len(chunk_text)
        else:
            break
    
    context = "\n\n".join(context_parts)
    
    prompt = (
        f"You are {personality_info['name']}, {personality_info['description']}. Answer the following question using the context provided. "
        f"{personality_info['style']} If the context doesn't provide enough information, "
        f"try to go through the given context again and again, until you find the answer from within the context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"{personality_info['name'].split()[0]}:"
    )
    return prompt

def ask_mistral(query, k=3, personality_info=None):
    if personality_info is None:
        raise Exception("personality_info must be provided")
    personality_key = None
    if 'key' in personality_info:
        personality_key = personality_info['key']
    else:
        personality_key = personality_info['name'].lower().split()[0]
    print(f"Processing query: {query} (personality: {personality_key})")
    top_chunks = search(query, k=k, personality_key=personality_key)
    print(f"Top {k} chunks:")
    for i, chunk in enumerate(top_chunks):
        print(f"[{i+1}] {chunk[:100]}...\n")

    prompt = build_prompt(query, top_chunks, personality_info)
    print(f"Prompt length: {len(prompt)} characters")
    print(f"Prompt (preview):\n{prompt[:300]}...\n{'='*50}")
    llm = llm_dict.get(personality_key)
    if llm is None:
        raise Exception(f"LLM not initialized for personality '{personality_key}'")
    try:
        output = llm(prompt, stop=["Question:", "Context:", "\n\n\n"], max_tokens=512)
        response = output["choices"][0]["text"].strip()
        print(f"Generated response: {response}")
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return f"Sorry, I encountered an error while processing your question: {e}"

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Change this to test different personalities manually
    personality = "peter"  # or "yapper_ravikant"
    folder_path = os.path.join(current_dir, personality)
    print(f"Looking for {personality} folder at: {folder_path}")
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found at {folder_path}")
        exit(1)
    hf_token = os.getenv('HFT_TOKEN', None)
    if initialize_model_and_index(folder_path, hf_token, personality_key=personality):
        user_input = input("Enter your question: ")
        response = ask_mistral(user_input, personality_info={
            'name': 'Naval Ravikant' if personality == 'yapper_ravikant' else 'Peter Thiel',
            'description': 'a philosopher and entrepreneur' if personality == 'yapper_ravikant' else 'a venture capitalist and author',
            'style': "Be authentic, thoughtful, and speak in Naval's style." if personality == 'yapper_ravikant' else "Be contrarian, analytical, and speak in Peter's style.",
            'key': personality
        })
        print(f"\nFinal Answer:\n{response}")
    else:
        print("Initialization failed.")
