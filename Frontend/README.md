# Multi-Personality AI Chat

An AI chat application that responds in the style of several famous thinkers, including Naval Ravikant, Paul Graham, Peter Thiel, Sam Altman, and Charlie Munger. Each personality is trained on their own writings and thoughts.

## Features

- Beautiful, responsive UI with dark/light mode toggle
- Real-time AI responses in the style of your chosen personality
- FastAPI backend with Llama model integration
- Vite + React + TypeScript frontend
- Easily extensible: add new personalities by adding a folder and updating the backend config

## Personalities Included
- Naval Ravikant
- Paul Graham
- Peter Thiel
- Sam Altman
- Charlie Munger

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
3. **(Optional) Set HuggingFace token (for better model access):**
   ```bash
   set HFT_TOKEN=your_huggingface_token_here
   ```

## Running the Application

1. **Start the backend:**
   ```bash
   python yapper_server.py
   ```
2. **Start the frontend (in a new terminal):**
   ```bash
   npm run dev
   ```
3. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8001

## Images
- All personality images are stored in `public/personalitiesimgs/`.
- Image URLs in the code are of the form `/personalitiesimgs/filename.jpg`.
- To update an image, replace the file in `public/personalitiesimgs/` and update the `img` field in `src/App.tsx` if needed.

## Project Structure

```
project/
├── yapper_server.py      # FastAPI backend with ML
├── yapper.py             # AI model and processing logic
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
├── src/
│   ├── App.tsx           # Main React component
│   ├── main.tsx          # React entry point
│   └── index.css         # Global styles
├── public/
│   └── personalitiesimgs/ # Personality images
├── js/naval/             # Naval's writings (training data)
├── paul/                 # Paul Graham's writings
├── peter/                # Peter Thiel's writings
├── sama/                 # Sam Altman's writings
├── charlie/              # Charlie Munger's writings
```

## How it Works

1. The backend loads each personality's writings from their folder
2. Text is chunked and embedded using sentence transformers
3. When a user asks a question, the system:
   - Searches for relevant chunks using FAISS
   - Builds a prompt with the selected personality's context
   - Generates a response using the Llama model
   - Returns the response in the selected style

## Troubleshooting

- **Model download issues**: Set your HuggingFace token as an environment variable
- **Port conflicts**: Make sure ports 8001 and 5173 are available
- **CORS errors**: Ensure both servers are running on the correct ports
- **Python dependency issues**: Double-check your Python version and dependencies

## License

This project is for educational purposes. The writings belong to their respective authors. 