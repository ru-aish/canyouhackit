# Database Schema Description

This document describes the database schema for the HackBite application, which facilitates team formation for hackathons, study groups, and gaming communities.

## Table Descriptions

### 1. users
**Purpose**: Core user authentication and profile information
- `user_id` (Primary Key, Auto-increment) - Unique identifier for each user
- `name` (VARCHAR, Required) - User's display name
- `email` (VARCHAR, Unique, Required) - User's email address for login and communication
- `password_hash` (VARCHAR, Required) - Encrypted password for authentication
- `profile_logo` (VARCHAR, Auto-generated avatar) - URL or path to user's profile image
- `created_at` (TIMESTAMP) - Account creation timestamp

### 2. user_profiles
**Purpose**: Extended user profile information for matching and team formation
- `profile_id` (Primary Key, Auto-increment) - Unique identifier for each profile
- `user_id` (Foreign Key → users.user_id) - Links to the main user account
- `category_type` (ENUM: 'hackathon', 'study_group', 'gaming') - Primary interest category
- `skills` (JSON/TEXT - comma separated) - Technical skills and competencies
- `languages_known` (JSON/TEXT) - Programming languages and spoken languages
- `github_profile` (VARCHAR, Optional) - GitHub username for code portfolio
- `experience_level` (ENUM: 'beginner', 'intermediate', 'advanced') - Skill level indicator
- `about_me` (TEXT, Optional) - Personal description and background
- `availability_status` (TEXT) - Current availability for joining teams

### 3. teams
**Purpose**: Team information and requirements for different activities
- `team_id` (Primary Key, Auto-increment) - Unique identifier for each team
- `team_name` (VARCHAR, Required) - Display name for the team
- `category_type` (ENUM: 'hackathon', 'study_group', 'gaming') - Team's focus area
- `creator_id` (Foreign Key → users.user_id) - User who created the team
- `description` (TEXT) - Detailed team description and goals
- `max_members` (INT, Default: 5) - Maximum number of team members allowed
- `required_skills` (JSON/TEXT) - Skills needed for team members
- `status` (ENUM: 'recruiting', 'full', 'inactive') - Current team status
- `deadline` (DATETIME) - Application or project deadline
- `created_at` (TIMESTAMP) - Team creation timestamp

### 4. team_members
**Purpose**: Manages team membership and member roles
- `membership_id` (Primary Key, Auto-increment) - Unique identifier for each membership
- `team_id` (Foreign Key → teams.team_id) - Links to the team
- `user_id` (Foreign Key → users.user_id) - Links to the user
- `role` (VARCHAR, Optional) - Member's role within the team (e.g., "Frontend Developer", "Designer")
- `joined_at` (TIMESTAMP) - When the user joined the team
- `is_accepted` (BOOLEAN, Default: False) - Whether the team creator has accepted this member

## Relationships

- **users** → **user_profiles**: One-to-One relationship (each user has one profile)
- **users** → **teams**: One-to-Many relationship (users can create multiple teams)
- **teams** → **team_members**: One-to-Many relationship (teams can have multiple members)
- **users** → **team_members**: One-to-Many relationship (users can join multiple teams)

## Key Features

1. **Multi-category Support**: The system supports three main categories: hackathons, study groups, and gaming
2. **Skill Matching**: Teams can specify required skills, and users can list their skills for better matching
3. **Approval System**: Team membership requires acceptance from the team creator
4. **Flexible Team Sizes**: Teams can set their own member limits (default: 5)
5. **Status Tracking**: Teams can be in different states (recruiting, full, inactive)