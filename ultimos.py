import requests
import json
import tkinter as tk
from tkinter import ttk

# URL de la API MockAPI
api_url = "https://66ecd6b22b6cf2b89c5f711e.mockapi.io/IoTCarStatus"

def obtener_ultimos_registros(cantidad=10):
    """Obtiene los últimos 'cantidad' registros de la API MockAPI.

    Args:
        cantidad (int, opcional): Número de registros a obtener. Por defecto, 10.

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un registro.
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        registros = response.json()
        return registros[-cantidad:]
    else:
        return []

def crear_interfaz():
    """Crea la interfaz gráfica de usuario."""
    ventana = tk.Tk()
    ventana.title("Últimos 10 Registros")

    # Tabla para mostrar los datos
    tabla = ttk.Treeview(ventana, columns=("status", "date", "ipClient", "name"))
    tabla.heading("status", text="Status")
    tabla.heading("date", text="Fecha")
    tabla.heading("ipClient", text="IP Cliente")
    tabla.heading("name", text="Nombre")
    tabla.pack(pady=20, padx=20)

    return ventana, tabla

def actualizar_tabla(tabla, registros):
    """Actualiza la tabla con los nuevos registros.

    Args:
        tabla: El objeto Treeview de la tabla.
        registros: Una lista de diccionarios con los registros.
    """
    for i in tabla.get_children():
        tabla.delete(i)

    for registro in registros:
        tabla.insert("", "end", values=(
            registro['status'],
            registro['date'],
            registro['ipClient'],
            registro['name']
        ))

if __name__ == "__main__":
    ventana, tabla = crear_interfaz()

    def actualizar_datos():
        registros = obtener_ultimos_registros()
        actualizar_tabla(tabla, registros)

    # Actualizar los datos al iniciar la aplicación y cada cierto tiempo (ajusta el intervalo según tus necesidades)
    actualizar_datos()
    ventana.after(5000, actualizar_datos)  # Actualizar cada 5 segundos

    ventana.mainloop()