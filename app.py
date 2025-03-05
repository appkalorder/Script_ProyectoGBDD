import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def connect_db():
    return psycopg2.connect(
        dbname="motopower_db",
        user="postgres",
        password="sa",
        host="localhost"
    )

def query_to_dataframe(query):
    conn = connect_db()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def moto_mas_vendida(): #check
    query = """
    SELECT m.brand || ' ' || m.model AS moto, COUNT(s.motorcycle_id) AS total_vendidos
    FROM sales s
    JOIN motorcycles m ON s.motorcycle_id = m.id
    GROUP BY m.brand, m.model
    ORDER BY total_vendidos DESC;
    """
    df = query_to_dataframe(query)
    print(df)  # Para depurar y ver qué datos devuelve
    plt.bar(df['moto'], df['total_vendidos'], color='blue')
    plt.xlabel('Moto')
    plt.ylabel('Cantidad Vendida')
    plt.title('Moto más vendida en el año')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def mes_mas_vendido(): #check
    query = """
    SELECT TO_CHAR(sale_date, 'Month') AS mes, COUNT(*) AS total_ventas
    FROM sales
    GROUP BY mes
    ORDER BY total_ventas DESC
    """
    df = query_to_dataframe(query)
    plt.bar(df['mes'], df['total_ventas'], color='green')
    plt.xlabel('Mes')
    plt.ylabel('Ventas')
    plt.title('Mes con más ventas')
    plt.xticks(rotation=45)
    plt.show()

def dia_mas_vendido(): #check
    query = """
    SELECT TO_CHAR(sale_date, 'YYYY-MM-DD') AS sale_date, COUNT(*) AS total_ventas
    FROM sales
    GROUP BY sale_date
    ORDER BY total_ventas DESC
    LIMIT 10
    """
    df = query_to_dataframe(query)
    plt.figure(figsize=(10, 5))
    plt.bar(df['sale_date'], df['total_ventas'], color='red')
    plt.xlabel('Fecha')
    plt.ylabel('Ventas')
    plt.title('Días con más ventas')
    plt.xticks(rotation=45, ha='right')
    
    plt.show()

def cliente_que_mas_compro(): #check
    query = """
    SELECT c.first_name AS name, COUNT(s.customer_id) AS total_compras
    FROM sales s
    JOIN customers c ON s.customer_id = c.id
    GROUP BY c.first_name
    ORDER BY total_compras DESC
    LIMIT 10
    """
    df = query_to_dataframe(query)
    plt.barh(df['name'], df['total_compras'], color='purple')
    plt.xlabel('Total Compras')
    plt.ylabel('Cliente')
    plt.title('Cliente que más compró')
    plt.gca().invert_yaxis()
    plt.show()

def menu():
    while True:
        print("\nSeleccione una consulta:")
        print("1. Moto más vendida")
        print("2. Mes con más ventas")
        print("3. Día con más ventas")
        print("4. Cliente que más compró")
        print("5. Salir")
        opcion = input("Ingrese una opción: ")
        
        if opcion == '1':
            moto_mas_vendida()
        elif opcion == '2':
            mes_mas_vendido()
        elif opcion == '3':
            dia_mas_vendido()
        elif opcion == '4':
            cliente_que_mas_compro()
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu()
