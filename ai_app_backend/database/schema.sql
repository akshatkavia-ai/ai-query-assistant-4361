-- Create qa_history table for storing question and answer pairs
CREATE TABLE IF NOT EXISTS qa_history (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create an index on created_at for faster queries ordered by time
CREATE INDEX IF NOT EXISTS idx_qa_history_created_at ON qa_history(created_at DESC);
