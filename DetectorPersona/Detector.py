import requests
import base64
from tkinter import filedialog, Tk

# === TU API KEY DE GOOGLE CLOUD VISION ===
API_KEY = ""  # ← Reemplázalo por tu clave real

# === FUNCIÓN PARA SELECCIONAR UNA IMAGEN ===
def seleccionar_imagen():
    root = Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(filetypes=[("Imagen", "*.jpg *.png *.jpeg")])
    return archivo

# === FUNCIÓN PRINCIPAL ===
def detectar_objeto_principal(ruta_imagen):
    with open(ruta_imagen, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
    body = {
        "requests": [
            {
                "image": {"content": img_base64},
                "features": [{"type": "OBJECT_LOCALIZATION", "maxResults": 10}]
            }
        ]
    }

    response = requests.post(url, json=body)

    if response.status_code == 200:
        data = response.json()
        objetos = data["responses"][0].get("localizedObjectAnnotations", [])

        if not objetos:
            print("❌ No se detectó ningún objeto.")
            return

        # Obtener el objeto con mayor score
        objeto_principal = max(objetos, key=lambda obj: obj["score"])
        nombre = objeto_principal["name"].lower()
        score = objeto_principal["score"] * 100

        print(f"🔍 Objeto con mayor confianza: {nombre} ({score:.2f}%)")

        if nombre == "person":
            print("✅ El objeto principal ES una persona.")
        else:
            print("❌ El objeto principal NO es una persona.")
    else:
        print("❌ Error en la solicitud:", response.status_code)
        print(response.text)

# === EJECUCIÓN ===
ruta = seleccionar_imagen()
if ruta:
    detectar_objeto_principal(ruta)
else:
    print("No seleccionaste ninguna imagen.")
