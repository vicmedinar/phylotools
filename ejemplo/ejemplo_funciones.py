import os
import phylotools.phylotools as phylo


# Define la ruta del directorio
directorio = r"C:/Users/..."
resultados = os.path.join(directorio, "resultados")


#####1 extraer codigos
#ruta al paper
ruta = os.path.join(directorio, "ejemplo", "codigos_rine.xlsx")

#ejecutar funcion
phylo.genbank_codes(ruta)


####2 descargar codigos
#ruta a los codigos extraidos
codigos = os.path.join(directorio, "resultados", "resultados_codigos.txt")

#ejecutar funcion
phylo.descargar_secuencias(codigos, resultados)
#phylo.descargar_secuencias()


####3 alineamiento
# rutas alineamiento
muscle = os.path.join(directorio, "bin", "muscle.exe")
secuencias = os.path.join(directorio, "resultados", "secuencias.fasta")
alineamiento = os.path.join(directorio, "resultados", "alineamiento.fasta")

#ejecutar alineamiento
phylo.ejecutar_muscle(muscle,secuencias,alineamiento)
#phylo.ejecutar_muscle()


####4 analisis ml
# Ruta donde está el ejecutable de IQ-TREE2
iqtree = os.path.join(directorio, "bin", "iqtree2.exe")
resultados_iqtree = os.path.join(directorio, "resultados", "resultados_iqtree")

#ejecutar ml
phylo.ml_analysis(iqtree,alineamiento, resultados_iqtree)
#phylo.ml_analysis()


####5 grafico del arbol
contree = os.path.join(directorio, "resultados", "resultados_iqtree", "analysis.contree" )
tree = os.path.join(directorio, "resultados", "arbol_filogenetico.jpg" )

#ejecutar arbol
phylo.graficar_arbol(contree, tree)
#phylo.graficar_arbol()

##reporte
phylo.generar_reporte_iqtree(resultados_iqtree)



