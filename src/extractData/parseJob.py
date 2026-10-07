import json
# from callAI import askAI
from extractData.llm import jobParserModel
from pydantic import BaseModel

class JobData(BaseModel):
    title: str
    seniority: str #Enum?
    required_skills: list[str]
    domains: list[str]
    soft_skills: list[str]
    experience_years: int

def extractJobInfo(jobDescription: str) -> None:
    prompt = f"""You are an expert HR analyst. Extract the following information from the given job description.
        Return ONLY a JSON object with these keys in English:
        title, seniority, required_skills, domains, soft_skills, experience_years.
        If a field is not mentioned, use an empty list (for list fields) or an empty string (for title/seniority) or 0 (for experience_years).
        Job description:
        \"\"\"
        {jobDescription}
        \"\"\"
        """
    try:
        # AIResponse = askAI("fast", prompt)
        structuredModel = jobParserModel.with_structured_output(JobData)
        AIResponse = structuredModel.invoke(prompt)
        return AIResponse.model_dump()
        # parsed = json.loads(AIResponse)
        # print(json.dumps(parsed, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error al procesar la respuesta de la IA: {e}")
        print("Respuesta original:")
        print(AIResponse if 'AIResponse' in locals() else "")


if __name__ == "__main__":
    import time
    start = time.perf_counter()
    # Ejemplo rápido de uso desde la línea de comandos
    example_description = """ 
        Somos una desarrolladora de software con operaciones en Monterrey, NL. Nos enfocamos en creación de aplicaciones y servicios web/móvil utilizando una combinación de herramientas ágiles. Buscamos un desarrollador con un solido conocimiento de las bases de programación y quisiera acelerar su aprendizaje al colaborar en proyectos reales.

        Serás responsable de colaborar en múltiples proyectos con nuestro equipo y tienes experiencia con los siguientes lenguajes/herramientas:

        Javascript 1 año
        React 1 año
        Tailwind (deseable)
        NextJS (deseable)
        Liquid
        Ingles intermedio (puedes leer/escribir en inglés)
        Proficient es un equipo que cuenta con múltiples disciplinas, lenguajes y frameworks cubriendo las áreas de Frontend (diseño y codificación) y Backend. Tenemos un fuerte enfoque en fomentar la comunicación abierta entre nuestro equipo, “No hay preguntas tontas”, tendrás la oportunidad de aprender y enseñar a nuestro lado. Nos encantaría oír de ti, contáctanos!

        Datos curiosos de Proficient:

        15-20 días de vacaciones
        Trabajo remoto
        Sigue aprendiendo, Proficient da cursos internos y también puede apoyarte a solventar cursos para mejorar o aprender nuevos lenguajes/herramientas
        Tipo de puesto: Tiempo completo (con finalidad de unirte al equipo oficialmente como desarrollador JR)
        """
    print(extractJobInfo(example_description))
    end = time.perf_counter()
    print(f"La tarea tomó {end-start:.2f}s")
