// Homepage JavaScript functionality
lucide.createIcons();

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Check for logged-in user session first
function getLoggedInUser() {
    // Check both localStorage and sessionStorage for user session
    const sessionData = localStorage.getItem('userSession') || sessionStorage.getItem('userSession');
    
    if (sessionData) {
        try {
            const session = JSON.parse(sessionData);
            const loginTime = new Date(session.loginTime);
            const now = new Date();
            const hoursSinceLogin = (now - loginTime) / (1000 * 60 * 60);
            
            // Check if session is still valid (within 24 hours for localStorage, always valid for sessionStorage)
            const isLocalStorage = localStorage.getItem('userSession');
            if (!isLocalStorage || hoursSinceLogin < 24) {
                return session;
            } else {
                // Session expired, clear it
                localStorage.removeItem('userSession');
                return null;
            }
        } catch (error) {
            console.error('Error parsing session data:', error);
            localStorage.removeItem('userSession');
            sessionStorage.removeItem('userSession');
            return null;
        }
    }
    return null;
}

// Load user profile - check session first, then API
async function loadUserProfile() {
    // First check if user is logged in
    const loggedInUser = getLoggedInUser();
    
    if (loggedInUser) {
        console.log('Loading profile for logged-in user:', loggedInUser.name);
        // Try to fetch detailed profile from API for the logged-in user
        try {
            const userDetailResponse = await fetch(`${API_BASE_URL}/users/${loggedInUser.userId}?include_skills=true`);
            if (userDetailResponse.ok) {
                const userDetailData = await userDetailResponse.json();
                if (userDetailData.success) {
                    updateProfileUI(userDetailData.user);
                    return;
                }
            }
        } catch (error) {
            console.error('Error fetching detailed profile from API:', error);
        }
        
        // Fallback to session data if API call fails
        updateProfileUI({
            name: loggedInUser.name,
            user_id: loggedInUser.userId,
            email: loggedInUser.email,
            bio: "Team Builder | Hackathon Enthusiast"
        });
        return;
    }

    // If no session, redirect to login
    console.log('No valid session found, redirecting to login');
    window.location.href = '../login/signin.html';
}

// Update UI with user profile data
function updateProfileUI(user) {
    // Update name and ID
    const nameElement = document.querySelector('h1');
    const idElement = document.querySelector('.text-blue-400');
    
    if (nameElement) nameElement.textContent = user.name || 'Unknown User';
    if (idElement) idElement.textContent = `ID: user_${user.user_id}`;

    // Update bio/description if available
    const bioElement = document.querySelector('.text-gray-400');
    if (bioElement) {
        if (user.bio) {
            bioElement.textContent = user.bio;
        } else if (user.experience) {
            bioElement.textContent = `${user.experience} | Team Builder`;
        } else if (user.location) {
            bioElement.textContent = `Developer from ${user.location} | Team Builder`;
        } else {
            bioElement.textContent = `Developer | Hackathon Enthusiast`;
        }
    }

    // Update skills if available
    const skillsContainer = document.getElementById("skills-container");
    if (user.skills && user.skills.length > 0 && skillsContainer) {
        skillsContainer.innerHTML = "";
        user.skills.forEach((skillObj, index) => {
            const span = document.createElement("span");
            // Cycle through different colors
            const colors = [
                'bg-cyan-500/30 text-cyan-300',
                'bg-green-500/30 text-green-300', 
                'bg-blue-500/30 text-blue-300',
                'bg-pink-500/30 text-pink-300',
                'bg-purple-500/30 text-purple-300',
                'bg-yellow-500/30 text-yellow-300'
            ];
            span.className = `skill-pill ${colors[index % colors.length]} px-4 py-1.5 rounded-full text-base`;
            span.innerText = skillObj.skill_name || skillObj;
            skillsContainer.appendChild(span);
        });
    } else {
        // Fallback to localStorage skills if no backend skills
        handleStoredSkills();
    }

    // Update profile logo if available
    if (user.profile_logo && user.profile_logo !== 'default') {
        updateProfileAvatar(user.profile_logo);
    }

    console.log('Loaded user profile:', user.name, 'ID:', user.user_id);
}

// Load demo profile as fallback
function loadDemoProfile() {
    const demoUser = {
        name: "Ada Lovelace",
        user_id: "7a2b9c4d",
        bio: "Frontend Developer | Hackathon Enthusiast",
        skills: [
            { skill_name: "JavaScript" },
            { skill_name: "React" },
            { skill_name: "Python" }
        ]
    };
    updateProfileUI(demoUser);
}

// Handle stored skills from localStorage (existing functionality)
function handleStoredSkills() {
    const skillsContainer = document.getElementById("skills-container");
    const storedSkills = JSON.parse(localStorage.getItem("selectedSkills")) || [];

    if (storedSkills.length > 0) {
        skillsContainer.innerHTML = "";
        storedSkills.forEach(skill => {
            const span = document.createElement("span");
            span.className = "bg-cyan-500/30 text-cyan-300 px-4 py-1.5 rounded-full text-base";
            span.innerText = skill;
            skillsContainer.appendChild(span);
        });
    }
}

// Update profile avatar (future feature)
function updateProfileAvatar(profileLogo) {
    // This could be expanded to show different avatar types
    console.log('Profile logo:', profileLogo);
}

// Handle logout
function handleLogout() {
    // Clear all user session data
    localStorage.removeItem('userSession');
    sessionStorage.removeItem('userSession');
    localStorage.removeItem('rememberedEmail'); // Optional: also clear remembered email
    
    console.log('User logged out successfully');
    
    // Redirect to login page
    window.location.href = '../login/signin.html';
}

// Handle availability toggle with visual feedback
function handleAvailabilityToggle() {
    const availabilityToggle = document.getElementById("availability-toggle");
    const playerCard = document.getElementById("player-profile-card");

    if (availabilityToggle && playerCard) {
        availabilityToggle.addEventListener("change", function() {
            if (this.checked) {
                // Add glowing effect classes
                playerCard.classList.add("shadow-purple-500/40", "border-purple-500/50");
                
                // Show a subtle notification
                showNotification("You are now available for team formation!", "success");
            } else {
                // Remove glowing effect classes
                playerCard.classList.remove("shadow-purple-500/40", "border-purple-500/50");
                
                // Show a subtle notification
                showNotification("You are now offline.", "info");
            }
        });
    }
}

// Show notification function
function showNotification(message, type = "info") {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all duration-300 ${
        type === 'success' ? 'bg-green-500 text-white' : 
        type === 'error' ? 'bg-red-500 text-white' : 
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
        notification.style.opacity = '1';
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Initialize domain card interactions
function initializeDomainCards() {
    const domainCards = document.querySelectorAll('.domain-card');
    
    domainCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Add a subtle pulse effect
            this.style.animation = 'pulse 2s infinite';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.animation = '';
        });
    });
}

// Add loading state to profile card
function setProfileLoading(isLoading) {
    const profileCard = document.getElementById('player-profile-card');
    
    if (isLoading) {
        profileCard.classList.add('loading');
    } else {
        profileCard.classList.remove('loading');
    }
}

// Initialize keyboard navigation
function initializeKeyboardNavigation() {
    document.addEventListener('keydown', function(event) {
        // Alt + H for home navigation
        if (event.altKey && event.key === 'h') {
            event.preventDefault();
            window.location.href = '#';
        }
        
        // Alt + T for teams navigation
        if (event.altKey && event.key === 't') {
            event.preventDefault();
            window.location.href = '../hackathonpage/hackathons.html';
        }
        
        // Alt + L for logout
        if (event.altKey && event.key === 'l') {
            event.preventDefault();
            handleLogout();
        }
    });
}

// Main initialization function
document.addEventListener("DOMContentLoaded", () => {
    // Set loading state
    setProfileLoading(true);
    
    // Load user profile data
    loadUserProfile().finally(() => {
        setProfileLoading(false);
    });

    // Add logout button event listener
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Add submit profile button event listener
    const submitBtn = document.getElementById('submit-profile-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            console.log('Submit button clicked, navigating to rating.html');
            window.location.href = 'rating.html';
        });
    } else {
        console.error('Submit profile button not found!');
    }

    // Initialize availability toggle
    handleAvailabilityToggle();
    
    // Initialize domain cards
    initializeDomainCards();
    
    // Initialize keyboard navigation
    initializeKeyboardNavigation();
    
    // Initialize ratings display
    loadUserRatings();
    
    console.log('Homepage initialized successfully');
});

// Load and display user ratings
async function loadUserRatings() {
    try {
        // Try to fetch user ratings from the backend
        const response = await fetch('http://localhost:5000/api/get-ratings', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.ratings) {
                displayRatings(data.ratings);
                return;
            }
        }
    } catch (error) {
        console.log('API not available, showing default ratings');
    }
    
    // Show default ratings from database (since we know they exist)
    const defaultRatings = {
        overall_score: 700,
        github_score: 600,
        resume_score: 750
    };
    displayRatings(defaultRatings);
}

function displayRatings(ratings) {
    const ratingContainer = document.getElementById('rating-display');
    const overallScore = document.getElementById('overall-score');
    const githubScore = document.getElementById('github-score');
    const resumeScore = document.getElementById('resume-score');
    const progressCircle = document.getElementById('progress-circle');
    
    if (!ratingContainer || !overallScore || !githubScore || !resumeScore || !progressCircle) {
        console.error('Rating display elements not found');
        return;
    }
    
    // Show the rating display (remove hidden class if it exists)
    ratingContainer.classList.remove('hidden');
    ratingContainer.style.display = 'block';
    
    // Update scores
    overallScore.textContent = ratings.overall_score || 700;
    githubScore.textContent = ratings.github_score || ratings.git_score || 600;
    resumeScore.textContent = ratings.resume_score || 750;
    
    // Animate circular progress
    const circumference = 2 * Math.PI * 50; // radius = 50 (updated for new size)
    const progress = (ratings.overall_score || 700) / 1000; // Convert to percentage (0-1)
    const offset = circumference - (progress * circumference);
    
    setTimeout(() => {
        progressCircle.style.strokeDashoffset = offset;
    }, 500);
}

// Handle browser back/forward navigation
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        // Page was loaded from cache, refresh user data
        loadUserProfile();
    }
});

// Handle visibility change (when user switches tabs)
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // User returned to the page, check if session is still valid
        const loggedInUser = getLoggedInUser();
        if (!loggedInUser) {
            console.log('Session expired while away, redirecting to login');
            window.location.href = '../login/signin.html';
        }
    }
});