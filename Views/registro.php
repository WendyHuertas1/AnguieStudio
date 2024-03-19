<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="./IMG/Logo.png" rel="icon">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="../css/style.css">
    <title>Formulario de registro</title>
</head>
<body id="Registro">
    <div class="container-form">
        <div class="form-information">
            <div class="form-information-childs">
                <h2>Crear una Cuenta</h2>
                <div class="icons">
                    <i class='bx bxl-google'></i>
                    <i class='bx bxl-instagram'></i>
                </div>
                <form class="form" method="POST" action="../rolcliente.php">
                    <label>
                        <i class='bx bx-user'></i>
                        <input type="text" placeholder="Nombres" name="Nombre" class="Nombre" required>
                    </label>
                    <label>
                        <i class='bx bx-user'></i>
                        <input type="text" placeholder="Apellidos" name="Apellido" class="Apellido" required>
                    </label>
                    <label>
                        <i class='bx bx-user'></i>
                        <input type="number" placeholder="Numero de documento" name="Cedula" class="Cedula" required>
                    </label>
                    <label>
                        <i class='bx bx-phone'class='bx bx-envelope'></i>
                        <input type="number" placeholder="Telefono" name="Telefono" class="Telefono" required>
                    </label>
                    <label>
                        <i class='bx bx-envelope'></i>
                        <input type="email" placeholder="Correo electronico" name="Correo" class="Correo" required>
                    </label>
                    <label>
                        <i class='bx bx-lock'></i>
                        <input type="password" placeholder="Contraseña" name="password" class="password" required>
                    </label>
                    <button type="submit" class="btn btn-primary" name="btnsubmit" value="ok" id="boton">Registrar</button>
                </form>
            </div>
        </div>
        <div class="information">
            <div class="info-childs">
                <h2>Bienvenido</h2>
                <p>
                    Para ser beneficiario de nuestros servicios te invitamos a registrarte.
                </p>
                <a href="./Login.html"><input type="button" value="Inicio de sesión"></a>
            </div>
        </div>
    </div>
    <button id="volver"> <a href="../index.html">Volver</a></button>
</body>
</html>
