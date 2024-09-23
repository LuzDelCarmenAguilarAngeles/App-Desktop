import requests
import json
import socket
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# URL de la API local
api_local_url = "http://127.0.0.1:5000/procesar"
api_local_get_url = "http://127.0.0.1:5000/cars"

# Función para obtener la IP local de la computadora
def obtener_ip_local():
    try:
        hostname = socket.gethostname()
        ip_local = socket.gethostbyname(hostname)
        return ip_local
    except Exception as e:
        return "No se pudo obtener la IP"

# Función para enviar datos a la API RESTful local
def enviar_a_restful(status, name):
    ip_client = obtener_ip_local()
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    datos = {
        "status": status,
        "date": date,
        "ipClient": ip_client,
        "name": name
    }

    # Asegurarse de que se esté enviando una solicitud POST
    response = requests.post(api_local_url, data=json.dumps(datos), headers={"Content-Type": "application/json"})

    if response.status_code == 201:
        messagebox.showinfo("Éxito", "Datos enviados y procesados correctamente.")
        mostrar_ultimos_registros()  # Actualizar la visualización con los últimos registros
    else:
        messagebox.showerror("Error", f"Error al procesar los datos: {response.status_code}")

# Función para mostrar los últimos 10 registros en formato tabla
def mostrar_ultimos_registros():
    response = requests.get(api_local_get_url)
    if response.status_code == 200:
        registros = response.json()
        if registros:
            # Limpiar la tabla antes de actualizarla
            for item in tree.get_children():
                tree.delete(item)

            # Insertar los registros en la tabla
            for i, registro in enumerate(registros):
                tree.insert('', 'end', text=str(i+1), values=(registro['status'], registro['name'], registro['ipClient'], registro['date']))
        else:
            messagebox.showinfo("Info", "No hay registros disponibles.")
    else:
        messagebox.showerror("Error", "Error al obtener registros.")

# Función que maneja el botón de enviar
def enviar_datos(status):
    name = name_entry.get()

    if name.strip() == "":
        messagebox.showwarning("Advertencia", "El campo 'nombre' no puede estar vacío.")
    else:
        enviar_a_restful(status, name)

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

# Flechas arriba y abajo centradas
btn_up = tk.Button(flechas_frame, text="⬆", font=("Arial", 20), command=lambda: enviar_datos("Arriba"))
btn_up.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

btn_down = tk.Button(flechas_frame, text="⬇", font=("Arial", 20), command=lambda: enviar_datos("Abajo"))
btn_down.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

# Flechas izquierda (90° y 180°), detenerse, y derecha (90° y 180°)
btn_left_180 = tk.Button(flechas_frame, text="⬅ 180°", font=("Arial", 20), command=lambda: enviar_datos("180° a la izquierda"))
btn_left_180.grid(row=1, column=0, padx=10, pady=10)

btn_left_90 = tk.Button(flechas_frame, text="⬅ 90°", font=("Arial", 20), command=lambda: enviar_datos("90° a la izquierda"))
btn_left_90.grid(row=1, column=1, padx=10, pady=10)

# Botón de detenerse con símbolo de cuadrado
btn_detenerse = tk.Button(flechas_frame, text="■", font=("Arial", 20), command=lambda: enviar_datos("Detenerse"))
btn_detenerse.grid(row=1, column=2, padx=10, pady=10)

btn_right_90 = tk.Button(flechas_frame, text="➡ 90°", font=("Arial", 20), command=lambda: enviar_datos("90° a la derecha"))
btn_right_90.grid(row=1, column=3, padx=10, pady=10)

btn_right_180 = tk.Button(flechas_frame, text="➡ 180°", font=("Arial", 20), command=lambda: enviar_datos("180° a la derecha"))
btn_right_180.grid(row=1, column=4, padx=10, pady=10)

# Crear la tabla para mostrar los últimos 10 registros
columns = ('status', 'name', 'ipClient', 'date')
tree = ttk.Treeview(root, columns=columns, show='headings')

# Definir los encabezados de la tabla
tree.heading('status', text='Status')
tree.heading('name', text='Nombre')
tree.heading('ipClient', text='IP Cliente')
tree.heading('date', text='Fecha')

# Ajustar el tamaño de las columnas
tree.column('status', width=100)
tree.column('name', width=150)
tree.column('ipClient', width=150)
tree.column('date', width=150)

# Empaquetar la tabla en la ventana principal
tree.pack(pady=20)

# Iniciar el loop de la ventana
root.mainloop()
