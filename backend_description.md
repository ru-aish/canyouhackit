# HackBite Backend System

## Overview
The HackBite backend is a **Flask-based REST API** designed with **extensibility and future scalability** in mind. It provides user registration, authentication, and profile management services for hackathon participants, with a modular architecture that supports easy addition of new features.

## Architecture

### Core Components

#### 1. **DatabaseManager** (`backend/database.py`)
- **Purpose**: Centralized database connection and table initialization
- **Features**:
  - SQLite3 with foreign key constraints enabled
  - Row factory for dict-like access to query results
  - Automatic table initialization from SQL schema
  - Connection management with proper error handling

#### 2. **UserManager** (`backend/database.py`)
- **Purpose**: Complete user lifecycle management
- **Features**:
  - Secure password hashing (SHA-256)
  - Email uniqueness validation
  - Avatar system with SVG support
  - Extended profile information storage
  - Activity logging for security and analytics
  - Extensible user registration with **kwargs support

#### 3. **SkillManager** (`backend/database.py`)
- **Purpose**: Skills and categories management for team matching
- **Features**:
  - Hierarchical skill categorization
  - Proficiency level tracking
  - User-skill relationship management
  - Future team matching algorithm support

#### 4. **SystemManager** (`backend/database.py`)
- **Purpose**: Configuration and system settings management
- **Features**:
  - Type-safe setting storage (string, integer, boolean, JSON)
  - Runtime configuration updates
  - Default system settings initialization

### Database Schema

#### Extensible Design Principles
1. **JSON Fields**: Store complex data structures for future flexibility
2. **Activity Logging**: Track all user actions for analytics
3. **Soft Deletes**: Use `is_active` flags instead of hard deletes
4. **Audit Trails**: Created/updated timestamps on all entities
5. **Relationship Support**: Foreign keys with proper constraints

#### Key Tables
- **`users`**: Core user authentication and profile
- **`user_profiles`**: Extended profile information
- **`user_skills`**: Individual skill tracking with proficiency
- **`skill_categories`**: Organized skill taxonomy
- **`teams`**: Team formation and management
- **`hackathons`**: Multi-event support
- **`activity_logs`**: Security and analytics tracking
- **`notifications`**: User notification system
- **`system_settings`**: Runtime configuration

## API Endpoints

### User Management
```
POST   /api/register           # Register new user with extended data
POST   /api/login              # Authenticate user with activity logging
GET    /api/users              # List users (with optional profile data)
GET    /api/users/<id>         # Get specific user (with optional skills)
PUT    /api/users/<id>/profile-logo  # Update avatar
```

### Profile & Skills
```
GET    /api/profile-logos      # Get available avatars with SVG content
GET    /api/statistics         # User analytics and statistics
GET    /api/skill-categories   # Get skill taxonomy
GET    /api/skill-categories/<id>/skills  # Skills in category
```

### System Management
```
GET    /api/settings/<key>     # Get system configuration
PUT    /api/settings/<key>     # Update system configuration
GET    /health                 # Health check endpoint
```

## Avatar System

### Frontend Integration
The backend seamlessly integrates with the existing frontend avatar system:

```javascript
// Frontend avatars (login.js)
const avatars = ['rocket', 'code', 'brain', 'planet', 'abstract', 'user', 'default'];

// Backend avatar storage (database.py)
profile_logos = {
    "rocket": '<svg viewBox="0 0 24 24">...</svg>',
    "code": '<svg viewBox="0 0 24 24">...</svg>',
    // ... all avatars with SVG content
}
```

### Benefits
- **No Frontend Changes**: Existing avatar selection UI works unchanged
- **SVG Storage**: Scalable vector graphics stored in backend
- **Validation**: Backend validates avatar selection against available options
- **Extensible**: Easy to add new avatars by updating the avatar dictionary

## Future Extensibility Features

### 1. **Team Formation System**
- Ready-to-use team and team_members tables
- Leader/member role management
- Team status tracking (forming, active, completed)
- Maximum member limits with automatic enforcement

### 2. **Multi-Hackathon Support**
- Dedicated hackathons table with event management
- User participation tracking across events
- Team assignments per hackathon
- Scoring and ranking system

### 3. **Skill-Based Matching**
- Comprehensive skill taxonomy with categories
- Proficiency level tracking (beginner to expert)
- Years of experience per skill
- Primary skill designation for quick matching

### 4. **Analytics & Monitoring**
- Complete activity logging with IP and user agent
- User statistics with temporal analysis
- Popular skills and avatar distribution
- Registration trends and user engagement metrics

### 5. **Notification System**
- Built-in notification table with types and expiration
- Action URLs for interactive notifications
- Read/unread status tracking
- User-specific notification management

### 6. **System Configuration**
- Runtime configuration without code changes
- Type-safe setting storage and retrieval
- Public/private setting visibility
- Default configuration initialization

## Security Features

### 1. **Password Security**
- SHA-256 password hashing
- No plain text password storage
- Secure authentication workflow

### 2. **Data Validation**
- Email format validation
- Avatar selection validation
- SQL injection prevention with parameterized queries
- Input sanitization and trimming

### 3. **Activity Tracking**
- Login/logout event logging
- Registration attempt tracking
- Profile modification history
- Failed authentication monitoring
- IP address and user agent logging

### 4. **Database Security**
- Foreign key constraints enabled
- Transaction rollback on errors
- Proper connection management
- Error handling without data exposure

## Installation & Setup

### Requirements
```bash
# Install dependencies
pip install -r requirements.txt

# Or using UV (recommended)
uv pip install -r requirements.txt
```

### Database Initialization
```bash
# Database and tables are auto-created on first run
cd /path/to/hackbite
python backend/api_server.py
```

### Development Server
```bash
# Start API server
python backend/api_server.py

# Server runs on http://localhost:5000
# CORS enabled for frontend integration
```

## Integration with Frontend

### Existing Registration Form
The backend is designed to work seamlessly with the existing registration form in `/1/frontend/registration/`:

```javascript
// Frontend data collection (login.js)
const userData = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    password: document.getElementById('password').value,
    profile_logo: avatars[selectedAvatar] || 'default',
    location: document.getElementById('location').value,
    experience: document.getElementById('experience').value,
    skills: selectedSkills
};

// API call
const response = await fetch(`${API_BASE_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
});
```

### Response Format
```json
{
    "success": true,
    "message": "User registered successfully",
    "user_id": 1,
    "profile": {
        "name": "John Doe",
        "email": "john@example.com",
        "profile_logo": "rocket",
        "location": "San Francisco",
        "experience": "Intermediate"
    }
}
```

## Testing

### Manual Testing
```bash
# Test registration
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"testpass123","profile_logo":"rocket"}'

# Test login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Get users
curl http://localhost:5000/api/users

# Get avatars
curl http://localhost:5000/api/profile-logos
```

### Automated Testing
```bash
# Run test suite
python test/test_registration.py

# Or with pytest
pytest test/
```

## Performance Considerations

### Database Optimization
- **Indexes**: Created on frequently queried columns (email, user_id, etc.)
- **Connection Pooling**: Single connection with proper lifecycle management
- **Query Optimization**: Parameterized queries with minimal data transfer

### API Performance
- **CORS Optimization**: Configured for specific origins in production
- **Error Handling**: Graceful error responses without internal details
- **Response Caching**: Headers configured for appropriate caching

### Scalability Preparation
- **Modular Architecture**: Easy to split into microservices
- **Database Abstraction**: Can migrate from SQLite to PostgreSQL/MySQL
- **Configuration Management**: Runtime settings for easy deployment

## Production Deployment

### Environment Configuration
```bash
# Set production environment
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:pass@host:port/db

# Configure CORS for production
export ALLOWED_ORIGINS=https://hackbite.com,https://app.hackbite.com
```

### Security Recommendations
1. Use environment variables for sensitive configuration
2. Enable HTTPS in production
3. Configure proper CORS origins
4. Set up database backups
5. Monitor activity logs for suspicious behavior
6. Implement rate limiting for API endpoints

### Monitoring
- Health check endpoint: `/health`
- User statistics endpoint: `/api/statistics`
- Activity log monitoring via database queries
- Error tracking through application logs

---

## Summary

The HackBite backend provides a **robust, extensible foundation** for hackathon team formation and user management. Its modular architecture and comprehensive feature set make it ready for both immediate use and future enhancements, while maintaining seamless integration with the existing frontend interface.