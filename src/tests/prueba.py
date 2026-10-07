import json

prueba = '{"Soft Skills": ["Problem-solving", "Proactivity"]}'
print(prueba)
jsonText = json.loads(prueba)
print(jsonText["Soft Skills"])