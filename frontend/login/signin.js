// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const loginForm = document.getElementById('login-form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const togglePasswordBtn = document.getElementById('toggle-password');
const eyeIcon = document.getElementById('eye-icon');
const signinBtn = document.getElementById('signin-btn');
const signinText = document.getElementById('signin-text');
const signinLoading = document.getElementById('signin-loading');
const loginError = document.getElementById('login-error');
const loginSuccess = document.getElementById('login-success');
const emailError = document.getElementById('email-error');
const passwordError = document.getElementById('password-error');
const rememberMeCheckbox = document.getElementById('remember-me');

// Utility Functions
function showError(element, message) {
    element.textContent = message;
    element.classList.remove('hidden');
    element.classList.add('message-enter');
}

function hideError(element) {
    element.classList.add('hidden');
    element.classList.remove('message-enter');
}

function showMainError(message) {
    showError(loginError, message);
    hideError(loginSuccess);
}

function showSuccess(message) {
    showError(loginSuccess, message);
    hideError(loginError);
}

function setLoadingState(isLoading) {
    signinBtn.disabled = isLoading;
    
    if (isLoading) {
        signinText.classList.add('hidden');
        signinLoading.classList.remove('hidden');
        signinBtn.classList.add('loading-disabled');
    } else {
        signinText.classList.remove('hidden');
        signinLoading.classList.add('hidden');
        signinBtn.classList.remove('loading-disabled');
    }
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateForm() {
    let isValid = true;
    
    // Hide all previous errors
    hideError(emailError);
    hideError(passwordError);
    hideError(loginError);
    
    // Remove error styling
    emailInput.classList.remove('input-error');
    passwordInput.classList.remove('input-error');
    
    // Validate email
    const email = emailInput.value.trim();
    if (!email) {
        showError(emailError, 'Email is required.');
        emailInput.classList.add('input-error');
        isValid = false;
    } else if (!validateEmail(email)) {
        showError(emailError, 'Please enter a valid email address.');
        emailInput.classList.add('input-error');
        isValid = false;
    }
    
    // Validate password
    const password = passwordInput.value.trim();
    if (!password) {
        showError(passwordError, 'Password is required.');
        passwordInput.classList.add('input-error');
        isValid = false;
    }
    
    return isValid;
}

// Password toggle functionality
function togglePasswordVisibility() {
    const isPassword = passwordInput.type === 'password';
    
    if (isPassword) {
        passwordInput.type = 'text';
        eyeIcon.innerHTML = `
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
        `;
    } else {
        passwordInput.type = 'password';
        eyeIcon.innerHTML = `
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
        `;
    }
}

// Login API call
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Login failed');
        }
        
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Handle form submission
async function handleLogin(event) {
    event.preventDefault();
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    // Get form values
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const rememberMe = rememberMeCheckbox.checked;
    
    // Set loading state
    setLoadingState(true);
    hideError(loginError);
    hideError(loginSuccess);
    
    try {
        // Attempt login
        const result = await loginUser(email, password);
        
        if (result.success) {
            // Store user data if remember me is checked
            if (rememberMe) {
                localStorage.setItem('rememberedEmail', email);
                localStorage.setItem('userSession', JSON.stringify({
                    userId: result.user.user_id,
                    email: result.user.email,
                    name: result.user.name,
                    loginTime: new Date().toISOString()
                }));
            } else {
                // Store in session storage (will be cleared when browser closes)
                sessionStorage.setItem('userSession', JSON.stringify({
                    userId: result.user.user_id,
                    email: result.user.email,
                    name: result.user.name,
                    loginTime: new Date().toISOString()
                }));
            }
            
            // Show success message
            showSuccess('Login successful! Redirecting to your profile...');
            
            // Redirect to homepage after a short delay
            setTimeout(() => {
                window.location.href = '../homepage/homepage.html';
            }, 1500);
            
        } else {
            throw new Error(result.message || 'Login failed');
        }
        
    } catch (error) {
        setLoadingState(false);
        showMainError(error.message || 'An error occurred during login. Please try again.');
    }
}

// Load remembered email on page load
function loadRememberedEmail() {
    const rememberedEmail = localStorage.getItem('rememberedEmail');
    if (rememberedEmail) {
        emailInput.value = rememberedEmail;
        rememberMeCheckbox.checked = true;
    }
}

// Real-time validation
function setupRealTimeValidation() {
    emailInput.addEventListener('blur', () => {
        const email = emailInput.value.trim();
        if (email) {
            if (validateEmail(email)) {
                emailInput.classList.remove('input-error');
                emailInput.classList.add('input-success');
                hideError(emailError);
            } else {
                emailInput.classList.remove('input-success');
                emailInput.classList.add('input-error');
                showError(emailError, 'Please enter a valid email address.');
            }
        }
    });
    
    passwordInput.addEventListener('blur', () => {
        const password = passwordInput.value.trim();
        if (password) {
            passwordInput.classList.remove('input-error');
            passwordInput.classList.add('input-success');
            hideError(passwordError);
        }
    });
    
    // Clear error styling when user starts typing
    emailInput.addEventListener('input', () => {
        emailInput.classList.remove('input-error', 'input-success');
        hideError(emailError);
    });
    
    passwordInput.addEventListener('input', () => {
        passwordInput.classList.remove('input-error', 'input-success');
        hideError(passwordError);
    });
}

// Check if user is already logged in
function checkExistingSession() {
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
                // User is already logged in, redirect to homepage
                window.location.href = '../homepage/homepage.html';
                return;
            } else {
                // Session expired, clear it
                localStorage.removeItem('userSession');
            }
        } catch (error) {
            console.error('Error parsing session data:', error);
            localStorage.removeItem('userSession');
            sessionStorage.removeItem('userSession');
        }
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    // Check for existing session
    checkExistingSession();
    
    // Load remembered email
    loadRememberedEmail();
    
    // Setup real-time validation
    setupRealTimeValidation();
    
    // Add event listeners
    loginForm.addEventListener('submit', handleLogin);
    togglePasswordBtn.addEventListener('click', togglePasswordVisibility);
    
    // Focus on email input
    emailInput.focus();
    
    console.log('Login page initialized');
});

// Handle browser back button
window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        // Page was loaded from cache, check session again
        checkExistingSession();
    }
});