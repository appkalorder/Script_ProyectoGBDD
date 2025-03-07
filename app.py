import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine

# Función para conectar a la base de datos
def connect_db():
    return create_engine('postgresql+psycopg2://postgres:sa@localhost/motopower_db')

# Consulta SQL a DataFrame
def query_to_dataframe(query):
    engine = connect_db()
    df = pd.read_sql_query(query, engine)
    return df

# Funciones para las gráficas
def moto_mas_vendida():
    query = """
    SELECT m.brand || ' ' || m.model AS moto, COUNT(s.motorcycle_id) AS total_vendidos
    FROM sales s
    JOIN motorcycles m ON s.motorcycle_id = m.id
    GROUP BY m.brand, m.model
    ORDER BY total_vendidos DESC;
    """
    df = query_to_dataframe(query)
    fig, ax = plt.subplots()
    ax.bar(df['moto'], df['total_vendidos'], color='blue')
    ax.set_xlabel('Moto')
    ax.set_ylabel('Cantidad Vendida')
    ax.set_title('Moto más vendida en el año')
    ax.set_xticks(range(len(df['moto'])))
    ax.set_xticklabels(df['moto'], rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.39)

    canvas = FigureCanvasTkAgg(fig, master=frame_graficas)  # Llama al Frame de gráficas
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def mes_mas_vendido():
    query = """
    SELECT TO_CHAR(sale_date, 'Month') AS mes, COUNT(*) AS total_ventas
    FROM sales
    GROUP BY mes
    ORDER BY total_ventas DESC
    """
    df = query_to_dataframe(query)
    fig, ax = plt.subplots()
    ax.bar(df['mes'], df['total_ventas'], color='green')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Ventas')
    ax.set_title('Mes con más ventas')
    ax.set_xticks(range(len(df['mes'])))
    ax.set_xticklabels(df['mes'], rotation=45)
    plt.subplots_adjust(bottom=0.25)

    canvas = FigureCanvasTkAgg(fig, master=frame_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def dia_mas_vendido():
    query = """
    SELECT TO_CHAR(sale_date, 'YYYY-MM-DD') AS sale_date, COUNT(*) AS total_ventas
    FROM sales
    GROUP BY sale_date
    ORDER BY total_ventas DESC
    LIMIT 10
    """
    df = query_to_dataframe(query)
    fig, ax = plt.subplots()
    ax.bar(df['sale_date'], df['total_ventas'], color='red')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Ventas')
    ax.set_title('Días con más ventas')
    ax.set_xticks(range(len(df['sale_date'])))
    ax.set_xticklabels(df['sale_date'], rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.25)

    canvas = FigureCanvasTkAgg(fig, master=frame_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def cliente_que_mas_compro():
    query = """
    SELECT c.first_name AS name, COUNT(s.customer_id) AS total_compras
    FROM sales s
    JOIN customers c ON s.customer_id = c.id
    GROUP BY c.first_name
    ORDER BY total_compras DESC
    LIMIT 10
    """
    df = query_to_dataframe(query)
    fig, ax = plt.subplots()
    ax.barh(df['name'], df['total_compras'], color='purple')
    ax.set_xlabel('Total Compras')
    ax.set_ylabel('Cliente')
    ax.set_title('Cliente que más compró')
    ax.invert_yaxis()

    canvas = FigureCanvasTkAgg(fig, master=frame_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Función para limpiar el Frame de gráficas
def clear_graph():
    for widget in frame_graficas.winfo_children():
        widget.destroy()

# Función para cerrar la aplicación
def on_closing():
    root.destroy()
    plt.close('all')

# Configuración de la ventana
root = tk.Tk()
root.title("Gestión de Ventas - MotoPower")
root.geometry("1000x600")

# Crear un Frame para el menú
frame_menu = tk.Frame(root, width=250, bg="lightgray")
frame_menu.pack(side=tk.LEFT, fill=tk.Y)

# Crear un Frame para las gráficas
frame_graficas = tk.Frame(root, width=750)
frame_graficas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Título
label = tk.Label(frame_menu, text="Seleccione una consulta", font=("Arial", 14), bg="lightgray")
label.pack(pady=10)

# Botones
btn1 = ttk.Button(frame_menu, text="Moto más vendida", command=lambda: [clear_graph(), moto_mas_vendida()])
btn1.pack(pady=5)

btn2 = ttk.Button(frame_menu, text="Mes con más ventas", command=lambda: [clear_graph(), mes_mas_vendido()])
btn2.pack(pady=5)

btn3 = ttk.Button(frame_menu, text="Día con más ventas", command=lambda: [clear_graph(), dia_mas_vendido()])
btn3.pack(pady=5)

btn4 = ttk.Button(frame_menu, text="Cliente que más compró", command=lambda: [clear_graph(), cliente_que_mas_compro()])
btn4.pack(pady=5)

btn_exit = ttk.Button(frame_menu, text="Salir", command=on_closing)
btn_exit.pack(pady=20)

# Vincular la función de cierre a la ventana
root.protocol("WM_DELETE_WINDOW", on_closing)

# Ejecutar ventana
root.mainloop()
