import json
import asyncio
from softSkills import selectSoftSkills
from matchedSkills import getMatchedSkills
from callAI import callAI
from getBullets import selectProjectBullets
from generatePDF import render_template, generate_pdf

# --------------------------------------------------------------------------- #
# Descripción del puesto (job description)
# --------------------------------------------------------------------------- #
jobDescription = {
  "title": "Desarrollador Junior",
  "seniority": "Junior",
  "required_skills": [
    "JavaScript",
    "React",
    "Tailwind",
    "NextJS",
    "Liquid",
    "English (intermediate)"
  ],
  "domains": [
    "Frontend development",
    "Web development",
    "Mobile development"
  ],
  "soft_skills": [
    "Open communication",
    "Willingness to learn",
    "Willingness to teach",
    "Team collaboration"
  ],
  "experience_years": 1
}
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
    summary = callAI(prompt)
    # La API devuelve el texto con posibles saltos de línea; lo limpiamos.
    return summary.strip()


def generateCV() -> dict:
    """
    Ejecuta todo el flujo de generación del CV y devuelve los datos
    necesarios para renderizar la plantilla HTML.

    Retorna un diccionario con:
        - hard_skills: lista de hard skills coincidentes
        - soft_skills: lista de soft skills seleccionadas
        - summary:    texto del resumen profesional
        - experience: lista de proyectos (bullets) seleccionados
    """
    # 1️⃣ Matching de hard skills
    affinity, hardSkills = getMatchedSkills(jobDescription, personalData["Hard Skills"])
    if affinity < 20:
        print("No hay match suficiente entre el perfil y la oferta.")
        return {}

    # 2️⃣ Selección de soft skills
    softSkills = selectSoftSkills(jobDescription["soft_skills"], personalData["Soft Skills"])
    softSkills = json.loads(softSkills)
    print("Soft skills", type(softSkills))
    # 3️⃣ Selección de proyectos (bullets)
    projects = selectProjectBullets(jobDescription, personalData["Projects"])

    # 4️⃣ Construcción de los datos relevantes para el resumen
    relevantData = {
        "candidate": {
            "experience_level": "Entry level",
            "hard_skills": hardSkills,
            "soft_skills": softSkills
        },
        "job": {
            "title": jobDescription["title"],
            "domains": jobDescription["domains"],
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


def main():
    """
    Punto de entrada del script.
    Genera los datos del CV y luego crea el PDF llamando a generatePDF.py.
    """
    cv_data = generateCV()
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

    # Ruta al template HTML (puede ser relativo al proyecto)
    template_path = "index.html"
    output_pdf = "cv.pdf"

    # Renderizamos la plantilla con los datos del candidato
    rendered_html = render_template(template_path, candidateData)

    # Generamos el PDF a partir del HTML renderizado
    asyncio.run(generate_pdf(rendered_html, output_pdf))


if __name__ == "__main__":
    main()
