import json
from callAI import callAI

jobDescription = {
  "title": "Practicante de Desarrollo de Software",
  "seniority": "",
  "required_skills": [
    "JavaScript",
    "Python",
    "C#",
    "Java",
    "web development",
    "APIs",
    "SQL databases",
    "Git/GitHub",
    "automation tools"
  ],
  "domains": [
    "Software Development",
    "Automation",
    "CRM",
    "Conversational Agents",
    "Legal Services"
  ],
  "soft_skills": [
    "analysis",
    "problem solving",
    "organization",
    "responsibility",
    "autonomy",
    "communication",
    "teamwork",
    "proactivity",
    "curiosity",
    "attention to detail",
    "openness to learning"
  ],
  "experience_years": 0
}
projectData = [
    {
        "name": "Robotic Control and Simulation Platform",
        "summary": "Web-based application for visualizing, simulating, and controlling robotic manipulators through both joint-space and Cartesian-space control. The system integrates a React frontend, a Python backend implementing forward and inverse kinematics, interactive 3D visualization, and real-time communication with ESP32-based hardware.",
        "technologies": [
            "Python",
            "React",
            "Three.js",
            "React Three Fiber",
            "WebSockets",
            "ESP32",
            "JSON",
            "JavaScript",
            "HTML",
            "TailwindCSS"
        ],
        "facts": [
            "Developed a web application for controlling a physical robotic arm over Wi-Fi.",
            "Implemented forward kinematics to compute TCP position and orientation from joint variables.",
            "Implemented inverse kinematics for Cartesian-space robot control.",
            "Integrated an interactive 3D robot visualization using Three.js and React Three Fiber.",
            "Developed real-time bidirectional communication between frontend, backend, and hardware using WebSockets.",
            "Implemented both joint-space and Cartesian-space robot control through interactive sliders.",
            "Developed a CRUD system for storing and managing robot joint positions.",
            "Implemented a monitoring console for displaying system events and error messages.",
            "Integrated an ESP32-based controller to operate physical stepper motors.",
            "Designed a decoupled architecture separating frontend, backend, and hardware layers.",
            "Developed a second-generation platform supporting robot definitions through JSON configuration files.",
            "Implemented dynamic UI generation based on robot configuration parameters.",
            "Designed a modular robot description system allowing serial manipulators to be defined through configuration files.",
            "Developed generalized kinematic algorithms for serial robots defined through configuration files.",
            "Implemented visual indicators for coordinate frames and joint axes within the 3D scene.",
            "Developed a CRUD system for managing robotic motion sequences.",
            "Implemented UI customization features including dark mode and configurable accent colors.",
            "Designed a wizard-based workflow for building robot configurations from a component catalog."
        ],
        "domains": [
            "robotics",
            "software-development",
            "frontend",
            "backend",
            "3d-graphics",
            "embedded-systems",
            "websockets",
            "simulation",
            "automation"
        ]
    },{
        "name": "Boat Rental Management System",
        "summary": "Business management application designed to support the daily operations of a boat rental company. The system centralizes rental records, customer information, and operational workflows through an intuitive interface optimized for real-world usage.",
        "technologies": [
            "React",
            "Vite",
            "JavaScript",
            "HTML",
            "TailwindCSS"
        ],
        "facts": [
            "Developed a business application for managing boat rental operations.",
            "Designed and implemented a user interface optimized for daily operational use.",
            "Built CRUD functionality for managing rental records and business data.",
            "Implemented local data persistence to allow operation without a dedicated server.",
            "Designed workflows focused on reducing manual record-keeping and improving operational efficiency.",
            "Developed the MVP and deployed it for use in a real business environment.",
            "Adapted the application based on practical operational requirements and user feedback.",
            "Organized business information into a centralized management system.",
            "Designed the application to be usable by non-technical users in a day-to-day work environment.",
            "Evaluated deployment strategies for mobile and desktop usage scenarios."
        ],
        "domains": [
            "software-development",
            "business-software",
            "frontend",
            "web-development",
            "productivity",
            "data-management",
            "user-experience"
        ]
    }
]

def selectProjectBullets(jobDescription, projects):
    """
    Selecciona las 4 bullets más relevantes para cada proyecto.

    Parámetros:
        jobDescription (dict): JSON completo de la vacante.
        projects (list): Lista de proyectos.

    Devuelve:
        list: [
            {
                "name": "...",
                "bullets": [...]
            }
        ]
    """

    result = []

    reduced_job = {
        "title": jobDescription.get("title", ""),
        "required_skills": jobDescription.get("required_skills", []),
        "domains": jobDescription.get("domains", [])
    }

    for project in projects:

        reduced_project = {
            "name": project["name"],
            "facts": project["facts"]
        }

        prompt = f"""
        You are an experienced technical recruiter.

        Select the 4 most relevant resume bullets for the target position.

        Prioritize:
        - Required skills
        - Relevant domains
        - Business value
        - Technical complexity

        Do not rewrite bullets.
        Do not invent information.

        Return ONLY valid JSON:

        {{
            "selected_bullets": []
        }}

        Job:
        {json.dumps(reduced_job, indent=2)}

        Project:
        {json.dumps(reduced_project, indent=2)}
        """

        try:
            response = callAI(prompt)

            data = json.loads(response)

            selected = {
                "name": project["name"],
                "bullets": data.get("selected_bullets", [])
            }

            result.append(selected)

        except Exception as e:

            print(
                f"Error selecting bullets for "
                f"{project['name']}: {e}"
            )

            result.append({
                "name": project["name"],
                "bullets": project["facts"][:4]
            })

    print("\n=== SELECTED PROJECT BULLETS ===\n")

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )

    return result

selectProjectBullets(jobDescription,projectData)