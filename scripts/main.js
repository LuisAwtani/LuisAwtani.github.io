document.addEventListener('DOMContentLoaded', function() {
    const projectCards = document.querySelectorAll('.project-card');
    const defaultMessage = document.querySelector('.default-message');
    const detailContents = document.querySelectorAll('.project-detail-content');

    projectCards.forEach(card => {
        card.addEventListener('click', function() {
            const projectId = this.dataset.project;
            
            // Hide all detail contents and show default message
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
            this.classList.add('active');
        });
    });
}); 