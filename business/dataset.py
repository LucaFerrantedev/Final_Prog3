import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import io
import base64

def procesar_dataset(file_storage):
    # Cargar datos
    df = pd.read_csv(file_storage)
    df.columns = df.columns.str.strip()
    
    # Validar columnas
    X_col = 'Income composition of resources'
    Y_col = 'Life expectancy'
    
    if X_col not in df.columns or Y_col not in df.columns:
        raise ValueError(f"El CSV debe contener las columnas: '{X_col}' y '{Y_col}'")

    # Limpieza y lógica
    df_clean = df[[X_col, Y_col]].dropna()
    mask = df_clean[X_col] > 0.2
    X = np.array(df_clean[mask][X_col]).reshape(-1, 1)
    Y = np.array(df_clean[mask][Y_col]).reshape(-1, 1)
    
    if len(X) == 0:
        raise ValueError("No hay datos suficientes después del filtrado (>0.2).")

    Y_log = np.log(Y)

    # Entrenar modelo
    model = LinearRegression(fit_intercept=True)
    model.fit(X, Y_log)
    r_squared = model.score(X, Y_log)

    # Predicción para la línea de tendencia
    X_new = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    Y_new = np.exp(model.predict(X_new))

    # Generar Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(X, Y, label='Datos Reales')
    ax.plot(X_new, Y_new, color='red', label=r'Regresión Exponencial')
    
    ax.set_xlabel('Índice Composición de ingresos de los recursos')
    ax.set_ylabel('Expectativa de vida (Años)')
    ax.legend()
    ax.grid(True)
    
    # Guardar gráfico en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)

    return plot_url, r_squared