import json
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Add parent directory to path to import GitHub scraper
sys.path.append('/home/rudra/Code/hackbite')

# Load environment variables
load_dotenv()

class RatingService:
    def __init__(self):
        """Initialize the rating service with Gemini API configuration."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        # Load prompt template
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self):
        """Load the prompt template from prompt.txt."""
        prompt_path = '/home/rudra/Code/hackbite/1/prompt.txt'
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt template not found at {prompt_path}")
    
    def generate_ratings(self, github_url, resume_text):
        """
        Generate ratings using Gemini API based on GitHub profile and resume.
        
        Args:
            github_url (str): GitHub profile URL
            resume_text (str): Extracted resume text
            
        Returns:
            dict: JSON response with git_rating, resume_rating, and overall_rating
        """
        try:
            # Extract GitHub username from URL
            github_username = self._extract_github_username(github_url)
            
            # Import and use GitHub scraper
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("github_scraper", "/home/rudra/Code/hackbite/2.py")
                github_scraper_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(github_scraper_module)
                
                # Create scraper instance and use it
                scraper = github_scraper_module.GithubScraper(github_username)
                github_data = scraper.scrape_profile()
                
                # Convert the data format to match our expected structure
                if github_data:
                    # Extract useful metrics from the scraped data
                    total_stars = 0
                    analyzed_repos = github_data.get('analyzedRepositories', [])
                    total_repos = len(analyzed_repos)
                    
                    # Debug: print the actual structure
                    print(f"DEBUG: First repo structure: {analyzed_repos[0] if analyzed_repos else 'No repos'}")
                    
                    for repo in analyzed_repos:
                        if isinstance(repo, dict):
                            total_stars += repo.get('stars', 0)
                    
                    # Convert to simplified format
                    github_data = {
                        'username': github_username,
                        'total_repos': total_repos,
                        'total_stars': total_stars,
                        'total_forks': 0,  # Not readily available in new format
                        'following': 0,    # Not readily available in new format
                        'followers': 0,    # Not readily available in new format
                        'repositories': analyzed_repos  # Keep original format for prompt
                    }
                else:
                    raise Exception("No data returned from scraper")
                    
            except Exception as scraper_error:
                print(f"GitHub scraper error: {scraper_error}")
                # Create minimal GitHub data for fallback
                github_data = {
                    'username': github_username,
                    'total_repos': 0,
                    'total_stars': 0,
                    'total_forks': 0,
                    'following': 0,
                    'followers': 0,
                    'repositories': []
                }
            
            # Prepare the analysis prompt
            analysis_prompt = self._create_analysis_prompt(github_data, resume_text)
            
            # Call Gemini API
            response = self.model.generate_content(analysis_prompt)
            
            # Parse JSON response
            ratings_json = self._parse_json_response(response.text)
            
            return ratings_json
            
        except Exception as e:
            print(f"Error generating ratings: {e}")
            # Return default ratings on error
            return {
                "git_rating": {"score": 0, "reasoning": ["Error occurred during rating generation"]},
                "resume_rating": {"score": 0, "reasoning": ["Error occurred during rating generation"]}, 
                "overall_rating": {"score": 0, "reasoning": ["Error occurred during rating generation"]}
            }
    
    def _extract_github_username(self, github_url):
        """Extract username from GitHub URL."""
        if github_url.startswith('https://github.com/'):
            return github_url.replace('https://github.com/', '').strip('/')
        return github_url
    
    def _create_analysis_prompt(self, github_data, resume_text):
        """Create the analysis prompt combining GitHub data and resume."""
        
        # Format GitHub data
        github_summary = f"""
GitHub Profile Analysis:
- Username: {github_data.get('username', 'N/A')}
- Total Repositories: {github_data.get('total_repos', 0)}
- Total Stars: {github_data.get('total_stars', 0)}
- Total Forks: {github_data.get('total_forks', 0)}
- Following: {github_data.get('following', 0)}
- Followers: {github_data.get('followers', 0)}

Top Repositories:
"""
        
        # Add repository details - handle both formats
        repositories = github_data.get('repositories', [])
        for i, repo in enumerate(repositories[:5], 1):
            # Handle different data structures
            if isinstance(repo, dict):
                name = repo.get('name', 'Unknown')
                language = repo.get('primaryLanguage', repo.get('language', 'N/A'))
                stars = repo.get('stars', 0)
                description = repo.get('description', 'No description')
                
                github_summary += f"""
{i}. {name}
   - Language: {language}
   - Stars: {stars}
   - Description: {description}
"""
            else:
                # Handle unexpected format - just convert to string
                github_summary += f"""
{i}. Repository data: {str(repo)[:100]}...
"""
        
        # Combine with resume
        full_prompt = f"""
{self.prompt_template}

=== DATA TO ANALYZE ===

{github_summary}

Resume Content:
{resume_text}

=== END DATA ===

Please analyze the above data and respond with the JSON rating structure only.
"""
        
        return full_prompt
    
    def _parse_json_response(self, response_text):
        """Parse and validate JSON response from Gemini."""
        try:
            # Clean response - remove any markdown formatting
            cleaned_response = response_text.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON
            ratings = json.loads(cleaned_response)
            
            # Validate structure
            required_keys = ['git_rating', 'resume_rating', 'overall_rating']
            for key in required_keys:
                if key not in ratings:
                    raise ValueError(f"Missing key: {key}")
                if 'score' not in ratings[key]:
                    raise ValueError(f"Missing score in {key}")
                if 'reasoning' not in ratings[key]:
                    raise ValueError(f"Missing reasoning in {key}")
            
            return ratings
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response_text}")
            raise
        except Exception as e:
            print(f"Error parsing response: {e}")
            raise

def test_rating_service():
    """Test the rating service with sample data."""
    service = RatingService()
    
    sample_resume = """
John Doe
Software Engineer
Email: john@example.com

Experience:
- Software Engineer at TechCorp (2020-2023)
- Developed web applications using Python and React
- Led team of 3 developers on major project

Skills:
- Python, JavaScript, React, Node.js
- Docker, Kubernetes, AWS
- PostgreSQL, MongoDB

Education:
- BS Computer Science, MIT (2020)
"""
    
    ratings = service.generate_ratings("https://github.com/octocat", sample_resume)
    print(json.dumps(ratings, indent=2))

if __name__ == "__main__":
    test_rating_service()