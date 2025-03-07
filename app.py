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
def create_bar_chart(df, x_column, y_column, title, x_label, y_label, color, orient='v'):
    fig, ax = plt.subplots()
    if orient == 'v':
        ax.bar(df[x_column], df[y_column], color=color)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_xticklabels(df[x_column], rotation=45, ha='right')
    else:
        ax.barh(df[x_column], df[y_column], color=color)
        ax.set_ylabel(x_label)
        ax.set_xlabel(y_label)
        ax.invert_yaxis()
    ax.set_title(title)
    plt.subplots_adjust(bottom=0.25)

    canvas = FigureCanvasTkAgg(fig, master=frame_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def moto_mas_vendida():
    query = """
    SELECT m.brand || ' ' || m.model AS moto, COUNT(s.motorcycle_id) AS total_vendidos
    FROM sales s
    JOIN motorcycles m ON s.motorcycle_id = m.id
    GROUP BY m.brand, m.model
    ORDER BY total_vendidos DESC;
    """
    df = query_to_dataframe(query)
    create_bar_chart(df, 'moto', 'total_vendidos', 'Moto más vendida en el año', 'Moto', 'Cantidad Vendida', 'blue')

def mes_mas_vendido():
    query = """
    SELECT TO_CHAR(sale_date, 'Month') AS mes, COUNT(*) AS total_ventas
    FROM sales
    GROUP BY mes
    ORDER BY total_ventas DESC
    """
    df = query_to_dataframe(query)
    create_bar_chart(df, 'mes', 'total_ventas', 'Mes con más ventas', 'Mes', 'Ventas', 'green')

def dia_mas_vendido():
    query = """
    SELECT TO_CHAR(sale_date, 'YYYY-MM-DD') AS sale_date, COUNT(*) AS total_ventas
    FROM sales
    GROUP BY sale_date
    ORDER BY total_ventas DESC
    LIMIT 10
    """
    df = query_to_dataframe(query)
    create_bar_chart(df, 'sale_date', 'total_ventas', 'Días con más ventas', 'Fecha', 'Ventas', 'red')

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
    create_bar_chart(df, 'name', 'total_compras', 'Cliente que más compró', 'Cliente', 'Total Compras', 'purple', orient='h')

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
frame_menu = tk.Frame(root, width=250, bg="#223843")
frame_menu.pack(side=tk.LEFT, fill=tk.Y)

# Crear un Frame para las gráficas
frame_graficas = tk.Frame(root, width=750)
frame_graficas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Título
label = tk.Label(frame_menu, text="Gestion de Datos - MotoPower", font=("Helvetica", 13), bg="#223843" , fg="white")
label.pack(pady=10)

# Estilo personalizado para los botones
style = ttk.Style()
style.configure('Custom.TButton', font=('Helvetica', 10), padding=10, width=20)

# Botones personalizados
buttons = [
    ("Moto más vendida", moto_mas_vendida, '#d8b4a0'),
    ("Mes con más ventas", mes_mas_vendido, '#d8b4a0'),
    ("Día con más ventas", dia_mas_vendido, '#d8b4a0'),
    ("Cliente que más compró", cliente_que_mas_compro, '#d8b4a0'),
    ("Salir", on_closing, '#d8b4a0')
]

for text, command, color in buttons:
    
    btn = tk.Button(frame_menu, text=text, command=lambda c=command: [clear_graph(), c()], bg=color, fg='#223843', font=('Helvetica', 12, 'bold'), width=20, height=2)
    btn.pack(pady=5)

# Vincular la función de cierre a la ventana
root.protocol("WM_DELETE_WINDOW", on_closing)

# Ejecutar ventana
root.mainloop()