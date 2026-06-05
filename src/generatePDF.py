#!/usr/bin/env python3
"""
Script to generate a PDF from a local HTML file using Playwright.

Now the script also renders the Jinja2 template (index.html) with real data
before converting it to PDF.

Usage:
  python src/generatePDF.py [path/to/template.html] [output/path.pdf]

If no arguments are provided, default values are used:
  - Template HTML file: ./index.html (project root)
  - PDF file:          ./cv.pdf
"""

import sys
import os
import tempfile
from pathlib import Path
import asyncio

from playwright.async_api import async_playwright

# Jinja2 is used to render the HTML template with real data.
# It is a lightweight dependency; if it is not installed, the script will
# inform the user how to install it.
try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError as e:
    print(
        "❌ Jinja2 is required to render the HTML template. Install it with:\n"
        "   pip install jinja2"
    )
    raise e

# --------------------------------------------------------------------------- #
# Datos del candidato. En un proyecto real estos datos podrían provenir de
# una base de datos, de la salida de otro script, etc.
# --------------------------------------------------------------------------- #
candidateData = {
    "name": "Ismael Hernandez",
    # "title": "Desarrollador Full Stack",
    # "location": "Guadalajara, Jalisco",
    "phone": "+52 33 14 16 17 81",
    "email": "ismael21502@gmail.com",
    "github": "https://github.com/ismael21502",
    "profile": """Robotics Engineering student
        with hands-on experience in
        software 
        development,
        backend/frontend applications,
        and system integration. Strong
        foundation in object-oriented
        programming, algorithms, and
        problem-solving""",
    "skills": ['Git', 'Github', 'Python', 'JavaScript', 'SQL', 'APIs', 'Web development'],
    "softSkills": ["Problem-solving", "Proactivity", "Responsibility", "Curiosity"],
    "experience": [
        {
            "company": "Robotic Control and Simulation Platform",
            "responsibilities": [
                "Developed a robotics control platform integrating React, Python, ESP32 hardware, and real-time WebSocket communication.",
                "Implemented generalized forward and inverse kinematics algorithms for configurable serial manipulators.",
                "Created interactive 3D visualization tools using Three.js and React Three Fiber to monitor robot state and coordinate systems.",
                "Designed a modular robot configuration framework allowing robot structure, kinematics, and UI controls to be generated from JSON definitions."
            ]
            },
        {
            "company": "Boat Rental Management System",
            "responsibilities": [
                "Developed a web application to manage boat rental operations, fleet information, and payment records.",
                "Designed and implemented CRUD workflows for maintaining operational and business data through an intuitive user interface.",
                "Delivered an MVP adopted in a real business environment and refined features based on operational feedback."
            ]
            }
    ],
    "education": [
        {
            "degree": "B.Sc. Robotics Engineering",
            "institution": "Universidad de Guadalajara",
            "status": "En curso"
        }
    ]
}


def render_template(template_path: str, context: dict) -> str:
    """
    Renderiza una plantilla Jinja2 con el contexto proporcionado y devuelve
    la ruta a un archivo HTML temporal que contiene el resultado.

    Parámetros
    ----------
    template_path: str
        Ruta al archivo HTML que contiene la plantilla (index.html).
    context: dict
        Diccionario con los datos que se insertarán en la plantilla.

    Retorna
    -------
    str
        Ruta absoluta al archivo HTML temporal generado.
    """
    template_dir = Path(template_path).parent.resolve()
    template_name = Path(template_path).name

    # Configuramos el entorno Jinja2.
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_name)
    rendered_html = template.render(**context)

    # Guardamos el HTML renderizado en un archivo temporal.
    tmp_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".html", mode="w", encoding="utf-8"
    )
    tmp_file.write(rendered_html)
    tmp_file.close()

    return tmp_file.name


async def generate_pdf(html_path: str, pdf_path: str):
    """
    Genera un PDF a partir de un archivo HTML (ya renderizado).

    Parámetros
    ----------
    html_path: str
        Ruta al archivo HTML que será convertido a PDF.
    pdf_path: str
        Ruta donde se guardará el PDF resultante.
    """
    # Resolve absolute paths
    html_file = Path(html_path).resolve()
    pdf_file = Path(pdf_path).resolve()

    # Verificamos que el HTML exista
    if not html_file.is_file():
        raise FileNotFoundError(f"HTML file not found at: {html_file}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Cargamos el archivo local
        await page.goto(f"file://{html_file}")
        # Generamos el PDF
        await page.pdf(
            path=str(pdf_file),
            format="Letter",
            print_background=True
        )
        await browser.close()
        print(f"✅ PDF generado exitosamente en: {pdf_file}")


def main():
    # Parámetros por defecto
    default_template = "index.html"
    default_pdf = "cv.pdf"

    # Argumentos de la línea de comandos (omitiendo el nombre del script)
    args = sys.argv[1:]
    template_arg = args[0] if len(args) > 0 else default_template
    pdf_arg = args[1] if len(args) > 1 else default_pdf

    try:
        # 1️⃣ Renderizamos la plantilla con los datos reales.
        rendered_html_path = render_template(template_arg, candidateData)

        # 2️⃣ Generamos el PDF a partir del HTML renderizado.
        asyncio.run(generate_pdf(rendered_html_path, pdf_arg))

        # Opcional: eliminamos el archivo temporal después de crear el PDF.
        try:
            os.remove(rendered_html_path)
        except OSError:
            pass

    except Exception as e:
        print(f"❌ Error al generar el PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
