#!/usr/bin/env python3
"""
Rating Generator using Gemini API
Combines GitHub analysis, resume data, and custom prompt to generate ratings
"""

import sys
import os
import sqlite3
import json
from pathlib import Path
from google import genai

# Add the parent directory to sys.path to import from 2.py
sys.path.append('/home/rudra/Code/hackbite')

# Import classes from 2.py
sys.path.append('/home/rudra/Code/hackbite')
import importlib.util
spec = importlib.util.spec_from_file_location("github_scraper", "/home/rudra/Code/hackbite/2.py")
github_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github_module)

GithubScraper = github_module.GithubScraper
HighlightGenerator = github_module.HighlightGenerator


class RatingGenerator:
    def __init__(self, db_path="/home/rudra/Code/hackbite/1/database/database.db"):
        self.db_path = db_path
        # The client gets the API key from the environment variable `GEMINI_API_KEY`
        try:
            self.client = genai.Client()
        except Exception as e:
            print("❌ Error: GEMINI_API_KEY environment variable not set or invalid")
            print("Please set it with: export GEMINI_API_KEY='your_api_key_here'")
            print(f"Error details: {e}")
            sys.exit(1)
    
    def convert_github_number(self, text):
        """Convert GitHub number format like '16.7k' to integer"""
        try:
            text = text.strip().replace(',', '')
            if 'k' in text.lower():
                return int(float(text.lower().replace('k', '')) * 1000)
            elif 'm' in text.lower():
                return int(float(text.lower().replace('m', '')) * 1000000)
            else:
                return int(text)
        except:
            return 0
    
    def get_resume_data_from_db(self, user_id=None, github_username=None):
        """Get resume data from user_ratings table"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if user_id:
                query = """
                    SELECT resume_data, github_link, github_analysis 
                    FROM user_ratings 
                    WHERE user_id = ? 
                    ORDER BY updated_at DESC 
                    LIMIT 1
                """
                cursor.execute(query, (user_id,))
            elif github_username:
                query = """
                    SELECT resume_data, github_link, github_analysis 
                    FROM user_ratings 
                    WHERE github_link = ? 
                    ORDER BY updated_at DESC 
                    LIMIT 1
                """
                cursor.execute(query, (github_username,))
            else:
                # Get the most recent entry
                query = """
                    SELECT resume_data, github_link, github_analysis 
                    FROM user_ratings 
                    ORDER BY updated_at DESC 
                    LIMIT 1
                """
                cursor.execute(query)
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'resume_data': result['resume_data'],
                    'github_link': result['github_link'], 
                    'github_analysis': result['github_analysis']
                }
            else:
                print("❌ No resume data found in database")
                return None
                
        except Exception as e:
            print(f"❌ Database error: {e}")
            return None
    
    def get_fresh_github_data(self, github_username):
        """Get fresh GitHub data using the scraper from 2.py"""
        try:
            # Extract username from URL if it's a full URL
            if github_username.startswith('https://github.com/'):
                github_username = github_username.replace('https://github.com/', '')
            elif github_username.startswith('github.com/'):
                github_username = github_username.replace('github.com/', '')
            elif github_username.startswith('http://github.com/'):
                github_username = github_username.replace('http://github.com/', '')
            
            print(f"🔄 Scraping fresh GitHub data for: {github_username}")
            
            # Create a patched scraper that handles k/m notation
            scraper = GithubScraper(github_username)
            
            # Patch the _extract_pinned_repos method to handle star conversion
            original_extract = scraper._extract_pinned_repos
            def patched_extract_pinned_repos(soup):
                pinned_section = soup.find('div', class_='js-pinned-items-reorder-container')
                if not pinned_section:
                    return []

                repos = []
                pinned_items = pinned_section.find_all('div', class_='Box')
                for item in pinned_items:
                    repo_link = item.find('a', {'data-view-component': 'true'}, href=True)
                    if not repo_link or not repo_link.find('span', class_='repo'):
                        continue

                    repo_url = f"https://github.com{repo_link['href']}"
                    name = repo_link.find('span', class_='repo').get_text(strip=True)
                    desc_tag = item.find('p', class_='pinned-item-desc')
                    lang_tag = item.find('span', itemprop='programmingLanguage')
                    star_tag = item.find('a', href=f"{repo_link['href']}/stargazers")

                    # Use our number converter for stars
                    stars = 0
                    if star_tag:
                        star_text = star_tag.get_text(strip=True)
                        stars = self.convert_github_number(star_text)

                    repos.append({
                        "name": name,
                        "url": repo_url,
                        "description": desc_tag.get_text(strip=True) if desc_tag else "N/A",
                        "primaryLanguage": lang_tag.get_text(strip=True) if lang_tag else "N/A",
                        "stars": stars
                    })
                return repos
            
            # Patch the HighlightGenerator to handle missing variables
            def patched_generate_report(self):
                """Creates the full text report with error handling."""
                profile_info = self.data.get('profileInfo', {})
                username = profile_info.get('fullName') or self.data.get('username', 'N/A')
                report_lines = []

                report_lines.append("\n" + "="*50)
                report_lines.append(f"      GITHUB PROFILE HIGHLIGHTS for {username}")
                report_lines.append("="*50)

                # Work Ethic & Consistency
                contrib_stats = self.data.get('contributionStats', {})
                contributions = contrib_stats.get('totalContributionsInLastYear') or contrib_stats.get('totalContributionDaysInLastYear', 0)
                contrib_type = "Total Contributions" if 'totalContributionsInLastYear' in contrib_stats else "Active Days"
                report_lines.append("\n**1. Work Ethic & Consistency:**")
                report_lines.append(f"* **Activity (Last Year):** {contributions} ({contrib_type}).")

                # Project Analysis
                repos = self.data.get('analyzedRepositories', [])
                report_lines.append("\n**2. Project Details (Pinned Repositories):**")

                if not repos:
                    report_lines.append("* No pinned repositories found.")
                    total_stars = 0
                    documented_repos_count = 0
                    non_trivial_projects = []
                else:
                    total_stars = 0
                    documented_repos_count = 0
                    non_trivial_projects = []

                    for repo in repos:
                        total_stars += repo.get('stars', 0)
                        if repo.get('readme', {}).get('exists'):
                            documented_repos_count += 1
                        if "solution" not in repo['name'].lower() and "leetcode" not in repo['name'].lower():
                            non_trivial_projects.append(f"{repo['name']} ({repo.get('primaryLanguage', 'N/A')})")

                        report_lines.append(f"* **{repo.get('name', 'N/A')}:**")
                        report_lines.append(f"  - **Description:** {repo.get('description', 'N/A')}")
                        report_lines.append(f"  - **Stars:** {repo.get('stars', 0)}")
                        report_lines.append(f"  - **README:** {'Exists' if repo.get('readme', {}).get('exists') else 'MISSING'}")

                # Key Takeaways for AI Prompt
                report_lines.append("\n" + "="*50)
                report_lines.append("      KEY DATA POINTS FOR SCORING")
                report_lines.append("="*50)

                report_lines.append(f"* **IMPACT (Community Validation):**")
                report_lines.append(f"  - Total Stars on Pinned Repos: {total_stars}")

                report_lines.append(f"\n* **COMPLEXITY (Project Types):**")
                if non_trivial_projects:
                    report_lines.append(f"  - Non-trivial projects identified: {', '.join(non_trivial_projects)}")
                else:
                    report_lines.append("  - Projects appear to be primarily foundational or solution-based.")

                report_lines.append(f"\n* **DOCUMENTATION (Professionalism):**")
                report_lines.append(f"  - README files exist for {documented_repos_count} out of {len(repos)} pinned repositories.")

                report_lines.append("\n" + "="*50)

                return "\n".join(report_lines)
            
            # Apply the patches
            scraper._extract_pinned_repos = patched_extract_pinned_repos
            
            github_data = scraper.scrape_profile()
            
            if github_data:
                # Create reporter and patch its method
                reporter = HighlightGenerator(github_data)
                reporter.generate_report = patched_generate_report.__get__(reporter, HighlightGenerator)
                return reporter.generate_report()
            else:
                print("❌ Could not scrape GitHub profile")
                return None
                
        except Exception as e:
            print(f"❌ GitHub scraping error: {e}")
            return None
    
    def read_prompt_file(self, prompt_file="prompt.txt"):
        """Read prompt from file"""
        try:
            prompt_path = Path(prompt_file)
            if not prompt_path.exists():
                print(f"❌ Prompt file {prompt_file} not found")
                return None
            
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
                
        except Exception as e:
            print(f"❌ Error reading prompt file: {e}")
            return None
    
    def send_to_gemini(self, github_analysis, resume_data, prompt):
        """Send data to Gemini API for rating"""
        try:
            # Construct the complete prompt
            complete_prompt = f"""
{prompt}

=== GITHUB ANALYSIS ===
{github_analysis}

=== RESUME DATA ===
{resume_data}

Please provide 3 specific ratings based on the above data.
"""
            
            print("🚀 Sending request to Gemini API...")
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=complete_prompt
            )
            
            return response.text
                
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return None
    
    def generate_ratings(self, user_id=None, github_username=None, prompt_file="prompt.txt", use_fresh_github=False):
        """Main method to generate ratings"""
        print("=" * 60)
        print("🎯 RATING GENERATOR STARTING")
        print("=" * 60)
        
        # 1. Get resume data from database
        print("\n📊 Step 1: Getting resume data from database...")
        
        # If github_username is provided with fresh_github, get resume from any user in DB
        if github_username and use_fresh_github:
            print(f"🔄 Using resume from database but fresh GitHub data for: {github_username}")
            db_data = self.get_resume_data_from_db()  # Get most recent resume
        else:
            db_data = self.get_resume_data_from_db(user_id, github_username)
            
        if not db_data:
            return False
        
        resume_data = db_data['resume_data']
        github_link = db_data['github_link']
        
        print(f"✅ Found resume data from database")
        print(f"✅ Resume data length: {len(resume_data)} characters")
        
        # 2. Get GitHub analysis
        print("\n🐙 Step 2: Getting GitHub analysis...")
        
        # If fresh github username provided, use that instead of DB github
        if github_username and use_fresh_github:
            print(f"🔄 Using fresh GitHub profile: {github_username}")
            github_analysis = self.get_fresh_github_data(github_username)
        elif use_fresh_github:
            github_analysis = self.get_fresh_github_data(github_link)
        else:
            github_analysis = db_data.get('github_analysis')
            if github_analysis:
                print("✅ Using cached GitHub analysis from database")
            else:
                print("⚠️  No cached GitHub analysis, fetching fresh data...")
                github_analysis = self.get_fresh_github_data(github_link)
        
        if not github_analysis:
            return False
            
        # 3. Read prompt
        print("\n📝 Step 3: Reading prompt file...")
        prompt = self.read_prompt_file(prompt_file)
        if not prompt:
            return False
            
        print(f"✅ Prompt loaded: {len(prompt)} characters")
        
        # 4. Send to Gemini API
        print("\n🤖 Step 4: Sending to Gemini API for rating...")
        ratings = self.send_to_gemini(github_analysis, resume_data, prompt)
        
        if ratings:
            print("\n" + "=" * 60)
            print("🎯 GEMINI API RATINGS RESPONSE")
            print("=" * 60)
            print(ratings)
            print("=" * 60)
            return True
        else:
            print("❌ Failed to get ratings from Gemini API")
            return False


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate ratings using Gemini API')
    parser.add_argument('--user-id', type=int, help='User ID to get data for')
    parser.add_argument('--github', type=str, help='GitHub username to get data for')
    parser.add_argument('--prompt', type=str, default='prompt.txt', help='Prompt file path')
    parser.add_argument('--fresh-github', action='store_true', help='Fetch fresh GitHub data instead of using cached')
    
    args = parser.parse_args()
    
    # Create rating generator
    generator = RatingGenerator()
    
    # Generate ratings
    success = generator.generate_ratings(
        user_id=args.user_id,
        github_username=args.github,
        prompt_file=args.prompt,
        use_fresh_github=args.fresh_github
    )
    
    if success:
        print("\n✅ Rating generation completed successfully!")
    else:
        print("\n❌ Rating generation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()