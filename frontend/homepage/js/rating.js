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
    submitButton.textContent = 'Analyzing... Please Wait';
    resultContainer.innerHTML = `<p class="text-yellow-400">Reading file and contacting AI... this may take a moment.</p>`;

    // Convert PDF to base64 to send as a string
    const reader = new FileReader();
    reader.readAsDataURL(resumeFile);
    reader.onload = async () => {
        const resumeBase64 = reader.result.split(',')[1]; // Get only the base64 part

        const profileData = {
            githubUsername,
            resumeBase64, // Send resume as a base64 encoded string
        };

        try {
            const response = await fetch('http://localhost:3000/api/rate-profile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profileData),
            });

            if (!response.ok) {
                throw new Error('Server responded with an error.');
            }

            const result = await response.json();
            const { reasoning, githubRating, resumeRating, finalRating } = result.ratingData;

            // Store the ratings in localStorage to be used on the home page
            localStorage.setItem('userRatings', JSON.stringify({
                github: githubRating,
                resume: resumeRating,
                overall: finalRating
            }));

            resultContainer.innerHTML = `
                <div class="bg-gray-700 p-4 rounded-lg">
                    <p class="text-gray-300 mb-2"><strong>AI Reasoning:</strong> "${reasoning}"</p>
                    <p class="text-xl font-bold text-green-400">Overall Rating: ${finalRating}</p>
                    <a href="index.html" class="inline-block mt-4 text-blue-400 hover:text-blue-300">&larr; Go back to your profile to see the update</a>
                </div>
            `;
            submitButton.textContent = 'Rating Complete!';

        } catch (error) {
            console.error('Failed to get rating:', error);
            resultContainer.innerHTML = `<p class="text-red-500">Error: Could not get a rating. Is the backend server running?</p>`;
            submitButton.disabled = false;
            submitButton.textContent = 'Get My AI Rating';
        }
    };

    reader.onerror = (error) => {
        console.error('Error reading file:', error);
        resultContainer.innerHTML = `<p class="text-red-500">Error: Could not read the resume file.</p>`;
        submitButton.disabled = false;
        submitButton.textContent = 'Get My AI Rating';
    };
});