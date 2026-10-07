from callAI import askAI

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
def selectProjects(relevantData: dict, projects): #RelevantData debería ser jobTitle, jobDomains, jobSkills
    promptTemplate = """
    # ROL
    Eres un validador de candidatos estricto. Tu función es verificar si las tecnologías del proyecto coinciden EXACTAMENTE con las requeridas en la vacante.

    # INSTRUCCIONES DE PROCESAMIENTO
    1. Analiza el campo 'job_skills' como una lista cerrada (Whitelist).
    2. Busca coincidencias de substrings exactos entre las skills del proyecto y la whitelist de la vacante.
    3. DESCARTA cualquier tecnología mencionada en el proyecto que NO esté explícitamente en 'job_skills'.

    # REGLAS DE NEGACIÓN
    - NUNCA inventes habilidades.
    - Si la vacante pide ['Python', 'Docker'], y el proyecto usa ['threejs', 'React'], la lista de skills_covered debe ser vacía [] porque ninguno coincide exactamente con la whitelist (a menos que 'React' esté en job_skills).
    - Ignora habilidades implícitas o relacionadas.

    # EJEMPLO DE CORRECTO (Few-Shot)
    Vacante Skills: ["Python", "Docker", "APIs"]
    Proyecto Usos: ["threejs", "React", "Python"]
    Salida Esperada: {{"project_title": "...", "skills_covered": ["Python"]}}

    Ejemplo de INCORRECTO (No hagas esto):
    {{"project_title": "...", "skills_covered": ["Python", "Docker", "React"]}} <-- Error por incluir React si no estaba en la lista vacante.

    # FORMATO DE SALIDA
    Retornarás ÚNICAMENTE un JSON válido, sin markdown ni comentarios.
    Estructura: {{"project_title": "", "skills_covered": []}}

    INPUT VACANTE: {jobInfo}
    INPUT PROYECTO: {projects}
    """

    projectsData = [{
        'name': project["name"],
        'summary': project["summary"],
        'technologies': project["technologies"],
        'domains': project["domains"]
    } for project in projects]
    # print("INPUT: ", promptTemplate.format(jobInfo=relevantData, projects=projectData))
    for i in range(len(projectData)):
        print("Respuesta IA: ", askAI("bigger", promptTemplate.format(jobInfo=relevantData, projects=projectsData[i])))
    # print("Project summaries: ", [project["summary"] for project in projects])

relevantData = {
    "job_title": jobDescription["title"],
    "job_domains": jobDescription["domains"],
    "job_skills": jobDescription["required_skills"]
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
    },
    {
            "name": "Fallout Kanban",
            "summary": "Full-stack web-based Kanban board inspired by the Fallout franchise. The application combines task management functionality with a custom post-apocalyptic user interface, providing an engaging productivity experience while demonstrating full-stack development skills.",
            "technologies": [
                "React",
                "Django",
                "PostgreSQL",
                "Railway",
                "JavaScript",
                "HTML",
                "CSS"
            ],
            "facts": [
                "Developed a full-stack web application using React and Django.",
                "Designed and implemented a Kanban-style task management system.",
                "Built CRUD functionality for creating, updating, organizing, and deleting tasks.",
                "Integrated a PostgreSQL database for persistent task storage.",
                "Deployed the application using Railway.",
                "Designed a custom user interface inspired by the Fallout franchise and Pip-Boy aesthetic.",
                "Created a cohesive visual identity through custom typography, color palettes, and interface components.",
                "Developed both frontend and backend components of the application."
            ],
            "domains": [
                "software-development",
                "full-stack",
                "frontend",
                "backend",
                "web-development",
                "ui-design",
                "productivity"
            ]
        },
        {
                    "name": "AI agent",
                    "summary": "AI general agent made with local models and python",
                    "technologies": [
                        "Python",
                        "LangChain",
                        "LangGraph",
                        "API consumption"
                    ],
                    "facts": [
                        "Developed a python script that runs a general AI agent"
                    ],
                    "domains": [
                        "software-development",
                        "productivity"
                    ]
                }
]
selectProjects(relevantData, projectData)