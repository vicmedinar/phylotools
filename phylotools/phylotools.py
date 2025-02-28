##buscar codigos
import re
import os
import docx
import PyPDF2
import pandas as pd

def read_txt(file_path):
    """Leer un archivo de texto plano (.txt)."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_docx_tables(file_path):
    """Leer las tablas de un archivo DOCX y concatenar el contenido."""
    doc = docx.Document(file_path)
    text = ""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text += cell.text + "\n"
    return text

def read_pdf(file_path):
    """Extraer el texto de un archivo PDF."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

def read_excel(file_path):
    """Leer un archivo Excel y convertir su contenido en texto."""
    df = pd.read_excel(file_path, sheet_name=None)
    text = ""
    for sheet_name, sheet_data in df.items():
        text += sheet_data.to_string(index=False) + "\n"
    return text

def extract_genbank_codes(text):
    """
    Extrae los códigos GenBank del texto usando una expresión regular.
    Se buscan cadenas que empiecen con dos letras mayúsculas seguidas de 5 o más dígitos.
    """
    pattern = r'\b[A-Z]{2}\d{5,}\b'
    codigos = re.findall(pattern, text)
    return list(set(codigos))  # Eliminar duplicados

def genbank_codes(file_path=None):
    """
    Función principal que:
      - Pide la ruta del archivo que contiene los códigos si no se proporciona.
      - Lee el archivo según su extensión (.txt, .docx, .pdf o .xlsx).
      - Extrae los códigos GenBank encontrados.
      - Crea una carpeta "resultados" y guarda los códigos en un archivo .txt.
    """
    # Solicitar la ruta si no se proporcionó
    if file_path is None or file_path.strip() == "":
        file_path = input("Ingrese la ruta del archivo que contiene los códigos: ").strip()

    # Seleccionar la función de lectura según la extensión del archivo
    if file_path.endswith('.docx'):
        text = read_docx_tables(file_path)
    elif file_path.endswith('.pdf'):
        text = read_pdf(file_path)
    elif file_path.endswith('.xlsx'):
        text = read_excel(file_path)
    elif file_path.endswith('.txt'):
        text = read_txt(file_path)
    else:
        print("Formato de archivo no soportado")
        return []

    codigos = extract_genbank_codes(text)

    # Definir la ruta de trabajo y la carpeta de resultados
    ruta_trabajo = r"C:/Users/Vistor/Desktop/victor/maestria Nacional/materias/primer semestre/programacion para biologos/ensayo/tareas/trabajo final"
    carpeta_resultados = os.path.join(ruta_trabajo, "resultados")
    os.makedirs(carpeta_resultados, exist_ok=True)

    # Crear y escribir el archivo de resultados en formato .txt
    archivo_resultado = os.path.join(carpeta_resultados, "resultados_codigos.txt")
    with open(archivo_resultado, 'w', encoding='utf-8') as f:
        for codigo in codigos:
            f.write(codigo + "\n")

    print(f"Los códigos han sido guardados en: {archivo_resultado}")
    return codigos

if __name__ == '__main__':
    codigos = genbank_codes()
    if codigos:
        print("Códigos GenBank encontrados:")
        print(codigos)
    else:
        print("No se encontraron códigos GenBank.")

##descargar secuencias
import os
import io
from Bio import Entrez, SeqIO

# Configura tu dirección de correo electrónico para acceder a la API de NCBI
Entrez.email = "tu_correo@ejemplo.com"

def descargar_y_renombrar_secuencias(codigos, ruta_salida, nombre_archivo="secuencias.fasta"):
    """
    Descarga las secuencias de NCBI para cada código, les asigna un nuevo encabezado
    y guarda todas las secuencias en un archivo FASTA dentro de la ruta de salida.
    """
    ruta_completa = os.path.join(ruta_salida, nombre_archivo)

    with open(ruta_completa, "w", encoding="utf-8") as archivo_salida:
        for num_acceso in codigos:
            try:
                # Obtener secuencia de NCBI
                handle = Entrez.efetch(db="nucleotide", id=num_acceso, rettype="fasta", retmode="text")
                secuencia = handle.read()
                handle.close()

                # Parsear la secuencia
                registro_secuencia = SeqIO.read(io.StringIO(secuencia), "fasta")

                # Generar nuevo encabezado (nombre de especie + número de acceso)
                partes_especie = registro_secuencia.description.split()
                if len(partes_especie) >= 3:
                    nuevo_encabezado = f">{partes_especie[1]}_{partes_especie[2].replace('.', '')}_{num_acceso}"
                else:
                    nuevo_encabezado = f">Especie_Desconocida_{num_acceso}"

                # Escribir en archivo de salida
                archivo_salida.write(f"{nuevo_encabezado}\n")
                archivo_salida.write(f"{registro_secuencia.seq}\n")

                print(f"Descargado y renombrado: {num_acceso}")

            except Exception as e:
                print(f"Error procesando {num_acceso}: {e}")

    print(f"Secuencias guardadas en {ruta_completa}")

def descargar_secuencias(codigos_path=None, ruta_salida=None, nombre_archivo="secuencias.fasta"):
    """
    Función principal que:
      - Solicita la ruta del archivo que contiene los códigos GenBank (uno por línea) si no se proporciona.
      - Solicita la ruta de salida para guardar el archivo de secuencias si no se proporciona.
      - Lee los códigos y llama a la función que descarga y renombra las secuencias.
    """
    # Solicitar la ruta al archivo con códigos si no se especificó
    if codigos_path is None or codigos_path.strip() == "":
        codigos_path = input("Ingrese la ruta del archivo que contiene los códigos GenBank: ").strip()

    # Leer los códigos desde el archivo (se asume un código por línea)
    with open(codigos_path, "r", encoding="utf-8") as f:
        codigos = [line.strip() for line in f if line.strip()]

    # Solicitar la ruta de salida si no se especificó
    if ruta_salida is None or ruta_salida.strip() == "":
        ruta_salida = input("Ingrese la ruta de salida para guardar las secuencias: ").strip()

    # Crear la carpeta de salida si no existe
    os.makedirs(ruta_salida, exist_ok=True)

    descargar_y_renombrar_secuencias(codigos, ruta_salida, nombre_archivo)

if __name__ == '__main__':
    descargar_secuencias()

# #####  Parte 3        Alinemiento MUSCLE

import sys
import subprocess

def ejecutar_muscle(muscle_path=None, input_file=None, output_file=None):
    """
    Ejecuta MUSCLE para realizar el alineamiento de secuencias.
    Si no se especifican las rutas al ejecutable, al archivo de entrada o al archivo de salida,
    se solicitan al usuario por consola.
    """
    if not muscle_path:
        muscle_path = input("Ingresa la ruta al ejecutable de MUSCLE: ")
    if not input_file:
        input_file = input("Ingresa la ruta al archivo de entrada (.fasta): ")
    if not output_file:
        output_file = input("Ingresa la ruta al archivo de salida (.fasta): ")

    command = [muscle_path, "-in", input_file, "-out", output_file]

    try:
        subprocess.run(command, check=True)
        print(f"El alineamiento se ha completado y guardado en: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar MUSCLE: {e}")
    except FileNotFoundError:
        print(f"No se encontró el ejecutable de MUSCLE en la ruta especificada: {muscle_path}")

if __name__ == "__main__":
    # Se verifican los argumentos pasados por la línea de comandos
    muscle_path = sys.argv[1] if len(sys.argv) > 1 else None
    input_file  = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    ejecutar_muscle(muscle_path, input_file, output_file)
# ###### parte 4     ML con IQtree

import os
import subprocess


def ml_analysis(executable_path=None, alignment_path=None, results_path=None):
    """
    Ejecuta IQ-TREE2 para análisis de Maximum Likelihood.

    Parámetros:
      executable_path: Ruta completa al ejecutable de IQ-TREE2.
      alignment_path: Ruta completa al archivo de alineamiento (.fasta).
      results_path: Ruta a la carpeta donde se guardarán los resultados.

    Si alguno no se proporciona, se solicitará de forma interactiva.

    Luego, se pregunta si se desea usar los parámetros por defecto:
      - Si la respuesta es "si", se usa el modelo "MFP" y 1000 réplicas de ultrafast bootstrap.
      - Si la respuesta es "no", se solicitarán los parámetros personalizados.
    """
    # Solicitar los argumentos si no se proporcionan o están vacíos
    if executable_path is None or not executable_path.strip():
        executable_path = input("Ingrese la ruta al ejecutable de IQ-TREE2: ").strip()

    if alignment_path is None or not alignment_path.strip():
        alignment_path = input("Ingrese la ruta al archivo de alineamiento (.fasta): ").strip()

    if results_path is None or not results_path.strip():
        results_path = input("Ingrese la ruta de la carpeta para guardar los resultados: ").strip()

    # Crear la carpeta de resultados si no existe
    os.makedirs(results_path, exist_ok=True)

    # Definir el prefijo de resultados (se añadirá "analysis")
    results_prefix = os.path.join(results_path, "analysis")

    # Preguntar si se desea usar parámetros por defecto
    respuesta = input(
        "¿Desea correr el análisis de Maximum Likelihood con parámetros por defecto? (si/no): ").strip().lower()
    if respuesta == "si":
        model = "MFP"  # Selección automática del mejor modelo
        bb_value = "1000"  # 1000 réplicas de ultrafast bootstrap
    else:
        bb_value = input("Ingrese el valor para ultrafast bootstrap: ").strip()
        modelo_auto = input("¿Desea selección automática del mejor modelo? (si/no): ").strip().lower()
        if modelo_auto == "si":
            model = "MFP"
        else:
            model = input("Escriba el modelo que desea usar: ").strip()

    # Construir el comando para IQ-TREE2
    command = [
        executable_path,
        "-s", alignment_path,
        "-m", model,
        "-bb", bb_value,
        "-nt", "AUTO",
        "-pre", results_prefix
    ]

    try:
        subprocess.run(command, check=True)
        print("¡Análisis completado!")
        print(f"Los resultados se han guardado en la carpeta: {results_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar IQ-TREE2: {e}")
    except FileNotFoundError:
        print(f"No se encontró el ejecutable de IQ-TREE2 en la ruta especificada: {executable_path}")


if __name__ == '__main__':
    ml_analysis()

# ###  parte 5    grafica arbol

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from Bio import Phylo

def graficar_arbol(archivo_contree=None, output_file=None):
    """
    Lee un árbol en formato Newick, lo enraíza en el nodo más lejano,
    lo dibuja y guarda la imagen resultante en la ruta especificada.
    Si no se provee la ruta de entrada o de salida, se solicitan al usuario.
    """
    # Si se recibe una tupla, usar el primer elemento
    if isinstance(archivo_contree, tuple):
        archivo_contree = archivo_contree[0]
    if not isinstance(archivo_contree, str) or archivo_contree.strip() == "":
        archivo_contree = input("Ingrese la ruta del archivo .contree (entrada): ").strip()

    if isinstance(output_file, tuple):
        output_file = output_file[0]
    if not isinstance(output_file, str) or output_file.strip() == "":
        output_file = input("Ingrese la ruta de salida para guardar el árbol (.jpg): ").strip()

    # Leer el árbol en formato Newick
    arbol = Phylo.read(archivo_contree, "newick")

    # Enraizar el árbol en el nodo más lejano (ajustar si es necesario)
    arbol.root_at_midpoint()

    # Configurar los parámetros de visualización
    plt.rcParams['font.size'] = 16
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.style'] = 'italic'

    # Crear figura con dimensiones adecuadas para mejor legibilidad
    fig, ax = plt.subplots(figsize=(10, 12))

    # Dibujar el árbol con configuraciones personalizadas
    Phylo.draw(arbol, axes=ax, do_show=False)

    # Personalizar la apariencia del gráfico
    ax.set_title('')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='both', which='both', length=0)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Ajustar diseño para maximizar el espacio
    plt.tight_layout()

    # Mostrar el gráfico en pantalla
    plt.show()

    # Guardar la imagen del árbol en alta resolución
    plt.savefig(output_file, dpi=300, bbox_inches='tight')


    print(f"El árbol se ha guardado en: {output_file}")

if __name__ == '__main__':
    graficar_arbol()


## reporte de analisis
import os
import glob
import re
import argparse

def generar_reporte_iqtree(ruta_resultados):
    """
    Esta función busca el archivo .iqtree en el directorio indicado, extrae la información y
    genera un reporte en consola.

    Se extrae la siguiente información:
      - Referencias IQ-TREE          (línea 16)
      - Referencias ModelFinder      (línea 23)
      - Ultrafast bootstrap          (línea 30)
      - Tiempo total del análisis    (línea 364)
      - Input data                   (buscado con regex)
      - Number of constant sites     (buscado con regex)
      - Number of invariant (constant or ambiguous constant) sites  (regex)
      - Number of parsimony informative sites  (regex)
      - Number of distinct site patterns       (regex)
      - Model of substitution        (regex)
    """
    # Buscar el archivo .iqtree en el directorio proporcionado
    archivos_iqtree = glob.glob(os.path.join(ruta_resultados, "*.iqtree"))
    if not archivos_iqtree:
        print("No se encontró ningún archivo .iqtree en la ruta proporcionada.")
        return
    archivo_iqtree = archivos_iqtree[0]  # Se toma el primero encontrado

    # Leer todas las líneas del archivo
    try:
        with open(archivo_iqtree, "r") as f:
            lineas = f.readlines()
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        return

    resultados = {}

    # Extraer información de líneas fijas (recordar que en Python la numeración inicia en 0)
    lineas_fijas = {
        "Referencias IQ-TREE": 15,          # línea 16
        "Referencias ModelFinder": 22,      # línea 23
        "Ultrafast bootstrap": 29,          # línea 30
        "Tiempo total del análisis": 363    # línea 364
    }

    for campo, idx in lineas_fijas.items():
        if idx < len(lineas):
            linea = lineas[idx].strip()
            partes = linea.split(":", 1)
            if len(partes) > 1:
                resultados[campo] = partes[1].strip()
            else:
                resultados[campo] = "Formato no esperado"
        else:
            resultados[campo] = "No disponible"

    # Definir patrones para buscar la información restante mediante expresiones regulares
    patrones = {
        "Input data": r"(?i)^.*Input data.*:\s*(.+)$",
        "Number of constant sites": r"(?i)^.*Number of constant sites.*:\s*(\d+).*",
        "Number of invariant (constant or ambiguous constant) sites": r"(?i)^.*Number of invariant.*sites.*:\s*(\d+).*",
        "Number of parsimony informative sites": r"(?i)^.*Number of parsimony informative sites.*:\s*(\d+).*",
        "Number of distinct site patterns": r"(?i)^.*Number of distinct site patterns.*:\s*(\d+).*",
        "Model of substitution": r"(?i)^.*Model of substitution.*:\s*(.+)$"
    }

    # Buscar en todas las líneas los campos definidos con regex, sin sobreescribir los ya extraídos
    for linea in lineas:
        for campo, patron in patrones.items():
            if campo not in resultados:
                match = re.search(patron, linea)
                if match:
                    resultados[campo] = match.group(1).strip()

    # Imprimir el reporte
    print("Reporte de resultados de IQ-TREE:")
    campos_orden = [
        "Referencias IQ-TREE",
        "Referencias ModelFinder",
        "Ultrafast bootstrap",
        "Tiempo total del análisis",
        "Input data",
        "Number of constant sites",
        "Number of invariant (constant or ambiguous constant) sites",
        "Number of parsimony informative sites",
        "Number of distinct site patterns",
        "Model of substitution"
    ]
    for campo in campos_orden:
        valor = resultados.get(campo, "No encontrado")
        print(f"{campo}: {valor}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Genera un reporte a partir de un archivo .iqtree de IQ-TREE.'
    )
    parser.add_argument('ruta', nargs='?', type=str,
                        help='Ruta al directorio que contiene el archivo .iqtree')
    args, unknown = parser.parse_known_args()

    if not args.ruta:
        ruta = input("Por favor ingrese la ruta al directorio que contiene el archivo .iqtree: ")
    else:
        ruta = args.ruta

    generar_reporte_iqtree(ruta)
