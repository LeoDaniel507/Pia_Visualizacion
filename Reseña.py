from PyQt5 import QtWidgets, QtGui, uic
import sqlite3
from sqlite3 import Error
from tkinter import messagebox

# Iniciar la aplicación
app = QtWidgets.QApplication([])

# Cargar archivos .ui
login = uic.loadUi("Inicio.ui")
entrar = uic.loadUi("Registro_exitoso.ui")
registrar_1 = uic.loadUi("Registro.ui")
reseñas = uic.loadUi("reseñas.ui")
agregar_reseñas = uic.loadUi("AgregarReseñas.ui")
mostrar_reseñas_ui = uic.loadUi("MostrarReseñas.ui")

# Crear un QListWidget
list_widget = QtWidgets.QListWidget()

#Carga de base de datos
try:
    con = sqlite3.connect("base_de_datos.db")
    con.commit()
    con.close()
except:
    print("Error en la base de datos...")

#Definir login
def gui_login():
    name = login.lineEdit.text()
    password = login.lineEdit_2.text()

    if len(name) == 0 or len(password) == 0:
        login.label_5.setText("Ingrese todos los datos")
    else:
        con = sqlite3.connect("base_de_datos.db")
        cursor = con.cursor()
        cursor.execute('SELECT nombre, contraseña FROM usuarios WHERE nombre = ? AND contraseña = ?', (name, password))
        if cursor.fetchall():
            gui_entrar()
        else:
            messagebox.askokcancel(message="La contraseña o usuario son incorrectos", title="Error")

#Definir creacion de tabla de base de datos
def crear_tabla():
    con = sqlite3.connect("base_de_datos.db")
    cursor = con.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS usuarios (
            nombre text,
            apellidos text,
            edad integer,
            sexo text,
            celular integer,
            correo text,
            contraseña text
            )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS reseñas (
            pelicula text,
            reseña text,
            usuario text
            )"""
    )
    con.commit()
    con.close()

#Definir los INSERT de registro
def registrar(nombre, ap, edad, sex, cel, mail, contraseña):
    con = sqlite3.connect("base_de_datos.db")
    cursor = con.cursor()
    instruccion = f"INSERT INTO usuarios VALUES ('{nombre}', '{ap}'," \
                  f"'{edad}', '{sex}', '{cel}', '{mail}', '{contraseña}')"
    cursor.execute(instruccion)
    con.commit()
    con.close()

#Definir los datos del registro
def datos():
    nombre = registrar_1.line_nombre.text()
    apellidos = registrar_1.line_ap.text()
    edad = int(registrar_1.line_edad.text())
    box = str(registrar_1.comboBox.currentText())
    celular = int(registrar_1.line_cel.text())
    correo = registrar_1.line_correo.text()
    contraseña = registrar_1.line_contra.text()
    contraseña_2 = registrar_1.line_contra_2.text()
    if contraseña != contraseña_2:
        messagebox.askokcancel(message="Las contraseñas no son iguales", title="Error")
    elif len(str(celular)) != 10:
        messagebox.askokcancel(message="El número de celular debe tener 10 dígitos", title="Error")
    elif contraseña == contraseña_2:
        registrar(nombre, apellidos, edad, box, celular, correo, contraseña)
        messagebox.askokcancel(message="Se ha ingresado correctamente los datos", title="¡Éxito!")
        registrar_1.line_nombre.setText("")
        registrar_1.line_ap.setText("")
        registrar_1.line_edad.setText("")
        registrar_1.line_cel.setText("")
        registrar_1.line_correo.setText("")
        registrar_1.line_contra.setText("")
        registrar_1.line_contra_2.setText("")

# Función para guardar una reseña en la base de datos
def guardar_reseña():
    usuario = agregar_reseñas.lineEdit_usuario.text()
    pelicula = agregar_reseñas.lineEdit_pelicula.text()
    reseña = agregar_reseñas.textEdit_res.toPlainText()

    if not usuario or not pelicula or not reseña:
        messagebox.askokcancel(message="Ingrese un nombre de usuario, una película y una reseña.", title="Error")
        return

    con = sqlite3.connect("base_de_datos.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO reseñas (usuario, pelicula, reseña) VALUES (?, ?, ?)", (usuario, pelicula, reseña))
    con.commit()
    con.close()

    QtWidgets.QMessageBox.information(agregar_reseñas, "Éxito", "La reseña ha sido guardada exitosamente.")
    agregar_reseñas.lineEdit_usuario.clear()
    agregar_reseñas.lineEdit_pelicula.clear()
    agregar_reseñas.textEdit_res.clear()

# Función para buscar y mostrar las reseñas según el nombre de usuario
def mostrar_reseñas_usuario():
    usuario = mostrar_reseñas_ui.lineEdit_usuario.text()

    if not usuario:
        messagebox.askokcancel(message="Ingrese un nombre de usuario.", title="Error")
        return

    list_widget.clear()

    con = sqlite3.connect("base_de_datos.db")
    cursor = con.cursor()
    cursor.execute("SELECT pelicula, reseña FROM reseñas WHERE usuario=?", (usuario,))
    reseñas = cursor.fetchall()
    con.close()

    if not reseñas:
        mostrar_reseñas_ui.listWidget.addItem("No se encontraron reseñas para el usuario especificado.")
    else:
        for reseña in reseñas:
            pelicula = reseña[0]
            texto_reseña = reseña[1]
            mostrar_reseñas_ui.list_widget.addItem(f"Película: {pelicula}\nReseña: {texto_reseña}\n")

    # Ejemplo: Agregar elementos al QListWidget
    pelicula = "Pelicula 1"
    texto_reseña = "Esta es la reseña de la Pelicula 1"
    list_widget.addItem(f"Película: {pelicula}\nReseña: {texto_reseña}\n")

    pelicula = "Pelicula 2"
    texto_reseña = "Esta es la reseña de la Pelicula 2"
    list_widget.addItem(f"Película: {pelicula}\nReseña: {texto_reseña}\n")

#Definir los botones
def gui_entrar():
    login.hide()
    entrar.show()

def gui_registrar():
    login.hide()
    registrar_1.show()
    crear_tabla()

def regresar_forma():
    registrar_1.hide()
    reseñas.hide()
    login.show()

def regresar_entrar():
    entrar.hide()
    login.label_5.setText("")
    login.show()

def ingresar_a_reseñas():
    entrar.hide()
    reseñas.show()

def salir():
    app.exit()

def ingreso_a_reseña():
    reseñas.hide()
    agregar_reseñas.show()

def mostrar_reseñas():
    reseñas.hide()
    mostrar_reseñas_ui.show()

def regresar_login():
    agregar_reseñas.hide()
    login.show()

# Botones de login
login.pushButton.clicked.connect(gui_login)
login.pushButton_3.clicked.connect(gui_registrar)
login.pushButton_2.clicked.connect(salir)

# Botones de entrar
entrar.pushButton_3.clicked.connect(regresar_entrar)
entrar.pushButton_2.clicked.connect(salir)
entrar.pushButton.clicked.connect(ingresar_a_reseñas)

# Botones de registrar_1
registrar_1.pushButton.clicked.connect(regresar_forma)
registrar_1.pushButton_3.clicked.connect(datos)
registrar_1.pushButton_2.clicked.connect(salir)

# Botones de reseñas
reseñas.pushButton_2.clicked.connect(mostrar_reseñas)
reseñas.pushButton.clicked.connect(ingreso_a_reseña)
reseñas.pushButton_3.clicked.connect(regresar_forma)
reseñas.pushButton_4.clicked.connect(salir)

# Conexión de los botones en la pestaña "AgregarReseñas"
agregar_reseñas.pushButton_guardar.clicked.connect(guardar_reseña)
agregar_reseñas.pushButton_regresar.clicked.connect(regresar_login)
agregar_reseñas.pushButton_2.clicked.connect(salir)

# Conexión de los botones en la pestaña "MostrarReseñas"
agregar_reseñas.pushButton_2.clicked.connect(salir)
mostrar_reseñas_ui.pushButton_buscar.clicked.connect(mostrar_reseñas_usuario)

# Ejecutable
login.show()
app.exec()
