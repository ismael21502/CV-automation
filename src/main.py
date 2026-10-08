import json
import asyncio
from extractData.getSoftSkills import selectSoftSkills
from extractData.getMatchedSkills import getMatchedSkills
from extractData.callAI import askAI
from extractData.getBullets import selectProjectBullets
from extractData.parseJob import extractJobInfo
from generatePDF import render_template, generate_pdf
from extractData.llm import writeSummaryModel
from editData import editExperience, editSkills, editField
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
        Write a concise professional summary for the candidate, tailored to the target position.
        Requirements:
        * Maximum 35 words.
        * Use a professional, clear, and natural tone.
        * Adapt the summary to the target position by emphasizing the candidate's most relevant professional focus, capabilities, and areas of experience.
        * Describe the candidate's profile at a high level rather than listing specific projects.
        * Do not simply repeat the skills section.
        * Mention specific technologies only when they meaningfully define the candidate's profile or are highly relevant to the position.
        * Use only information supported by the candidate data. Do not invent experience, technologies, achievements, interests, or responsibilities.
        * Do not imply professional experience that the candidate does not have.
        * Do not use first person ("I", "my").
        * Avoid corporate buzzwords, clichés, and exaggerated language.
        * Avoid phrases such as "proven ability", "passionate professional", "results-driven", "dynamic professional", "highly motivated", or similar resume clichés.
        * Prefer clear and direct wording over sophisticated vocabulary.
        * The summary should sound believable for the candidate's experience level.
        * Do not mention specific projects or skills unless they are highly relevant to the position.
        * Return ONLY the summary text.
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
    # jobData = extractJobInfo(jobDescription)
    # 1️⃣ Matching de hard skills
    # hardSkills = getMatchedSkills(jobData["required_skills"], personalData["Hard Skills"])
    hardSkills = getMatchedSkills(jobDescription, personalData["Hard Skills"])
    print("HARDSKILLS: ",hardSkills, type(hardSkills))
    # if affinity < 20:
    #     print("No hay match suficiente entre el perfil y la oferta.")
    #     return {}

    # 2️⃣ Selección de soft skills
    # softSkills = selectSoftSkills(jobData["soft_skills"], personalData["Soft Skills"])
    softSkills = selectSoftSkills(jobDescription, personalData["Soft Skills"])
    # softSkills = json.loads(softSkills)
    print("Soft skills", softSkills, type(softSkills))
    # 3️⃣ Selección de proyectos (bullets)
    projects = selectProjectBullets(jobDescription, personalData["Projects"])

    # 4️⃣ Construcción de los datos relevantes para el resumen
    # relevantData = {
    #     "candidate": {
    #         "experience_level": "Entry level",
    #         "hard_skills": hardSkills,
    #         "soft_skills": softSkills
    #     },
    #     "job": {
    #         "title": jobData["title"],
    #         "domains": jobData["domains"],
    #     },
    #     "projects": projects
    # }
    relevantData = {
        "candidate": {
            "experience_level": "Entry level",
            "hard_skills": hardSkills,
            "soft_skills": softSkills
        },
        "job_description": jobDescription,
        "projects": projects
    }

    # 5️⃣ Generación del resumen (profile)
    summary = getSummary(relevantData)
    print("Summary: ", summary)
    # 6️⃣ Devolvemos todo lo necesario para la plantilla
    # return {
    #     "hard_skills": hardSkills,
    #     "soft_skills": softSkills,
    #     "summary": summary,
    #     "experience": [{"title":project["name"], "bullets": project["bullets"]} for project in projects]
    # }
    return {
        "name": "Ismael Hernandez",
        "phone": "3314161781",
        "email": "ismael21502@gmail.com",
        "github": "https://github.com/ismael21502",
        "profile": summary,          # resumen generado por IA
        "skills": hardSkills,       # hard skills coincidentes
        "softSkills": softSkills,   # soft skills seleccionadas
        "experience": [{"title":project["name"], "bullets": project["bullets"]} for project in projects],     # proyectos seleccionados
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

def loadCVData() -> dict:
    try:
        with open("src/cv.json", "r") as file:
            cvData = json.load(file)
    except Exception as e:
        print("No se pudo abrir el archivo ", e)
        return None
    return cvData

def saveCVData(newData) -> bool:
    try:
        with open("src/cv.json", "w") as file:
            json.dump(newData, file, indent=4)
    except Exception as e:
        print("No se pudo guardar el archivo ", e)
        return False
    return True
def editCVData(cvData: dict):
    """
    Permite al usuario editar un campo específico del CV.
    """
    # field = input("Ingrese el nombre del campo a editar (profile, skills, softSkills, experience): ").strip()
    field = input("""1. Name
2. Phone number
3. Email
4. Github link
5. Summary
6. Hard skills
7. Soft skills
8. Experience/Projects
Elige el campo a editar: """).strip()
    if field == "1":
        cvData = editField(cvData, "name", "nombre")
    elif field == "2":
        cvData = editField(cvData, "phone", "número de teléfono")
    elif field == "3":
        cvData = editField(cvData, "email", "email")
    elif field == "4":
        cvData = editField(cvData, "github", "link de Github")
    elif field == "5":
        cvData = editField(cvData, "profile", "summary")
    elif field == "6":
        cvData = editSkills(cvData, "skills", "Hard Skills")
    elif field == "7":
        cvData = editSkills(cvData, "softSkills", "Soft Skills")
    elif field == "8":
        cvData = editExperience(cvData, "experience", "Experience")
    else:
        print("Opción inválida")
    return cvData
if __name__ == "__main__":
    cvData = loadCVData()
    while True:
        if bool(cvData):
            print("Hay datos CV guardados")
        else:
            print("No hay datos CV guardados")
        option = input("""1. Ver CV guardado
2. Generar nuevo CV
3. Generar PDF con los datos guardados
4. Editar manualmente un campo del CV
5. Salir
Elige tu opción: """)
        import time
        start = time.perf_counter()
        if option == "1":
            print("CV guardado: \n", json.dumps(cvData, indent=4))
        elif option == "2":
            jobDescription = getJobDescription()
            if not jobDescription:
                continue
            cvData = generateCV(jobDescription)
        elif option == "3":
            templatePath = "index.html"
            outputPdf = "cv.pdf"
            # Renderizamos la plantilla con los datos del candidato
            renderedHtml = render_template(templatePath, cvData)
            # Generamos el PDF a partir del HTML renderizado
            asyncio.run(generate_pdf(renderedHtml, outputPdf))
        elif option == "4":
            cvData = editCVData(cvData)
            if saveCVData(cvData):
                print("Datos guardados correctamente.")
            else:
                print("Error al guardar los datos.")
        elif option == "5":
            break
        else: 
            print("Opción inválida")
        end = time.perf_counter()
        print(f"La tarea tomó {end-start:.2f}s")
