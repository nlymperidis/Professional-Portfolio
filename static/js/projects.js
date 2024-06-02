document.addEventListener("DOMContentLoaded", function () {
    const projectsList = document.getElementById('projects-list');

    // Fetch GitHub repositories
    fetch('https://api.github.com/users/nlymperidis/repos')
        .then(response => response.json())
        .then(repos => {
            repos.forEach(repo => {
                const projectElement = document.createElement('div');
                projectElement.classList.add('project-wrapper');

                projectElement.innerHTML = `
                    <figure>
                        <img src="static/assets/img/programming.jpg" alt="Programming" />
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
