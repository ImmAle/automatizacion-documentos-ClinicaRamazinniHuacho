import tkinter as tk
from tkinter import ttk, messagebox
from docxtpl import DocxTemplate
import datetime
import os

# -BASE DE DATOS DE MÉDICOS (Faltan más)

MEDICOS_DB = {
    "Dr. SANTOS REYES MARTIN MANUEL DAJHALMAN": {
        "cmp": "25517", 
        "genero": "M"
    },
    "Dra. VALVERDE CHIRRE KELLY NICOLE": {
        "cmp": "113433", 
        "genero": "F"
    },
    "Dra. REA MARCOS JACKELINE ARACELY": {
        "cmp": "098761", 
        "genero": "F"
    },
    "Dra. JIMÉNEZ HUACHACA OSIRIS MALÍ": {
        "cmp": "098769", 
        "genero": "F"
    },
    "Dra. NAVA ZORRILLA ANA XIMENA": {
        "cmp": "113782", 
        "genero": "F"
    },
    "Dr. RAMIREZ CHAVEZ KEVIN ALEXIS": {
        "cmp": "100331", 
        "genero": "M"
    },
    "Dra. FLORES GRADOS ILEIN NAOMI": {
        "cmp": "104903", 
        "genero": "F"
    },
    "Dr. RODAS ESPINOZA ITALO HERMAN": {
        "cmp": "085941", 
        "genero": "M"
    },
    "Dr. CHUMBES CONDOR JEFFREY NIGEL": {
        "cmp": "089179", 
        "genero": "M"
    }
}

# --- LÓGICA---

def obtener_fecha_actual():
    """Genera la fecha en formato: Huacho, 10 de febrero 2026"""
    hoy = datetime.date.today()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"Huacho, {hoy.day} de {meses[hoy.month - 1]} del {hoy.year}"

def generar_documentos():
    # Obtener datos de la interfaz
    nombre = entry_nombre.get().upper()
    dni = entry_dni.get()
    edad = entry_edad.get()
    genero_seleccionado = combo_genero.get()
    medico_nombre = combo_medico.get()

    if not nombre or not dni or not edad or not genero_seleccionado or not medico_nombre:
        messagebox.showwarning("Faltan Datos", "Por favor, completa todos los campos.")
        return

    #  Crear la carpeta de destino si no existe (llamada Documentos Generados)
    carpeta_destino = "DOCUMENTOS_GENERADOS"
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    #  Lógica Automática (Paciente y Médico)
    if genero_seleccionado == "FEMENINO":
        genero_texto, estado_salud, titulo_cortesia = "FEMENINO", "SANA", "la Sra."
    else:
        genero_texto, estado_salud, titulo_cortesia = "MASCULINO", "SANO", "el Sr."

    datos_medico = MEDICOS_DB[medico_nombre]
    suscribe_prefix = "La que suscribe" if datos_medico["genero"] == "F" else "El que suscribe"

    #Diccionario de Contexto
    contexto = {
        'medico_nombre': medico_nombre,
        'medico_cmp': datos_medico["cmp"],
        'suscribe_prefix': suscribe_prefix, 
        'paciente_nombre': nombre,
        'dni': dni,
        'edad': edad,
        'genero': genero_texto,
        'estado_salud': estado_salud,
        'titulo_cortesia': titulo_cortesia,
        'fecha_larga': obtener_fecha_actual()
    }

    # Generación de Archivos en la carpeta que se creara (subcarpeta)
    try:
        if not os.path.exists("plantilla_certificado.docx") or not os.path.exists("plantilla_constancia.docx"):
            messagebox.showerror("Error", "Plantillas no encontradas.")
            return

        # Definir rutas completas dentro de la subcarpeta
        # Usamos el dni y nombre para que los archivos sean fáciles de identificar
        nombre_limpio = nombre.replace(" ", "_")
        ruta_cert = os.path.join(carpeta_destino, f"Certificado_{nombre_limpio}_{dni}.docx")
        ruta_const = os.path.join(carpeta_destino, f"Constancia_{nombre_limpio}_{dni}.docx")

        # Generar Certificado
        doc_cert = DocxTemplate("plantilla_certificado.docx")
        doc_cert.render(contexto)
        doc_cert.save(ruta_cert)

        # Generar Constancia
        doc_const = DocxTemplate("plantilla_constancia.docx")
        doc_const.render(contexto)
        doc_const.save(ruta_const)

        messagebox.showinfo("Éxito", f"Documentos guardados en la carpeta '{carpeta_destino}'")
        
        # Limpiar lo campos
        entry_nombre.delete(0, tk.END)
        entry_dni.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_nombre.focus()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")
        
# --- INTERFAZ GRÁFICA (GUI) ---

ventana = tk.Tk()
ventana.title("Clínica Ramazinni - Generador")
ventana.geometry("550x450")
ventana.resizable(False, False)

# Estilos visuales
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("TEntry", padding=5)

marco = ttk.Frame(ventana, padding="25")
marco.pack(fill=tk.BOTH, expand=True)

# Encabezado
lbl_titulo = ttk.Label(marco, text="Generación de Documentos", font=("Segoe UI", 16, "bold"))
lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 25))

# Formulario
# 1. Nombre
ttk.Label(marco, text="Nombre Paciente:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_nombre = ttk.Entry(marco, width=45)
entry_nombre.grid(row=1, column=1, pady=5, sticky=tk.W)

# 2. DNI
ttk.Label(marco, text="DNI:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_dni = ttk.Entry(marco, width=20)
entry_dni.grid(row=2, column=1, sticky=tk.W, pady=5)

# 3. Edad
ttk.Label(marco, text="Edad:").grid(row=3, column=0, sticky=tk.W, pady=5)
entry_edad = ttk.Entry(marco, width=10)
entry_edad.grid(row=3, column=1, sticky=tk.W, pady=5)

# 4. Género Paciente
ttk.Label(marco, text="Género Paciente:").grid(row=4, column=0, sticky=tk.W, pady=5)
combo_genero = ttk.Combobox(marco, values=["MASCULINO", "FEMENINO"], state="readonly", width=18)
combo_genero.grid(row=4, column=1, sticky=tk.W, pady=5)
combo_genero.current(0) 

# 5. Médico
ttk.Label(marco, text="Médico Tratante:").grid(row=5, column=0, sticky=tk.W, pady=5)
lista_medicos = list(MEDICOS_DB.keys())
combo_medico = ttk.Combobox(marco, values=lista_medicos, state="readonly", width=43)
combo_medico.grid(row=5, column=1, sticky=tk.W, pady=5)
if lista_medicos:
    combo_medico.current(0)

# Separador
ttk.Separator(marco, orient='horizontal').grid(row=6, column=0, columnspan=2, sticky='ew', pady=25)

# Botón Principal
btn_generar = ttk.Button(marco, text="GENERAR CERTIFICADO Y CONSTANCIA", command=generar_documentos)
btn_generar.grid(row=7, column=0, columnspan=2, ipady=10, sticky="ew")

# Nota al pie para 
lbl_footer = ttk.Label(marco, text="Nota: asegúrate de que las plantillas Word estén cerradas antes de generar.", font=("Segoe UI", 8), foreground="#666666")
lbl_footer.grid(row=8, column=0, columnspan=2, pady=15)

ventana.mainloop()