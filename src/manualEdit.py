from generatePDF import render_template, generate_pdf
import asyncio
data = {
    "name": "Ismael Hernandez",
    "phone": "3314161781",
    "email": "ismael21502@gmail.com",
    "github": "https://github.com/ismael21502",
    "profile": """Robotics Engineering student with hands-on experience in software and web development. Skilled in Python and JavaScript, with experience building web applications.""",
    "skills": [
        "JavaScript",
        "React",
        "TailwindCSS",
        "HTML",
        "CSS",
        "Python"
    ],
    "softSkills": [
        "Analytical thinking",
        "Teamwork",
        "Curiosity",
        "Proactivity",
        "Responsibility"
    ],
    "experience": [
        {
            "title": "Robotic Control and Simulation Platform",
            "bullets": [
                "Developed a web application for controlling a physical robotic arm over Wi-Fi.",
                "Integrated an interactive 3D robot visualization using Three.js and React Three Fiber.",
                "Developed real-time communication between frontend, backend, and hardware using WebSockets.",
                "Implemented UI customization features including dark mode and configurable colors."
            ]
        },
        {
            "title": "Boat Rental Management System",
            "bullets": [
                "Designed and implemented a user interface optimized for daily operational use.",
                "Built CRUD functionality for managing rental records and business data.",
                "Implemented local data persistence to allow operation without a dedicated server.",
                "Evaluated deployment strategies for mobile and desktop usage scenarios."
            ]
        }
    ],
    "education": [
        {
            "degree": "B.Sc. Robotics Engineering",
            "institution": "Universidad de Guadalajara",
            "status": "In Progress"
        }
    ],
    "languages": [
        {
            "name": "Spanish",
            "level": "Native"
        },
        {
            "name": "English",
            "level": "B2"
        }
    ]
}

template_path = "index.html"
output_pdf = "cv.pdf"

# Renderizamos la plantilla con los datos del candidato
rendered_html = render_template(template_path, data)

# Generamos el PDF a partir del HTML renderizado
asyncio.run(generate_pdf(rendered_html, output_pdf))