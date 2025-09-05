document.addEventListener('DOMContentLoaded', () => {
    const eventGrid = document.getElementById('event-grid');

    eventGrid.addEventListener('click', (e) => {
        const card = e.target.closest('.event-card');
        if (!card) return;

        const button = e.target.closest('.option-btn');
        const eventName = card.dataset.event;

        if (button) {
            e.stopPropagation();
            if (button.classList.contains('btn-info')) {
                const infoUrl = card.dataset.infoUrl;
                if (infoUrl) {
                    window.open(infoUrl, '_blank');
                } else {
                    window.open(`https://www.google.com/search?q=${encodeURIComponent(eventName)}`, '_blank');
                }
            } else if (button.classList.contains('btn-teams')) {
                alert(`Looking for teams for: ${eventName}`);
            } else if (button.classList.contains('btn-people')) {
                alert(`Looking for people for: ${eventName}`);
            }
            return;
        }

        const isSelected = card.classList.contains('selected');
        
        document.querySelectorAll('.event-card').forEach(c => {
            c.classList.remove('selected');
        });

        if (!isSelected) {
            card.classList.add('selected');
        }
    });
});

