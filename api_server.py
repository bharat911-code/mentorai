from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from yapper import initialize_model_and_index, ask_mistral

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    input: str

# Load model and index on startup
@app.on_event("startup")
def load_model():
    print("Starting model initialization...")
    # Use the correct path to the yapper_ravikant folder
    # The folder is nested: yapper_ravikant/yapper_ravikant/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "yapper_ravikant", "yapper_ravikant")
    
    print(f"Looking for yapper_ravikant folder at: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"❌ yapper_ravikant folder not found at {folder_path}")
        print("Please ensure the yapper_ravikant folder is in the correct location")
        return
    
    hf_token = os.getenv('HFT_TOKEN', None)
    
    success = initialize_model_and_index(folder_path, hf_token)
    if success:
        print("✅ Model and index initialized successfully!")
    else:
        print("❌ Failed to initialize model and index!")

@app.get("/")
async def root():
    return {"message": "Naval Ravikant AI API is running"}

@app.post("/predict")
async def predict(request: QueryRequest):
    user_input = request.input
    print(f"Received query: {user_input}")
    
    try:
        result = ask_mistral(user_input)
        print(f"Generated response: {result[:100]}...")
        return {"result": result}
    except Exception as e:
        print(f"Error processing query: {e}")
        return {"result": f"Sorry, I encountered an error while processing your question: {str(e)}"} 