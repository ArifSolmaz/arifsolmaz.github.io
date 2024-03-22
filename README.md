<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Github Portfolio</title>
    <style>
        /* Basic Reset */
        body, h1, h2, h3, p, ul { margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; }
        /* Header */
        header { background-color: #333; color: #fff; padding: 20px; text-align: center; }
        /* Navigation */
        nav ul { list-style-type: none; background-color: #444; text-align: center; padding: 10px; }
        nav ul li { display: inline; }
        nav ul li a { text-decoration: none; color: white; padding: 15px; }
        /* Hero Section */
        .hero { padding: 50px; text-align: center; background-color: #eee; }
        .hero h1 { margin-bottom: 20px; }
        /* Projects Section */
        .projects { display: flex; flex-wrap: wrap; justify-content: center; padding: 20px; }
        .project { margin: 10px; padding: 20px; border: 1px solid #ccc; width: calc(33% - 20px); }
        .project img { max-width: 100%; height: auto; }
        /* About Section */
        .about { background-color: #f9f9f9; padding: 50px; text-align: center; }
        /* Contact Section */
        .contact { background-color: #333; color: white; padding: 50px; text-align: center; }
    </style>
</head>
<body>
    <header>
        <h1>Github Portfolio</h1>
    </header>
    <nav>
        <ul>
            <li><a href="#projects">Projects</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
    <section class="hero">
        <h1>Welcome to My GitHub Portfolio</h1>
        <p>Discover my projects, learn about my skills, and get in touch!</p>
    </section>
    <section id="projects" class="projects">
        <div class="project">
            <img src="project1.jpg" alt="Project 1">
            <h3>Project Title 1</h3>
            <p>Short description of Project 1. <a href="https://github.com">View on GitHub</a></p>
        </div>
        <!-- Repeat for other projects -->
    </section>
    <section id="about" class="about">
        <h2>About Me</h2>
        <p>A brief paragraph about your background and what you do.</p>
    </section>
    <section id="contact" class="contact">
        <h2>Contact</h2>
        <p>Have a question or want to work together? <a href="mailto:your.email@example.com">your.email@example.com</a></p>
    </section>
    <footer>
        <p>&copy; 2024 Your Name. All rights reserved.</p>
    </footer>
</body>
</html> 
