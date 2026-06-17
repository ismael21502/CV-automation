import os
import json
import requests
from callAI import callAI



def _build_prompt(job_description: str) -> str:
    """
    Construye el prompt que será enviado al modelo de IA para extraer la información
    requerida del *job_description*.
    """
    return f"""You are an expert HR analyst. Extract the following information from the given job description.
        Return ONLY a JSON object with these keys in English:
        title, seniority, required_skills, domains, soft_skills, experience_years.
        If a field is not mentioned, use an empty list (for list fields) or an empty string (for title/seniority) or 0 (for experience_years).
        Job description:
        \"\"\"
        {job_description}
        \"\"\"
        """


def extractInfo(job_description: str) -> None:
    """
    Función pública que recibe la descripción del puesto, genera el prompt,
    llama a la IA y muestra por pantalla el JSON resultante.
    """
    prompt = _build_prompt(job_description)
    try:
        ai_response = callAI(prompt)
        # Se asume que la respuesta es un JSON válido; si no lo es, se captura la excepción.
        parsed = json.loads(ai_response)
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    except Exception as e:
        # En caso de error, se muestra la respuesta cruda para depuración.
        print(f"Error al procesar la respuesta de la IA: {e}")
        print("Respuesta original:")
        print(ai_response if 'ai_response' in locals() else "")


if __name__ == "__main__":
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
    extractInfo(example_description)
