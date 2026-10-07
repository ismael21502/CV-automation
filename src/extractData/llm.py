from langchain_ollama import ChatOllama
import json

softSkillsModel = ChatOllama(
    model="qwen3.6:35b-a3b",
    temperature=0,
    reasoning=False,
)

hardSkillsModel = ChatOllama(
    model="qwen3.6:35b-a3b",
    temperature=0,
    reasoning=False,
    # keep_alive=0
)

jobParserModel = ChatOllama(
    model="qwen3.6:35b-a3b",
    temperature=0,
    reasoning=False
)

bulletSelectorModel = ChatOllama(
    model="qwen3.6:35b-a3b",
    temperature=0,
    reasoning=False,
    keep_alive=-1  # -1 mantiene el modelo cargado indefinidamente; los enteros indican segundos (p. ej., 300) y también se admiten duraciones como "5m" o "1h".
)

writeSummaryModel = ChatOllama(
    model="qwen3.6:35b-a3b",
    temperature=0.5,
    reasoning=False
)