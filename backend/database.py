import sqlite3
import hashlib
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone
import os
from pathlib import Path

class DatabaseManager:
    """Enhanced database manager with extensible architecture for future features"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Use relative path from the project root
            project_root = Path(__file__).parent.parent
            self.db_path = str(project_root / "database" / "database.db")
        else:
            self.db_path = db_path
        self.connection = None
        
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            # Ensure database directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            self.connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            
    def initialize_tables(self):
        """Initialize all database tables from SQL file"""
        try:
            # Get SQL file path relative to project root
            project_root = Path(__file__).parent.parent
            sql_file = project_root / "sql" / "create_tables.sql"
            
            with open(sql_file, "r") as f:
                schema_sql = f.read()
            
            # Execute the entire schema
            self.connection.executescript(schema_sql)
            self.connection.commit()
            print("✅ Database tables initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Error initializing tables: {e}")
            return False

class UserManager:
    """Enhanced user management with future extensibility"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        # Avatar configuration matching frontend
        self.profile_logos = {
            "rocket": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 16.5-1.5 22M18 6l-5.5 5.5M13 2 2 13l3.5 3.5L18 4l-2-2Z"/><path d="m2 22 5.5-1.5M16.5 5.5 22 1.5M9 15l-1.5 1.5a2.828 2.828 0 1 0 4 4l1.5-1.5"/></svg>',
            "code": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
            "brain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a4.5 4.5 0 0 0-4.5 4.5c0 1.05.38 2.05.97 2.85L7 11.5v2.85c0 .3.15.58.4.75L12 18.5l4.6-3.4c.25-.17.4-.45.4-.75V11.5L15.53 9.35A4.5 4.5 0 0 0 12 2Z"/><path d="M12 2v4.5"/><path d="m16.5 6.5-3 3"/><path d="m7.5 6.5 3 3"/><path d="M12 18.5v3.5"/><path d="m7.5 14.5-5 2.5"/><path d="m16.5 14.5 5 2.5"/></svg>',
            "planet": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10c0-4.42-2.86-8.17-6.84-9.51"/><path d="M17.55 16.5A6.5 6.5 0 0 1 8 12.5a6.51 6.51 0 0 1 1.45-4"/></svg>',
            "abstract": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.42 12.61a2.1 2.1 0 1 1 2.97 2.97L7.95 21 2 22l1-5.95Z"/><path d="m16.5 5.5 2.97-2.97a2.1 2.1 0 0 1 2.97 0h0a2.1 2.1 0 0 1 0 2.97L19.53 8.47"/><path d="M15 3h6v6"/><path d="M2.12 15.88a2.1 2.1 0 0 1 0-2.97L5.05 10a2.1 2.1 0 0 1 2.97 0L12 13.92"/></svg>',
            "user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
            "default": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
        }

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _log_activity(self, user_id: Optional[int], activity_type: str, activity_data: Optional[Dict] = None, 
                     ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """Log user activity for analytics and security"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                INSERT INTO activity_logs (user_id, activity_type, activity_data, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, activity_type, json.dumps(activity_data) if activity_data else None, 
                  ip_address, user_agent))
            self.db.connection.commit()
        except Exception as e:
            print(f"Failed to log activity: {e}")

    def register_user(self, name: str, email: str, password: str, profile_logo: str = "default",
                     location: Optional[str] = None, experience: Optional[str] = None,
                     skills: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Register a new user with extensible parameters
        
        Args:
            name: User's full name
            email: User's email address
            password: Plain text password (will be hashed)
            profile_logo: Avatar identifier
            location: User's location
            experience: User's experience level
            skills: List of user skills
            **kwargs: Additional user data for future extensibility
        """
        try:
            cursor = self.db.connection.cursor()
            
            # Validate profile logo
            if profile_logo not in self.profile_logos:
                profile_logo = "default"
            
            # Check if email already exists
            cursor.execute("SELECT user_id FROM users WHERE email = ?", (email.lower(),))
            if cursor.fetchone():
                self._log_activity(None, "registration_failed", {"reason": "email_exists", "email": email})
                return {"success": False, "message": "Email already exists"}
            
            # Hash password
            password_hash = self._hash_password(password)
            
            # Insert user record
            cursor.execute("""
                INSERT INTO users (name, email, password_hash, profile_logo, location, experience)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email.lower(), password_hash, profile_logo, location, experience))
            
            user_id = cursor.lastrowid
            
            # Create extended profile
            self._create_user_profile(user_id, **kwargs)
            
            # Add user skills if provided
            if skills:
                self._add_user_skills(user_id, skills)
            
            self.db.connection.commit()
            
            # Log successful registration
            self._log_activity(user_id, "user_registered", {
                "email": email, "profile_logo": profile_logo, "has_skills": bool(skills)
            })
            
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": user_id,
                "profile": {
                    "name": name,
                    "email": email,
                    "profile_logo": profile_logo,
                    "location": location,
                    "experience": experience
                }
            }
            
        except Exception as e:
            self.db.connection.rollback()
            self._log_activity(None, "registration_failed", {"reason": "database_error", "error": str(e)})
            return {"success": False, "message": f"Registration failed: {str(e)}"}

    def _create_user_profile(self, user_id: int, **kwargs):
        """Create extended user profile with optional fields"""
        try:
            cursor = self.db.connection.cursor()
            
            # Extract known profile fields
            profile_fields = {
                'github_username': kwargs.get('github_username'),
                'linkedin_profile': kwargs.get('linkedin_profile'),
                'portfolio_url': kwargs.get('portfolio_url'),
                'timezone': kwargs.get('timezone'),
                'availability': json.dumps(kwargs.get('availability')) if kwargs.get('availability') else None,
                'communication_preference': kwargs.get('communication_preference', 'email'),
                'team_role_preference': kwargs.get('team_role_preference'),
                'hackathon_experience': kwargs.get('hackathon_experience', 0),
                'achievements': json.dumps(kwargs.get('achievements')) if kwargs.get('achievements') else None,
                'interests': json.dumps(kwargs.get('interests')) if kwargs.get('interests') else None
            }
            
            cursor.execute("""
                INSERT INTO user_profiles 
                (user_id, github_username, linkedin_profile, portfolio_url, timezone, availability,
                 communication_preference, team_role_preference, hackathon_experience, achievements, interests)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, *profile_fields.values()))
            
        except Exception as e:
            print(f"Failed to create user profile: {e}")

    def _add_user_skills(self, user_id: int, skills: List[str], proficiency_levels: Optional[List[str]] = None):
        """Add skills for a user"""
        try:
            cursor = self.db.connection.cursor()
            
            for i, skill in enumerate(skills):
                proficiency = proficiency_levels[i] if proficiency_levels and i < len(proficiency_levels) else 'intermediate'
                
                cursor.execute("""
                    INSERT OR IGNORE INTO user_skills (user_id, skill_name, proficiency_level)
                    VALUES (?, ?, ?)
                """, (user_id, skill.strip(), proficiency))
                
        except Exception as e:
            print(f"Failed to add user skills: {e}")

    def authenticate_user(self, email: str, password: str, ip_address: Optional[str] = None,
                         user_agent: Optional[str] = None) -> Dict[str, Any]:
        """Authenticate user with activity logging"""
        try:
            cursor = self.db.connection.cursor()
            password_hash = self._hash_password(password)
            
            cursor.execute("""
                SELECT user_id, name, email, profile_logo, location, experience, is_active
                FROM users WHERE email = ? AND password_hash = ?
            """, (email.lower(), password_hash))
            
            user = cursor.fetchone()
            
            if user and user['is_active']:
                user_dict = dict(user)
                self._log_activity(user['user_id'], "user_login", 
                                 {"email": email}, ip_address, user_agent)
                return {"success": True, "user": user_dict}
            else:
                self._log_activity(None, "login_failed", 
                                 {"email": email, "reason": "invalid_credentials"}, ip_address, user_agent)
                return {"success": False, "message": "Invalid credentials"}
                
        except Exception as e:
            self._log_activity(None, "login_failed", 
                             {"email": email, "reason": "database_error", "error": str(e)}, ip_address, user_agent)
            return {"success": False, "message": f"Authentication failed: {str(e)}"}

    def get_all_users(self, include_profiles: bool = False) -> Dict[str, Any]:
        """Get all users with optional profile information"""
        try:
            cursor = self.db.connection.cursor()
            
            if include_profiles:
                query = """
                    SELECT u.user_id, u.name, u.email, u.profile_logo, u.location, u.experience,
                           u.created_at, u.is_active,
                           p.github_username, p.linkedin_profile, p.portfolio_url,
                           p.communication_preference, p.team_role_preference, p.hackathon_experience
                    FROM users u
                    LEFT JOIN user_profiles p ON u.user_id = p.user_id
                    WHERE u.is_active = 1
                    ORDER BY u.created_at DESC
                """
            else:
                query = """
                    SELECT user_id, name, email, profile_logo, location, experience, created_at
                    FROM users WHERE is_active = 1
                    ORDER BY created_at DESC
                """
            
            cursor.execute(query)
            users = [dict(row) for row in cursor.fetchall()]
            
            return {"success": True, "users": users}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to retrieve users: {str(e)}"}

    def get_user_by_id(self, user_id: int, include_skills: bool = False) -> Dict[str, Any]:
        """Get user by ID with optional skills"""
        try:
            cursor = self.db.connection.cursor()
            
            # Get user and profile data
            cursor.execute("""
                SELECT u.*, p.github_username, p.linkedin_profile, p.portfolio_url,
                       p.timezone, p.communication_preference, p.team_role_preference,
                       p.hackathon_experience, p.achievements, p.interests
                FROM users u
                LEFT JOIN user_profiles p ON u.user_id = p.user_id
                WHERE u.user_id = ? AND u.is_active = 1
            """, (user_id,))
            
            user = cursor.fetchone()
            if not user:
                return {"success": False, "message": "User not found"}
            
            user_dict = dict(user)
            
            # Parse JSON fields
            for field in ['achievements', 'interests']:
                if user_dict.get(field):
                    try:
                        user_dict[field] = json.loads(user_dict[field])
                    except:
                        user_dict[field] = None
            
            # Get user skills if requested
            if include_skills:
                cursor.execute("""
                    SELECT skill_name, proficiency_level, years_experience, is_primary_skill
                    FROM user_skills WHERE user_id = ?
                    ORDER BY is_primary_skill DESC, proficiency_level DESC
                """, (user_id,))
                user_dict['skills'] = [dict(row) for row in cursor.fetchall()]
            
            return {"success": True, "user": user_dict}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to retrieve user: {str(e)}"}

    def update_profile_logo(self, user_id: int, profile_logo: str) -> Dict[str, Any]:
        """Update user's profile logo"""
        try:
            if profile_logo not in self.profile_logos:
                return {"success": False, "message": "Invalid profile logo"}
            
            cursor = self.db.connection.cursor()
            cursor.execute("""
                UPDATE users SET profile_logo = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (profile_logo, user_id))
            
            if cursor.rowcount == 0:
                return {"success": False, "message": "User not found"}
            
            self.db.connection.commit()
            self._log_activity(user_id, "profile_updated", {"field": "profile_logo", "new_value": profile_logo})
            
            return {"success": True, "message": "Profile logo updated successfully"}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to update profile logo: {str(e)}"}

    def get_available_logos(self) -> Dict[str, str]:
        """Get available profile logos with their SVG content"""
        return self.profile_logos.copy()

    def get_user_statistics(self) -> Dict[str, Any]:
        """Get user statistics for analytics"""
        try:
            cursor = self.db.connection.cursor()
            
            # Basic user stats
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            total_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE created_at >= date('now', '-7 days')")
            weekly_registrations = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE created_at >= date('now', '-30 days')")
            monthly_registrations = cursor.fetchone()[0]
            
            # Most popular skills
            cursor.execute("""
                SELECT skill_name, COUNT(*) as count
                FROM user_skills
                GROUP BY skill_name
                ORDER BY count DESC
                LIMIT 10
            """)
            popular_skills = [dict(row) for row in cursor.fetchall()]
            
            # Most popular avatars
            cursor.execute("""
                SELECT profile_logo, COUNT(*) as count
                FROM users
                WHERE is_active = 1
                GROUP BY profile_logo
                ORDER BY count DESC
            """)
            avatar_stats = [dict(row) for row in cursor.fetchall()]
            
            return {
                "success": True,
                "statistics": {
                    "total_users": total_users,
                    "weekly_registrations": weekly_registrations,
                    "monthly_registrations": monthly_registrations,
                    "popular_skills": popular_skills,
                    "avatar_distribution": avatar_stats
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Failed to get statistics: {str(e)}"}

class SkillManager:
    """Manage skills and skill categories for future team matching"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_skill_categories(self) -> Dict[str, Any]:
        """Get all skill categories"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT * FROM skill_categories 
                WHERE is_active = 1 
                ORDER BY category_name
            """)
            categories = [dict(row) for row in cursor.fetchall()]
            return {"success": True, "categories": categories}
        except Exception as e:
            return {"success": False, "message": f"Failed to get categories: {str(e)}"}
    
    def get_skills_by_category(self, category_id: int) -> Dict[str, Any]:
        """Get skills in a specific category"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT DISTINCT us.skill_name, COUNT(*) as user_count
                FROM user_skills us
                JOIN skill_category_mapping scm ON us.skill_name = scm.skill_name
                WHERE scm.category_id = ?
                GROUP BY us.skill_name
                ORDER BY user_count DESC, us.skill_name
            """, (category_id,))
            skills = [dict(row) for row in cursor.fetchall()]
            return {"success": True, "skills": skills}
        except Exception as e:
            return {"success": False, "message": f"Failed to get skills: {str(e)}"}

class SystemManager:
    """Manage system settings and configuration"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_setting(self, setting_key: str) -> Any:
        """Get a system setting value"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT setting_value, setting_type 
                FROM system_settings 
                WHERE setting_key = ?
            """, (setting_key,))
            result = cursor.fetchone()
            
            if not result:
                return None
            
            value, setting_type = result
            
            # Convert based on type
            if setting_type == 'integer':
                return int(value)
            elif setting_type == 'boolean':
                return value.lower() == 'true'
            elif setting_type == 'json':
                return json.loads(value)
            else:
                return value
                
        except Exception as e:
            print(f"Failed to get setting {setting_key}: {e}")
            return None
    
    def update_setting(self, setting_key: str, setting_value: Any, setting_type: str = 'string') -> bool:
        """Update a system setting"""
        try:
            cursor = self.db.connection.cursor()
            
            # Convert value to string based on type
            if setting_type == 'json':
                value_str = json.dumps(setting_value)
            elif setting_type == 'boolean':
                value_str = 'true' if setting_value else 'false'
            else:
                value_str = str(setting_value)
            
            cursor.execute("""
                INSERT OR REPLACE INTO system_settings 
                (setting_key, setting_value, setting_type, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (setting_key, value_str, setting_type))
            
            self.db.connection.commit()
            return True
            
        except Exception as e:
            print(f"Failed to update setting {setting_key}: {e}")
            return False