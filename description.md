# HackBite Application - Database Schema & System Description

This document describes the database schema and system architecture for the HackBite application, which facilitates team formation for hackathons, study groups, and gaming communities.

## Recent Updates & New Features

### Dynamic Hackathon Management System
- **Database-driven Hackathons**: Hackathons are now stored in the database and displayed dynamically on the frontend
- **Team Request System**: Users can apply to join teams for specific hackathons with duplicate prevention
- **Hackathon Tracking**: Each team request is linked to a specific hackathon to prevent multiple applications

### Enhanced Frontend Features
- **Dynamic Content Loading**: Hackathon cards are generated from database content via REST API
- **Status Indicators**: Real-time hackathon status display (active, upcoming, completed)
- **Smart Navigation**: Look for Teams button passes hackathon context to application page
- **Duplicate Prevention**: Users cannot apply for the same hackathon multiple times

## Database Schema

### Core Tables

#### 1. users
**Purpose**: Core user authentication and profile information
- `user_id` (Primary Key, Auto-increment) - Unique identifier for each user
- `name` (VARCHAR, Required) - User's display name
- `email` (VARCHAR, Unique, Required) - User's email address for login and communication
- `password_hash` (VARCHAR, Required) - Encrypted password for authentication
- `profile_logo` (VARCHAR, Default: 'default') - User's profile avatar selection
- `location` (VARCHAR, Optional) - User's geographical location
- `experience` (VARCHAR, Optional) - User's experience level description
- `created_at` (TIMESTAMP) - Account creation timestamp
- `updated_at` (TIMESTAMP) - Last profile update timestamp
- `is_active` (BOOLEAN, Default: 1) - Account status flag
- `bio` (TEXT, Optional) - User biography
- `contact_info` (TEXT, Optional) - Additional contact information
- `social_links` (JSON, Optional) - Social media profiles
- `preferences` (JSON, Optional) - User preferences and settings
- `status` (VARCHAR, Default: 'active') - Account status

#### 2. hackathons
**Purpose**: Stores hackathon event information and details
- `hackathon_id` (Primary Key, Auto-increment) - Unique identifier for each hackathon
- `name` (VARCHAR, Required) - Hackathon display name
- `description` (TEXT, Optional) - Detailed hackathon description
- `start_date` (TIMESTAMP) - Event start date and time
- `end_date` (TIMESTAMP) - Event end date and time
- `registration_deadline` (TIMESTAMP) - Registration cutoff date
- `max_participants` (INT) - Maximum number of participants allowed
- `current_participants` (INT, Default: 0) - Current participant count
- `status` (VARCHAR, Default: 'upcoming') - Event status (upcoming, active, completed, cancelled)
- `theme` (VARCHAR, Optional) - Hackathon theme or focus area
- `prizes` (JSON, Optional) - Prize information and structure
- `rules` (TEXT, Optional) - Event rules and guidelines
- `created_at` (TIMESTAMP) - Record creation timestamp
- `updated_at` (TIMESTAMP) - Last update timestamp

#### 3. team_requests *(NEW)*
**Purpose**: Manages user applications to join teams for specific hackathons
- `request_id` (Primary Key, Auto-increment) - Unique identifier for each request
- `hackathon_id` (Foreign Key → hackathons.hackathon_id) - Links to specific hackathon
- `user_email` (VARCHAR, Required) - Applicant's email address
- `message` (TEXT, Required) - User's application message/introduction
- `status` (VARCHAR, Default: 'pending') - Request status (pending, approved, rejected)
- `created_at` (TIMESTAMP) - Application submission timestamp
- `updated_at` (TIMESTAMP) - Last status update timestamp
- **UNIQUE Constraint**: (hackathon_id, user_email) - Prevents duplicate applications

#### 4. user_profiles
**Purpose**: Extended user profile information for matching and team formation
- `profile_id` (Primary Key, Auto-increment) - Unique identifier for each profile
- `user_id` (Foreign Key → users.user_id) - Links to the main user account
- `github_username` (VARCHAR, Optional) - GitHub profile username
- `linkedin_profile` (VARCHAR, Optional) - LinkedIn profile URL
- `portfolio_url` (VARCHAR, Optional) - Personal portfolio website
- `timezone` (VARCHAR, Optional) - User's timezone for coordination
- `availability` (JSON, Optional) - Availability schedule information
- `communication_preference` (VARCHAR, Default: 'email') - Preferred communication method
- `team_role_preference` (VARCHAR, Optional) - Preferred role in teams
- `hackathon_experience` (INT, Default: 0) - Number of hackathons participated
- `achievements` (JSON, Optional) - Awards and achievements
- `interests` (JSON, Optional) - Personal interests and hobbies
- `created_at` (TIMESTAMP) - Profile creation timestamp
- `updated_at` (TIMESTAMP) - Last profile update timestamp

#### 5. teams
**Purpose**: Team information and requirements for different activities
- `team_id` (Primary Key, Auto-increment) - Unique identifier for each team
- `team_name` (VARCHAR, Required) - Display name for the team
- `description` (TEXT, Optional) - Detailed team description and goals
- `max_members` (INT, Default: 4) - Maximum number of team members allowed
- `current_members` (INT, Default: 0) - Current team member count
- `leader_id` (Foreign Key → users.user_id) - Team leader/creator
- `status` (VARCHAR, Default: 'forming') - Team status (forming, active, completed, disbanded)
- `hackathon_id` (INT, Optional) - Associated hackathon (for multi-hackathon support)
- `tech_stack` (JSON, Optional) - Preferred technologies and tools
- `project_idea` (TEXT, Optional) - Team's project concept
- `created_at` (TIMESTAMP) - Team creation timestamp
- `updated_at` (TIMESTAMP) - Last team update timestamp

#### 6. user_skills
**Purpose**: User skills and competencies for team matching
- `skill_id` (Primary Key, Auto-increment) - Unique identifier for each skill entry
- `user_id` (Foreign Key → users.user_id) - Links to user account
- `skill_name` (VARCHAR, Required) - Name of the skill
- `proficiency_level` (VARCHAR, Default: 'intermediate') - Skill level (beginner, intermediate, advanced, expert)
- `years_experience` (INT, Default: 0) - Years of experience with this skill
- `is_primary_skill` (BOOLEAN, Default: 0) - Whether this is a primary skill
- `created_at` (TIMESTAMP) - Skill addition timestamp

### Supporting Tables

#### 7. skill_categories
**Purpose**: Organizes skills into categories for better management
- `category_id` (Primary Key, Auto-increment) - Unique identifier
- `category_name` (VARCHAR, Unique) - Category name
- `description` (TEXT, Optional) - Category description
- `icon` (VARCHAR, Optional) - Icon identifier for UI
- `color_code` (VARCHAR, Optional) - Color code for UI theming
- `is_active` (BOOLEAN, Default: 1) - Category status

#### 8. team_members
**Purpose**: Manages team membership and member roles
- `member_id` (Primary Key, Auto-increment) - Unique identifier for each membership
- `team_id` (Foreign Key → teams.team_id) - Links to the team
- `user_id` (Foreign Key → users.user_id) - Links to the user
- `role` (VARCHAR, Default: 'member') - Member's role (leader, member, mentor)
- `joined_at` (TIMESTAMP) - When the user joined the team
- `status` (VARCHAR, Default: 'active') - Membership status (active, inactive, left)
- `contribution_score` (INT, Default: 0) - For future gamification features

## API Endpoints

### Hackathon Management
- `GET /api/hackathons` - Retrieve all hackathons with optional status filtering
- `GET /api/hackathons/<id>` - Get specific hackathon details

### Team Request System *(NEW)*
- `POST /api/team-requests` - Submit team join request for a hackathon
- `GET /api/team-requests/check` - Check if user already applied for a hackathon
- `GET /api/team-requests` - Get team requests with filtering options

### User Management
- `POST /api/register` - Register new user account
- `POST /api/login` - User authentication
- `GET /api/users` - Get all users with optional profile inclusion
- `GET /api/users/<id>` - Get specific user details
- `PUT /api/users/<id>/profile-logo` - Update user profile avatar

### Team Management
- `POST /api/teams` - Create new team
- `GET /api/teams` - Get teams with status and member filtering
- `GET /api/teams/<id>` - Get specific team details
- `POST /api/teams/<id>/join` - Join a team
- `POST /api/teams/<id>/leave` - Leave a team
- `PUT /api/teams/<id>` - Update team information
- `GET /api/teams/search` - Search teams with multiple filters

## Key Features

### 1. Dynamic Hackathon Management
- **Database-driven Content**: Hackathons stored in database, displayed dynamically
- **Real-time Status**: Live status updates (active, upcoming, completed, cancelled)
- **Easy Management**: Add/modify hackathons through database without code changes

### 2. Smart Team Request System
- **Hackathon-specific Applications**: Each request linked to specific hackathon
- **Duplicate Prevention**: Users cannot apply for same hackathon multiple times
- **Context Preservation**: Hackathon information passed through navigation flow
- **Status Tracking**: Track application status and user journey

### 3. User Experience Enhancements
- **Smart Navigation**: Seamless flow from hackathon selection to team application
- **Form Pre-filling**: Email addresses remembered for convenience
- **Visual Feedback**: Clear status indicators and error messages
- **Responsive Design**: Works across different screen sizes

### 4. Data Integrity & Security
- **Unique Constraints**: Prevent duplicate applications at database level
- **Foreign Key Relationships**: Maintain data consistency across tables
- **Input Validation**: Both frontend and backend validation
- **Error Handling**: Comprehensive error handling with user-friendly messages

### 5. Extensibility Features
- **Multi-category Support**: Ready for hackathons, study groups, and gaming
- **Skill Matching**: Advanced skill-based team formation capabilities
- **Gamification Ready**: Contribution scoring and achievement systems
- **Analytics Support**: Activity logging for future insights

## Frontend Architecture

### Dynamic Content Loading
- **API Integration**: Frontend fetches data from REST API endpoints
- **Error Handling**: Graceful handling of network errors with retry options
- **Loading States**: User-friendly loading indicators and status messages
- **Local Storage**: Smart caching of user preferences and email addresses

### Component Structure
- **Hackathon Cards**: Dynamically generated from database content
- **Form Handling**: Smart forms with validation and duplicate detection
- **Navigation Flow**: Context-aware navigation between pages
- **Status Management**: Real-time status updates and user feedback

## Database Relationships

### Primary Relationships
- **users** ↔ **user_profiles**: One-to-One (Extended profile information)
- **users** ↔ **teams**: One-to-Many (Users can create multiple teams)
- **teams** ↔ **team_members**: One-to-Many (Teams have multiple members)
- **users** ↔ **team_members**: One-to-Many (Users can join multiple teams)
- **hackathons** ↔ **team_requests**: One-to-Many (Hackathons have multiple requests)
- **users** ↔ **user_skills**: One-to-Many (Users have multiple skills)

### Data Integrity
- **Foreign Key Constraints**: Ensure referential integrity
- **Unique Constraints**: Prevent duplicate data where appropriate
- **Check Constraints**: Validate data at database level
- **Indexes**: Optimize query performance for common operations

## SQL Statements

### Create Tables

```sql
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

-- Team requests for hackathon applications
CREATE TABLE IF NOT EXISTS team_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hackathon_id INTEGER NOT NULL,
    user_email TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id) ON DELETE CASCADE,
    UNIQUE(hackathon_id, user_email)
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

-- User ratings for AI-powered team matching
CREATE TABLE IF NOT EXISTS user_ratings (
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
CREATE INDEX IF NOT EXISTS idx_team_requests_hackathon ON team_requests(hackathon_id);
CREATE INDEX IF NOT EXISTS idx_team_requests_email ON team_requests(user_email);
CREATE INDEX IF NOT EXISTS idx_team_requests_status ON team_requests(status);
CREATE INDEX IF NOT EXISTS idx_user_ratings_user_id ON user_ratings(user_id);
```

### Insert Default Data

```sql
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
```