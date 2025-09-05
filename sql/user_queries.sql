-- Insert a new user
INSERT INTO users (name, email, password_hash, profile_logo) 
VALUES (?, ?, ?, ?);

-- Get user by email for login
SELECT user_id, name, email, password_hash, profile_logo, created_at 
FROM users 
WHERE email = ?;

-- Get user by ID
SELECT user_id, name, email, profile_logo, created_at 
FROM users 
WHERE user_id = ?;

-- Update user profile logo
UPDATE users 
SET profile_logo = ? 
WHERE user_id = ?;

-- Check if email exists
SELECT COUNT(*) as count 
FROM users 
WHERE email = ?;

-- Get all users
SELECT user_id, name, email, profile_logo, created_at 
FROM users 
ORDER BY created_at DESC;

-- Delete user
DELETE FROM users 
WHERE user_id = ?;