import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.database import DatabaseManager, UserManager

class RegistrationSystem:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.user_manager = UserManager(self.db_manager)
        self.initialize()
    
    def initialize(self):
        if not self.db_manager.connect():
            print("❌ Failed to connect to database")
            return False
        
        if not self.db_manager.initialize_tables():
            print("❌ Failed to initialize database tables")
            return False
        
        print("✅ Registration system initialized successfully")
        return True
    
    def display_logo_choices(self):
        logos = self.user_manager.get_available_logos()
        print("\n📸 Available Profile Logos:")
        for i, logo in enumerate(logos, 1):
            print(f"  {i}. {logo}")
        return logos
    
    def get_user_input(self):
        print("\n" + "="*50)
        print("🚀 HackBite User Registration")
        print("="*50)
        
        name = input("👤 Enter your name: ").strip()
        if not name:
            print("❌ Name cannot be empty")
            return None
        
        email = input("📧 Enter your email: ").strip()
        if not email or "@" not in email:
            print("❌ Please enter a valid email")
            return None
        
        password = input("🔒 Enter your password: ").strip()
        if len(password) < 6:
            print("❌ Password must be at least 6 characters")
            return None
        
        logos = self.display_logo_choices()
        try:
            logo_choice = int(input(f"\n🎨 Choose profile logo (1-{len(logos)}): "))
            if 1 <= logo_choice <= len(logos):
                profile_logo = logos[logo_choice - 1]
            else:
                print("⚠️  Invalid choice, using default avatar")
                profile_logo = "default_avatar.png"
        except ValueError:
            print("⚠️  Invalid input, using default avatar")
            profile_logo = "default_avatar.png"
        
        return {
            "name": name,
            "email": email,
            "password": password,
            "profile_logo": profile_logo
        }
    
    def register_new_user(self):
        user_data = self.get_user_input()
        if not user_data:
            return False
        
        print("\n🔄 Registering user...")
        result = self.user_manager.register_user(
            user_data["name"],
            user_data["email"],
            user_data["password"],
            user_data["profile_logo"]
        )
        
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"👤 User ID: {result['user_id']}")
            print(f"🎨 Profile Logo: {result['profile_logo']}")
            return True
        else:
            print(f"❌ {result['message']}")
            return False
    
    def login_user(self):
        print("\n" + "="*50)
        print("🔐 HackBite User Login")
        print("="*50)
        
        email = input("📧 Enter your email: ").strip()
        password = input("🔒 Enter your password: ").strip()
        
        print("\n🔄 Logging in...")
        result = self.user_manager.login_user(email, password)
        
        if result["success"]:
            user = result["user"]
            print(f"✅ {result['message']}")
            print(f"👤 Welcome back, {user['name']}!")
            print(f"🎨 Profile Logo: {user['profile_logo']}")
            print(f"📅 Member since: {user['created_at']}")
            return user
        else:
            print(f"❌ {result['message']}")
            return None
    
    def list_all_users(self):
        print("\n" + "="*50)
        print("👥 All Registered Users")
        print("="*50)
        
        users = self.user_manager.get_all_users()
        if not users:
            print("📭 No users found")
            return
        
        for user in users:
            print(f"ID: {user['user_id']} | Name: {user['name']} | Email: {user['email']} | Logo: {user['profile_logo']}")
    
    def main_menu(self):
        while True:
            print("\n" + "="*50)
            print("🏠 HackBite Registration System - Main Menu")
            print("="*50)
            print("1. 📝 Register New User")
            print("2. 🔐 Login User")
            print("3. 👥 List All Users")
            print("4. 🚪 Exit")
            
            choice = input("\n🎯 Choose an option (1-4): ").strip()
            
            if choice == "1":
                self.register_new_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                self.list_all_users()
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def cleanup(self):
        self.db_manager.close()

if __name__ == "__main__":
    try:
        system = RegistrationSystem()
        system.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    finally:
        try:
            system.cleanup()
        except:
            pass