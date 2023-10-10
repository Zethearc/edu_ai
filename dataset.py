import os
import csv
import faker
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Ruta del archivo CSV
nombre_archivo = "datos.csv"

# Verificar si el archivo CSV ya existe
if not os.path.exists(nombre_archivo):

    # Crear una lista de encabezados para las columnas.
    columnas = ["Area", "Tema", "Subtema", "Descripcion", "Preguntas", "Respuestas" , "Teoremas", "Formulas", "Aplicaciones", "Ejercicios", "Material_Audiovisual"]

    # Definir la cantidad de filas por tema.
    filas_por_tema = 100

    # Definir los temas y subtemas exactos.
    temas = [
        "FUNDAMENTOS",
        "FUNCIONES",
        "FUNCIONES_POLINOMIALES_Y_RACIONALES",
        "FUNCIONES_EXPONENCIALES_Y_LOGARITMICAS",
        "FUNCIONES_TRIGONOMETRICAS_METODO_DE_LA_CIRCUNFERENCIA_UNITARIA",
        "FUNCIONES_TRIGONOMETRICAS_METODO_DEL_TRIANGULO_RECTANGULO",
        "TRIGONOMETRIA_ANALITICA",
        "COORDENADAS_POLARES_Y_ECUACIONES_PARAMETRICAS",
        "VECTORES_EN_DOS_Y_TRES_DIMENSIONES",
        "SISTEMAS_DE_ECUACIONES_Y_DESIGUALDADES",
        "SECCIONES_CONICAS"
    ]

    subtemas_por_tema = {
        "FUNDAMENTOS": ["Numeros_reales", "Exponentes_y_radicales", "Expresiones_algebraicas", "Expresiones_racionales", "Ecuaciones", "Modelado_con_ecuaciones", "Desigualdades", "Geometria_de_coordenadas", "Calculadoras_graficadoras_resolucion_grafica_de_ecuaciones_y_desigualdades", "Rectas", "Modelos_con_el_uso_de_variaciones"],
        "FUNCIONES": ["Que_es_una_funcion", "Graficas_de_funciones", "Informacion_a_partir_de_la_grafica_de_una_funcion", "Rapidez_de_cambio_promedio_de_una_funcion", "Transformaciones_de_funciones", "Combinacion_de_funciones", "Funciones_uno_a_uno_y_sus_inversas", "Modelado_con_funciones"],
        "FUNCIONES_POLINOMIALES_Y_RACIONALES": ["Funciones_y_modelos_cuadraticos", "Funciones_polinomiales_y_sus_graficas", "Division_de_polinomios", "Ceros_reales_de_funciones_polinomiales", "Numeros_complejos", "Ceros_complejos_y_el_Teorema_Fundamental_de_Algebra", "Funciones_racionales"],
        "FUNCIONES_EXPONENCIALES_Y_LOGARITMICAS": ["Funciones_exponenciales", "La_funcion_exponencial_natural", "Funciones_logaritmicas", "Leyes_de_logaritmos", "Ecuaciones_exponenciales_y_logaritmicas", "Modelado_con_funciones_exponenciales_y_logaritmicas"],
        "FUNCIONES_TRIGONOMETRICAS_METODO_DE_LA_CIRCUNFERENCIA_UNITARIA": ["La_circunferencia_unitaria", "Funciones_trigonometricas_de_numeros_reales", "Graficas_trigonometricas", "Mas_graficas_trigonometricas", "Funciones_trigonometricas_inversas_y_sus_graficas", "Modelado_de_movimiento_armonico"],
        "FUNCIONES_TRIGONOMETRICAS_METODO_DEL_TRIANGULO_RECTANGULO": ["Medida_de_un_angulo", "Trigonometria_de_triangulos_rectangulos", "Funciones_trigonometricas_de_angulos", "Funciones_trigonometricas_inversas_y_triangulos_rectangulos", "La_Ley_de_Senos"],
        "TRIGONOMETRIA_ANALITICA": ["Identidades_trigonometricas", "Formulas_de_adicion_y_sustraccion", "Formulas_de_angulo_doble_semiangulo_y_producto_a_suma", "Ecuaciones_trigonometricas_basicas", "Mas_ecuaciones_trigonometricas"],
        "COORDENADAS_POLARES_Y_ECUACIONES_PARAMETRICAS": ["Coordenadas_polares", "Graficas_de_ecuaciones_polares", "Forma_polar_de_numeros_complejos_Teorema_de_De_Moivre", "Curvas_planas_y_ecuaciones_parametricas"],
        "VECTORES_EN_DOS_Y_TRES_DIMENSIONES": ["Vectores_en_dos_dimensiones", "El_producto_punto", "Geometria_de_coordenadas_en_tres_dimensiones", "Vectores_en_tres_dimensiones", "El_producto_cruz", "Ecuaciones_de_rectas_y_planos"],
        "SISTEMAS_DE_ECUACIONES_Y_DESIGUALDADES": ["Sistemas_de_ecuaciones_lineales_con_dos_incognitas", "Sistemas_de_ecuaciones_lineales_con_varias_incognitas", "Matrices_y_sistemas_de_ecuaciones_lineales", "El_algebra_de_matrices", "Inversas_de_matrices_y_ecuaciones_matriciales", "Determinantes_y_Regla_de_Cramer", "Fracciones_parciales", "Sistemas_de_ecuaciones_no_lineales", "Sistemas_de_desigualdades", "Programacion_lineal"],
        "SECCIONES_CONICAS": ["Parabolas", "Elipses", "Hiperbolas", "Conicas_desplazadas", "Rotacion_de_ejes", "Ecuaciones_polares_de_conicas"]
    }

    # Crear una función para generar datos ficticios usando la biblioteca Faker.
    def generar_datos_ficticios(tema, subtema):
        fake = faker.Faker()
        return [
            "Matematicas",
            tema,
            subtema,
            fake.sentence(),
            fake.random_int(min=1, max=10),
            fake.random_int(min=1, max=5),
            fake.random_int(min=1, max=3),
            fake.random_int(min=1, max=5),
            fake.random_int(min=1, max=10),
            fake.random_int(min=1, max=5),
        ]

    # Crear y escribir en el archivo CSV.
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        # Escribir los encabezados en el archivo.
        escritor_csv.writerow(columnas)

        # Generar datos ficticios para cada tema y subtema.
        for tema, subtemas in subtemas_por_tema.items():
            filas_por_subtema = filas_por_tema // len(subtemas)

            for subtema in subtemas:
                for _ in range(filas_por_subtema):
                    datos = generar_datos_ficticios(tema, subtema)
                    escritor_csv.writerow(datos)

    print(f"Se ha creado el archivo '{nombre_archivo}' con '{filas_por_tema}' filas por tema, distribuidas homogéneamente entre los subtemas.")

# Leer el archivo CSV original
nombre_archivo = "datos.csv"
df = pd.read_csv(nombre_archivo)

# Concatenar las columnas relevantes en 'text'
cols = ["Area", "Tema", "Subtema", "Descripcion", "Preguntas", "Respuestas", "Teoremas", "Formulas", "Aplicaciones", "Ejercicios", "Material_Audiovisual"]
df['text'] = df[cols].astype(str).agg(''.join, axis=1)

# Crear un modelo de SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Calcular embeddings
embeddings = model.encode(df['text'], batch_size=64, show_progress_bar=True)

# Agregar las columnas 'embeddings' y 'ids' al DataFrame
df['embeddings'] = embeddings.tolist()
df['ids'] = df.index
df['ids'] = df['ids'].astype('str')

# Guardar el DataFrame actualizado en un nuevo archivo CSV
nombre_archivo_embeddings = "datos_embeddings.csv"

# Forzar que 'ids' se guarde como cadena (str) en el archivo CSV
df.to_csv(nombre_archivo_embeddings, index=False, quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')