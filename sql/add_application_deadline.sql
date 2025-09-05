-- Add application_deadline column to teams table
-- Run this migration to fix team creation

-- Add the missing application_deadline column
ALTER TABLE teams ADD COLUMN application_deadline DATE;

-- Create index for performance
CREATE INDEX IF NOT EXISTS idx_teams_deadline ON teams(application_deadline);

-- Verify the change
.schema teams