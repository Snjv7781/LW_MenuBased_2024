document.querySelectorAll('.drawer-menu a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        // Extract the target ID from the href attribute
        const targetId = this.getAttribute('href').substring(1);
        
        // Check if the target element exists
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth' });
        } else {
            console.error(`Element with ID ${targetId} not found.`);
        }
    });
});
