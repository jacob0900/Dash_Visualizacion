"""
train_model.py
Prueba de estacionariedad de la serie TasaColocacionTotal
Pruebas: ADF (Augmented Dickey-Fuller) y KPSS
Ejecutar directamente: python model/train_model.py
"""

import os, sys
import json
import pickle
import pandas as pd
import numpy as np

# Permitir importación desde raíz del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from statsmodels.tsa.stattools import adfuller, kpss
from data.generate_data import load_data

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def run_adf_test(series: pd.Series) -> dict:
    """Ejecuta el test ADF y retorna resultados como dict."""
    result = adfuller(series.dropna(), autolag="AIC")
    adf_stat, p_value, n_lags, n_obs, crit_vals, icbest = result
    return {
        "test":        "ADF (Augmented Dickey-Fuller)",
        "estadistico": round(float(adf_stat), 4),
        "p_value":     round(float(p_value), 4),
        "lags_usados": int(n_lags),
        "n_obs":       int(n_obs),
        "valores_criticos": {k: round(float(v), 4) for k, v in crit_vals.items()},
        "es_estacionaria": p_value < 0.05,
        "hipotesis_nula": "La serie tiene raíz unitaria (no estacionaria)",
        "conclusion": (
            "✅ Se rechaza H₀ → la serie ES estacionaria (p < 0.05)"
            if p_value < 0.05
            else "⚠️ No se rechaza H₀ → la serie NO ES estacionaria (p ≥ 0.05)"
        ),
    }


def run_kpss_test(series: pd.Series) -> dict:
    """Ejecuta el test KPSS y retorna resultados como dict."""
    result = kpss(series.dropna(), regression="c", nlags="auto")
    kpss_stat, p_value, n_lags, crit_vals = result
    return {
        "test":        "KPSS (Kwiatkowski-Phillips-Schmidt-Shin)",
        "estadistico": round(float(kpss_stat), 4),
        "p_value":     round(float(p_value), 4),
        "lags_usados": int(n_lags),
        "valores_criticos": {k: round(float(v), 4) for k, v in crit_vals.items()},
        "es_estacionaria": p_value >= 0.05,
        "hipotesis_nula": "La serie es estacionaria",
        "conclusion": (
            "✅ No se rechaza H₀ → la serie ES estacionaria (p ≥ 0.05)"
            if p_value >= 0.05
            else "⚠️ Se rechaza H₀ → la serie NO ES estacionaria (p < 0.05)"
        ),
    }


def run_stationarity_analysis(df: pd.DataFrame) -> dict:
    """
    Ejecuta ADF y KPSS sobre TasaColocacionTotal y su primera diferencia.
    Retorna un dict serializable con todos los resultados.
    """
    serie = df.set_index("Fecha")["TasaColocacionTotal"]
    serie_diff = serie.diff().dropna()

    results = {
        "variable":       "TasaColocacionTotal",
        "n_observaciones": int(len(serie)),
        "fecha_inicio":   str(serie.index.min().date()),
        "fecha_fin":      str(serie.index.max().date()),
        "serie_original": {
            "adf":  run_adf_test(serie),
            "kpss": run_kpss_test(serie),
        },
        "primera_diferencia": {
            "adf":  run_adf_test(serie_diff),
            "kpss": run_kpss_test(serie_diff),
        },
        "interpretacion_conjunta": _interpret(
            run_adf_test(serie),
            run_kpss_test(serie),
        ),
    }
    return results


def _interpret(adf: dict, kpss: dict) -> str:
    """Interpretación conjunta ADF + KPSS."""
    adf_ok  = adf["es_estacionaria"]
    kpss_ok = kpss["es_estacionaria"]
    if adf_ok and kpss_ok:
        return "Ambas pruebas concuerdan: la serie ES estacionaria. No se requiere diferenciación."
    elif not adf_ok and not kpss_ok:
        return "Ambas pruebas concuerdan: la serie NO ES estacionaria. Se recomienda diferenciación (d=1)."
    elif adf_ok and not kpss_ok:
        return "Resultado mixto: En conclusión, aunque el ADF sugiere que tu serie original podría ser estacionaria, el KPSS detecta una tendencia y marca que no lo es; ambos coinciden en que la primera diferencia sí es estacionaria, por lo que la decisión más robusta es trabajar con la serie diferenciada y ajustar un modelo ARIMA(p,1,q) sobre ella, garantizando que cumpla la condición de estacionariedad y evitando problemas futuros en el modelado.."
    else:
        return "Resultado mixto: KPSS indica estacionariedad, pero ADF sugiere raíz unitaria. Revisar con mayor número de lags."


def train_and_save():
    """Punto de entrada principal: entrena y serializa los resultados."""
    print("📊 Cargando datos...")
    df = load_data()

    print("🔬 Ejecutando pruebas de estacionariedad...")
    results = run_stationarity_analysis(df)

    print("\n=== RESULTADOS ADF (Serie original) ===")
    adf = results["serie_original"]["adf"]
    print(f"  Estadístico : {adf['estadistico']}")
    print(f"  p-valor     : {adf['p_value']}")
    print(f"  Conclusión  : {adf['conclusion']}")

    print("\n=== RESULTADOS KPSS (Serie original) ===")
    kp = results["serie_original"]["kpss"]
    print(f"  Estadístico : {kp['estadistico']}")
    print(f"  p-valor     : {kp['p_value']}")
    print(f"  Conclusión  : {kp['conclusion']}")

    print(f"\n📌 Interpretación conjunta: {results['interpretacion_conjunta']}")

    # Guardar resultados en pickle
    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump(results, f)
    print(f"\n✅ Resultados guardados en {OUTPUT_PATH}")
    return results


def load_model_results() -> dict:
    """Carga los resultados desde el pickle; si no existe, los genera."""
    if not os.path.exists(OUTPUT_PATH):
        return train_and_save()
    with open(OUTPUT_PATH, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    train_and_save()
