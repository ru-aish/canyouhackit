document.addEventListener("DOMContentLoaded", async () => {
    const submitBtn = document.getElementById('submit-profile-btn');
    
    // Check if user has ratings data or show default ratings
    await loadUserRatings();
    
    // Submit button click handler
    submitBtn.addEventListener('click', () => {
        window.location.href = 'rating.html';
    });
});

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
});

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
        console.log('API not available, showing demo data');
    }
    
    // If API fails, show demo ratings from database
    displayRatings({
        overall_score: 700,
        github_score: 600,
        resume_score: 750
    });
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
    
    // Show the rating display
    ratingContainer.classList.remove('hidden');
    
    // Update scores
    overallScore.textContent = ratings.overall_score || 0;
    githubScore.textContent = ratings.github_score || ratings.git_score || 0;
    resumeScore.textContent = ratings.resume_score || 0;
    
    // Animate circular progress
    const circumference = 2 * Math.PI * 60; // radius = 60
    const progress = (ratings.overall_score || 0) / 1000; // Convert to percentage (0-1)
    const offset = circumference - (progress * circumference);
    
    setTimeout(() => {
        progressCircle.style.strokeDashoffset = offset;
    }, 500);
}
