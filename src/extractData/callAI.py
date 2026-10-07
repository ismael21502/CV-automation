import ollama

def askAI(model: str, prompt: str) -> str:
    MODELS = {
        "fast": {
            "model": "qwen3.6:35b-a3b",
            "think": True,
        },
        "big": {
            "model": "qwen3.5:9b",
            "think": False,
        },
        "bigger": {
            "model": "qwen3.6:35b-a3b",
            "think": False,
        },
        "cloud": {
            "model": "qwen3.5:9b",
            "think": True,
        }
    }
    selectedModel = MODELS[model]
    response = ollama.chat(
        model=selectedModel["model"],
        messages=[
            {"role": "user", "content": prompt}
        ],
        think=selectedModel["think"]
    )
    return response.message.content

# print(askAI("bigger", "Hola"))