from flask import Flask, render_template, request, url_for, flash, session, redirect, jsonify, send_from_directory

from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_mail import Message
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask import url_for, current_app
from flask import current_app
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración para MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'AngieStudio'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = 'static/IMG'

# Configuracion para enviar correos
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dilanyarce22@gmail.com'  
app.config['MAIL_PASSWORD'] = 'ppoj ltoy ryhq zrkg'  
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

mysql = MySQL(app)

# Rutas y funciones para la primera aplicación
# Ruta para cuando se inicialice el programa se inicie desde el index.html
@app.route('/')
def home():
    return render_template("index.html")

# Funcion del login para inicar sesion
@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account['id']  
            session['id_rol'] = account['id_rol']  
            session['nombre'] = account['nombre']  

            if session['id_rol'] == 1:
                client_count = get_client_count()
                return render_template("Administrador.html", nombre=session['nombre'], client_count=client_count)
            elif session['id_rol'] == 2:
                return render_template("Empleado.html", nombre=session['nombre'])
            elif session['id_rol'] == 3:
                return render_template("Cliente.html", nombre=session['nombre'])
        else:
            return render_template('login.html', mensaje="¡Usuario o contraseña incorrectas!")

    return render_template('login.html')


def get_client_count():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS count FROM usuarios WHERE id_rol = 2')  
    result = cur.fetchone()
    cur.close()
    return result['count'] if result else 0

# Funcion para redirigir al Administrador.html
@app.route('/admin')
def admin():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id_rol = 2")
    empleados = cur.fetchall()  
    cur.close()

    client_count = get_client_count()
    return render_template("Administrador.html", nombre=session.get('nombre'),  client_count=client_count, empleados=empleados)


# Redireccion al template del empleado
@app.route('/Empleado')
def Empleado():
    return render_template("Empleado.html", nombre=session.get('nombre'))

# Redireccion al template de cliente
@app.route('/Cliente')
def Cliente():
    return render_template("Cliente.html", nombre=session.get('nombre'))

# Redireccion al template de registrar empleado
@app.route('/Redirigir_Empleado')
def Redirigir_Empleado():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id_rol = 2")
    empleados = cur.fetchall()
    cur.close()
    return render_template("Registrar_Empleado.html", empleados=empleados, nombre=session.get('nombre'))

#Redirigir al template de Citas.html
@app.route('/Citas', methods=['GET', 'POST'])
def Citas():
    if request.method == 'POST':
        id_cita = request.form['id_cita']
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        servicio = request.form['servicio']
        empleado_nombre = request.form['empleado_nombre']
        fecha = request.form['Fecha']
        hora = request.form['Hora'] 
        motivo = request.form['motivo']
    
        cur = mysql.connection.cursor()
        cur.execute("UPDATE citas SET nombre=%s, cedula=%s, servicio=%s, empleado_nombre=%s, fecha=%s, hora=%s, motivo=%s WHERE id_cita=%s", 
                    (nombre, cedula, servicio,  empleado_nombre,  fecha, hora, motivo, id_cita)) 
        mysql.connection.commit()
        cur.close()
        
        flash("Cita actualizada correctamente.")
        return redirect(url_for('Citas'))

    # Obtener el ID del cliente logeado desde la sesión
    cliente_id = session.get('id')

    cursor = mysql.connection.cursor()

    if session.get('id_rol') == 2:  # Si el usuario es un empleado
        # Consulta para obtener el nombre del empleado logueado
        cursor.execute("SELECT nombre FROM usuarios WHERE id = %s", (cliente_id,))
        nombre_empleado = cursor.fetchone()['nombre']

        # Consulta para obtener las citas del empleado logeado
        cursor.execute("SELECT * FROM citas WHERE empleado_nombre = %s", (nombre_empleado,))
    elif session.get('id_rol') == 1:  # Si el usuario es un administrador
        # Consulta para obtener todas las citas
        cursor.execute("SELECT * FROM citas")
    else:
        # Consulta para obtener las citas del cliente logeado
        cursor.execute("SELECT * FROM citas WHERE id_cliente = %s", (cliente_id,))
    
    citas = cursor.fetchall()

    # Consulta para obtener nombres de servicios
    cursor.execute("SELECT nombre, FORMAT(precio, 2, 'es_CL') AS precio_formateado FROM servicios")
    servicios = cursor.fetchall()
    nombres_y_precios_servicios = [(servicio['nombre'], servicio['precio_formateado']) for servicio in servicios]
    
    # Consulta para obtener nombres de empleados
    cursor.execute("SELECT nombre FROM usuarios WHERE id_rol = 2")
    empleados = cursor.fetchall()
    empleados_servicios = [empleado['nombre'] for empleado in empleados]
    
    cursor.close()

    # Formato de horas par el campo de agendamiento de citas por parte de los clientes, empleados y administradores
    horas = []
    for i in range(8, 12): 
        hora_am = str(i).zfill(2) + ':00 am'
        horas.append(hora_am)

    for i in range(12, 18):  
        if i == 12:  
            hora_pm = str(i).zfill(2) + ':00 pm'
        else:
            hora_pm = str(i - 12).zfill(2) + ':00 pm'  
        horas.append(hora_pm)
        
    return render_template("Citas.html",  nombres_y_precios_servicios= nombres_y_precios_servicios, empleados_servicios=empleados_servicios, citas=citas, nombre=session.get('nombre'), lista_servicios= nombres_y_precios_servicios, horas=horas)

@app.route('/actualizar_cita_fecha_hora', methods=['POST'])
def actualizar_cita_fecha_hora():
    if request.method == 'POST':
        id_cita = request.form['id_cita']
        fecha = request.form['fecha']
        hora = request.form['hora'] 
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE citas SET fecha=%s, hora=%s WHERE id_cita=%s", (fecha, hora, id_cita))
        mysql.connection.commit()
        cur.close()
        
        flash("Cita actualizada correctamente.")
        return redirect(url_for('Citas'))

@app.route('/agregar_servicio', methods=['POST'])
def agregar_servicio():
    if request.method == 'POST':
        nombre_servicio = request.form['nombre_servicio']
        empleado = request.form['empleados_nombre']

        # Insertar el nuevo servicio en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO servicios (nombre, empleado) VALUES (%s, %s)", (nombre_servicio, empleado))
        mysql.connection.commit()
        cur.close()

        flash("Nuevo servicio agregado correctamente.")
        return redirect(url_for('Citas'))
    else:
        flash("Error al agregar el nuevo servicio.")
        return redirect(url_for('Citas'))

# Función para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar la sesión del usuario
    session.clear()
    # Redirigir al usuario a la página de inicio
    return redirect(url_for('home'))

# Función para redirigir al registro.html
@app.route('/registro')
def registro():
    return render_template("registro.html")

# Función para crear el registro desde el template del registro
@app.route('/crear-registro', methods=["GET", "POST"])
def crear_registro():
    if request.method == "POST":
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        nombre = request.form['txtNombre']
        apellido = request.form['txtApellido']
        telefono = request.form['txtTelefono']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (correo, password, nombre, apellido, telefono, id_rol) VALUES (%s, %s, %s, %s, %s, %s)",
                    (correo, password, nombre, apellido, telefono, '3'))
        mysql.connection.commit()
        cur.close()
        url_for('static', filename='style.css')
        return render_template("login.html")
    else:
        pass

# Función para crear Empleados
@app.route('/Registrar_Empleado', methods=["GET", "POST"])
def Registrar_Empleado():
    if request.method == "POST":
        correo = request.form.get('correo')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        dias_trabajo = request.form.get('dias_trabajo')
        horario_trabajo = request.form.get('horario_trabajo')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (correo, password, nombre, apellido, telefono, id_rol, dias_trabajo, horario_trabajo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (correo, password, nombre, apellido, telefono, 2, dias_trabajo, horario_trabajo))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Redirigir_Empleado'))  
    else:
        #Mostar los empleados
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, correo, dias_trabajo, horario_trabajo, nombre, apellido, telefono FROM usuarios WHERE id_rol = 2")
        empleados = cur.fetchall()  
        cur.close()
        return render_template("Registrar_Empleado.html", empleados=empleados)


# Función del inventario para seleccionar los productos y los campos
@app.route('/inventario')
def inventario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productos_data = cur.fetchall()
    cur.close()
    return render_template('inventario.html', productos=productos_data, nombre=session.get('nombre'))

# Función para insertar un nuevo producto
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Producto ingresado con éxito")
        Id = request.form['Id']
        Nombre = request.form['Nombre']
        Fecha_Ingreso = request.form['Fecha_Ingreso']
        Cantidad = request.form['Cantidad']
        Marca = request.form['Marca']
        Precio = request.form['Precio']
        Descripcion = request.form['Descripcion']
        Imagen = request.files['Imagen']
        Fecha_vencimiento = request.form['Fecha_vencimiento']

        # Save the image on the server
        filename = secure_filename(Imagen.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Imagen.save(image_path)

        # Insert the product into the catalog
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (Id, Nombre, Fecha_Ingreso, Cantidad, Marca, Precio, Descripcion, Imagen, Fecha_vencimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (Id, Nombre, Fecha_Ingreso, Cantidad, Marca, Precio, Descripcion, image_path, Fecha_vencimiento))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('inventario', nombre=session.get('nombre')))
    
@app.route('/add_to_catalog/<int:id>', methods=['POST'])
def add_to_catalog(id):
    # Obtener el producto desde la base de datos de productos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE Id = %s", (id,))
    product = cur.fetchone()
    cur.close()

    if product:
        # Insertar el producto en la tabla de catálogo
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO product (title, description, price, image_path, quantity) VALUES (%s, %s, %s, %s, %s)",
                    (product['Nombre'], product['Descripcion'], product['precio'], product['Imagen'], product['Cantidad']))
        mysql.connection.commit()
        cur.close()

        # flash('Producto agregado al catálogo', 'success')
        return redirect(url_for('inventario'))
    else:
        # flash('El producto no existe', 'error')
        return redirect(url_for('inventario'))

# Función para eliminar el producto
@app.route('/delete/<string:Id>', methods=['GET'])
def delete(Id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM productos WHERE Id=%s", (Id,))
        mysql.connection.commit()
        flash("Producto eliminado con éxito")
    except Exception as e:
        flash("Error al eliminar el producto: " + str(e))
    finally:
        cur.close()
    return redirect(url_for('inventario'))

@app.route('/Delete_Empleado/<string:id>', methods=['GET'])
def Delete_Empleado(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        mysql.connection.commit()
        # flash("Empleado eliminado con éxito")
    except Exception as e:
        flash("Error al eliminar el empleado: " + str(e))
    finally:
        cur.close()
    return render_template('Registrar_Empleado.html', nombre=session.get('nombre'))

# Función para actualizar un producto
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        Id = request.form['Id']
        Nombre = request.form['Nombre']
        Fecha_Ingreso = request.form['Fecha_Ingreso']
        Cantidad = request.form['Cantidad']
        Marca = request.form['Marca']
        Precio = request.form['precio']
        Descripcion = request.form['Descripcion']
        Imagen = request.files['Imagen']
        Fecha_vencimiento = request.form['Fecha_vencimiento']

        try:
            cur = mysql.connection.cursor()

            # Verifica si se ha subido una nueva imagen
            if Imagen.filename != '':
                # Obtener nombre de archivo seguro
                nombre_archivo = secure_filename(Imagen.filename)
                # Mueve la imagen a una ubicación segura en el servidor
                ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
                Imagen.save(ruta_imagen)
            else:
                # Si no se ha subido una nueva imagen, conserva la existente
                ruta_imagen = request.form['Imagen_actual']

            # Actualiza la fila en la base de datos con el nuevo nombre de archivo de imagen
            cur.execute("""
                UPDATE productos SET Nombre=%s, Fecha_Ingreso=%s, Cantidad=%s, Marca=%s, Precio=%s, Descripcion=%s, Imagen=%s, Fecha_vencimiento=%s
                WHERE Id=%s
            """, (Nombre, Fecha_Ingreso, Cantidad, Marca, Precio, Descripcion, nombre_archivo, Fecha_vencimiento, Id))
            
            mysql.connection.commit()
            flash("Actualizado con éxito")
            return redirect(url_for('inventario', nombre=session.get('nombre')))
        except Exception as e:
            flash(f"Error al actualizar: {str(e)}")
        finally:
            cur.close()
    return render_template('inventario.html', nombre=session.get('nombre'))


    
# Update_Empleado Función para editar al empleado
@app.route('/Update_Empleado', methods=['POST', 'GET'])
def Update_Empleado():
    if request.method == 'POST':
        id = request.form['id']
        correo = request.form['correo'] 
        correo = request.form['correo'] 
        dias_trabajo = request.form['dias_trabajo'] 
        horario_trabajo = request.form['horario_trabajo']  
        nombre = request.form['nombre']  
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE usuarios SET correo=%s ,Dias_trabajo=%s , Horario_trabajo=%s, nombre=%s, apellido=%s, telefono=%s
            WHERE id=%s
            """, (correo, dias_trabajo, horario_trabajo, nombre, apellido, telefono, id))
            
            mysql.connection.commit()
            # flash("Empleado actualizado con éxito")
        except Exception as e:
            flash(f"Error al actualizar al empleado: {str(e)}")
        
        return render_template('Registrar_Empleado.html', nombre=session.get('nombre'))

# Función del inventario para registrar las entradas
@app.route('/Entradas')
def Entradas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM entrada_productos")
    entradas_data = cur.fetchall()
    cur.close()
    return render_template('Entradas.html', entradas_data=entradas_data, nombre=session.get('nombre'))

# Función para redirigir al template de Entradas.html
@app.route('/redireccionar_a_entradas')
def redireccionar_a_entradas():
    # Redireccionar a la página de Entradas.html
    return redirect(url_for('Entradas', nombre=session.get('nombre')))

# Función para registrar las salidas de los productos
@app.route('/Salidas')
def Salidas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM salida_productos")
    salidas_data = cur.fetchall()
    cur.close()
    return render_template('Salidas.html', salidas=salidas_data, nombre=session.get('nombre'))

# Función para registrar las novedades de los productos
# Función para mostrar las novedades de entrada
@app.route('/Novedades')
def Novedades():
    Id_Producto = request.args.get('Id_Producto')
    marca = request.args.get('Marca')
    if Id_Producto:
        cur = mysql.connection.cursor()
        if marca:
            cur.execute("""
                SELECT n.*, p.Cantidad AS Cantidad_Actual 
                FROM Novedades n 
                JOIN productos p ON n.Id_Producto = p.Id 
                WHERE p.Id = %s AND n.Marca = %s
            """, (Id_Producto, marca))
        else:
            cur.execute("""
                SELECT n.*, p.Cantidad AS Cantidad_Actual 
                FROM Novedades n 
                JOIN productos p ON n.Id_Producto = p.Id 
                WHERE p.Id = %s
            """, (Id_Producto,))
    else:
        cur = mysql.connection.cursor()
        if marca:
            cur.execute("""
                SELECT n.*, p.Cantidad AS Cantidad_Actual 
                FROM Novedades n 
                JOIN productos p ON n.Id_Producto = p.Id 
                WHERE n.Marca = %s
            """, (marca,))
        else:
            cur.execute("""
                SELECT n.*, p.Cantidad AS Cantidad_Actual 
                FROM Novedades n 
                JOIN productos p ON n.Id_Producto = p.Id
            """)
    novedades_data = cur.fetchall()
    cur.close()

    # Obtener todas las marcas distintas de la tabla de novedades
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT Marca FROM Novedades")
    marcas_data = cur.fetchall()
    cur.close()

    return render_template('Novedades.html', novedades=novedades_data, marcas=marcas_data, nombre=session.get('nombre'))


# --------------------------------------------------------Registrar Citas
# --------------------------------------------------------Registrar Citas
@app.route('/Registrar_Cita', methods=["GET", "POST"])
def Registrar_Cita():
    if request.method == "POST":
        cliente_id = session.get('id')

        # Verificar el límite de citas
        cur = mysql.connection.cursor()
        cur.execute("SELECT num_citas FROM usuarios WHERE id = %s", (cliente_id,))
        num_citas = cur.fetchone()['num_citas']
        cur.close()

        if num_citas >= 5:
            flash("Has alcanzado el límite de 5 citas. Por favor, elimina una cita existente para agregar una nueva.")
            return redirect(url_for('Citas'))
        
        # Procesar el formulario de cita
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')
        servicio = request.form.get('servicio')
        empleado_nombre = request.form.get('empleados_nombre')
        fecha = request.form.get('Fecha')
        hora = request.form.get('Hora')
        motivo = request.form.get('motivo')

        # Verificar si la cita ya existe
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM citas WHERE empleado_nombre = %s AND fecha = %s AND hora = %s",
                    (empleado_nombre, fecha, hora))
        existing_cita = cur.fetchone()
        cur.close()

        if existing_cita:
            flash(f"Ya hay una cita programada para el empleado {empleado_nombre} a las {hora} el día {fecha}. Por favor, elige otra hora.")
            return redirect(url_for('Citas'))

        # Insertar la cita en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO citas (nombre, cedula, servicio, empleado_nombre, fecha, hora, motivo, id_cliente) VALUES (%s, %s,%s, %s, %s, %s, %s, %s)",
                    (nombre, cedula, servicio, empleado_nombre, fecha, hora, motivo, cliente_id))
        mysql.connection.commit()

        # Incrementar el número de citas del usuario en la base de datos
        cur.execute("UPDATE usuarios SET num_citas = num_citas + 1 WHERE id = %s", (cliente_id,))
        mysql.connection.commit()

        # Obtener el correo electrónico del usuario
        cur = mysql.connection.cursor()
        cur.execute("SELECT correo FROM usuarios WHERE id = %s", (cliente_id,))
        user_email = cur.fetchone()['correo']
        cur.close()

        # Enviar correo electrónico
        # Obtener la ruta completa del archivo email.html en la carpeta templates
    email1_template_path = current_app.root_path + '/templates/email1.html'
    
    with open(email1_template_path, 'r') as archivo:
        email_content = archivo.read()
        
        # Renderizar el contenido HTML del archivo email1.html
        html_content = render_template('email1.html')
        
        msg = Message('Nueva cita registrada', sender='dilanyarce22@gmail.com', recipients=[user_email])
        msg.html = f"""\
        <h1>Nueva cita registrada</h1>
        <br><br>
        {html_content}
        <br><br>

        <p>Se ha registrado una nueva cita para: {nombre} el día: {fecha} a las: {hora} con el empleado: {empleado_nombre}. Motivo: {motivo}.</p>.
        """
        mail.send(msg)

        flash("Cita agregada correctamente.")
        return redirect(url_for('Citas'))

    return render_template("Citas.html", nombre=session.get('nombre'))

# ---------------------------------------------------Funcion pora eliminar cita
@app.route('/eliminar_cita/<int:cita_id>', methods=["POST"])
def eliminar_cita(cita_id):
    if request.method == "POST":
        try:
            # Obtener el ID del cliente asociado con la cita
            cur = mysql.connection.cursor()
            cur.execute("SELECT id_cliente FROM citas WHERE id_cita = %s", (cita_id,))
            cliente_id = cur.fetchone()['id_cliente']
            cur.close()

            # Eliminar la cita de la base de datos
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM citas WHERE id_cita = %s", (cita_id,))
            mysql.connection.commit()
            cur.close()

            # Decrementar el número de citas del cliente
            cur = mysql.connection.cursor()
            cur.execute("UPDATE usuarios SET num_citas = num_citas - 1 WHERE id = %s", (cliente_id,))
            mysql.connection.commit()
            cur.close()

            flash("Cita eliminada correctamente.")
        except Exception as e:
            flash("Error al eliminar la cita: " + str(e))

    return redirect(url_for('Citas'))

# -----------------------------------------Funcion para pedir el correo para el restablecimiento de contraseña
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    error = None
    if request.method == 'POST':
        user_email = request.form['txtCorreo']
            
        session['reset_email'] = user_email
        send_reset_email(user_email)
        return redirect(url_for('login'))
    return render_template('forgot.html', error=error)

# -----------------------Función para enviar el correo electrónico con el enlace de restablecimiento de contraseña
def send_reset_email(user_email):
    reset_link = url_for('newpassword', _external=True)
    
    # Obtener la ruta completa del archivo email.html en la carpeta templates
    email_template_path = current_app.root_path + '/templates/email.html'
    
    with open(email_template_path, 'r') as archivo:
        email_content = archivo.read()

    msg = Message('Recuperación de contraseña', sender='dilanyarce22@gmail.com', recipients=[user_email])
    
    msg.html = f'''
    <html>
    <head>
        <style>
            .button {{
                background-color: #F3D0D7;
                color: #fff;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <h2>Recuperación de contraseña</h2>
        <br><br>
        {email_content}
        <br><br>
        <a href="{reset_link}" class="button">Restablecer Contraseña</a>
        <p>Atentamente,<br>
        Tu Equipo de Soporte</p>
    </body>
    </html>
    '''

    mail.send(msg)

# -----------------------------------------------------Ruta para restablecer la contraseña
@app.route('/newpassword', methods=['GET', 'POST'])
def newpassword():
    if request.method == 'POST':
        if request.form['newPassword'] != request.form['conpass']:
            return redirect(url_for('newpassword'))
        else:
            user_email = session.get('reset_email')
            new_password = request.form['newPassword']
            if update_password_in_database(user_email, new_password):
                session.pop('reset_email', None)
                return redirect(url_for('login'))
            else:
                return render_template('newpassword.html', error='Error al actualizar la contraseña. Por favor, inténtalo de nuevo.')
    return render_template('newpassword.html')

#---------------------------------------- Función para actualizar la contraseña en la base de datos
def update_password_in_database(user_email, new_password):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET password = %s WHERE correo = %s", (new_password, user_email))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print("Error al actualizar la contraseña:", e)
        return False
    
#------------------------------------------------------------------ Actualizar cuenta
@app.route('/actualizar-cuenta', methods=['GET', 'POST'])
def actualizar_cuenta():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nuevo_nombre = request.form['txtNombre']
        nuevo_apellido = request.form['txtApellido']
        nuevo_correo = request.form['txtCorreo']
        nuevo_telefono = request.form['txtTelefono']
        nueva_contrasena = request.form['txtPassword']
        confirmar_contrasena = request.form['txtConfirmPassword']

        # Actualizar los datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, telefono = %s, password = %s WHERE id = %s",
                    (nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono, nueva_contrasena, session['id']))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('actualizar_cuenta'))

    # Obtener los datos actuales del usuario
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", (session['id'],))
    usuario = cur.fetchone()
    cur.close()

    return render_template('Cambiar_perfil.html', usuario=usuario)

# ---------------------------------------------------- Catalogo
@app.route('/Home_Catalogo')
def Home_Catalogo():
    cur = mysql.connection.cursor()
    cur.execute("SELECT *, IFNULL((SELECT SUM(quantity) FROM product WHERE id = product.id), 0) AS quantity FROM product WHERE active = 1")
    products = cur.fetchall()
    cur.close()
    return render_template('home.html', products=products)



@app.route('/add_to_cart/<int:id>', methods=['POST'])
def add_to_cart(id):
    product_id = id
    quantity = int(request.form.get('quantity', 1))  # Obtener la cantidad del formulario

    # Consultar la base de datos para verificar si el producto ya está en el carrito
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart WHERE product_id = %s", (product_id,))
    already_in_cart = cur.fetchone()

    if already_in_cart:
        flash('El producto ya está en el carrito', 'danger')
    else:
        # Consultar la base de datos para obtener el producto completo
        cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
        product_data = cur.fetchone()  # Obtener los datos del producto como un diccionario

        if product_data:
            # Insertar el producto en la tabla de carrito en la base de datos
            cur.execute("INSERT INTO cart (product_id, title, image_path, price, quantity, total) VALUES (%s, %s, %s, %s, %s, %s)",
                        (product_data['id'], product_data['title'], product_data['image_path'], product_data['price'], quantity, product_data['price'] * quantity))
            mysql.connection.commit()
            flash('Producto agregado al carrito exitosamente', 'success')
        else:
            flash('El producto no existe', 'danger')

    cur.close()

    return redirect(url_for('Home_Catalogo'))




# ------------------------------- Finalizar compra --- carrito


# Lista global para almacenar los elementos del carrito
cart_items = []

# Clase de ejemplo para un producto
class Product:
    def __init__(self, id, title, price):
        self.id = id
        self.title = title
        self.price = price

# Ruta para el carrito de compras
@app.route('/cart')
def cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart")
    cart_items = cur.fetchall()
    cur.close()
    
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)



@app.route('/remove_from_cart/<int:id>', methods=['POST'])
def remove_from_cart(id):
    product_id = id

    # Eliminar el producto del carrito en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
    mysql.connection.commit()
    cur.close()

    flash('Producto removido del carrito exitosamente', 'success')
    return redirect(url_for('cart'))


#----------------------------------- apartar producto 


# Ruta y función para procesar la orden
# Ruta y función para procesar la orden
@app.route('/order_processed', methods=['POST'])
def order_processed():
    # Obtener los datos del cliente del formulario
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')

    # Insertar datos del cliente en la tabla 'client'
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO client (nombre, apellidos, direccion, telefono, correo) VALUES (%s, %s, %s, %s, %s)",
                (nombre, apellidos, direccion, telefono, correo))
    mysql.connection.commit()
    cur.close()

    # Obtener el ID del cliente recién insertado
    cur = mysql.connection.cursor()
    cur.execute("SELECT LAST_INSERT_ID()")
    client_id = cur.fetchone()['LAST_INSERT_ID()']
    cur.close()

    # Consultar la base de datos para obtener los elementos del carrito con los detalles de los productos
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.*, p.title as product_title, p.price as product_price, p.title as product_name
        FROM cart c 
        JOIN product p ON c.product_id = p.id
    """)
    cart_items = cur.fetchall()

    # Insertar detalles de la orden en la tabla 'order_detail'
    for item in cart_items:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO order_detail (client_id, product_id, product_name, quantity, total) VALUES (%s, %s, %s, %s, %s)",
                    (client_id, item['product_id'], item['product_name'], item['quantity'], item['total']))
        mysql.connection.commit()
        cur.close()

    if cart_items:
        return render_template('order_processed.html',
                               nombre=nombre,
                               apellidos=apellidos,
                               direccion=direccion,
                               telefono=telefono,
                               correo=correo,
                               cart_items=cart_items)
    else:
        flash('Error: Carrito vacío', 'danger')
        return redirect(url_for('Home_Catalogo'))


# Ruta y función para mostrar la página de apartado de productos
@app.route('/apartado_produc', methods=['GET'])
def apartado_produc():
    product_ids = request.args.getlist('product_id')  # Obtener lista de IDs de productos
    if product_ids:
        cart_items = []
        cur = mysql.connection.cursor()
        for product_id in product_ids:
            cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
            product_data = cur.fetchone()
            if product_data:
                cart_items.append({
                    'title': product_data['title'],
                    'description': product_data['description'],
                    'price': product_data['price']
                })
            else:
                flash(f'Producto con ID {product_id} no encontrado', 'danger')
        cur.close()
        return render_template('apartado_produc.html', cart_items=cart_items)
    else:
        flash('No se proporcionaron IDs de productos para apartar', 'danger')
        return redirect(url_for('Home_Catalogo'))


# Ruta y función para limpiar el carrito
@app.route('/limpiar_carrito', methods=['POST'])
def limpiar_carrito():
    # Elimina todos los productos del carrito
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart")
    mysql.connection.commit()
    cur.close()
    
    # Redirige al catálogo después de limpiar el carrito
    return redirect(url_for('Home_Catalogo'))


# ---------------------- crear productos

@app.route('/products', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity') 

        # Save the image on the server
        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Create the product in the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO product (title, description, price, image_path, quantity) VALUES (%s, %s, %s, %s, %s)", (title, description, price, image_path, quantity))
        mysql.connection.commit()
        cur.close()

        # flash('Producto creado exitosamente', 'success')
        return redirect(url_for('Home_Catalogo'))
    return render_template('create_product.html')


# --------------------- borrar productos

@app.route('/products/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM product WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    # flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('Home_Catalogo'))

# ---------------------------- actualizar producto

@app.route('/products/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity') 
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT image_path FROM product WHERE id = %s", (id,))
            image_path = cur.fetchone()['image_path']
            cur.close()

        # Update the product in the database
        cur = mysql.connection.cursor()
        cur.execute("UPDATE product SET title = %s, description = %s, price = %s, image_path = %s, quantity = %s WHERE id = %s", (title, description, price, image_path, quantity, id))
        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('Home_Catalogo'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product WHERE id = %s", (id,))
    product = cur.fetchone()
    cur.close()
    return render_template('update_product.html', product=product)

# ---------------------- boton de activar o descativar

@app.route('/products/activate/<int:id>', methods=['GET', 'POST'])
def activate_product(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE product SET active = 1 WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Producto activado exitosamente', 'success')
    return redirect(url_for('Home_Catalogo'))

@app.route('/products/deactivate/<int:id>', methods=['GET', 'POST'])
def deactivate_product(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE product SET active = 0 WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Producto desactivado exitosamente', 'success')
    return redirect(url_for('Home_Catalogo'))

# ------------ producto

@app.route('/product_actions')
def product_actions():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    cur.close()
    return render_template('product_actions.html', products=products)


# --------------------------------------------- editar clientes y detalles del producto
@app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE client
            SET nombre = %s, apellidos = %s, direccion = %s, telefono = %s, correo = %s
            WHERE id = %s
        """, (nombre, apellidos, direccion, telefono, correo, cliente_id))
        mysql.connection.commit()
        cur.close()

        flash('Detalles del cliente actualizados correctamente', 'success')
        return redirect(url_for('ver_clientes'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM client WHERE id = %s", (cliente_id,))
    cliente = cur.fetchone()

    # Obtener los detalles del pedido del cliente
    cur.execute("""
        SELECT * FROM order_detail WHERE client_id = %s
    """, (cliente_id,))
    order_details = cur.fetchall()
    cur.close()

    return render_template('editar_cliente.html', cliente=cliente, order_details=order_details)



# Ruta y función para eliminar un cliente y sus órdenes asociadas
@app.route('/eliminar_cliente/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    cur = mysql.connection.cursor()

    # Eliminar órdenes asociadas al cliente
    cur.execute("DELETE FROM order_detail WHERE client_id = %s", (cliente_id,))
    mysql.connection.commit()

    # Eliminar al cliente
    cur.execute("DELETE FROM client WHERE id = %s", (cliente_id,))
    mysql.connection.commit()
    cur.close()

    flash('Cliente y sus órdenes asociadas eliminadas correctamente', 'success')
    return redirect(url_for('ver_clientes'))

# Ruta y función para ver todos los clientes
@app.route('/ver_clientes')
def ver_clientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM client")
    clientes = cur.fetchall()
    cur.close()

    return render_template('ver_clientes.html', clientes=clientes)

if __name__ == "__main__":
    app.run(debug=True)
