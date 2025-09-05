// API configuration
const API_BASE_URL = 'http://localhost:5000';

// Function to fetch hackathons from the API
async function loadHackathons() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/hackathons`);
        const data = await response.json();
        
        if (data.success) {
            renderHackathons(data.hackathons);
        } else {
            showError('Failed to load hackathons');
        }
    } catch (error) {
        console.error('Error loading hackathons:', error);
        showError('Network error. Please check if the API server is running.');
    }
}

// Function to render hackathons
function renderHackathons(hackathons) {
    const eventGrid = document.getElementById('event-grid');
    const loading = document.getElementById('loading');
    
    // Remove loading indicator
    if (loading) {
        loading.remove();
    }
    
    // Clear existing content
    eventGrid.innerHTML = '';
    
    if (hackathons.length === 0) {
        eventGrid.innerHTML = '<div class="text-center py-8"><p class="text-gray-400">No hackathons available at the moment.</p></div>';
        return;
    }
    
    hackathons.forEach(hackathon => {
        const card = createHackathonCard(hackathon);
        eventGrid.appendChild(card);
    });
}

// Function to create a hackathon card element
function createHackathonCard(hackathon) {
    const card = document.createElement('div');
    card.className = 'event-card bg-gray-800 rounded-xl shadow-lg overflow-hidden cursor-pointer border-2 border-transparent transition-all duration-300 ease-in-out hover:shadow-2xl hover:border-indigo-500';
    card.setAttribute('data-event', hackathon.name);
    card.setAttribute('data-info-url', getInfoUrl(hackathon.name));
    card.setAttribute('data-hackathon-id', hackathon.hackathon_id);
    
    // Format dates
    const startDate = new Date(hackathon.start_date);
    const endDate = new Date(hackathon.end_date);
    const regDeadline = new Date(hackathon.registration_deadline);
    
    const dateStr = `${startDate.toLocaleDateString()} - ${endDate.toLocaleDateString()}`;
    const regStr = `Registration: ${regDeadline.toLocaleDateString()}`;
    
    card.innerHTML = `
        <div class="relative">
            <img src="${getHackathonImage(hackathon.name)}" alt="${hackathon.name}" class="w-full h-48 object-cover">
            <div class="absolute top-2 right-2 bg-${getStatusColor(hackathon.status)}-600 text-white px-2 py-1 rounded text-xs font-bold">
                ${hackathon.status.toUpperCase()}
            </div>
        </div>
        <div class="p-6">
            <h2 class="text-xl font-bold text-white mb-2">${hackathon.name}</h2>
            <p class="text-gray-400 text-sm mb-2">${hackathon.description || 'No description available'}</p>
            <div class="text-xs text-gray-500 mb-2">
                <p>${dateStr}</p>
                <p>${regStr}</p>
                ${hackathon.theme ? `<p>Theme: ${hackathon.theme}</p>` : ''}
            </div>
            
            <!-- Options Container -->
            <div class="options-container hidden mt-4">
                <button class="option-btn btn-info w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg shadow-md hover:bg-indigo-700 transition-all duration-300 mb-2">
                    Get More Info
                </button>
                <div class="grid grid-cols-2 gap-2">
                    <button class="option-btn btn-teams w-full bg-gray-700 text-white font-bold py-2 px-4 rounded-lg shadow-md hover:bg-gray-600 transition-all duration-300">
                        Look for Teams
                    </button>
                    <button class="option-btn btn-people w-full bg-gray-700 text-white font-bold py-2 px-4 rounded-lg shadow-md hover:bg-gray-600 transition-all duration-300">
                        Look for People
                    </button>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Helper function to get status color
function getStatusColor(status) {
    switch (status.toLowerCase()) {
        case 'active': return 'green';
        case 'upcoming': return 'blue';
        case 'completed': return 'gray';
        case 'cancelled': return 'red';
        default: return 'gray';
    }
}

// Helper function to get hackathon image (fallback to existing images)
function getHackathonImage(name) {
    if (name === 'MLH Hackabyte 3.0' || name.toLowerCase().includes('hackbyte') || name.toLowerCase().includes('mlh')) {
        return 'image.png';
    } else if (name === 'Smart India Hackathon' || name.toLowerCase().includes('smart india') || name.toLowerCase().includes('sih')) {
        return 'Screenshot from 2025-09-05 15-33-34.png';
    }
    // Default placeholder image
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMzc0MTUxIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxOCIgZmlsbD0iIzk0YTNiOCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkhhY2thdGhvbjwvdGV4dD48L3N2Zz4=';
}

// Helper function to get info URL (fallback logic)
function getInfoUrl(name) {
    if (name === 'MLH Hackabyte 3.0' || name.toLowerCase().includes('hackbyte') || name.toLowerCase().includes('mlh')) {
        return 'https://www.hackbyte.in/';
    } else if (name === 'Smart India Hackathon' || name.toLowerCase().includes('smart india') || name.toLowerCase().includes('sih')) {
        return 'https://www.sih.gov.in/';
    }
    return `https://www.google.com/search?q=${encodeURIComponent(name)}`;
}

// Function to show error message
function showError(message) {
    const eventGrid = document.getElementById('event-grid');
    const loading = document.getElementById('loading');
    
    if (loading) {
        loading.remove();
    }
    
    eventGrid.innerHTML = `
        <div class="text-center py-8">
            <p class="text-red-400 mb-4">${message}</p>
            <button onclick="loadHackathons()" class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
                Retry
            </button>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    // Load hackathons when page loads
    loadHackathons();
    
    const eventGrid = document.getElementById('event-grid');

    eventGrid.addEventListener('click', (e) => {
        const card = e.target.closest('.event-card');
        if (!card) return;

        const button = e.target.closest('.option-btn');
        const eventName = card.dataset.event;
        const infoUrl = card.dataset.infoUrl;

        if (button) {
            e.stopPropagation();
            if (button.classList.contains('btn-info')) {
                if (infoUrl) {
                    window.open(infoUrl, '_blank');
                } else {
                    window.open(`https://www.google.com/search?q=${encodeURIComponent(eventName)}`, '_blank');
                }
            } else if (button.classList.contains('btn-teams')) {
                const hackathonId = card.getAttribute('data-hackathon-id');
                const hackathonName = card.getAttribute('data-event');
                window.location.href = `messageforteams.html?hackathon_id=${hackathonId}&hackathon_name=${encodeURIComponent(hackathonName)}`;
            } else if (button.classList.contains('btn-people')) {
                window.location.href = 'createateam.html';
            }
            return;
        }

        const isSelected = card.classList.contains('selected');
        
        // Remove selected class from all cards
        document.querySelectorAll('.event-card').forEach(c => {
            c.classList.remove('selected');
        });

        if (!isSelected) {
            card.classList.add('selected');
        }
    });
});

