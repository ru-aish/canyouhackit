document.addEventListener('DOMContentLoaded', () => {
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
                alert(`Looking for teams for: ${eventName}`);
            } else if (button.classList.contains('btn-people')) {
                window.location.href = 'createateam.html';
            }
            return;
        }

        const isSelected = card.classList.contains('selected');
        
        // This line is now corrected to use '.event-card'
        document.querySelectorAll('.event-card').forEach(c => {
            c.classList.remove('selected');
        });

        if (!isSelected) {
            card.classList.add('selected');
        }
    });
});

