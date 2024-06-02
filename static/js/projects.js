document.addEventListener("DOMContentLoaded", function () {
    const projectsList = document.getElementById('projects-list');

    // Define an array of images
    const projectImages = [
        "static/assets/img/projects/billboard.jpg",
        "static/assets/img/projects/blog-for-deployment.jpg",
        "static/assets/img/projects/cafe-api.jpg",
        "static/assets/img/projects/finalassignment.jpg",
        "static/assets/img/projects/flight-deals.jpg",
        "static/assets/img/projects/professional-portfolio.jpg",
        "static/assets/img/projects/rain_alert.jpg",
        // Add more images here as needed
    ];

    // Fetch GitHub repositories
    fetch('https://api.github.com/users/nlymperidis/repos')
        .then(response => response.json())
        .then(repos => {
            repos.forEach((repo, index) => {
                const projectElement = document.createElement('div');
                projectElement.classList.add('project-wrapper');

                const imageUrl = projectImages[index % projectImages.length]; // Cycle through images

                projectElement.innerHTML = `
                    <figure>
                        <img src="${imageUrl}" alt="Project Image" />
                    </figure>
                    <div class="project-body">
                        <h2>${repo.name}</h2>
                        <p>${repo.description || 'No description available'}</p>
                        <a href="${repo.html_url}" target="_blank">View on GitHub</a>
                    </div>
                `;

                projectsList.appendChild(projectElement);
            });
        })
        .catch(error => {
            console.error('Error fetching repositories:', error);
        });
});
