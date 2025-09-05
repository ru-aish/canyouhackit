-- Populate hackathons table with required events for frontend compatibility
-- This file provides the events expected by the frontend team creation system

-- First, ensure the hackathons table has the event_id column for frontend compatibility
ALTER TABLE hackathons ADD COLUMN event_id TEXT UNIQUE;

-- Insert the required hackathon events that the frontend expects
INSERT OR REPLACE INTO hackathons (
    event_id,
    name, 
    description, 
    start_date, 
    end_date, 
    registration_deadline, 
    max_participants, 
    current_participants,
    status, 
    theme, 
    prizes,
    rules,
    created_at
) VALUES 
(
    'hackthon_hackbyte_1',
    'HackByte 2025',
    'First annual HackByte hackathon focused on innovative solutions',
    '2025-09-12 17:00:37',
    '2025-09-14 17:00:37',
    '2025-09-10 17:00:37',
    100,
    0,
    'active',
    'Innovation & Technology',
    '{"first": "₹50,000", "second": "₹30,000", "third": "₹20,000"}',
    'Teams of 2-6 members. Submit working prototype with source code.',
    '2025-09-05 17:00:37'
),
(
    'hackthon_hackbyte_2',
    'HackByte AI Challenge',
    'AI and Machine Learning focused hackathon',
    '2025-10-05 17:00:37',
    '2025-10-07 17:00:37',
    '2025-10-03 17:00:37',
    150,
    0,
    'upcoming',
    'Artificial Intelligence',
    '{"first": "₹75,000", "second": "₹45,000", "third": "₹25,000", "special": "Best AI Innovation ₹10,000"}',
    'AI/ML focused projects only. Teams of 3-5 members. Must use AI/ML technologies.',
    '2025-09-05 17:00:37'
);

-- Update the teams table to support event_id if not already done
ALTER TABLE teams ADD COLUMN event_id TEXT;
CREATE INDEX IF NOT EXISTS idx_teams_event_id ON teams(event_id);

-- Add application_deadline column if not already done  
ALTER TABLE teams ADD COLUMN application_deadline DATE;
CREATE INDEX IF NOT EXISTS idx_teams_deadline ON teams(application_deadline);

-- Verify the changes
SELECT 'Hackathons created:' as status, COUNT(*) as count FROM hackathons;
SELECT 'Teams table columns:' as status;
PRAGMA table_info(teams);

-- Show the created events
SELECT event_id, name, status, theme FROM hackathons ORDER BY created_at;