# Supabase Vector Database Setup (Optional)

This is an optional enhancement to store embeddings in Supabase for better performance and scalability.

## Setup Steps

### 1. Create Supabase Account
- Go to https://supabase.com
- Sign up for free account
- Create a new project

### 2. Enable Vector Extension
```sql
-- Run this in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

### 3. Create Tables
```sql
-- Create personalities table
CREATE TABLE personalities (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  key VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  style TEXT
);

-- Create chunks table with vector storage
CREATE TABLE chunks (
  id SERIAL PRIMARY KEY,
  personality_key VARCHAR(50) REFERENCES personalities(key),
  content TEXT NOT NULL,
  embedding vector(768), -- for all-mpnet-base-v2
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### 4. Insert Personalities
```sql
INSERT INTO personalities (name, key, description, style) VALUES
('Naval Ravikant', 'naval', 'a philosopher and entrepreneur', 'Be authentic, thoughtful, and speak in Naval''s style.'),
('Peter Thiel', 'peter', 'a venture capitalist and author', 'Be contrarian, analytical, and speak in Peter''s style.'),
('Paul Graham', 'paul', 'a programmer, writer, and venture capitalist', 'Be insightful, clear, and speak in Paul''s style.'),
('Sam Altman', 'sama', 'CEO of OpenAI and former president of Y Combinator', 'Be optimistic about technology, pragmatic about AI safety, and speak with Sam''s characteristic clarity and forward-thinking vision.'),
('Charlie Munger', 'charlie', 'Investor, vice chairman of Berkshire Hathaway, and renowned for his wisdom and wit.', 'Be practical, witty, and speak with Charlie''s characteristic directness and multidisciplinary insight.');
```

### 5. Update Backend Code
If you want to use Supabase, you'll need to:
1. Install `supabase-py` package
2. Update the backend to store/retrieve embeddings from Supabase
3. Add environment variables for Supabase URL and key

### 6. Environment Variables
Add to your Render environment:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

## Benefits of Using Supabase
- Persistent storage of embeddings
- Better scalability
- Faster similarity search
- No need to recompute embeddings on restart

## Current Setup
The current setup uses in-memory embeddings which is simpler and works well for the free tier. Supabase is optional for future scaling. 