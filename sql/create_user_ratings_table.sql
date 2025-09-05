-- Create table for storing user resume ratings and analysis
CREATE TABLE IF NOT EXISTS user_ratings (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resume_data TEXT,  -- Store base64 encoded resume data or file path
    github_link TEXT,  -- GitHub username or profile link
    git_score INTEGER DEFAULT 0,  -- GitHub score (0-1000)
    resume_score INTEGER DEFAULT 0,  -- Resume score (0-1000)
    overall_score INTEGER DEFAULT 0,  -- Overall combined score (0-1000)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create index for faster lookups by user_id
CREATE INDEX IF NOT EXISTS idx_user_ratings_user_id ON user_ratings(user_id);

-- Create trigger to update the updated_at timestamp when record is modified
CREATE TRIGGER IF NOT EXISTS update_user_ratings_timestamp 
    AFTER UPDATE ON user_ratings
    FOR EACH ROW
    BEGIN
        UPDATE user_ratings SET updated_at = CURRENT_TIMESTAMP WHERE uid = NEW.uid;
    END;