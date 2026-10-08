import json
# from callAI import askAI
from extractData.llm import bulletSelectorModel
from pydantic import BaseModel

class Result(BaseModel):
    selectedBullets: list[int]

def selectProjectBulletsFromJobData(jobData, projects): #TODO: projects debería ser una lista reducida, no todos los proyectos
    """
    Selecciona las 4 bullets más relevantes para cada proyecto.
    Parámetros:
        jobData (dict): JSON completo de la vacante.
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
        "title": jobData.get("title", ""),
        "required_skills": jobData.get("required_skills", []),
        "domains": jobData.get("domains", [])
    }
    for project in projects:
        reduced_project = {
            "name": project["name"],
            "facts": project["facts"]
        }
        prompt = f"""
        You are an experienced technical recruiter.
        Select the 4 most relevant resume bullets for the target position. Minimum 2
        Prioritize:
        - Required skills
        - Relevant domains
        - Business value
        - Technical complexity
        Do not invent information.
        Job:
        {json.dumps(reduced_job, indent=2)}
        Project:
        {json.dumps(reduced_project, indent=2)}
        """
        try:
            # response = askAI("fast", prompt)
            # data = json.loads(response)
            # selected = {
            #     "name": project["name"],
            #     "bullets": data.get("selected_bullets", [])
            # }
            structuredModel = bulletSelectorModel.with_structured_output(Result)
            response = structuredModel.invoke(prompt)

            # for bullet in response.selectedBullets:
            #     print(project["facts"][bullet])
            bullets = [project["facts"][bullet] for bullet in response.selectedBullets]
            # response = response.model_dump()
            selected = {
                "name": project["name"],
                # "bullets": response.selectedBullets
                "bullets": bullets
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
    return result

def selectProjectBullets(jobDescription, projects): #TODO: projects debería ser una lista reducida, no todos los proyectos
    """
    Selecciona las 4 bullets más relevantes para cada proyecto.
    Parámetros:
        jobDescription (str): Descripción completa de la vacante.
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
    # reduced_job = {
    #     "title": jobData.get("title", ""),
    #     "required_skills": jobData.get("required_skills", []),
    #     "domains": jobData.get("domains", [])
    # }
    for project in projects:
        reducedProject = {
            "name": project["name"],
            "facts": project["facts"]
        }
        prompt = f"""
        You are an experienced technical recruiter.
        Select the 4 most relevant resume bullets for the target position. Minimum 2
        Prioritize:
        - Required skills
        - Relevant domains
        - Business value
        - Technical complexity
        Do not invent information.
        Job:
        {jobDescription}
        Project:
        {json.dumps(reducedProject, indent=2)}
        """
        try:
            # response = askAI("fast", prompt)
            # data = json.loads(response)
            # selected = {
            #     "name": project["name"],
            #     "bullets": data.get("selected_bullets", [])
            # }
            structuredModel = bulletSelectorModel.with_structured_output(Result)
            response = structuredModel.invoke(prompt)

            # for bullet in response.selectedBullets:
            #     print(project["facts"][bullet])
            bullets = [project["facts"][bullet] for bullet in response.selectedBullets]
            # response = response.model_dump()
            selected = {
                "name": project["name"],
                # "bullets": response.selectedBullets
                "bullets": bullets
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
    return result

# selectProjectBullets(jobData,projectData)

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    jobData = {
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
    result = selectProjectBullets("""AI-Native Software Engineer - Early Career
Location: Remote — global applications welcome; please apply via the region closest to you
Company: ChainGPT
Type: Full-Time

About ChainGPT
ChainGPT is a fast-moving Web3 and AI company building products at the intersection of blockchain infrastructure, token ecosystems, and intelligent automation. We value speed, ownership, clarity, and high standards. Our team is made up of self-driven operators who move fast, think independently, and use cutting-edge tools to create real commercial impact.

We foster a transparent, collaborative, and high-performance culture where strong ideas win, autonomy is expected, and execution matters.

We’re building Brain by AIVM, a platform that makes enterprise AI verifiable, governed, and genuinely trustworthy.

We’re a small, fast-moving team working at the frontier of AI, governance, and enterprise trust. At this stage, a sharp AI-native marketer can have an outsized impact on how the world sees us.

About the Role
We’re looking for an exceptional early-career engineer who has grown up building with AI.

You may be fresh out of university, still studying, or entirely self-taught. What matters most is raw ability, curiosity, strong technical instincts, and a genuine obsession with modern AI tooling.

This is a high-growth role for someone who wants to learn how a company is built from the inside while contributing to real product work from day one. You’ll work closely with the founders and senior engineers, build real features and prototypes, and learn how to use AI agents to move faster than traditional teams.

What You’ll Do
Build real features, prototypes, and demos using tools like Codex, Claude Code, and modern AI coding agents.
Turn ideas into working demos quickly, then help make them more reliable, scalable, and production-ready.
Learn how to direct, evaluate, and control AI coding agents to multiply engineering output.
Work closely with founders and senior engineers across product, engineering, and strategy.
Explore new AI development workflows and help the team move faster.
Contribute to a fast-moving product where experimentation, speed, and quality all matter.

Requirements

What We’re Looking For
You build with AI tools regularly and can show us what you’ve made.
You have examples of projects, repos, demos, prototypes, or technical experiments.
You’re excited about tools like Codex, Claude Code, Cursor, AI agents, and agentic development workflows.
You learn by building and ship constantly.
You have strong technical curiosity and are willing to figure things out independently.
You care more about output and learning speed than titles or credentials.
You’re comfortable working in a fast-moving environment with real responsibility.
Bonus Points
You’ve created content, demos, or tutorials around AI or software development.
You’ve tried to start something of your own.
You have a side project you’re deeply interested in.
You’ve experimented with AI agents, coding workflows, automations, or developer tools.
You’re interested in AI infrastructure, enterprise AI, governance, or agentic systems.
Why Join Us
Front-row seat: Learn how a company is built directly from founders and senior engineers.
Real responsibility: You’ll work on meaningful projects, not just small tasks.
Strong mentorship: You’ll be supported while being pushed to grow quickly.
Frontier work: Build in one of the most exciting categories in tech right now.
Output-first culture: We care about what you can build, learn, and ship.

Benefits

What We Offer

Work alongside the ChainGPT core team on high-impact AI and Web3 products across our ecosystem.
Remote-first setup with flexible hours, focused on outcomes, trust, and ownership.
Competitive compensation, with performance-based upside where applicable to the role.
Fast-moving environment with direct collaboration across all team members, including senior management, and clear accountability with no micromanagement.
The support to do your best work, including the tools you need, structured onboarding, and clear room to grow.
Company Culture and Values

At ChainGPT, we value Trust, Effective Speed, Innovation, and Growth. As our AI-Native Software Engineer - Early Career, you will embody these core values and have the opportunity to contribute to our culture and help drive our success. Join us on this exciting journey as we shape the future of blockchain and crypto technology.

Additional Information:

Employment Compliance and Confidentiality:
All employees will be onboarded through our official payroll and HR provider, which manages employment documentation, tax withholdings, and compliance with legal requirements based on the employee’s country of residence. As part of the onboarding process, each new hire is required to complete a Know Your Customer (KYC) verification, sign a Non-Disclosure Agreement (NDA), execute an employment contract, and fulfill any additional legal requirements specific to your jurisdiction. This process ensures compliance, protects company information, and establishes a secure and professional employment relationship.
Employment Structure:
The position is offered on either an employee or contractor basis, depending on the location and role. Individuals will receive payment via direct deposit on a monthly basis. Additional details regarding compensation, benefits, and company policies will be provided during onboarding and outlined in the official employment agreement.
Compensation:
Salaries are paid in fiat currency via direct deposit on a monthly schedule, with payments issued on the first business day of each month. This structure ensures timely and transparent compensation aligned with local financial systems.
Probationary Period:
All new employees will undergo a 90-day probationary period, which serves as a mutual evaluation phase. During this time, both the employee and ChainGPT can assess fit, performance, and long-term alignment with the role and company.""", projectData)
    print("\n=== SELECTED PROJECT BULLETS ===\n")
    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )
    # print(projectData["Robotic Control and Simulation Platform"])
    # for project in projectData:
    #     for bullet in result[0]["bullets"]:
    #         print(project["facts"][bullet])
    end = time.perf_counter()
    print(f"La tarea tomó {end-start:.2f}s")