let currentStep = 1;
const totalSteps = 5;
let selectedAvatar = null;

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Header text for each step
const headerContent = {
    1: { title: "Let's build your profile", subtitle: "Join a team of innovators." },
    2: { title: "Choose your avatar", subtitle: "Pick an avatar that represents you." },
    3: { title: "What are your superpowers?", subtitle: "Select the skills you're proficient in." },
    4: { title: "Tell us more about you", subtitle: "A little more detail goes a long way." },
    5: { title: "Finding your dream team...", subtitle: "Get ready to collaborate and create!" }
};

const avatars = [
    // Avatar 1: Rocket
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 16.5-1.5 22M18 6l-5.5 5.5M13 2 2 13l3.5 3.5L18 4l-2-2Z"/><path d="m2 22 5.5-1.5M16.5 5.5 22 1.5M9 15l-1.5 1.5a2.828 2.828 0 1 0 4 4l1.5-1.5"/></svg>`,
    // Avatar 2: Code
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>`,
    // Avatar 3: Brain
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a4.5 4.5 0 0 0-4.5 4.5c0 1.05.38 2.05.97 2.85L7 11.5v2.85c0 .3.15.58.4.75L12 18.5l4.6-3.4c.25-.17.4-.45.4-.75V11.5L15.53 9.35A4.5 4.5 0 0 0 12 2Z"/><path d="M12 2v4.5"/><path d="m16.5 6.5-3 3"/><path d="m7.5 6.5 3 3"/><path d="M12 18.5v3.5"/><path d="m7.5 14.5-5 2.5"/><path d="m16.5 14.5 5 2.5"/></svg>`,
    // Avatar 4: Planet
     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10c0-4.42-2.86-8.17-6.84-9.51"/><path d="M17.55 16.5A6.5 6.5 0 0 1 8 12.5a6.51 6.51 0 0 1 1.45-4"/></svg>`,
    // Avatar 5: Abstract
     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.42 12.61a2.1 2.1 0 1 1 2.97 2.97L7.95 21 2 22l1-5.95Z"/><path d="m16.5 5.5 2.97-2.97a2.1 2.1 0 0 1 2.97 0h0a2.1 2.1 0 0 1 0 2.97L19.53 8.47"/><path d="M15 3h6v6"/><path d="M2.12 15.88a2.1 2.1 0 0 1 0-2.97L5.05 10a2.1 2.1 0 0 1 2.97 0L12 13.92"/></svg>`,
    // Avatar 6: User
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`
];

function showStep(stepNumber) {
    document.querySelectorAll('.step').forEach(step => step.classList.add('hidden'));
    const currentStepElement = document.getElementById(`step-${stepNumber}`);
    if (currentStepElement) {
        currentStepElement.classList.remove('hidden');
    }
}

function updateHeader(stepNumber) {
    const content = headerContent[stepNumber];
    document.getElementById('header-title').textContent = content.title;
    document.getElementById('header-subtitle').textContent = content.subtitle;
}

function nextStep(step) {
    // Validation
    if (step === 1) {
    // --- Name validation ---
    const nameInput = document.getElementById('name');
    const nameError = document.getElementById('name-error');
    if (nameInput.value.trim() === '') {
        nameError.classList.remove('hidden');
        nameInput.classList.add('border-red-400');
        return;
    } else {
        nameError.classList.add('hidden');
        nameInput.classList.remove('border-red-400');
    }

    // --- Email validation ---
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('email-error');
    const emailValue = emailInput.value.trim();

    if (emailValue === '') {
        emailError.textContent = 'Please enter your email to continue.';
        emailError.classList.remove('hidden');
        emailInput.classList.add('border-red-400');
        return;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue)) {
        emailError.textContent = 'Please enter a valid email address.';
        emailError.classList.remove('hidden');
        emailInput.classList.add('border-red-400');
        return;
    } else {
        emailError.classList.add('hidden');
        emailInput.classList.remove('border-red-400');
    }

    // --- Password validation ---
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('password-error');
    const passwordValue = passwordInput.value.trim();

    if (passwordValue === '') {
        passwordError.textContent = 'Please enter a password to continue.';
        passwordError.classList.remove('hidden');
        passwordInput.classList.add('border-red-400');
        return;
    } else if (passwordValue.length < 8) {
        passwordError.textContent = 'Password must be at least 8 characters.';
        passwordError.classList.remove('hidden');
        passwordInput.classList.add('border-red-400');
        return;
    } else {
        passwordError.classList.add('hidden');
        passwordInput.classList.remove('border-red-400');
    }
}


    else if (step === 2) {
        const avatarError = document.getElementById('avatar-error');
         if (!selectedAvatar) {
            avatarError.classList.remove('hidden');
            return;
         } else {
            avatarError.classList.add('hidden');
         }
    }


    if (currentStep < totalSteps) {
        currentStep++;
        showStep(currentStep);
        updateHeader(currentStep);
        
        // Update progress bar
        const progressBar = document.getElementById('progress-bar');
        progressBar.style.width = `${(currentStep / totalSteps) * 100}%`;
    }

     // Simulate loading and completion
    if (step === 4) { // This is the new final user-interactive step
        // Collect all registration data
        const registrationData = collectRegistrationData();
        
        // Show loading state
        document.getElementById('header-title').textContent = "Creating your profile...";
        document.getElementById('header-subtitle').textContent = "Please wait while we set up your account.";
        
        // Submit registration to backend
        submitRegistration(registrationData);
    }
}

// Add click listeners to skill tags
document.addEventListener('DOMContentLoaded', function() {
    // Wait for DOM to be ready, then set up skill tag listeners
    setTimeout(() => {
        document.querySelectorAll('.skill-tag').forEach(tag => {
            tag.addEventListener('click', () => {
                tag.classList.toggle('selected');
                // Visual feedback for selected skills
                if (tag.classList.contains('selected')) {
                    tag.classList.remove('bg-gray-700', 'border-gray-600');
                    tag.classList.add('bg-indigo-600', 'border-indigo-500');
                } else {
                    tag.classList.remove('bg-indigo-600', 'border-indigo-500');
                    tag.classList.add('bg-gray-700', 'border-gray-600');
                }
            });
        });
    }, 100);
});

// Populate and handle avatar selection
const avatarContainer = document.querySelector('#step-2 .grid');
avatars.forEach((avatarSVG, index) => {
    const div = document.createElement('div');
    div.innerHTML = avatarSVG;
    div.className = 'avatar-option cursor-pointer bg-gray-700 p-4 rounded-full border-4 border-transparent aspect-square flex items-center justify-center hover:border-gray-500 transition-colors';
    div.dataset.avatarId = index;
    
    div.addEventListener('click', () => {
         document.querySelectorAll('.avatar-option').forEach(opt => {
             opt.classList.remove('selected', 'border-indigo-500', 'bg-indigo-600');
             opt.classList.add('border-transparent', 'bg-gray-700');
         });
         div.classList.add('selected', 'border-indigo-500', 'bg-indigo-600');
         div.classList.remove('border-transparent', 'bg-gray-700');
         selectedAvatar = index;
         document.getElementById('avatar-error').classList.add('hidden');
    });
    avatarContainer.appendChild(div);
});

// Initialize view
showStep(currentStep);

// Function to redirect to sign in page
function redirectToSignIn() {
    window.location.href = '../login/signin.html';
}

// Collect registration data from form
function collectRegistrationData() {
    // Basic information
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    
    // Avatar selection - map index to avatar name
    const avatarNames = ['rocket', 'code', 'brain', 'planet', 'abstract', 'user'];
    const profile_logo = selectedAvatar !== null ? avatarNames[selectedAvatar] : 'default';
    
    // Skills selection
    const selectedSkills = [];
    document.querySelectorAll('.skill-tag.selected').forEach(tag => {
        selectedSkills.push(tag.textContent.trim());
    });
    
    // Location and experience
    const location = document.getElementById('location').value.trim() || null;
    const experience = document.getElementById('experience').value.trim() || null;
    
    return {
        name,
        email,
        password,
        profile_logo,
        skills: selectedSkills,
        location,
        experience
    };
}

// Submit registration to backend API
async function submitRegistration(registrationData) {
    try {
        console.log('Submitting registration:', registrationData);
        
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registrationData)
        });
        
        const result = await response.json();
        console.log('Registration response:', result);
        
        if (result.success) {
            // Registration successful
            setTimeout(() => {
                document.getElementById('header-title').textContent = "You're all set!";
                document.getElementById('header-subtitle').textContent = "Happy hacking!";
                document.getElementById('step-5').innerHTML = `
                    <div class="flex justify-center items-center mb-6">
                         <svg class="w-20 h-20 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </div>
                    <h2 class="text-2xl font-bold mb-2">Profile Created!</h2>
                    <p class="text-gray-400 mb-6">Account created successfully! You can now sign in with your credentials.</p>
                    <button onclick="redirectToSignIn()" class="w-full text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-800 font-medium rounded-lg text-md px-5 py-4 text-center transition">Sign In to Your Account</button>
               `;
            }, 1000); // 1-second delay for better UX
        } else {
            // Registration failed
            document.getElementById('header-title').textContent = "Registration Failed";
            document.getElementById('header-subtitle').textContent = "Please try again.";
            document.getElementById('step-5').innerHTML = `
                <div class="flex justify-center items-center mb-6">
                     <svg class="w-20 h-20 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <h2 class="text-2xl font-bold mb-2">Registration Failed</h2>
                <p class="text-red-400 mb-6">${result.message || 'An error occurred during registration.'}</p>
                <button onclick="location.reload()" class="w-full text-white bg-red-600 hover:bg-red-700 focus:ring-4 focus:ring-red-800 font-medium rounded-lg text-md px-5 py-4 text-center transition">Try Again</button>
           `;
        }
        
    } catch (error) {
        console.error('Registration error:', error);
        
        // Network or other error
        document.getElementById('header-title').textContent = "Connection Error";
        document.getElementById('header-subtitle').textContent = "Please check your connection.";
        document.getElementById('step-5').innerHTML = `
            <div class="flex justify-center items-center mb-6">
                 <svg class="w-20 h-20 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.664-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"></path></svg>
            </div>
            <h2 class="text-2xl font-bold mb-2">Connection Error</h2>
            <p class="text-yellow-400 mb-6">Unable to connect to the server. Please check your internet connection and try again.</p>
            <button onclick="location.reload()" class="w-full text-white bg-yellow-600 hover:bg-yellow-700 focus:ring-4 focus:ring-yellow-800 font-medium rounded-lg text-md px-5 py-4 text-center transition">Try Again</button>
       `;
    }
}

// Add Enter key functionality to forms
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        
        // Get the current step's continue button and click it
        const currentStepElement = document.getElementById(`step-${currentStep}`);
        if (currentStepElement && !currentStepElement.classList.contains('hidden')) {
            const continueButton = currentStepElement.querySelector('button');
            if (continueButton) {
                continueButton.click();
            }
        }
    }
});
