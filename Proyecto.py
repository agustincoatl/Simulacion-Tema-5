import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from collections import Counter


# SIMULAR HISTORIAL
# -------------------------------
def simular_historial(valores, n=20):
    media = np.mean(valores)
    std = np.std(valores)
    return np.random.normal(media, std, n)


# CARGAR EXCEL
# -------------------------------
def cargar_excel():
    archivo = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if archivo:
        return pd.read_excel(archivo)
    return None


# SIMULACIÓN
# -------------------------------
def simular_partido(e1, e2, n_sim=30000):
    pos1 = simular_historial(e1['posesion']).mean()
    tir1 = simular_historial(e1['tiros']).mean()
    efe1 = simular_historial(e1['efectividad']).mean()

    pos2 = simular_historial(e2['posesion']).mean()
    tir2 = simular_historial(e2['tiros']).mean()
    efe2 = simular_historial(e2['efectividad']).mean()

    tiros1 = tir1 * (pos1 / 100)
    tiros2 = tir2 * (pos2 / 100)

    xg1 = tiros1 * (efe1 / 100)
    xg2 = tiros2 * (efe2 / 100)

    goles1 = np.random.poisson(xg1, n_sim)
    goles2 = np.random.poisson(xg2, n_sim)

    p1 = np.sum(goles1 > goles2) / n_sim * 100
    pe = np.sum(goles1 == goles2) / n_sim * 100
    p2 = np.sum(goles1 < goles2) / n_sim * 100

    resultados = list(zip(goles1, goles2))
    marcador, _ = Counter(resultados).most_common(1)[0]

    media_goles1 = np.mean(goles1)
    media_goles2 = np.mean(goles2)

    return p1, pe, p2, marcador, media_goles1, media_goles2


# GENERAR GRÁFICAS
# -------------------------------
def generar_graficas(p1, pe, p2):
    etiquetas = ['Local', 'Empate', 'Visitante']
    valores = [p1, pe, p2]
    plt.plot(10, 100)
    plt.bar(etiquetas, valores)
    plt.title("Probabilidades del Partido")
    plt.ylabel("Porcentaje (%)")
    plt.savefig("grafica_resultados.png")
    plt.close()


# EXPORTAR A EXCEL
# -------------------------------
def exportar_excel(equipo1, equipo2, p1, pe, p2, marcador, g1, g2):
    datos = {
        "Métrica": [
            "Equipo Local",
            "Equipo Visitante",
            "Probabilidad victoria Local (%)",
            "Probabilidad de Empate (%)",
            "Probabilidad victoria Visitante (%)",
            "Media de goles Local",
            "Media de goles Visitante",
            "Marcador más probable"
        ],
        "Valor": [
            equipo1,
            equipo2,
            round(p1,2),
            round(pe,2),
            round(p2,2),
            round(g1,2),
            round(g2,2),
            f"{marcador[0]} - {marcador[1]}"
        ]
    }

    df = pd.DataFrame(datos)
    df.to_excel("Resultados_Simulacion.xlsx", index=False)


# INTERFAZ
# -------------------------------
def simular():
    global df1, df2

    if df1 is None or df2 is None:
        resultado.config(text="❌ Carga ambos archivos de Excel")
        return

    p1, pe, p2, marcador, g1, g2 = simular_partido(df1, df2)

    generar_graficas(p1, pe, p2)

    exportar_excel(
        df1['equipo'][0],
        df2['equipo'][0],
        p1, pe, p2, marcador, g1, g2
    )

    resultado.config(text=f"""
✅ Resultados del Partido

{df1['equipo'][0]} vs {df2['equipo'][0]}

🏠 Local: {p1:.2f}%
🤝 Empate: {pe:.2f}%
🚩 Visitante: {p2:.2f}%

⚽ Marcador más probable:
{marcador[0]} - {marcador[1]}

📁 Se generó: Resultados_Simulacion.xlsx
📊 Se generó: grafica_resultados.png
""")


# VENTANA
# -------------------------------
ventana = tk.Tk()
ventana.title("Simulador de Fútbol - Excel + Gráficas")
ventana.geometry("600x520")

df1 = None
df2 = None

def load1():
    global df1
    df1 = cargar_excel()

def load2():
    global df2
    df2 = cargar_excel()

tk.Label(ventana, text="SIMULADOR DE PARTIDOS DE FÚTBOL", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(ventana, text="📂 Cargar Excel Equipo Local", command=load1).pack(pady=5)
tk.Button(ventana, text="📂 Cargar Excel Equipo Visitante", command=load2).pack(pady=5)

tk.Button(ventana, text="⚽ Simular Partido", command=simular, bg="green", fg="white").pack(pady=15)

resultado = tk.Label(ventana, text="", font=("Consolas", 11), justify="left")
resultado.pack(pady=10)

ventana.mainloop()
