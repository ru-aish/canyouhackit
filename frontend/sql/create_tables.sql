-- Enhanced database schema for HackBite application with future extensibility

-- Users table with core authentication and profile information
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    profile_logo TEXT DEFAULT 'default',
    location TEXT,
    experience TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    -- Future extensibility fields
    bio TEXT,
    contact_info TEXT,
    social_links TEXT, -- JSON string for multiple social links
    preferences TEXT, -- JSON string for user preferences
    status TEXT DEFAULT 'active' -- active, inactive, suspended
);

-- User skills for future team matching features
CREATE TABLE IF NOT EXISTS user_skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    proficiency_level TEXT DEFAULT 'intermediate', -- beginner, intermediate, advanced, expert
    years_experience INTEGER DEFAULT 0,
    is_primary_skill BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, skill_name)
);

-- Skill categories for organization
CREATE TABLE IF NOT EXISTS skill_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL,
    description TEXT,
    icon TEXT,
    color_code TEXT,
    is_active BOOLEAN DEFAULT 1
);

-- Link skills to categories
CREATE TABLE IF NOT EXISTS skill_category_mapping (
    mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES skill_categories(category_id) ON DELETE CASCADE,
    UNIQUE(skill_name, category_id)
);

-- User profiles table for extended information
CREATE TABLE IF NOT EXISTS user_profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    github_username TEXT,
    linkedin_profile TEXT,
    portfolio_url TEXT,
    timezone TEXT,
    availability TEXT, -- JSON string for availability schedule
    communication_preference TEXT DEFAULT 'email', -- email, slack, discord, etc.
    team_role_preference TEXT, -- leader, member, flexible
    hackathon_experience INTEGER DEFAULT 0, -- number of hackathons participated
    achievements TEXT, -- JSON string for achievements/awards
    interests TEXT, -- JSON string for interests/hobbies
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Teams table for future team formation features
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    description TEXT,
    max_members INTEGER DEFAULT 4,
    current_members INTEGER DEFAULT 0,
    leader_id INTEGER NOT NULL,
    status TEXT DEFAULT 'forming', -- forming, active, completed, disbanded
    hackathon_id INTEGER, -- for future multi-hackathon support
    tech_stack TEXT, -- JSON string for preferred technologies
    project_idea TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (leader_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Team members relationship
CREATE TABLE IF NOT EXISTS team_members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role TEXT DEFAULT 'member', -- leader, member, mentor
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active', -- active, inactive, left
    contribution_score INTEGER DEFAULT 0, -- for future gamification
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(team_id, user_id)
);

-- Hackathons table for future multi-event support
CREATE TABLE IF NOT EXISTS hackathons (
    hackathon_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    registration_deadline TIMESTAMP,
    max_participants INTEGER,
    current_participants INTEGER DEFAULT 0,
    status TEXT DEFAULT 'upcoming', -- upcoming, active, completed, cancelled
    theme TEXT,
    prizes TEXT, -- JSON string for prize information
    rules TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User hackathon participation
CREATE TABLE IF NOT EXISTS user_hackathon_participation (
    participation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    hackathon_id INTEGER NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'registered', -- registered, checked_in, completed, no_show
    team_id INTEGER,
    final_submission TEXT, -- URL or description of submission
    score INTEGER DEFAULT 0,
    rank_position INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    UNIQUE(user_id, hackathon_id)
);

-- Activity logs for future analytics
CREATE TABLE IF NOT EXISTS activity_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    activity_type TEXT NOT NULL, -- login, logout, register, join_team, etc.
    activity_data TEXT, -- JSON string for additional data
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Notifications system for future features
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info', -- info, warning, success, error
    is_read BOOLEAN DEFAULT 0,
    action_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- System settings for configuration
CREATE TABLE IF NOT EXISTS system_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    setting_type TEXT DEFAULT 'string', -- string, integer, boolean, json
    description TEXT,
    is_public BOOLEAN DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default skill categories
INSERT OR IGNORE INTO skill_categories (category_name, description, icon, color_code) VALUES
('Frontend Development', 'UI/UX and client-side technologies', 'monitor', '#3B82F6'),
('Backend Development', 'Server-side and database technologies', 'server', '#10B981'),
('Mobile Development', 'iOS, Android, and cross-platform mobile apps', 'smartphone', '#8B5CF6'),
('Data Science', 'Data analysis, machine learning, and AI', 'bar-chart', '#F59E0B'),
('DevOps', 'Infrastructure, deployment, and operations', 'settings', '#EF4444'),
('Design', 'Visual design, UX/UI, and creative skills', 'palette', '#EC4899'),
('Project Management', 'Leadership, planning, and coordination', 'users', '#6B7280'),
('Quality Assurance', 'Testing, debugging, and quality control', 'check-circle', '#14B8A6');

-- Insert default system settings
INSERT OR IGNORE INTO system_settings (setting_key, setting_value, setting_type, description) VALUES
('max_team_size', '4', 'integer', 'Maximum number of members per team'),
('registration_open', 'true', 'boolean', 'Whether new user registration is open'),
('default_hackathon_duration', '48', 'integer', 'Default hackathon duration in hours'),
('notification_retention_days', '30', 'integer', 'How long to keep notifications'),
('avatar_options', '["rocket", "code", "brain", "planet", "abstract", "user", "default"]', 'json', 'Available profile avatar options');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_user_skills_user_id ON user_skills(user_id);
CREATE INDEX IF NOT EXISTS idx_user_skills_skill_name ON user_skills(skill_name);
CREATE INDEX IF NOT EXISTS idx_teams_leader ON teams(leader_id);
CREATE INDEX IF NOT EXISTS idx_teams_status ON teams(status);
CREATE INDEX IF NOT EXISTS idx_team_members_team ON team_members(team_id);
CREATE INDEX IF NOT EXISTS idx_team_members_user ON team_members(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_type ON activity_logs(activity_type);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_unread ON notifications(user_id, is_read);