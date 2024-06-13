from flask import Flask, render_template, request, url_for, flash, session, redirect, send_from_directory

from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_mail import Message
from werkzeug.utils import secure_filename
from flask import url_for, current_app
from flask import current_app
import os, bcrypt, re
from MySQLdb import IntegrityError
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración para MySQL
app.config['MYSQL_HOST'] = 'proyecto.cta008mymt9s.us-east-2.rds.amazonaws.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'proyecto'  # Usuario de la base de datos
app.config['MYSQL_PASSWORD'] = '12345678'  # Contraseña del usuario de la base de datos
app.config['MYSQL_DB'] = 'AngieStudio'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = 'static/IMG'

# Configuracion para enviar correos
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'studioanguie@gmail.com'  
app.config['MAIL_PASSWORD'] = 'qrln ofuh smow loyk'  
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
    if request.method == 'POST':
        correo = request.form.get('txtCorreo')
        password = request.form.get('txtPassword')

        if not correo or not password:
            return render_template('login.html', mensaje="¡Faltan datos de acceso!")
        account = validate_login(correo, password)
        
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
            session['nombre'] = account['nombre']

            return redirect_to_user_dashboard(session['id_rol'])
        else:
            return render_template('login.html', mensaje="¡Usuario o contraseña incorrectas!")

    return render_template('login.html')

# Validacion de login requerido para poder entrar a los demas templates
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logueado' not in session:
            return render_template('403.html')
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'logueado' not in session:
                return render_template('403.html')
            if session.get('id_rol') not in allowed_roles:
                return render_template('403.html'), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.before_request
def require_login():
    allowed_routes = ['login', 'static', 'home', 'Inventario', 'logout', 'registro', 'newpassword', 'forgot', 'crear_registro']
    print(f"Endpoint: {request.endpoint}")  # Añadir para verificar el endpoint actual
    if 'logueado' not in session and request.endpoint not in allowed_routes:
        return render_template('403.html')

# Función para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar la sesión del usuario
    session.clear()
    # Redirigir al usuario a la página de inicio (o a la página de login)
    return redirect(url_for('home'))

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)
# Fin de la validacion

# Validacioin del login para la contraseña y el correo
def validate_login(correo, password):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE correo = %s', (correo,))
    account = cur.fetchone()
    cur.close()  

    if account:
        if account['password'].startswith('$2b$'):
            if bcrypt.checkpw(password.encode('utf-8'), account['password'].encode('utf-8')):
                return account  
        else:
            if password == account['password']:
                return account 
    return None 

def redirect_to_user_dashboard(role_id):
    if role_id == 1:
        return redirect(url_for('Administrador'))
    elif role_id == 2:
        return redirect(url_for('Empleado'))
    elif role_id == 3:
        return redirect(url_for('Cliente'))
    else:
        return render_template('login.html', mensaje="¡Rol de usuario no encontrado!")

def get_client_count():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS count FROM usuarios WHERE id_rol = 2')  
    result = cur.fetchone()
    cur.close()
    return result['count'] if result else 0

def get_citas_count():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS count FROM citas')  
    result = cur.fetchone()
    cur.close()
    return result['count'] if result else 0

def get_productos_count():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS count FROM productos')  
    result = cur.fetchone()
    cur.close()
    return result['count'] if result else 0

def get_product_count():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS count FROM product')  
    result = cur.fetchone()
    cur.close()
    return result['count'] if result else 0

# Funcion para redirigir al Administrador.html
@app.route('/Administrador')
@login_required
@role_required([1])
def Administrador():
    cur = mysql.connection.cursor()
    # Consulta SQL para obtener los empleados
    cur.execute("SELECT * FROM usuarios WHERE id_rol = 2") 
    empleados = cur.fetchall()

    # Consulta SQL para obtener la cantidad de citas por mes
    cur.execute("SELECT MONTHNAME(fecha) AS mes, COUNT(*) AS cantidad_citas FROM citas WHERE YEAR(fecha) = YEAR(CURDATE()) GROUP BY MONTH(fecha)")
    citas_por_mes = cur.fetchall()

    # Consulta SQL para obtener la cantidad de productos por mes
    cur.execute("SELECT MONTHNAME(Fecha_Ingreso) AS mes, COUNT(*) AS cantidad_productos FROM productos WHERE YEAR(Fecha_Ingreso) = YEAR(CURDATE()) GROUP BY MONTH(Fecha_Ingreso)")
    productos_por_mes = cur.fetchall()

    cur.close()

    # Asumiendo que existe una función `get_client_count` que devuelve algún conteo
    client_count = get_client_count()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM citas")
    citasa = cur.fetchall()
    cur.close()
    citas_count= get_citas_count()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productosa = cur.fetchall()
    cur.close()
    productos_count= get_productos_count()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    producta = cur.fetchall()
    cur.close()
    product_count= get_product_count()
    return render_template("Administrador.html", nombre=session.get('nombre'),  client_count=client_count, empleados=empleados, citas_count=citas_count, citasa=citasa, productos_count=productos_count, productosa=productosa, product_count=product_count, producta=producta, citas_por_mes=citas_por_mes, productos_por_mes=productos_por_mes)


# Redireccion al template del empleado
@app.route('/Empleado')
@login_required
@role_required([2])
def Empleado():
    cur = mysql.connection.cursor()

    # Obtener el ID del usuario logueado desde la sesión
    cliente_id = session.get('id')

    # Consulta para obtener el nombre del empleado logueado
    cur.execute("SELECT nombre FROM usuarios WHERE id = %s", (cliente_id,))

    # Consulta SQL para obtener la cantidad de citas por mes
    cur.execute("SELECT MONTHNAME(fecha) AS mes, COUNT(*) AS cantidad_citas FROM citas WHERE YEAR(fecha) = YEAR(CURDATE()) GROUP BY MONTH(fecha)")
    citas_por_mes = cur.fetchall()

    # Consulta SQL para obtener la cantidad de productos por mes
    cur.execute("SELECT MONTHNAME(Fecha_Ingreso) AS mes, COUNT(*) AS cantidad_productos FROM productos WHERE YEAR(Fecha_Ingreso) = YEAR(CURDATE()) GROUP BY MONTH(Fecha_Ingreso)")
    productos_por_mes = cur.fetchall()

    # Consulta SQL para obtener todos los empleados
    cur.execute("SELECT * FROM usuarios WHERE id_rol = 2")
    empleados = cur.fetchall()

    cur.close()

    # Asumiendo que existe una función `get_client_count` que devuelve algún conteo
    client_count = get_client_count()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM citas")
    citasa = cur.fetchall()
    cur.close()
    citas_count= get_citas_count()
    
    # Obtener el conteo de productos
    productos_count = get_productos_count()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productosa = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    producta = cur.fetchall()
    cur.close()
    product_count = get_product_count()
    return render_template("Empleado.html", nombre=session.get('nombre'), empleados=empleados, productos_count=productos_count, productosa=productosa, product_count=product_count, producta=producta, citas_count=citas_count, citas_por_mes=citas_por_mes, productos_por_mes=productos_por_mes)

# Redireccion al template de cliente
@app.route('/Cliente')
@login_required
@role_required([3])
def Cliente():
    return render_template("Cliente.html", nombre=session.get('nombre'))

# Redireccion al template de registrar empleado
@app.route('/Redirigir_Empleado')
@login_required
def Redirigir_Empleado():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id_rol = 2")
    empleados = cur.fetchall()
    cur.close()
    return render_template("Registrar_Empleado.html", empleados=empleados, nombre=session.get('nombre'))

# Redireccion al template de ver clientes
@app.route('/RedirigirClientes')
@login_required
def RedirigirClientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id_rol = 3")
    clientes = cur.fetchall()  
    cur.close()
    return render_template("Clientes.html", clientes=clientes, nombre=session.get('nombre'))

#Redirigir al template de Citas.html
@app.route('/Citas', methods=['GET', 'POST'])
@login_required
def Citas():
    if request.method == 'POST':
        id_cita = request.form['id_cita']
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        servicio = request.form['servicio']
        fecha = request.form['Fecha']
        hora = request.form['Hora'] 
        motivo = request.form['motivo']
    
        cur = mysql.connection.cursor()
        cur.execute("UPDATE citas SET nombre=%s, cedula=%s, servicio=%s, fecha=%s, hora=%s, motivo=%s WHERE id_cita=%s", 
                    (nombre, cedula, servicio,  fecha, hora, motivo, id_cita)) 
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('Citas'))

    # Obtener el ID del cliente logeado desde la sesión
    cliente_id = session.get('id')

    cursor = mysql.connection.cursor()

    if session.get('id_rol') == 1 or session.get('id_rol') == 2:  # Si el usuario es un empleado
        # Consulta para obtener el nombre del empleado logueado
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

# Actualizar fecha y hora de la cita desde el empleado
@app.route('/actualizar_cita_fecha_hora', methods=['POST'])
@login_required
def actualizar_cita_fecha_hora():
    if request.method == 'POST':
        id_cita = request.form['id_cita']
        fecha = request.form['fecha']
        hora = request.form['hora'] 
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE citas SET fecha=%s, hora=%s WHERE id_cita=%s", (fecha, hora, id_cita))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('Citas'))

# Agregar servicio desde el administrador
@app.route('/agregar_servicio', methods=['POST'])
@login_required
def agregar_servicio():
    if request.method == 'POST':
        nombre_servicio = request.form['nombre_servicio']
        precio = request.form['precio']

        # Insertar el nuevo servicio en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO servicios (nombre, precio) VALUES (%s, %s)", (nombre_servicio, precio))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('Citas'))
    else:
        return redirect(url_for('Citas'))

# Función para redirigir al registro.html
@app.route('/registro')
def registro():
    return render_template("registro.html")

@app.route('/crear-registro', methods=["GET", "POST"])
def crear_registro():
    if request.method == "POST":
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        
        # Verificar si el correo ya existe en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1 FROM usuarios WHERE correo = %s LIMIT 1", (correo,))
        row = cur.fetchone()
        cur.close()

        if row:  # Si hay algún resultado en la consulta
            flash('El correo ya está registrado, por favor inicia sesión o ingresa otro correo.', 'error')
            return redirect(url_for('registro'))
        else:
            # Validar la contraseña
            regex = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
            if not re.match(regex, password):
                flash('La contraseña debe tener al menos 8 caracteres, incluir al menos una mayúscula y un número.', 'error')
                return redirect(url_for('registro'))

            # Si la contraseña cumple los requisitos, proceder con el registro
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            nombre = request.form['txtNombre']
            apellido = request.form['txtApellido']
            telefono = request.form['txtTelefono']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (correo, password, nombre, apellido, telefono, id_rol) VALUES (%s, %s, %s, %s, %s, %s)",
                        (correo, password_hash, nombre, apellido, telefono, '3'))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("login"))
    else:
        mensaje = session.pop('mensaje_registro', None) 
        return render_template("registro.html", mensaje=mensaje)

# Función para crear Empleados
@app.route('/Registrar_Empleado', methods=["GET", "POST"])
@login_required
def Registrar_Empleado():
    if request.method == "POST":
        correo = request.form.get('correo')
        # Encriptar la contraseña 
        password = bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt())
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
        return redirect(url_for('Registrar_Empleado'))  
    else:
        # Mostrar los empleados
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, correo, dias_trabajo, horario_trabajo, nombre, apellido, telefono FROM usuarios WHERE id_rol = 2")
        empleados = cur.fetchall()  
        cur.close()
        return render_template("Registrar_Empleado.html", empleados=empleados)
    

# Función del inventario para seleccionar los productos y los campos
@app.route('/inventario')
@login_required
def inventario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Id, Nombre, Fecha_Ingreso, Cantidad, Marca, FORMAT(Precio, 2) AS Precio, Descripcion, Imagen, Fecha_vencimiento FROM productos")
    productos_data = cur.fetchall()
    cur.close()
    return render_template('Inventario.html', productos=productos_data, nombre=session.get('nombre'))

# Función para insertar un nuevo producto
@app.route('/insert', methods=['POST'])
@login_required
def insert():
    if request.method == "POST":
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

        try:
            # Insert the product into the catalog
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO productos (Id, Nombre, Fecha_Ingreso, Cantidad, Marca, Precio, Descripcion, Imagen, Fecha_vencimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        (Id, Nombre, Fecha_Ingreso, Cantidad, Marca, Precio, Descripcion, filename, Fecha_vencimiento))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('inventario', nombre=session.get('nombre')))
        
        except IntegrityError:
            flash("El código de producto ya existe. Por favor, ingrese un código único.", "error")
            return redirect(url_for('inventario', nombre=session.get('nombre')))

    return render_template("insert.html")
    
# Añadir productos al catalogo
@app.route('/add_to_catalog/<int:id>', methods=['POST'])
@login_required
def add_to_catalog(id):
    cur = mysql.connection.cursor()
    
    # Verificar si el producto ya existe en el catálogo
    cur.execute("SELECT 1 FROM product WHERE id = %s LIMIT 1", (id,))
    existing_product = cur.fetchone()
    
    if existing_product:
        # Si el producto ya está en el catálogo, mostrar un mensaje de error
        flash('El nombre del producto ya se encuentra en el catálogo, selecciona otro o edita el actual, gracias.', 'error')
        cur.close()
        return redirect(url_for('inventario'))
    else:
        # Obtener el producto desde la base de datos de productos
        cur.execute("SELECT * FROM productos WHERE Id = %s", (id,))
        product = cur.fetchone()
        
        if product:
            # Insertar el producto en la tabla de catálogo sin formatear el precio
            cur.execute("INSERT INTO product (id, title, description, price, image_path, quantity) VALUES (%s, %s, %s, %s, %s, %s)",
                        (product['Id'], product['Nombre'], product['Descripcion'], product['precio'], product['Imagen'], product['Cantidad']))
            mysql.connection.commit()
        
        cur.close()
        return redirect(url_for('inventario'))

# Función para eliminar el producto
@app.route('/delete/<string:Id>', methods=['GET'])
@login_required
def delete(Id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM productos WHERE Id=%s", (Id,))
        mysql.connection.commit()
    except Exception as e:
        flash("Error al eliminar el producto: " + str(e))
    finally:
        cur.close()
    return redirect(url_for('inventario'))

# Eliminar empleado desde el administrador
@app.route('/Delete_Empleado/<string:id>', methods=['GET'])
@login_required
def Delete_Empleado(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        mysql.connection.commit()
    except Exception as e:
        flash("Error al eliminar el empleado: " + str(e))
    finally:
        cur.close()
    return redirect(url_for('Registrar_Empleado'))

# Eliminar cliente desde el administrador
@app.route('/Delete_Cliente/<string:id>', methods=['GET'])
@login_required
def Delete_Cliente(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        mysql.connection.commit()
    except Exception as e:
        flash("Error al eliminar el cliente: " + str(e))
    finally:
        cur.close()
    return redirect(url_for('RedirigirClientes', nombre=session.get('nombre')))

# Función para actualizar un producto
@app.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        Id = request.form['Id']
        Nombre = request.form['Nombre']
        Fecha_Ingreso = request.form['Fecha_Ingreso']
        Cantidad = request.form['Cantidad']
        Marca = request.form['Marca']
        Precio = request.form['Precio']
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
            return redirect(url_for('inventario', nombre=session.get('nombre')))
        except Exception as e:
            flash(f"Error al actualizar: {str(e)}")
        finally:
            cur.close()
    return render_template('inventario.html', nombre=session.get('nombre'))

# Update_Empleado Función para editar al empleado
@app.route('/Update_Empleado', methods=['POST', 'GET'])
@login_required
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
        except Exception as e:
            flash(f"Error al actualizar al empleado: {str(e)}")
        return redirect(url_for('Registrar_Empleado', nombre=session.get('nombre')))

# Redireccion al template para ver los clientes desde el administrador

# Update de clientes desde el administrador
@app.route('/Update_Cliente', methods=['POST', 'GET'])
@login_required
def Update_Cliente():
    if request.method == 'POST':
        id = request.form['id']
        correo = request.form['correo'] 
        correo = request.form['correo']  
        nombre = request.form['nombre']  
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE usuarios SET correo=%s, nombre=%s, apellido=%s, telefono=%s
            WHERE id=%s
            """, (correo, nombre, apellido, telefono, id))  
            mysql.connection.commit()
        except Exception as e:
            flash(f"Error al actualizar al Cliente: {str(e)}")
        
        return redirect(url_for('RedirigirClientes',  nombre=session.get('nombre')))

# Función del inventario para registrar las entradas
@app.route('/Entradas')
@login_required
def Entradas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Id_Entrada, Id_Producto, Nombre, Cantidad, FORMAT(Precio, 2) AS Precio, Fecha_Entrada FROM entrada_productos")
    entradas_data = cur.fetchall()
    cur.close()
    return render_template('Entradas.html', entradas_data=entradas_data, nombre=session.get('nombre'))

# Función para redirigir al template de Entradas.html
@app.route('/redireccionar_a_entradas')
@login_required
def redireccionar_a_entradas():
    # Redireccionar a la página de Entradas.html
    return redirect(url_for('Entradas', nombre=session.get('nombre')))

# Función para registrar las salidas de los productos
@app.route('/Salidas')
@login_required
def Salidas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Id_Producto, Nombre, Cantidad, FORMAT(Precio, 2) AS precio, Fecha_Salida FROM salida_productos")
    salidas_data = cur.fetchall()
    cur.close()
    return render_template('Salidas.html', salidas=salidas_data, nombre=session.get('nombre'))

# Función para registrar las novedades de los productos
# Función para mostrar las novedades de entrada
@app.route('/Novedades')
@login_required
def Novedades():
    Id_Producto = request.args.get('Id_Producto')
    marca = request.args.get('Marca')
    if Id_Producto:
        cur = mysql.connection.cursor()
        if marca:
            cur.execute("""
                SELECT n.*, p.Cantidad AS Cantidad_Actual 
                FROM novedades n 
                JOIN productos p ON n.Id_Producto = p.Id 
                WHERE p.Id = %s AND n.Marca = %s
            """, (Id_Producto, marca))
        else:
            cur.execute("""
                SELECT n.*, p.Cantidad AS Cantidad_Actual 
                FROM novedades n 
                JOIN productos p ON n.Id_Producto = p.Id 
                WHERE p.Id = %s
            """, (Id_Producto,))
    else:
        cur = mysql.connection.cursor()
        if marca:
            cur.execute("""
                SELECT n.*, p.Cantidad AS Cantidad_Actual 
                FROM novedades n 
                JOIN productos p ON n.Id_Producto = p.Id 
                WHERE n.Marca = %s
            """, (marca,))
        else:
            cur.execute("""
                SELECT n.*, p.Cantidad AS Cantidad_Actual 
                FROM novedades n 
                JOIN productos p ON n.Id_Producto = p.Id
            """)
    novedades_data = cur.fetchall()
    cur.close()

    # Obtener todas las marcas distintas de la tabla de novedades
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT Marca FROM novedades")
    marcas_data = cur.fetchall()
    cur.close()

    return render_template('Novedades.html', novedades=novedades_data, marcas=marcas_data, nombre=session.get('nombre'))

# --------------------------------------------------------Registrar Citas
@app.route('/Registrar_Cita', methods=["GET", "POST"])
@login_required
def Registrar_Cita():
    if request.method == "POST":
        cliente_id = session.get('id')

        # Verificar el límite de citas
        cur = mysql.connection.cursor()
        cur.execute("SELECT num_citas FROM usuarios WHERE id = %s", (cliente_id,))
        num_citas = cur.fetchone()['num_citas']
        cur.close()

        if (num_citas is not None) and (num_citas >= 5):
            flash("Has alcanzado el límite de 5 citas. Por favor, elimina una cita existente para agregar una nueva.")
            return redirect(url_for('Citas'))

        # Procesar el formulario de cita
        servicio = request.form.get('servicio')

        # Dividir el campo servicio en nombre y precio
        nombre_servicio, precio_servicio = servicio.split('-')

        # Resto de campos del formulario
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')
        fecha = request.form.get('Fecha')
        hora = request.form.get('Hora')

        try:
            # Insertar la cita en la base de datos
            cur = mysql.connection.cursor()

            # Convertir y formatear el precio
            # Reemplazar los puntos con una cadena vacía y la coma con un punto
            precio_servicio = precio_servicio.replace('.', '').replace(',', '.')

            # Convertir a float y formatear con dos decimales
            precio_servicio = '{:.2f}'.format(float(precio_servicio))

            cur.execute("INSERT INTO citas (nombre, cedula, servicio, precio, fecha, hora,  id_cliente) VALUES ( %s,  %s, %s, %s, %s, %s, %s)",
                        (nombre, cedula, nombre_servicio, precio_servicio, fecha, hora,  cliente_id))
            mysql.connection.commit()

            # Incrementar el número de citas del usuario en la base de datos
            cur.execute("UPDATE usuarios SET num_citas = num_citas + 1 WHERE id = %s", (cliente_id,))
            mysql.connection.commit()

            # Obtener el correo electrónico del usuario
            cur.execute("SELECT correo FROM usuarios WHERE id = %s", (cliente_id,))
            user_email = cur.fetchone()['correo']
            cur.close()

            # Enviar correo electrónico
            email1_template_path = current_app.root_path + '/templates/email1.html'

            with open(email1_template_path, 'r') as archivo:
                email_content = archivo.read()
                
                # Renderizar el contenido HTML del archivo email1.html
                html_content = render_template('email1.html', nombre=nombre, fecha=fecha, servicio=servicio, hora=hora)

                msg = Message('Nueva cita registrada', sender='dilanyarce22@gmail.com', recipients=[user_email])
                msg.html = f"""\
                
                {html_content}

                """
                mail.send(msg)

        except IntegrityError:
            flash(f"Ya hay una cita programada a las {hora} el día {fecha}. Por favor, elige otra hora.")
            return redirect(url_for('Citas'))

        return redirect(url_for('Citas'))

    return render_template("Citas.html", nombre=session.get('nombre'))

# ---------------------------------------------------Funcion pora eliminar cita
@app.route('/eliminar_cita/<int:cita_id>', methods=["POST"])
@login_required
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

        except Exception as e:
            flash("Error al eliminar la cita: " + str(e))

    return redirect(url_for('Citas'))

# -----------------------------------------Funcion para pedir el correo para el restablecimiento de contraseña
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    error = None
    if request.method == 'POST' and 'txtCorreo' in request.form:
        user_email = request.form['txtCorreo']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s', (user_email,))
        user = cur.fetchone()

        if user:
            session['reset_email'] = user_email
            send_reset_email(user_email)
            return redirect(url_for('login'))
        else:
            error = "La dirección de correo electrónico no está registrada."

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
            new_password = bcrypt.hashpw(request.form['newPassword'].encode('utf-8'), bcrypt.gensalt())
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
@login_required
def actualizar_cuenta():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nuevo_nombre = request.form['txtNombre']
        nuevo_apellido = request.form['txtApellido']
        nuevo_correo = request.form['txtCorreo']
        nuevo_telefono = request.form['txtTelefono']
        nueva_contrasena = bcrypt.hashpw(request.form.get('txtPassword').encode('utf-8'), bcrypt.gensalt())
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

    return render_template('Cambiar_Perfil.html', usuario=usuario)

# ---------------------------------------------------- Catalogo
@app.route('/Home_Catalogo')
@login_required
def Home_Catalogo():
    cur = mysql.connection.cursor()
    cur.execute("SELECT *, IFNULL((SELECT SUM(quantity) FROM product WHERE id = product.id), 0) AS quantity FROM product WHERE active = 1")
    products = cur.fetchall()
    cur.close()
    return render_template('home.html', products=products)



@app.route('/add_to_cart/<int:id>', methods=['POST'])
@login_required
def add_to_cart(id):
    if 'id' not in session:
        flash('Necesitas iniciar sesión para agregar productos al carrito', 'danger')
        return redirect(url_for('login'))

    user_id = session['id']
    product_id = id
    quantity = int(request.form.get('quantity', 1))  # Obtener la cantidad del formulario

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart WHERE product_id = %s AND user_id = %s", (product_id, user_id))
    already_in_cart = cur.fetchone()

    cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
    product_data = cur.fetchone()

    if product_data:
        if product_data['quantity'] >= quantity:
            if already_in_cart:
                # Actualizar la cantidad del producto en el carrito
                new_quantity = already_in_cart['quantity'] + quantity
                new_total = product_data['price'] * new_quantity
                cur.execute(
                    "UPDATE cart SET quantity = %s, total = %s WHERE product_id = %s AND user_id = %s",
                    (new_quantity, new_total, product_id, user_id)
                )
                flash('La cantidad del producto en el carrito ha sido actualizada', 'success')
            else:
                # Insertar el producto en el carrito
                cur.execute(
                    "INSERT INTO cart (product_id, title, image_path, price, quantity, total, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (product_data['id'], product_data['title'], product_data['image_path'], product_data['price'], quantity, product_data['price'] * quantity, user_id)
                )
            mysql.connection.commit()
            # Actualizar la cantidad del producto en el inventario
            cur.execute("UPDATE product SET quantity = quantity - %s WHERE id = %s", (quantity, product_id))
            mysql.connection.commit()
        else:
            flash('No hay suficiente cantidad disponible de este producto', 'danger')
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
@login_required
def cart():
    if 'id' not in session:
        flash('Necesitas iniciar sesión para ver tu carrito', 'danger')
        return redirect(url_for('login'))

    user_id = session['id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
    cart_items = cur.fetchall()
    cur.close()

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:id>', methods=['POST'])
@login_required
def remove_from_cart(id):
    product_id = id
    quantity = int(request.form.get('quantity', 1))  # Obtener la cantidad del formulario

    # Consultar la base de datos para verificar si el producto está en el carrito
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart WHERE product_id = %s", (product_id,))
    cart_item = cur.fetchone()

    if cart_item:
        # Obtener la cantidad actual en el carrito
        current_quantity = cart_item['quantity']
        
        # Verificar si la cantidad a eliminar es igual a la cantidad en el carrito
        if quantity == current_quantity:
            # Eliminar el producto del carrito en la base de datos
            cur.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
            mysql.connection.commit()

            # Devolver la cantidad eliminada al catálogo
            cur.execute("UPDATE product SET quantity = quantity + %s WHERE id = %s", (quantity, product_id))
            mysql.connection.commit()

            flash('Producto eliminado completamente del carrito', 'success')
        elif quantity < current_quantity:
            # Actualizar la cantidad en el carrito
            cur.execute("UPDATE cart SET quantity = quantity - %s WHERE product_id = %s", (quantity, product_id))
            mysql.connection.commit()

            # Devolver la cantidad eliminada al catálogo
            cur.execute("UPDATE product SET quantity = quantity + %s WHERE id = %s", (quantity, product_id))
            mysql.connection.commit()

            flash('Cantidad de producto eliminada del carrito', 'success')
        else:
            flash('No puedes eliminar más productos de los que tienes en el carrito', 'danger')
    else:
        flash('El producto no está en el carrito', 'danger')

    cur.close()

    return redirect(url_for('cart'))

#----------------------------------- apartar producto 
# Ruta y función para procesar la orden
@app.route('/order_processed', methods=['POST'])
@login_required
def order_processed():
    # Obtener los datos del cliente del formulario
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')

    # Insertar datos del cliente en la tabla 'client'
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO client (nombre, apellidos, telefono, correo) VALUES ( %s, %s, %s, %s)",
                (nombre, apellidos, telefono, correo))
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
                            telefono=telefono,
                            correo=correo,
                            cart_items=cart_items)
    else:
        flash('Error: Carrito vacío', 'danger')
        return redirect(url_for('Home_Catalogo'))


# Ruta y función para mostrar la página de apartado de productos
@app.route('/apartado_produc', methods=['GET'])
@login_required
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
        return redirect(url_for('Home_Catalogo'))

# Ruta y función para limpiar el carrito
@app.route('/limpiar_carrito', methods=['POST'])
@login_required
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
@login_required
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

        return redirect(url_for('Home_Catalogo'))
    return render_template('create_product.html')

# --------------------- borrar productos
@app.route('/products/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    cur = mysql.connection.cursor()

    # Eliminar registros relacionados en la tabla order_detail
    cur.execute("DELETE FROM order_detail WHERE product_id = %s", (id,))
    
    # Obtener el cliente asociado con el producto
    cur.execute("SELECT client_id FROM order_detail WHERE product_id = %s", (id,))
    client_row = cur.fetchone()
    if client_row:
        client_id = client_row[0]
        # Eliminar órdenes asociadas al cliente
        cur.execute("DELETE FROM order_detail WHERE client_id = %s", (client_id,))
        mysql.connection.commit()

        # Eliminar al cliente
        cur.execute("DELETE FROM client WHERE id = %s", (client_id,))
        mysql.connection.commit()

    # Eliminar registros relacionados en la tabla cart
    cur.execute("DELETE FROM cart WHERE product_id = %s", (id,))

    # Eliminar el producto de la tabla product
    cur.execute("DELETE FROM product WHERE id = %s", (id,))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('ver_clientes'))

# ---------------------------- actualizar producto
@app.route('/products/update/<int:id>', methods=['GET', 'POST'])
@login_required
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

        return redirect(url_for('Home_Catalogo'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product WHERE id = %s", (id,))
    product = cur.fetchone()
    cur.close()
    return render_template('update_product.html', product=product)

# ---------------------- boton de activar o descativar
@app.route('/products/activate/<int:id>', methods=['GET', 'POST'])
@login_required
def activate_product(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE product SET active = 1 WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('Home_Catalogo'))

@app.route('/products/deactivate/<int:id>', methods=['GET', 'POST'])
@login_required
def deactivate_product(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE product SET active = 0 WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('Home_Catalogo'))

# ------------ producto
@app.route('/product_actions')
@login_required
def product_actions():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    cur.close()
    return render_template('product_actions.html', products=products)


# --------------------------------------------- editar clientes y detalles del producto
@app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def eliminar_cliente(cliente_id):
    cur = mysql.connection.cursor()

    # Eliminar órdenes asociadas al cliente
    cur.execute("DELETE FROM order_detail WHERE client_id = %s", (cliente_id,))
    mysql.connection.commit()

    # Eliminar al cliente
    cur.execute("DELETE FROM client WHERE id = %s", (cliente_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_clientes'))

# Ruta y función para ver todos los clientes
@app.route('/ver_clientes')
@login_required
def ver_clientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM client")
    clientes = cur.fetchall()
    cur.close()

    return render_template('ver_clientes.html', clientes=clientes)

# Final
if __name__ == "__main__":
    app.run(debug=True)
