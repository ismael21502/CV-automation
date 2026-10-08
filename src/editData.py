def editExperience(cvData, key, label):
    print(f"\n{'=' * 21}\n     {label}\n{'=' * 21}")
    options = cvData[key]
    while True:
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option['title']}")
        print(f"{len(options) + 1}. Cancelar")
        try:
            selectedOption = int(input("Elige una opción para editarla: "))
        except ValueError:
            print("Ingresa un número válido.")
            continue
        if selectedOption == len(options) + 1:
            return cvData
        if not 1 <= selectedOption <= len(options):
            print("Opción inválida.")
            continue
        break
    experience = options[selectedOption - 1]
    print("\n¿Qué valor quieres cambiar?")
    print(f"1. Título - {experience['title']}")
    for i, bullet in enumerate(experience["bullets"], start=2):
        print(f"{i}. Bullet - {bullet}")

    print(f"{len(experience['bullets']) + 2}. Cancelar")
    try:
        selectedField = int(input("Elige una opción: "))
    except ValueError:
        print("Ingresa un número válido.")
        return cvData
    if selectedField == len(experience["bullets"]) + 2:
        return cvData
    if not 1 <= selectedField <= len(experience["bullets"]) + 1:
        print("Opción inválida.")
        return cvData
    if selectedField == 1:
        newValue = input("Ingresa el nuevo título: ").strip()
        if newValue:
            experience["title"] = newValue
    else:
        bulletIndex = selectedField - 2
        newValue = input("Ingresa el nuevo bullet: ").strip()
        if newValue:
            experience["bullets"][bulletIndex] = newValue
    return cvData

def editSkills(cvData: dict, key: str, label: str):
    print(f"\n{'='*21} \n     {label} \n{'='*21}")
    options = cvData[key]
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    print(f"{i+2}. Salir")
    selectedOption = int(input("Elige una opción para editarla: "))
    if selectedOption < 0 or selectedOption > len(options)-1:
        print("")
        return cvData
    #validar el número seleccionado
    newValue = input(f"Seleccionaste {options[selectedOption-1]}. Elige un nuevo valor: ")
    cvData[key] = [option if i != selectedOption-1 else newValue for i, option in enumerate(options)]
    return cvData

def editField(cvData, key, label):
    newValue = input(f"Ingresa el nuevo {label}: ").strip()
    if newValue:
        cvData[key] = newValue
    else:
        print("El valor no puede estar vacío.")
    return cvData