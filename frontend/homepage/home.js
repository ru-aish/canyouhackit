document.addEventListener("DOMContentLoaded", () => {
    const ratingContainer = document.getElementById('rating-container');
    const savedRatings = JSON.parse(localStorage.getItem('userRatings'));

    if (savedRatings) {
        // If ratings exist, display them
        const { github, resume, overall } = savedRatings;
        const radius = 60;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (overall / 1000) * circumference;

        ratingContainer.innerHTML = `
            <div class="rating-display">
                <div class="rating-circle-container">
                    <svg class="w-full h-full" viewBox="0 0 140 140">
                        <circle class="rating-circle-bg" cx="70" cy="70" r="${radius}" stroke-width="12"></circle>
                        <circle id="rating-fg" class="rating-circle-fg" cx="70" cy="70" r="${radius}" stroke-width="12"
                                stroke-dasharray="${circumference}" stroke-dashoffset="${circumference}"></circle>
                    </svg>
                    <div class="rating-text">
                        ${overall}
                        <span class="small">Overall</span>
                    </div>
                </div>
                <div class="rating-breakdown">
                    <div class="rating-item">GitHub Score: <span>${github}</span></div>
                    <div class="rating-item">Resume Score: <span>${resume}</span></div>
                </div>
            </div>
        `;
        
        // Trigger the animation after a short delay
        setTimeout(() => {
            document.getElementById('rating-fg').style.strokeDashoffset = offset;
        }, 100);

    } else {
        // If no ratings, show the "Get Rating" button
        ratingContainer.innerHTML = `
            <div class="text-center">
                <p class="text-gray-400 mb-4">Your profile has not been rated yet.</p>
                <a href="rating.html" class="inline-block w-full md:w-auto bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg text-lg transition-all duration-200 transform hover:scale-105">
                    Get Your AI Rating
                </a>
            </div>
        `;
    }
});

