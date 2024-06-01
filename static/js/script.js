const aboutMeElement = document.getElementById('about-me');

setTimeout(() => {
  aboutMeElement.style.opacity = 0;
  aboutMeElement.textContent = "My name is Nikos Lymperidis, a Data Analyst based in Serres, Greece"; // Set the text content
  aboutMeElement.classList.add('animated'); // Add a class to trigger animation from style.css
}, 2000); // Delay in milliseconds (2 seconds)

document.querySelector('#contact-form').addEventListener('submit', (e) => {
    e.preventDefault();
    e.target.elements.name.value = '';
    e.target.elements.email.value = '';
    e.target.elements.message.value = '';
  });
