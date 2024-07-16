import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
import os

CATEGORIAS = ['Alimentación', 'Transporte', 'Entretenimiento', 'Salud', 'Educación', 'Otros']

# Función para agregar un gasto
def agregar_gasto(datos, categoria, cantidad, fecha):
    nuevo_gasto = {'Fecha': fecha, 'Categoría': categoria, 'Cantidad': cantidad}
    datos = datos._append(nuevo_gasto, ignore_index=True)
    datos.to_csv('gastos.csv', index=False)
    return datos

# Función para cargar los gastos desde el archivo CSV
def cargar_gastos():
    if not os.path.exists('gastos.csv') or os.path.getsize('gastos.csv') == 0:
        datos = pd.DataFrame(columns=['Fecha', 'Categoría', 'Cantidad'])
    else:
        datos = pd.read_csv('gastos.csv')
    return datos

# Función para mostrar un gráfico de los gastos
def mostrar_grafico(datos):
    if not datos.empty:
        datos.groupby('Categoría')['Cantidad'].sum().plot(kind='bar')
        plt.ylabel('Cantidad')
        plt.title('Gastos por Categoría')
        plt.show()
    else:
        sg.popup('No hay datos para mostrar el gráfico.')

# Función para validar los datos ingresados
def validar_datos(fecha, categoria, cantidad):
    try:
        pd.to_datetime(fecha)
    except ValueError:
        return False, "Fecha inválida"
    if categoria not in CATEGORIAS:
        return False, "Categoría inválida"
    try:
        float(cantidad)
    except ValueError:
        return False, "Cantidad inválida"
    return True, ""

# Configuración de la interfaz gráfica
layout = [
    [sg.Text('Fecha (YYYY-MM-DD)'), sg.InputText(key='fecha')],
    [sg.Text('Categoría'), sg.Combo(CATEGORIAS, key='categoria')],
    [sg.Text('Cantidad'), sg.InputText(key='cantidad')],
    [sg.Button('Agregar Gasto')],
    [sg.Button('Mostrar Gráfico')],
    [sg.Button('Salir')]
]

window = sg.Window('Registro de Gastos', layout)

# Cargar los gastos existentes
datos = cargar_gastos()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Salir':
        break
    elif event == 'Agregar Gasto':
        valido, mensaje = validar_datos(values['fecha'], values['categoria'], values['cantidad'])
        if valido:
            datos = agregar_gasto(datos, values['categoria'], float(values['cantidad']), values['fecha'])
            sg.popup('Gasto agregado con éxito!')
        else:
            sg.popup(mensaje)
    elif event == 'Mostrar Gráfico':
        mostrar_grafico(datos)

window.close()
