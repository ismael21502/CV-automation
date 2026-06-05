import os
import time
import json
import random
import requests
from typing import Any, Dict
from dotenv import load_dotenv
load_dotenv()

# Configuración básica
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")  # Se recomienda usar variables de entorno

# Parámetros de reintento
MAX_RETRIES = 3               # Número máximo de intentos
BASE_DELAY = 2                # Retraso base en segundos (se aplicará backoff exponencial)
TIMEOUT = 30                  # Timeout de la petición en segundos


def _prepare_headers() -> Dict[str, str]:
    """
    Construye los encabezados HTTP necesarios para la llamada a la API.
    """
    if not API_KEY:
        raise EnvironmentError(
            "La variable de entorno OPENROUTER_API_KEY no está definida. "
            "Configura tu clave de API antes de ejecutar el script."
        )
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _make_request(payload: Dict[str, Any]) -> requests.Response:
    """
    Envía la petición POST a OpenRouter y devuelve la respuesta.
    """
    headers = _prepare_headers()
    return requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )


def callAI(prompt: str) -> str:
    """
    Envía un *prompt* a la API de OpenRouter y devuelve la respuesta generada.
    Implementa lógica de reintento para manejar errores 429 (Too Many Requests)
    y otros errores transitorios.

    Parámetros
    ----------
    prompt: str
        Texto que se enviará a la IA.

    Retorna
    -------
    str
        Texto de la respuesta de la IA. Si después de los reintentos no se
        obtiene una respuesta válida, se devuelve un mensaje de error amigable.
    """
    payload = {
        "model": "openai/gpt-oss-20b:free",   # Ajusta el modelo según tu suscripción
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    attempt = 0
    while attempt <= MAX_RETRIES:
        try:
            response = _make_request(payload)
            # Si la respuesta es 429, lanzamos una excepción para entrar al bloque except
            if response.status_code == 429:
                raise requests.exceptions.HTTPError(
                    f"429 Too Many Requests (attempt {attempt + 1})",
                    response=response,
                )
            response.raise_for_status()  # Lanza excepción para códigos >=400 diferentes a 429
            data = response.json()
            # La estructura de la respuesta de OpenRouter suele contener:
            # data["choices"][0]["message"]["content"]
            return data["choices"][0]["message"]["content"].strip()
        except requests.exceptions.HTTPError as http_err:
            # Manejo específico de 429
            if response.status_code == 429:
                attempt += 1
                if attempt > MAX_RETRIES:
                    return (
                        "Error: se excedió el número máximo de intentos por límite de "
                        "peticiones (429). Intenta más tarde o revisa tu cuota."
                    )
                # Backoff exponencial con jitter
                delay = BASE_DELAY * (2 ** (attempt - 1))
                jitter = delay * 0.1 * (2 * random.random() - 1)  # +/-10%
                time.sleep(delay + jitter)
                continue
            else:
                # Otros errores HTTP se devuelven directamente
                return f"Error al llamar a la API: {http_err}"
        except requests.exceptions.RequestException as req_err:
            # Errores de red, timeout, etc.
            attempt += 1
            if attempt > MAX_RETRIES:
                return f"Error de red después de varios intentos: {req_err}"
            delay = BASE_DELAY * (2 ** (attempt - 1))
            time.sleep(delay)
        except json.JSONDecodeError:
            return "Error: la respuesta de la API no es JSON válido."
        except Exception as e:
            return f"Error inesperado: {e}"

    # Si se sale del bucle sin retornar, devolvemos un mensaje genérico
    return "No se pudo obtener una respuesta de la IA."
