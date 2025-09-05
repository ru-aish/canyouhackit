from flask import Flask, request, jsonify
from flask_cors import CORS
from database import DatabaseManager, UserManager, SkillManager, SystemManager, TeamManager
import json

app = Flask(__name__)
CORS(app)

# Global managers
db_manager = None
user_manager = None
skill_manager = None
system_manager = None
team_manager = None

def initialize_app():
    """Initialize the Flask app with database connections"""
    global db_manager, user_manager, skill_manager, system_manager, team_manager
    try:
        db_manager = DatabaseManager()
        if not db_manager.connect():
            raise Exception("Failed to connect to database")
        
        # Initialize tables
        db_manager.initialize_tables()
        
        # Initialize managers
        user_manager = UserManager(db_manager)
        skill_manager = SkillManager(db_manager)
        system_manager = SystemManager(db_manager)
        team_manager = TeamManager(db_manager)
        
        print("✅ Flask app initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app initialization failed: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "HackBite API is running"})

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Extract required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        profile_logo = data.get('profile_logo', 'default')
        
        # Extract optional fields
        location = data.get('location', '').strip() or None
        experience = data.get('experience', '').strip() or None
        skills = data.get('skills', [])
        
        # Validate required fields
        if not all([name, email, password]):
            return jsonify({"success": False, "message": "Name, email, and password are required"}), 400
        
        # Register user with extensible parameters
        result = user_manager.register_user(
            name=name,
            email=email,
            password=password,
            profile_logo=profile_logo,
            location=location,
            experience=experience,
            skills=skills,
            **{k: v for k, v in data.items() if k not in ['name', 'email', 'password', 'profile_logo', 'location', 'experience', 'skills']}
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Registration failed: {str(e)}"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate user login"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        # Get client info for activity logging
        ip_address = request.environ.get('REMOTE_ADDR')
        user_agent = request.headers.get('User-Agent')
        
        result = user_manager.authenticate_user(email, password, ip_address, user_agent)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Login failed: {str(e)}"}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        include_profiles = request.args.get('include_profiles', 'false').lower() == 'true'
        result = user_manager.get_all_users(include_profiles=include_profiles)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get users: {str(e)}"}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        include_skills = request.args.get('include_skills', 'false').lower() == 'true'
        result = user_manager.get_user_by_id(user_id, include_skills=include_skills)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404 if "not found" in result['message'].lower() else 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get user: {str(e)}"}), 500

@app.route('/api/users/<int:user_id>/profile-logo', methods=['PUT'])
def update_profile_logo(user_id):
    """Update user's profile logo"""
    try:
        data = request.get_json()
        profile_logo = data.get('profile_logo', '').strip()
        
        if not profile_logo:
            return jsonify({"success": False, "message": "Profile logo is required"}), 400
        
        result = user_manager.update_profile_logo(user_id, profile_logo)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400 if "Invalid" in result['message'] else 404
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to update profile logo: {str(e)}"}), 500

@app.route('/api/profile-logos', methods=['GET'])
def get_profile_logos():
    """Get available profile logos"""
    try:
        logos = user_manager.get_available_logos()
        return jsonify({
            "success": True,
            "logos": logos,
            "avatar_names": list(logos.keys())
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get logos: {str(e)}"}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get user statistics"""
    try:
        result = user_manager.get_user_statistics()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get statistics: {str(e)}"}), 500

@app.route('/api/skill-categories', methods=['GET'])
def get_skill_categories():
    """Get all skill categories"""
    try:
        result = skill_manager.get_skill_categories()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get skill categories: {str(e)}"}), 500

@app.route('/api/skill-categories/<int:category_id>/skills', methods=['GET'])
def get_skills_by_category(category_id):
    """Get skills in a specific category"""
    try:
        result = skill_manager.get_skills_by_category(category_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get skills: {str(e)}"}), 500

@app.route('/api/settings/<setting_key>', methods=['GET'])
def get_system_setting(setting_key):
    """Get a system setting"""
    try:
        value = system_manager.get_setting(setting_key)
        
        if value is not None:
            return jsonify({"success": True, "setting_key": setting_key, "value": value}), 200
        else:
            return jsonify({"success": False, "message": "Setting not found"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get setting: {str(e)}"}), 500

@app.route('/api/settings/<setting_key>', methods=['PUT'])
def update_system_setting(setting_key):
    """Update a system setting"""
    try:
        data = request.get_json()
        value = data.get('value')
        setting_type = data.get('type', 'string')
        
        if value is None:
            return jsonify({"success": False, "message": "Value is required"}), 400
        
        success = system_manager.update_setting(setting_key, value, setting_type)
        
        if success:
            return jsonify({"success": True, "message": "Setting updated successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to update setting"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to update setting: {str(e)}"}), 500

# Team Management Endpoints

@app.route('/api/teams', methods=['POST'])
def create_team():
    """Create a new team"""
    try:
        data = request.get_json()
        
        # Extract required fields
        team_name = data.get('team_name', '').strip()
        description = data.get('description', '').strip()
        leader_id = data.get('leader_id')
        
        # Extract optional fields
        max_members = data.get('max_members', 4)
        application_deadline = data.get('application_deadline')
        tech_stack = data.get('tech_stack', [])
        project_idea = data.get('project_idea', '').strip()
        
        # Validate required fields
        if not all([team_name, description, leader_id]):
            return jsonify({"success": False, "message": "Team name, description, and leader ID are required"}), 400
        
        # Create team
        result = team_manager.create_team(
            team_name=team_name,
            description=description,
            leader_id=leader_id,
            max_members=max_members,
            application_deadline=application_deadline,
            tech_stack=tech_stack,
            project_idea=project_idea
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Team creation failed: {str(e)}"}), 500

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all teams"""
    try:
        status = request.args.get('status', 'forming')
        include_members = request.args.get('include_members', 'false').lower() == 'true'
        
        result = team_manager.get_all_teams(status=status, include_members=include_members)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get teams: {str(e)}"}), 500

@app.route('/api/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """Get team by ID"""
    try:
        include_members = request.args.get('include_members', 'true').lower() == 'true'
        
        result = team_manager.get_team_by_id(team_id, include_members=include_members)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404 if "not found" in result['message'].lower() else 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get team: {str(e)}"}), 500

@app.route('/api/teams/<int:team_id>/join', methods=['POST'])
def join_team(team_id):
    """Join a team"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"success": False, "message": "User ID is required"}), 400
        
        result = team_manager.join_team(team_id, user_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to join team: {str(e)}"}), 500

@app.route('/api/teams/<int:team_id>/leave', methods=['POST'])
def leave_team(team_id):
    """Leave a team"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"success": False, "message": "User ID is required"}), 400
        
        result = team_manager.leave_team(team_id, user_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to leave team: {str(e)}"}), 500

@app.route('/api/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    """Update team details"""
    try:
        data = request.get_json()
        leader_id = data.get('leader_id')
        
        if not leader_id:
            return jsonify({"success": False, "message": "Leader ID is required"}), 400
        
        # Remove leader_id from updates
        updates = {k: v for k, v in data.items() if k != 'leader_id'}
        
        result = team_manager.update_team(team_id, leader_id, **updates)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to update team: {str(e)}"}), 500

@app.route('/api/teams/search', methods=['GET'])
def search_teams():
    """Search teams with filters"""
    try:
        search_term = request.args.get('q')
        tech_stack = request.args.getlist('tech')
        min_members = request.args.get('min_members', type=int)
        max_members = request.args.get('max_members', type=int)
        status = request.args.get('status', 'forming')
        
        max_members_range = None
        if min_members is not None and max_members is not None:
            max_members_range = (min_members, max_members)
        
        result = team_manager.search_teams(
            search_term=search_term,
            tech_stack=tech_stack if tech_stack else None,
            max_members_range=max_members_range,
            status=status
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to search teams: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"success": False, "message": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({"success": False, "message": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"success": False, "message": "Internal server error"}), 500

if __name__ == '__main__':
    if initialize_app():
        print("🚀 Starting HackBite Registration API Server...")
        print("📍 API Endpoints:")
        print("  POST /api/register - Register new user")
        print("  POST /api/login - Login user")
        print("  GET /api/users - Get all users")
        print("  GET /api/users/<id> - Get user by ID")
        print("  GET /api/profile-logos - Get available logos")
        print("  PUT /api/users/<id>/profile-logo - Update profile logo")
        print("  GET /api/statistics - Get user statistics")
        print("  GET /api/skill-categories - Get skill categories")
        print("  GET /api/skill-categories/<id>/skills - Get skills by category")
        print("  GET /api/settings/<key> - Get system setting")
        print("  PUT /api/settings/<key> - Update system setting")
        print("  POST /api/teams - Create new team")
        print("  GET /api/teams - Get all teams")
        print("  GET /api/teams/<id> - Get team by ID")
        print("  POST /api/teams/<id>/join - Join team")
        print("  POST /api/teams/<id>/leave - Leave team")
        print("  PUT /api/teams/<id> - Update team")
        print("  GET /api/teams/search - Search teams")
        print("  GET /health - Health check")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize app. Exiting...")
        exit(1)