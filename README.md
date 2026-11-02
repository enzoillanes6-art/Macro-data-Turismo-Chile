# Proyecto 14: Evolución del Turismo Nacional e Internacional

- **Institución:** Universidad Autónoma de Chile · **Asignatura:** Programación Avanzada
- **Docente:** Alex Flores Fuentealba
- **Integrantes:** Benjamín Aguayo, Enzo Illanes, Jaime Panguinao
- **Repositorio:** https://github.com/BenjaAgx/proyecto-analisis-datos
- **Avance actual:** Avance 2 – Limpieza y transformación de datos

## Descripción
Análisis de la matriz de movilidad turística comunal (SERNATUR / INE) para identificar tendencias
y estacionalidad del flujo de visitantes. Este avance deja el dataset listo para el análisis
mediante un pipeline reproducible en Python + Pandas.

## Pipeline
```
datos/originales/dataset.csv  (solo lectura)
   ↓ carga.py            Lectura (sep ';', latin-1, decimal ',')
   ↓ validaciones.py     Diagnóstico inicial (nulos, duplicados, fuera de rango)
   ↓ limpieza.py         Nombres de columnas, espacios, categorías, rangos, duplicados
   ↓ limpieza.py         Tratamiento de nulos (estrategia por variable)
   ↓ transformaciones.py Tipos, fecha, total_anual, mes_pico, pct_verano, es_intrarregional, nivel_flujo
   ↓ validaciones.py     Validación de columnas, tipos y rangos
   ↓ carga.py            datos/procesados/dataset_limpio.csv
```

## Estructura
```
├── datos/
│   ├── originales/            # dataset.csv original (no se versiona ni se modifica)
│   ├── procesados/            # dataset_limpio.csv (+ muestra de 1000 filas)
│   ├── README.md
│   └── instrucciones_descarga.txt
├── reportes/                  # avance_1.pdf, avance_2.pdf y resumen_ejecucion.md (autogenerado)
├── src/
│   ├── __init__.py
│   ├── carga.py               # lectura y escritura de archivos
│   ├── limpieza.py            # normalización, duplicados, rangos y nulos
│   ├── transformaciones.py    # conversión de tipos y variables nuevas
│   ├── validaciones.py        # diagnóstico y validación de columnas, tipos y rangos
│   └── reporte.py             # bitácora de cambios y resumen en Markdown
├── main.py
└── requirements.txt
```

## Instrucciones de ejecución
1. Clonar: `git clone https://github.com/BenjaAgx/proyecto-analisis-datos.git && cd proyecto-analisis-datos`
2. Descargar `dataset.csv` (164 MB) desde el enlace de `datos/instrucciones_descarga.txt` y guardarlo en `datos/originales/dataset.csv`.
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar desde la raíz: `python main.py`

Salidas: `datos/procesados/dataset_limpio.csv` y `reportes/resumen_ejecucion.md`
(tablas de diagnóstico, nulos, transformaciones y comparación antes/después para el informe).

## Decisiones de limpieza (resumen)
| Tema | Decisión |
| --- | --- |
| Duplicados exactos | Se elimina la repetición y se conserva la primera |
| Identificadores repetidos (origen-destino-año) | Se informan, no se modifican |
| Flujos negativos / códigos de región fuera de 1-16 | Pasan a nulo y se tratan como nulos |
| Año fuera de 2018-2025 o nulo | Se elimina la fila |
| Códigos y nombres territoriales nulos | Se recuperan desde su par código↔nombre; si no, `desconocido` o se elimina |
| Meses nulos | Fila sin ningún mes: se elimina. Resto: 0 + columna `n_meses_imputados` |
| Otras columnas con nulos | Mediana (numéricas) o `desconocido` (texto) |

Toda eliminación y corrección queda registrada en `reportes/resumen_ejecucion.md`.
