# PHYLOTOOLS – Herramientas para Filogenias Moleculares

## Introducción
Phylotools es un paquete diseñado para facilitar el análisis filogenético molecular. Incluye herramientas para:
- Extraer códigos GenBank desde archivos en formatos TXT, DOCX, PDF y Excel.
- Descargar secuencias de NCBI basadas en dichos códigos.
- Realizar alineamientos de secuencias con MUSCLE.
- Ejecutar análisis de máxima verosimilitud (ML) con IQ-TREE.
- Visualizar árboles filogenéticos en formato Newick.
- Generar reportes a partir de los resultados de IQ-TREE.

## Requisitos
- **Python 3.x**
- **Librerías**: `re`, `os`, `sys`, `subprocess`, `argparse`, `glob`, `docx`, `PyPDF2`, `pandas`, `Bio` (Biopython), `matplotlib`
- Ejecutables de [MUSCLE](https://www.drive5.com/muscle/) e [IQ-TREE2](http://www.iqtree.org/)

## Funciones y Variables del Paquete

### 1. Lectura de Archivos y Extracción de Códigos GenBank
**Descripción**: Permite leer diferentes tipos de archivos y extraer los códigos GenBank que contengan.

- **read_txt(file_path):** Lee un archivo .txt y devuelve su contenido en forma de cadena.
- **read_docx_tables(file_path):** Lee todas las tablas de un archivo .docx y concatena su contenido en una sola cadena.
- **read_pdf(file_path):** Extrae todo el texto de un archivo PDF y lo devuelve como cadena.
- **read_excel(file_path):** Lee las hojas de un archivo Excel (.xlsx) y devuelve una cadena con la información combinada.
- **extract_genbank_codes(text):** Utiliza una expresión regular para encontrar y extraer códigos GenBank (dos letras mayúsculas seguidas de 5 o más dígitos).
- **genbank_codes(file_path=None):** Función principal para extraer códigos GenBank desde un archivo; identifica el tipo de archivo y llama a la lectura correspondiente.

### 2. Descarga de Secuencias
**Descripción**: Descarga secuencias de la base de datos de NCBI y renombra los encabezados para facilitar la identificación de las especies.

- **descargar_y_renombrar_secuencias(codigos, ruta_salida, nombre_archivo="secuencias.fasta"):** Descarga secuencias de NCBI según los códigos proporcionados, renombra los encabezados y guarda todo en un archivo FASTA.
- **descargar_secuencias(codigos_path=None, ruta_salida=None, nombre_archivo="secuencias.fasta"):** Función principal que solicita la ruta con los códigos, los lee y llama a la descarga de secuencias.

### 3. Alineamiento de Secuencias con MUSCLE
**Descripción**: Ejecuta el software MUSCLE para alinear las secuencias FASTA obtenidas.

- **ejecutar_muscle(muscle_path=None, input_file=None, output_file=None):** Lanza el ejecutable de MUSCLE para alinear secuencias de un archivo FASTA y genera un archivo de alineamiento.

### 4. Análisis de Máxima Verosimilitud con IQ-TREE
**Descripción**: Mediante IQ-TREE2, realiza un análisis filogenético de máxima verosimilitud, estimando el mejor modelo y calculando los valores de soporte.

- **ml_analysis(executable_path=None, alignment_path=None, results_path=None):** Ejecuta IQ-TREE2 para realizar un análisis filogenético de máxima verosimilitud sobre un archivo de alineamiento. los paramatros predeterminados son: 1000 ultrafast bootstrap y selecion automatica del modelo 

### 5. Visualización del Árbol Filogenético
**Descripción**: Carga el árbol resultante en formato Newick y genera una representación gráfica enraizada.

- **graficar_arbol(archivo_contree=None, output_file=None):** Lee un árbol en formato Newick, lo enraíza de forma automática y genera una imagen para visualizar la filogenia.

### 6. Generación de Reporte de IQ-TREE
**Descripción**: Extrae información esencial del archivo .iqtree (como tiempo de ejecución, modelo, bootstrap) y la muestra en un reporte.

- **generar_reporte_iqtree(ruta_resultados):** Busca el archivo .iqtree en la carpeta de resultados y extrae información clave (tiempo de ejecución, modelo, bootstrap, etc.) para mostrarla en consola.

## Flujo de Trabajo
1. **Extracción de Códigos GenBank** – `genbank_codes`
2. **Descarga de Secuencias** – `descargar_secuencias`
3. **Alineamiento** – `ejecutar_muscle`
4. **Análisis ML** – `ml_analysis`
5. **Visualización** – `graficar_arbol`
6. **Reporte** – `generar_reporte_iqtree`

## Configuración y Personalización
- Asegúrate de proporcionar rutas correctas en cada función.
- Ajusta parámetros de MUSCLE e IQ-TREE según tus necesidades.

## Ejemplo de uso 

La carpeta ejemplo contiene distintos archivos para poner aprueba la funcion apartir de un conjunto de datos publicados para la descripcion de dos especies nuevas de peces.

