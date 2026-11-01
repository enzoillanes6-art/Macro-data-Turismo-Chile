"""Pipeline: carga -> diagnóstico -> limpieza -> nulos -> transformaciones -> validación -> exportación.

Ejecutar desde la raíz del proyecto:  python main.py
"""
from pathlib import Path

from src import carga, limpieza, transformaciones as tr, validaciones as val, reporte

RAIZ = Path(__file__).resolve().parent
SALIDA = RAIZ / "datos" / "procesados" / "dataset_limpio.csv"
RESUMEN = RAIZ / "reportes" / "resumen_ejecucion.md"


def main():
    registro = reporte.nuevo_registro()

    print("1. CARGA")
    ruta = carga.localizar_original(RAIZ)
    if ruta is None:
        print("No se encontró el dataset. Colócalo en datos/originales/dataset.csv "
              "(ver datos/instrucciones_descarga.txt).")
        return 1
    df = carga.cargar_datos(ruta)
    if df is None:
        return 1
    print(f"Archivo: {ruta.relative_to(RAIZ)} (solo lectura)")

    print("\n2. DIAGNÓSTICO INICIAL")
    antes = val.diagnosticar(df)
    val.imprimir_diagnostico(antes, "Dataset original")

    print("\n3. LIMPIEZA")
    df = limpieza.normalizar_nombres_columnas(df, registro)
    df = limpieza.limpiar_espacios(df, registro)
    df = limpieza.unificar_categorias(df, registro)
    df = limpieza.corregir_fuera_de_rango(df, registro)
    df = limpieza.eliminar_duplicados(df, registro)
    limpieza.revisar_ids_repetidos(df, registro)

    print("4. TRATAMIENTO DE NULOS")
    df = limpieza.tratar_nulos(df, registro)

    print("5. TRANSFORMACIONES")
    df = tr.convertir_tipos(df, registro)
    df = tr.crear_fecha(df, registro)
    df = tr.crear_total_anual(df, registro)
    df = tr.crear_mes_pico(df, registro)
    df = tr.crear_porcentaje_verano(df, registro)
    df = tr.crear_intrarregional(df, registro)
    df = tr.clasificar_nivel_flujo(df, registro)

    print("6. VALIDACIÓN")
    resultados = val.validar(df)
    for nombre, ok, detalle in resultados:
        print(f"  [{'OK' if ok else 'FALLA'}] {nombre}: {detalle}")
    despues = val.diagnosticar(df)
    val.imprimir_diagnostico(despues, "Dataset procesado")

    print("\n7. EXPORTACIÓN")
    ruta_csv, ruta_muestra = carga.guardar_datos(df, SALIDA)
    reporte.guardar_resumen(
        reporte.construir_resumen(antes, despues, registro, df, resultados), RESUMEN)
    print(f"  {ruta_csv.relative_to(RAIZ)}  ({ruta_csv.stat().st_size / 1e6:.1f} MB)")
    print(f"  {ruta_muestra.relative_to(RAIZ)}")
    print(f"  {RESUMEN.relative_to(RAIZ)}  (tablas listas para el informe)")
    return 0 if all(ok for _, ok, _ in resultados) else 2


if __name__ == "__main__":
    raise SystemExit(main())
