document.addEventListener("DOMContentLoaded", function () {
    const projectsList = document.getElementById('projects-list');

    // Define the base path for project images and possible extensions
    const imageBasePath = "static/assets/img/projects/";
    const imageExtensions = ['.jpg', '.jpeg', '.png'];

    // Function to construct image URL based on available extensions
    const getImageUrl = (basePath, projectName, extensions) => {
        for (const ext of extensions) {
            const imageUrl = `${basePath}${projectName}${ext}`;
            const http = new XMLHttpRequest();
            http.open('HEAD', imageUrl, false);
            http.send();
            if (http.status !== 404) {
                return imageUrl;
            }
        }
        return `${basePath}default.jpg`; // Default image if no match is found
    };

    // Fetch GitHub repositories
    fetch('https://api.github.com/users/nlymperidis/repos')
        .then(response => response.json())
        .then(repos => {
            repos.forEach(repo => {
                const projectElement = document.createElement('div');
                projectElement.classList.add('project-wrapper');

                // Construct the image URL based on the repo name
                const imageUrl = getImageUrl(imageBasePath, repo.name, imageExtensions);

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
