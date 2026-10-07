import json
import asyncio
from extractData.getSoftSkills import selectSoftSkills
from extractData.getMatchedSkills import getMatchedSkills
from extractData.callAI import askAI
from extractData.getBullets import selectProjectBullets
from extractData.parseJob import extractJobInfo
from generatePDF import render_template, generate_pdf
from extractData.llm import writeSummaryModel
import pyperclip

# --------------------------------------------------------------------------- #
# Descripción del puesto (job description)
# --------------------------------------------------------------------------- #
# jobData = {
#   "title": "Desarrollador Junior",
#   "seniority": "Junior",
#   "required_skills": [
#     "JavaScript",
#     "React",
#     "Tailwind",
#     "NextJS",
#     "Liquid",
#     "English (intermediate)"
#   ],
#   "domains": [
#     "Frontend development",
#     "Web development",
#     "Mobile development"
#   ],
#   "soft_skills": [
#     "Open communication",
#     "Willingness to learn",
#     "Willingness to teach",
#     "Team collaboration"
#   ],
#   "experience_years": 1
# }
# --------------------------------------------------------------------------- #
# Carga de datos personales del candidato
# --------------------------------------------------------------------------- #
with open('src/data.json', 'r', encoding='utf-8') as file:
    personalData = json.load(file)


def getSummary(relevantData: dict) -> str:
    """
    Genera el resumen profesional (profile) a partir de la información
    relevante usando la API de IA.
    """
    prompt = f"""
        You are an expert resume writer.
        Using the candidate information below, write a concise professional summary for a resume.
        Requirements:
        - Maximum 35 words.
        - Professional tone.
        - Align the summary with the target position.
        - Focus on the type of projects the candidate has built and the value they can bring.
        - Highlight relevant domains, projects, and interests rather than listing technologies. Especially domains and interests.
        - Mention technical skills only if they are essential to understanding the candidate's profile.
        - Do not simply repeat items from the skills section.
        - Do not invent experience, technologies, or achievements.
        - Do not use first person ("I", "my").
        - Return ONLY the summary text.
        - Never mention domains that are only present in the job description.
        - Only mention domains supported by the candidate's projects or experience.
        - Write as an experienced human resume writer, not as an AI assistant.
        - Avoid corporate buzzwords, clichés, and exaggerated language.
        - Prefer clear and direct wording over sophisticated vocabulary.
        - The summary should sound believable for an entry-level candidate.
        - Do not use phrases such as "proven ability", "passionate professional", "results-driven", "dynamic professional", "highly motivated", or similar resume clichés.
        Candidate data:
        {relevantData}
        """
    # summary = askAI("bigger", prompt)
    summary = writeSummaryModel.invoke(prompt).content
    # La API devuelve el texto con posibles saltos de línea; lo limpiamos.
    return summary.strip()

def generateCV(jobDescription: str) -> dict:
    """
    Ejecuta todo el flujo de generación del CV y devuelve los datos
    necesarios para renderizar la plantilla HTML.
    Retorna un diccionario con:
        - hard_skills: lista de hard skills coincidentes
        - soft_skills: lista de soft skills seleccionadas
        - summary:    texto del resumen profesional
        - experience: lista de proyectos (bullets) seleccionados
    """
    jobData = extractJobInfo(jobDescription)
    # 1️⃣ Matching de hard skills
    # hardSkills = getMatchedSkills(jobData["required_skills"], personalData["Hard Skills"])
    hardSkills = getMatchedSkills(jobDescription, personalData["Hard Skills"])
    print("HARDSKILLS: ",hardSkills, type(hardSkills))
    # if affinity < 20:
    #     print("No hay match suficiente entre el perfil y la oferta.")
    #     return {}

    # 2️⃣ Selección de soft skills
    softSkills = selectSoftSkills(jobData["soft_skills"], personalData["Soft Skills"])
    # softSkills = json.loads(softSkills)
    print("Soft skills", softSkills, type(softSkills))
    # 3️⃣ Selección de proyectos (bullets)
    projects = selectProjectBullets(jobData, personalData["Projects"])

    # 4️⃣ Construcción de los datos relevantes para el resumen
    relevantData = {
        "candidate": {
            "experience_level": "Entry level",
            "hard_skills": hardSkills,
            "soft_skills": softSkills
        },
        "job": {
            "title": jobData["title"],
            "domains": jobData["domains"],
        },
        "projects": projects
    }

    # 5️⃣ Generación del resumen (profile)
    summary = getSummary(relevantData)

    # 6️⃣ Devolvemos todo lo necesario para la plantilla
    return {
        "hard_skills": hardSkills,
        "soft_skills": softSkills,
        "summary": summary,
        "experience": [{"title":project["name"], "bullets": project["bullets"]} for project in projects]
    }

def getJobDescription():
    while True:
        input(
            "\nCopia la descripción del puesto al portapapeles "
            "y presiona ENTER..."
        )
        text = pyperclip.paste().strip()
        if not text:
            print("El portapapeles está vacío.")
            continue
        preview = " ".join(text.split())[:150]
        print(f"\n{len(text)} caracteres encontrados.")
        print(f"Vista previa: {preview}...")
        confirm = input("\n¿Usar esta descripción? [S/n]: ").strip().lower()
        if confirm in ("", "s", "si", "sí", "y", "yes"):
            return text
        # print("Copia nuevamente la descripción.")

def main():
    """
    Punto de entrada del script.
    Genera los datos del CV y luego crea el PDF llamando a generatePDF.py.
    """
    cv_data = generateCV("""
    Becario de desarrollo de software
    At Jabil (NYSE: JBL), we are proud to be a trusted partner for the world's top brands, offering comprehensive engineering, supply chain, and manufacturing solutions. With 60 years of experience across industries and a vast network of over 100 sites worldwide, Jabil combines global reach with local expertise to deliver both scalable and customized solutions. Our commitment extends beyond business success as we strive to build sustainable processes that minimize environmental impact and foster vibrant and diverse communities around the globe.
    Job Summary
    The Intern provides support for day-to-day activities within the assigned function while gaining practical experience in a professional workplace environment. The role focuses on learning standard operational processes, safety practices, and quality requirements while contributing to team and organizational efficiency.

    Education & Experience
    Currently pursuing or recently completed a diploma, undergraduate, or postgraduate program in a relevant field. Prior academic, project, or internship exposure is an advantage but not mandatory.

    Responsibilities
    Support daily activities and assigned tasks under supervision. Assist with documentation, coordination, data handling, and routine activities as required. Participate in learning standard processes, safety practices, and quality requirements. Contribute to project-related work and continuous improvement initiatives while following established policies and timelines.

    Skills/ Ability Generic (High Level)
    Strong willingness to learn and adapt in a professional environment. Basic organizational, analytical, and communication skills. Ability to follow instructions, manage time effectively, and maintain attention to detail. Capable of working independently as well as collaboratively within a team setting.

    Leadership Capabilities (People Leader) "M" Career Stream
    NA

    TEN CUIDADO CON LOS FRAUDES: Las oportunidades laborales legítimas en Jabil se pueden encontrar en nuestro sitio web oficial Jabil.com. Ningun solicitante debe pagar para acceder a estas oportunidades de empleo. Al postularte para un empleo en Jabil, serás contactado a través del portal oficial de jabil por un correo electrónico con teminacion @jabil.com; llamada telefónica directa de un integrante del equipo de Jabil; o correo electrónico directo con una dirección de correo electrónico @jabil.com. Jabil no solicita pagos para realizar entrevistas ni en ningún otro momento durante el proceso de contratación. Jabil tampoco pedirá información personal de identificación como número de seguro social, acta de nacimiento, información de institución financiera, número de licencia de conducir o información de pasaporte por teléfono o correo electrónico. Si crees que estás siendo víctima de robo de identidad o fraude, repórtalo a la policía en los siguientes números y repórtala en el sitio web donde la encontraste. Llama a: 911 o 089.
    Jabil, including its subsidiaries, is an equal opportunity employer and considers qualified applicants for employment without regard to race, color, religion, national origin, sex, sexual orientation, gender identity, age, disability, genetic information, veteran status, or any other characteristic protected by law.

    Accessibility Accommodation
    If you are a qualified individual with a disability, you have the right to request a reasonable accommodation if you are unable or limited in your ability to use or access Jabil.com/Careers site as a result of your disability. You can request a reasonable accommodation by sending an e-mail to Always_Accessible@Jabil.com with the nature of your request and contact information. Please do not direct any other general employment related questions to this e-mail. Please note that only those inquiries concerning a request for reasonable accommodation will be responded to.
    """)
    if not cv_data:
        # No se pudo generar el CV (p.ej. affinity < 40)
        return

    # ------------------------------------------------------------------- #
    # Construcción del contexto que será pasado a la plantilla Jinja2.
    # Los campos que no provienen del proceso pueden quedar hardcodeados.
    # ------------------------------------------------------------------- #
    candidateData = {
        "name": "Ismael Hernandez",
        "phone": "3314161781",
        "email": "ismael21502@gmail.com",
        "github": "https://github.com/ismael21502",
        "profile": cv_data["summary"],          # resumen generado por IA
        "skills": cv_data["hard_skills"],       # hard skills coincidentes
        "softSkills": cv_data["soft_skills"],   # soft skills seleccionadas
        "experience": cv_data["experience"],     # proyectos seleccionados
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

    print("DATA: ",json.dumps(candidateData, indent=4))
    # Ruta al template HTML (puede ser relativo al proyecto)
    template_path = "index.html"
    output_pdf = "cv.pdf"

    # Renderizamos la plantilla con los datos del candidato
    rendered_html = render_template(template_path, candidateData)

    # Generamos el PDF a partir del HTML renderizado
    asyncio.run(generate_pdf(rendered_html, output_pdf))

if __name__ == "__main__":
    cvData = {}
    while True:
        if bool(cvData):
            print("Hay datos CV guardados")
        else:
            print("No hay datos CV guardados")
        option = input("""1. Ver CV guardado
2. Generar nuevo CV
3. Generar PDF con los datos guardados
Elige tu opción: """)
        import time
        start = time.perf_counter()
        if option == "1":
            print("CV guardado: \n", json.dumps(cvData, indent=4))
        elif option == "2":
            jobDescription = getJobDescription()
            if not jobDescription:
                continue
            llmData = generateCV(jobDescription)
            if not llmData: continue
            cvData = {
                    "name": "Ismael Hernandez",
                    "phone": "3314161781",
                    "email": "ismael21502@gmail.com",
                    "github": "https://github.com/ismael21502",
                    "profile": llmData["summary"],          # resumen generado por IA
                    "skills": llmData["hard_skills"],       # hard skills coincidentes
                    "softSkills": llmData["soft_skills"],   # soft skills seleccionadas
                    "experience": llmData["experience"],     # proyectos seleccionados
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
        elif option == "3":
            templatePath = "index.html"
            outputPdf = "cv.pdf"
            # Renderizamos la plantilla con los datos del candidato
            renderedHtml = render_template(templatePath, cvData)
            # Generamos el PDF a partir del HTML renderizado
            asyncio.run(generate_pdf(renderedHtml, outputPdf))
        else: 
            print("Opción inválida")
        end = time.perf_counter()
        print(f"La tarea tomó {end-start:.2f}")
