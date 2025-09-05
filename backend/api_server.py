from flask import Flask, request, jsonify
from flask_cors import CORS
from database import DatabaseManager, UserManager, SkillManager, SystemManager, TeamManager
import json
import base64
import io
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

# Global managers
db_manager = None
user_manager = None
skill_manager = None
system_manager = None
team_manager = None


def extract_text_from_pdf_base64(base64_data):
    """Extract text from base64 encoded PDF data"""
    try:
        # Remove data URL prefix if present (e.g., "data:application/pdf;base64,")
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]

        # Decode base64 to bytes
        pdf_bytes = base64.b64decode(base64_data)

        # Create a BytesIO object from the bytes
        pdf_file = io.BytesIO(pdf_bytes)

        # Read PDF using PyPDF2
        pdf_reader = PdfReader(pdf_file)

        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        # Clean up the text (remove excessive whitespace)
        text = ' '.join(text.split())

        return text.strip()

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return f"[PDF TEXT EXTRACTION FAILED: {str(e)}]"


class GithubScraper:
    """
    Scrapes a GitHub profile to extract data for technical evaluation based on raw HTML.
    This version is improved to handle asynchronously loaded content like the contribution graph.
    """

    def __init__(self, username):
        self.username = username
        self.base_url = f"https://github.com/{username}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def _get_soup(self, url):
        """Fetches and parses HTML content from a URL."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_profile(self):
        """Main method to orchestrate the scraping process."""
        print(f"Starting scrape for user: {self.username}...")
        main_page_soup = self._get_soup(self.base_url)
        if not main_page_soup:
            return None

        profile_info = self._extract_profile_info(main_page_soup)

        # Asynchronously loaded contribution data
        contribution_stats = self._extract_contribution_stats(main_page_soup)

        pinned_repos_data = self._extract_pinned_repos(main_page_soup)

        analyzed_repositories = []
        if pinned_repos_data:
            print(
                f"Found {len(pinned_repos_data)} pinned repositories. Analyzing each...")
            for repo in pinned_repos_data:
                repo_details = self._scrape_repo_details(repo['url'])
                if repo_details:
                    repo.update(repo_details)
                    analyzed_repositories.append(repo)

        print("Scraping complete.")
        return {
            "profileInfo": profile_info,
            "contributionStats": contribution_stats,
            "analyzedRepositories": analyzed_repositories
        }

    def _extract_profile_info(self, soup):
        """Extracts user's full name and bio using more stable selectors."""
        name_tag = soup.find('span', itemprop='name')
        bio_tag = soup.find('div', class_='user-profile-bio')
        return {
            "fullName": name_tag.get_text(strip=True) if name_tag else "N/A",
            "bio": bio_tag.get_text(strip=True) if bio_tag else "N/A"
        }

    def _extract_contribution_stats(self, soup):
        """
        Finds the include-fragment for the contribution graph and scrapes it.
        This is more reliable as the graph is loaded asynchronously.
        """
        # The main page has a placeholder that loads the contribution graph
        contrib_fragment = soup.find(
            'include-fragment', src=re.compile(r'/users/.*/contributions'))
        if not contrib_fragment:
            # Fallback for older page structures
            day_rects_main = soup.find_all(
                'rect', class_='ContributionCalendar-day')
            if day_rects_main:
                active_days = sum(1 for day in day_rects_main if day.get(
                    'data-level') and int(day['data-level']) > 0)
                return {"totalContributionDaysInLastYear": active_days}
            return {"totalContributionDaysInLastYear": "Could not load"}

        contributions_url = f"https://github.com{contrib_fragment['src']}"
        contrib_soup = self._get_soup(contributions_url)
        if not contrib_soup:
            return {"totalContributionDaysInLastYear": "Could not load"}

        # Extract the total from the text, e.g., "53 contributions in the last year"
        h2_text = contrib_soup.find('h2', class_='f4').get_text(
            strip=True) if contrib_soup.find('h2', class_='f4') else ''
        match = re.search(r'(\d+,\d+|\d+)\s+contributions', h2_text)
        if match:
            total_contributions = int(match.group(1).replace(',', ''))
            return {"totalContributionsInLastYear": total_contributions}

        # Fallback to counting days if the total isn't found
        day_rects = contrib_soup.find_all(
            'rect', class_='ContributionCalendar-day')
        active_days = sum(1 for day in day_rects if day.get(
            'data-level') and int(day['data-level']) > 0)
        return {"totalContributionDaysInLastYear": active_days}

    def _extract_pinned_repos(self, soup):
        """Extracts basic info from pinned repositories."""
        pinned_section = soup.find(
            'div', class_='js-pinned-items-reorder-container')
        if not pinned_section:
            return []

        repos = []
        # The selector for pinned items is more reliable targeting the Box element
        pinned_items = pinned_section.find_all('div', class_='Box')
        for item in pinned_items:
            repo_link = item.find(
                'a', {'data-view-component': 'true'}, href=True)
            if not repo_link or not repo_link.find('span', class_='repo'):
                continue

            repo_url = f"https://github.com{repo_link['href']}"
            name = repo_link.find('span', class_='repo').get_text(strip=True)
            desc_tag = item.find('p', class_='pinned-item-desc')
            lang_tag = item.find('span', itemprop='programmingLanguage')
            star_tag = item.find('a', href=f"{repo_link['href']}/stargazers")
            
            # Parse star count, handling 'k' notation
            stars = 0
            if star_tag:
                star_text = star_tag.get_text(strip=True).replace(',', '')
                if 'k' in star_text.lower():
                    stars = int(float(star_text.lower().replace('k', '')) * 1000)
                elif star_text.isdigit():
                    stars = int(star_text)

            repos.append({
                "name": name,
                "url": repo_url,
                "description": desc_tag.get_text(strip=True) if desc_tag else "N/A",
                "primaryLanguage": lang_tag.get_text(strip=True) if lang_tag else "N/A",
                "stars": stars
            })
        return repos

    def _scrape_repo_details(self, repo_url):
        """Scrapes detailed information from a single repository page."""
        soup = self._get_soup(repo_url)
        if not soup:
            return None

        readme_div = soup.find('div', id='readme')
        readme_content = readme_div.get_text() if readme_div else None

        # A more reliable way to find the license is to look for a link to a license file
        license_link = soup.find('a', href=re.compile(
            r'/blob/main/LICENSE', re.IGNORECASE))

        return {
            "readme": {
                "exists": bool(readme_content),
                "contentLength": len(readme_content) if readme_content else 0
            },
            "qualityFlags": {
                "hasLicense": bool(license_link)
            }
        }


class HighlightGenerator:
    """
    Takes raw scraped GitHub data and formats it into a human-readable
    highlights report for evaluation.
    """

    def __init__(self, github_data):
        self.data = github_data

    def generate_report(self):
        """Creates the full text report."""
        profile_info = self.data.get('profileInfo', {})
        username = profile_info.get(
            'fullName') or self.data.get('username', 'N/A')
        report_lines = []

        report_lines.append("\n" + "="*50)
        report_lines.append(f"      GITHUB PROFILE HIGHLIGHTS for {username}")
        report_lines.append("="*50)

        # Work Ethic & Consistency
        contrib_stats = self.data.get('contributionStats', {})
        contributions = contrib_stats.get('totalContributionsInLastYear') or contrib_stats.get(
            'totalContributionDaysInLastYear', 0)
        contrib_type = "Total Contributions" if 'totalContributionsInLastYear' in contrib_stats else "Active Days"
        report_lines.append("\n**1. Work Ethic & Consistency:**")
        report_lines.append(
            f"* **Activity (Last Year):** {contributions} ({contrib_type}).")

        # Project Analysis
        repos = self.data.get('analyzedRepositories', [])
        report_lines.append("\n**2. Project Details (Pinned Repositories):**")

        if not repos:
            report_lines.append("* No pinned repositories found.")
        else:
            total_stars = 0
            documented_repos_count = 0
            non_trivial_projects = []

            for repo in repos:
                total_stars += repo.get('stars', 0)
                if repo.get('readme', {}).get('exists'):
                    documented_repos_count += 1
                if "solution" not in repo['name'].lower() and "leetcode" not in repo['name'].lower():
                    non_trivial_projects.append(
                        f"{repo['name']} ({repo.get('primaryLanguage', 'N/A')})")

                report_lines.append(f"* **{repo.get('name', 'N/A')}:**")
                report_lines.append(
                    f"  - **Description:** {repo.get('description', 'N/A')}")
                report_lines.append(f"  - **Stars:** {repo.get('stars', 0)}")
                report_lines.append(
                    f"  - **README:** {'Exists' if repo.get('readme', {}).get('exists') else 'MISSING'}")

        # Key Takeaways for AI Prompt
        report_lines.append("\n" + "="*50)
        report_lines.append("      KEY DATA POINTS FOR SCORING")
        report_lines.append("="*50)

        report_lines.append(f"* **IMPACT (Community Validation):**")
        report_lines.append(f"  - Total Stars on Pinned Repos: {total_stars}")

        report_lines.append(f"\n* **COMPLEXITY (Project Types):**")
        if non_trivial_projects:
            report_lines.append(
                f"  - Non-trivial projects identified: {', '.join(non_trivial_projects)}")
        else:
            report_lines.append(
                "  - Projects appear to be primarily foundational or solution-based.")

        report_lines.append(f"\n* **DOCUMENTATION (Professionalism):**")
        report_lines.append(
            f"  - README files exist for {documented_repos_count} out of {len(repos)} pinned repositories.")

        report_lines.append("\n" + "="*50)

        return "\n".join(report_lines)


def get_github_score(github_username):
    """Get GitHub profile analysis for scoring"""
    try:
        scraper = GithubScraper(github_username)
        github_data = scraper.scrape_profile()
        
        if github_data:
            reporter = HighlightGenerator(github_data)
            return reporter.generate_report()
        return "Could not analyze GitHub profile"
    except Exception as e:
        print(f"Error analyzing GitHub profile: {e}")
        return f"GitHub analysis failed: {str(e)}"


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

        result = user_manager.authenticate_user(
            email, password, ip_address, user_agent)

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
        include_profiles = request.args.get(
            'include_profiles', 'false').lower() == 'true'
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
        include_skills = request.args.get(
            'include_skills', 'false').lower() == 'true'
        result = user_manager.get_user_by_id(
            user_id, include_skills=include_skills)

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

        success = system_manager.update_setting(
            setting_key, value, setting_type)

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
        hackathon_id = data.get('hackathon_id')  # NEW: hackathon linking

        # Validate required fields
        if not all([team_name, description, leader_id]):
            return jsonify({"success": False, "message": "Team name, description, and leader ID are required"}), 400

        # If hackathon_id is provided, check if hackathon exists
        if hackathon_id:
            cursor = db_manager.connection.execute(
                "SELECT hackathon_id FROM hackathons WHERE hackathon_id = ?",
                (hackathon_id,)
            )
            if not cursor.fetchone():
                return jsonify({"success": False, "message": "Hackathon not found"}), 404

            # Check if user already created a team for this hackathon
            cursor = db_manager.connection.execute(
                "SELECT team_id, team_name FROM teams WHERE hackathon_id = ? AND leader_id = ?",
                (hackathon_id, leader_id)
            )
            existing_team = cursor.fetchone()
            if existing_team:
                return jsonify({
                    "success": False,
                    "message": f"You have already created a team '{existing_team[1]}' for this hackathon",
                    "existing_team_id": existing_team[0]
                }), 400

        # Create team
        result = team_manager.create_team(
            team_name=team_name,
            description=description,
            leader_id=leader_id,
            max_members=max_members,
            application_deadline=application_deadline,
            tech_stack=tech_stack,
            project_idea=project_idea,
            hackathon_id=hackathon_id  # NEW: pass hackathon_id
        )

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({"success": False, "message": f"Team creation failed: {str(e)}"}), 500


@app.route('/api/teams/check-existing', methods=['GET'])
def check_existing_team():
    """Check if user already created a team for a specific hackathon"""
    try:
        hackathon_id = request.args.get('hackathon_id')
        leader_id = request.args.get('leader_id')

        if not hackathon_id or not leader_id:
            return jsonify({"success": False, "message": "Hackathon ID and leader ID are required"}), 400

        cursor = db_manager.connection.execute(
            """SELECT t.team_id, t.team_name, t.description, t.max_members, t.created_at, 
                      h.name as hackathon_name
               FROM teams t 
               JOIN hackathons h ON t.hackathon_id = h.hackathon_id 
               WHERE t.hackathon_id = ? AND t.leader_id = ?""",
            (hackathon_id, leader_id)
        )
        row = cursor.fetchone()

        if row:
            team_data = dict(row)
            return jsonify({
                "success": True,
                "exists": True,
                "team": team_data
            }), 200
        else:
            return jsonify({
                "success": True,
                "exists": False
            }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to check existing team: {str(e)}"}), 500


@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all teams"""
    try:
        status = request.args.get('status', 'forming')
        include_members = request.args.get(
            'include_members', 'false').lower() == 'true'

        result = team_manager.get_all_teams(
            status=status, include_members=include_members)

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
        include_members = request.args.get(
            'include_members', 'true').lower() == 'true'

        result = team_manager.get_team_by_id(
            team_id, include_members=include_members)

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

# Hackathon Management Endpoints


@app.route('/api/hackathons', methods=['GET'])
def get_hackathons():
    """Get all hackathons"""
    try:
        status = request.args.get('status')  # active, upcoming, completed

        # Build query
        query = "SELECT * FROM hackathons"
        params = []

        if status:
            query += " WHERE status = ?"
            params.append(status)

        query += " ORDER BY created_at DESC"

        cursor = db_manager.connection.execute(query, params)
        hackathons = cursor.fetchall()

        # Convert to list of dictionaries
        hackathon_list = []
        for row in hackathons:
            hackathon = dict(row)
            # Parse JSON fields
            if hackathon.get('prizes'):
                try:
                    hackathon['prizes'] = json.loads(hackathon['prizes'])
                except:
                    hackathon['prizes'] = {}
            hackathon_list.append(hackathon)

        return jsonify({
            "success": True,
            "hackathons": hackathon_list,
            "count": len(hackathon_list)
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get hackathons: {str(e)}"}), 500


@app.route('/api/hackathons/<int:hackathon_id>', methods=['GET'])
def get_hackathon(hackathon_id):
    """Get hackathon by ID"""
    try:
        cursor = db_manager.connection.execute(
            "SELECT * FROM hackathons WHERE hackathon_id = ?",
            (hackathon_id,)
        )
        row = cursor.fetchone()

        if not row:
            return jsonify({"success": False, "message": "Hackathon not found"}), 404

        hackathon = dict(row)
        # Parse JSON fields
        if hackathon.get('prizes'):
            try:
                hackathon['prizes'] = json.loads(hackathon['prizes'])
            except:
                hackathon['prizes'] = {}

        return jsonify({
            "success": True,
            "hackathon": hackathon
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get hackathon: {str(e)}"}), 500

# Resume Rating Endpoints


@app.route('/api/rate-profile', methods=['POST'])
def rate_profile():
    """Store user resume and GitHub data in database with real GitHub analysis"""
    try:
        data = request.get_json()

        # Extract required fields
        github_username = data.get('githubUsername', '').strip()
        resume_base64 = data.get('resumeBase64', '').strip()
        # Optional: if we want to link to specific user
        user_id = data.get('user_id')

        # Validate required fields
        if not all([github_username, resume_base64]):
            return jsonify({"success": False, "message": "GitHub username and resume are required"}), 400

        # Extract text from PDF
        print("Extracting text from PDF...")
        resume_text = extract_text_from_pdf_base64(resume_base64)
        print(f"Extracted {len(resume_text)} characters from PDF")

        # Analyze GitHub profile
        print(f"Analyzing GitHub profile for: {github_username}")
        github_analysis = get_github_score(github_username)
        print(f"GitHub analysis completed: {len(github_analysis)} characters")

        # Store in database with GitHub analysis
        try:
            # If no user_id provided, we'll use a default value for anonymous users
            if user_id is None:
                # First, let's create or get an anonymous user ID
                cursor = db_manager.connection.execute(
                    "SELECT user_id FROM users WHERE email = 'anonymous@temp.com' LIMIT 1"
                )
                anonymous_user = cursor.fetchone()

                if not anonymous_user:
                    # Create anonymous user
                    cursor = db_manager.connection.execute(
                        """INSERT INTO users (name, email, password_hash, profile_logo, created_at, updated_at)
                           VALUES ('Anonymous User', 'anonymous@temp.com', 'temp', 'default', datetime('now'), datetime('now'))"""
                    )
                    user_id = cursor.lastrowid
                    db_manager.connection.commit()
                    print(f"Created anonymous user with ID: {user_id}")
                else:
                    user_id = anonymous_user[0]
                    print(f"Using existing anonymous user with ID: {user_id}")

            print(
                f"Storing resume data: user_id={user_id}, github={github_username}")

            # Check if user already has a rating record
            cursor = db_manager.connection.execute(
                "SELECT uid FROM user_ratings WHERE user_id = ?",
                (user_id,)
            )
            existing_record = cursor.fetchone()

            if existing_record:
                # Update existing record with GitHub analysis
                cursor = db_manager.connection.execute(
                    """UPDATE user_ratings 
                       SET resume_data = ?, github_link = ?, github_analysis = ?, updated_at = datetime('now')
                       WHERE user_id = ?""",
                    (resume_text, github_username, github_analysis, user_id)
                )
                db_manager.connection.commit()
                rating_id = existing_record[0]
                print(
                    f"Successfully updated existing resume data with ID: {rating_id}")
            else:
                # Insert new record with GitHub analysis
                cursor = db_manager.connection.execute(
                    """INSERT INTO user_ratings 
                       (user_id, resume_data, github_link, github_analysis, git_score, resume_score, overall_score, created_at, updated_at)
                       VALUES (?, ?, ?, ?, 0, 0, 0, datetime('now'), datetime('now'))""",
                    (user_id, resume_text, github_username, github_analysis)
                )
                db_manager.connection.commit()
                rating_id = cursor.lastrowid
                print(
                    f"Successfully stored new resume data with ID: {rating_id}")

            return jsonify({
                "success": True,
                "message": "Your profile data has been saved. You can update your profile or resume anytime by submitting again",
                "rating_id": rating_id,
                "github_analysis_preview": github_analysis[:200] + "..." if len(github_analysis) > 200 else github_analysis
            }), 200

        except Exception as db_error:
            print(f"Database error in rate_profile: {db_error}")
            return jsonify({"success": False, "message": f"Failed to store data: {str(db_error)}"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to process request: {str(e)}"}), 500


@app.route('/api/user-ratings/<int:user_id>', methods=['GET'])
def get_user_rating(user_id):
    """Get user's latest rating"""
    try:
        cursor = db_manager.connection.execute(
            """SELECT uid, github_link, git_score, resume_score, overall_score, created_at
               FROM user_ratings 
               WHERE user_id = ? 
               ORDER BY created_at DESC 
               LIMIT 1""",
            (user_id,)
        )
        row = cursor.fetchone()

        if not row:
            return jsonify({"success": False, "message": "No rating found for this user"}), 404

        rating = dict(row)
        return jsonify({
            "success": True,
            "rating": rating
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get user rating: {str(e)}"}), 500

# Team Request Endpoints


@app.route('/api/team-requests', methods=['POST'])
def create_team_request():
    """Create a new team request"""
    try:
        data = request.get_json()

        # Extract required fields
        hackathon_id = data.get('hackathon_id')
        user_email = data.get('user_email', '').strip()
        message = data.get('message', '').strip()

        # Validate required fields
        if not all([hackathon_id, user_email, message]):
            return jsonify({"success": False, "message": "Hackathon ID, email, and message are required"}), 400

        # Check if hackathon exists
        cursor = db_manager.connection.execute(
            "SELECT hackathon_id FROM hackathons WHERE hackathon_id = ?",
            (hackathon_id,)
        )
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Hackathon not found"}), 404

        # Check if user already submitted request for this hackathon
        cursor = db_manager.connection.execute(
            "SELECT request_id FROM team_requests WHERE hackathon_id = ? AND user_email = ?",
            (hackathon_id, user_email)
        )
        if cursor.fetchone():
            return jsonify({"success": False, "message": "You have already submitted a request for this hackathon"}), 400

        # Insert team request
        cursor = db_manager.connection.execute(
            """INSERT INTO team_requests (hackathon_id, user_email, message, status, created_at, updated_at)
               VALUES (?, ?, ?, 'pending', datetime('now'), datetime('now'))""",
            (hackathon_id, user_email, message)
        )
        db_manager.connection.commit()

        return jsonify({
            "success": True,
            "message": "Team request submitted successfully",
            "request_id": cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to create team request: {str(e)}"}), 500


@app.route('/api/team-requests/check', methods=['GET'])
def check_team_request():
    """Check if user already submitted request for a hackathon"""
    try:
        hackathon_id = request.args.get('hackathon_id')
        user_email = request.args.get('email', '').strip()

        if not hackathon_id or not user_email:
            return jsonify({"success": False, "message": "Hackathon ID and email are required"}), 400

        cursor = db_manager.connection.execute(
            "SELECT request_id, status, created_at FROM team_requests WHERE hackathon_id = ? AND user_email = ?",
            (hackathon_id, user_email)
        )
        row = cursor.fetchone()

        if row:
            return jsonify({
                "success": True,
                "exists": True,
                "request": {
                    "request_id": row[0],
                    "status": row[1],
                    "created_at": row[2]
                }
            }), 200
        else:
            return jsonify({
                "success": True,
                "exists": False
            }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to check team request: {str(e)}"}), 500


@app.route('/api/team-requests', methods=['GET'])
def get_team_requests():
    """Get team requests with optional filters"""
    try:
        hackathon_id = request.args.get('hackathon_id')
        status = request.args.get('status')
        user_email = request.args.get('email')

        # Build query
        query = """
            SELECT tr.*, h.name as hackathon_name 
            FROM team_requests tr 
            JOIN hackathons h ON tr.hackathon_id = h.hackathon_id 
            WHERE 1=1
        """
        params = []

        if hackathon_id:
            query += " AND tr.hackathon_id = ?"
            params.append(hackathon_id)

        if status:
            query += " AND tr.status = ?"
            params.append(status)

        if user_email:
            query += " AND tr.user_email = ?"
            params.append(user_email)

        query += " ORDER BY tr.created_at DESC"

        cursor = db_manager.connection.execute(query, params)
        requests = cursor.fetchall()

        # Convert to list of dictionaries
        request_list = []
        for row in requests:
            request_list.append(dict(row))

        return jsonify({
            "success": True,
            "requests": request_list,
            "count": len(request_list)
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get team requests: {str(e)}"}), 500


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
        print("  GET /api/teams/check-existing - Check if user already created team for hackathon")
        print("  POST /api/teams/<id>/join - Join team")
        print("  POST /api/teams/<id>/leave - Leave team")
        print("  PUT /api/teams/<id> - Update team")
        print("  GET /api/teams/search - Search teams")
        print("  GET /api/hackathons - Get all hackathons")
        print("  GET /api/hackathons/<id> - Get hackathon by ID")
        print("  POST /api/rate-profile - Rate user profile with AI")
        print("  GET /api/user-ratings/<user_id> - Get user's latest rating")
        print("  POST /api/team-requests - Create team request")
        print("  GET /api/team-requests/check - Check if user already applied")
        print("  GET /api/team-requests - Get team requests")
        print("  GET /health - Health check")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize app. Exiting...")
        exit(1)
