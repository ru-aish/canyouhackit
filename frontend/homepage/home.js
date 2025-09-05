document.addEventListener("DOMContentLoaded", () => {
    const ratingContainer = document.getElementById('rating-container');
    
    // Since we're not generating ratings anymore, just show the submit button
    ratingContainer.innerHTML = `
        <div class="text-center">
            <p class="text-gray-400 mb-4">Submit your profile data for future AI analysis.</p>
            <a href="rating.html" class="inline-block w-full md:w-auto bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg text-lg transition-all duration-200 transform hover:scale-105">
                Submit Profile Data
            </a>
        </div>
    `;
});
