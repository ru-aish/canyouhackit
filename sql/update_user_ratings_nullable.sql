-- Update user_ratings table to allow NULL user_id for anonymous ratings
-- Since SQLite doesn't support ALTER COLUMN, we need to recreate the table

-- Create new table with nullable user_id
CREATE TABLE IF NOT EXISTS user_ratings_new (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT NULL,  -- Made nullable for anonymous users
    resume_data TEXT,  -- Store base64 encoded resume data or file path
    github_link TEXT,  -- GitHub username or profile link
    git_score INTEGER DEFAULT 0,  -- GitHub score (0-1000)
    resume_score INTEGER DEFAULT 0,  -- Resume score (0-1000)
    overall_score INTEGER DEFAULT 0,  -- Overall combined score (0-1000)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Copy data from old table (if any exists)
INSERT INTO user_ratings_new SELECT * FROM user_ratings;

-- Drop old table
DROP TABLE user_ratings;

-- Rename new table
ALTER TABLE user_ratings_new RENAME TO user_ratings;

-- Recreate index
CREATE INDEX IF NOT EXISTS idx_user_ratings_user_id ON user_ratings(user_id);

-- Recreate trigger
CREATE TRIGGER IF NOT EXISTS update_user_ratings_timestamp 
    AFTER UPDATE ON user_ratings
    FOR EACH ROW
    BEGIN
        UPDATE user_ratings SET updated_at = CURRENT_TIMESTAMP WHERE uid = NEW.uid;
    END;