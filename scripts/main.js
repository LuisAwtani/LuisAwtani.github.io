document.addEventListener('DOMContentLoaded', function() {
    const projectCards = document.querySelectorAll('.project-card');
    const defaultMessage = document.querySelector('.default-message');
    const detailContents = document.querySelectorAll('.project-detail-content');

    // Function to show project details
    function showProject(projectId) {
        // Hide all detail contents and default message
        detailContents.forEach(content => {
            content.style.display = 'none';
        });
        defaultMessage.style.display = 'none';

        // Show selected project details
        const selectedContent = document.getElementById(`${projectId}-details`);
        if (selectedContent) {
            selectedContent.style.display = 'block';
        }

        // Add active state to selected card
        projectCards.forEach(c => c.classList.remove('active'));
        const selectedCard = document.querySelector(`[data-project="${projectId}"]`);
        if (selectedCard) {
            selectedCard.classList.add('active');
        }
    }

    // Add click handlers to all project cards
    projectCards.forEach(card => {
        card.addEventListener('click', function() {
            const projectId = this.dataset.project;
            showProject(projectId);
        });
    });

    // Auto-select the Jane Street project on page load
    showProject('big2');
}); 