import requests
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def extractInfo(job_description: str) -> None: 
    prompt = f"""You are an expert HR analyst. Extract the following information from the given job description.
        Return ONLY a JSON object with these keys in English:
        title, seniority, required_skills, domains, soft_skills, experience_years.
        If a field is not mentioned, use an empty list (for list fields) or an empty string (for title/seniority) or 0 (for experience_years).
        Job description:
        \"\"\"
        {job_description}
        \"\"\"
        """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )
    result = response.json()
    # print(result)

    print(result["choices"][0]["message"]["content"])

extractInfo("""Descripción completa del empleo
Practicante de Desarrollo de Software

Modalidad 100% Home Office | Periodo de prácticas: 6 meses

Organización

Union Law Group

Acompañamiento

Trabajo conjunto con la Gerente de Procesos y un Ingeniero de Software.

Apoyo económico

Abiertos a ofrecer un apoyo económico acorde a experiencia, conocimientos y disponibilidad.

Objetivo del puesto

Apoyar en el desarrollo de aplicaciones internas, automatizaciones, herramientas tipo CRM, bots, agentes conversacionales y soluciones tecnológicas que ayuden a mejorar la operación, comunicación y seguimiento de procesos dentro de Union Law Group.

El practicante participará en proyectos reales enfocados en crear herramientas propias para la firma, optimizar procesos internos y automatizar tareas operativas, trabajando un proyecto a la vez bajo acompañamiento técnico y del área de Procesos.

Principales actividades

Apoyar en el desarrollo de aplicaciones internas para uso operativo de la firma.
Participar en el diseño y mejora de herramientas tipo CRM para seguimiento de clientes, casos, tareas o procesos internos.
Apoyar en la creación de bots, agentes conversacionales o automatizaciones para mejorar la comunicación por WhatsApp, teléfono u otros canales digitales.
Colaborar en proyectos de automatización de procesos administrativos, operativos y de atención al cliente.
Apoyar en el desarrollo de soluciones que permitan reducir procesos manuales y mejorar el seguimiento de información.
Participar en la integración de APIs, bases de datos, flujos digitales y herramientas internas.
Realizar pruebas, detección de errores, documentación básica y seguimiento de avances.
Trabajar con la Gerente de Procesos para comprender necesidades operativas y convertirlas en soluciones funcionales.
Colaborar con el Ingeniero de Software para aprender, desarrollar y dar continuidad a proyectos tecnológicos existentes.
Trabajar bajo un esquema ordenado, atendiendo un proyecto tecnológico a la vez, con objetivos, entregables y seguimiento definido.
Perfil requerido

Estudiante activo de Ingeniería en Software, Sistemas Computacionales, Tecnologías de la Información, Ciencias de la Computación o carrera afín.
Interés en desarrollo de aplicaciones, automatización de procesos, CRM, bots, agentes conversacionales y soluciones internas.
Conocimientos básicos o intermedios en alguno de los siguientes lenguajes o herramientas: JavaScript, Python, C#, Java o similares.
Conocimientos deseables en desarrollo web, APIs, bases de datos SQL, Git/GitHub, automatización o integración de herramientas digitales.
Interés en crear soluciones funcionales para procesos reales de negocio.
Capacidad de análisis y resolución de problemas.
Organización, responsabilidad y autonomía para trabajar bajo modalidad remota.
Buena comunicación, disposición para aprender y apertura a la retroalimentación.
Competencias deseables

Pensamiento lógico y enfoque a soluciones.
Proactividad y curiosidad tecnológica.
Interés por desarrollar aplicaciones internas y herramientas propias.
Atención al detalle.
Capacidad para entender procesos operativos y traducirlos en soluciones tecnológicas.
Organización para trabajar por proyectos, con avances y entregables definidos.
Trabajo en equipo con áreas técnicas y operativas.
Apertura para aprender sobre procesos legales, atención a clientes y operación interna.
Condiciones de la práctica

El practicante participará en proyectos reales de transformación tecnológica dentro de una firma de servicios legales con operación en México y Estados Unidos.

El objetivo es que adquiera experiencia aplicada en el desarrollo de aplicaciones internas, herramientas tipo CRM, bots, automatización de procesos y soluciones tecnológicas para mejorar la operación diaria de la firma.

Beneficios

Modalidad 100% home office.
Horarios flexibles.
Participación en proyectos reales.
Acompañamiento de una Gerente de Procesos y un Ingeniero de Software.
Oportunidad de aprendizaje en desarrollo de soluciones aplicadas a negocio.
Posibilidad de continuidad o contrato indefinido de acuerdo con desempeño, resultados y necesidades de la firma.
Programa de referidos.
Sueldo: $8,000.00 - $10,000.00 al mes

Beneficios:

Horarios flexibles
Opción a contrato indefinido
Programa de referidos""")