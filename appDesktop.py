import requests
import json
import socket
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# URL de la API MockAPI
api_url = "https://66ecd6b22b6cf2b89c5f711e.mockapi.io/IoTCarStatus"


# Función para obtener la IP local de la computadora
def obtener_ip_local():
    try:
        hostname = socket.gethostname()
        ip_local = socket.gethostbyname(hostname)
        return ip_local
    except Exception as e:
        return "No se pudo obtener la IP"


# Función para enviar datos a MockAPI
def guardar_en_mockapi(status, name):
    ip_client = obtener_ip_local()
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    datos = {
        "status": status,
        "date": date,
        "ipClient": ip_client,
        "name": name
    }

    response = requests.post(api_url, data=json.dumps(datos), headers={"Content-Type": "application/json"})

    if response.status_code == 201:
        resumen = f"""
        Datos guardados exitosamente:
        Status: {status}
        Nombre: {name}
        IP Cliente: {ip_client}
        Fecha: {date}
        """
        messagebox.showinfo("Éxito", resumen.strip())  # Mostrar el resumen con saltos de línea
        mostrar_ultimo_registro()  # Actualizar el último registro
    else:
        messagebox.showerror("Error", f"Error al guardar los datos: {response.status_code}")


# Función para mostrar el último registro
def mostrar_ultimo_registro():
    response = requests.get(api_url)
    if response.status_code == 200:
        registros = response.json()
        if registros:
            ultimo_registro = registros[-1]
            datos_ultimo_registro.set(f"Último Registro:\nStatus: {ultimo_registro['status']}\n"
                                      f"Nombre: {ultimo_registro['name']}\n"
                                      f"IP Cliente: {ultimo_registro['ipClient']}\n"
                                      f"Fecha: {ultimo_registro['date']}")
        else:
            datos_ultimo_registro.set("No hay registros disponibles.")
    else:
        datos_ultimo_registro.set("Error al obtener registros.")


# Función que maneja el botón de enviar
def enviar_datos(status):
    name = name_entry.get()

    if name.strip() == "":
        messagebox.showwarning("Advertencia", "El campo 'nombre' no puede estar vacío.")
    else:
        guardar_en_mockapi(status, name)


# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación IoT Car Status")

# Crear la interfaz
frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

# Etiqueta y campo de texto para el nombre
name_label = tk.Label(frame, text="Ingrese el nombre:")
name_label.pack(padx=5, pady=5)

name_entry = tk.Entry(frame)
name_entry.pack(padx=5, pady=5)

# Botones de flechas
flechas_frame = tk.Frame(root)
flechas_frame.pack(pady=20)

btn_up = tk.Button(flechas_frame, text="⬆", font=("Arial", 20), command=lambda: enviar_datos("Arriba"))
btn_up.grid(row=0, column=1, padx=10, pady=10)

btn_down = tk.Button(flechas_frame, text="⬇", font=("Arial", 20), command=lambda: enviar_datos("Abajo"))
btn_down.grid(row=2, column=1, padx=10, pady=10)

btn_left = tk.Button(flechas_frame, text="⬅", font=("Arial", 20), command=lambda: enviar_datos("Izquierda"))
btn_left.grid(row=1, column=0, padx=10, pady=10)

btn_right = tk.Button(flechas_frame, text="➡", font=("Arial", 20), command=lambda: enviar_datos("Derecha"))
btn_right.grid(row=1, column=2, padx=10, pady=10)

# Etiqueta para mostrar el último registro
datos_ultimo_registro = tk.StringVar()
ultimo_registro_label = tk.Label(root, textvariable=datos_ultimo_registro, wraplength=400)
ultimo_registro_label.pack(pady=20)

# Iniciar el loop de la ventana
root.mainloop()
