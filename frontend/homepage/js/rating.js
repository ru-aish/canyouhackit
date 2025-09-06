// Function to get logged-in user session (same as homepage)
function getLoggedInUser() {
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

document.getElementById('rating-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const githubUsername = document.getElementById('githubUsername').value;
    const resumeFile = document.getElementById('resumeFile').files[0];
    const resultContainer = document.getElementById('result-container');
    const submitButton = document.getElementById('submit-button');

    if (!resumeFile) {
        resultContainer.innerHTML = `<p class="text-red-500">Please upload a resume file.</p>`;
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = 'Storing Data...';
    resultContainer.innerHTML = `<p class="text-yellow-400">Uploading resume and GitHub information...</p>`;

    // Convert PDF to base64 to send as a string
    const reader = new FileReader();
    reader.readAsDataURL(resumeFile);
    reader.onload = async () => {
        const resumeBase64 = reader.result.split(',')[1]; // Get only the base64 part

        // Get current user session to include user_id
        const userSession = getLoggedInUser();
        
        const profileData = {
            githubUsername,
            resumeBase64, // Send resume as a base64 encoded string
            user_id: userSession ? userSession.userId : null // Include logged-in user ID
        };

        try {
            // Use our Python backend
            const response = await fetch('http://localhost:5000/api/rate-profile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profileData),
            });

            if (!response.ok) {
                throw new Error('Server responded with an error.');
            }

            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.message || 'Data storage failed');
            }

            // Clear any existing ratings from localStorage since we're just storing data now
            localStorage.removeItem('userRatings');

            resultContainer.innerHTML = `
                <div class="bg-gray-700 p-4 rounded-lg">
                    <p class="text-green-400 mb-2"><strong>✅ Success!</strong> Your profile data has been saved.</p>
                    <p class="text-gray-300 mb-2">You can update your profile or resume anytime by submitting again.</p>
                    <a href="homepage.html" class="inline-block mt-4 text-blue-400 hover:text-blue-300">&larr; Go back to homepage</a>
                </div>
            `;
            submitButton.textContent = 'Profile Saved!';

        } catch (error) {
            console.error('Failed to store data:', error);
            resultContainer.innerHTML = `<p class="text-red-500">Error: Could not store data. ${error.message}</p>`;
            submitButton.disabled = false;
            submitButton.textContent = 'Store My Data';
        }
    };

    reader.onerror = (error) => {
        console.error('Error reading file:', error);
        resultContainer.innerHTML = `<p class="text-red-500">Error: Could not read the resume file.</p>`;
        submitButton.disabled = false;
        submitButton.textContent = 'Store My Data';
    };
});