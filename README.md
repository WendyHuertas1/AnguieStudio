

# My ADSO Project from Otro brazo

In this repository you are going to find the code relative to my adso project...

## Clonar Repositorio

Entra en tu terminal o tu visual estudio code y escribe lo siguiente 

```shell
git clone https://github.com/Dilanss/Project.git
cd Project
```

Ahora ya puedes abrir tu proyecto en visual studio code


### Initialize git

```shell
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Dilanss/Project.git
git push origin main
```


### Añadir origen desde un nuevo proyecto 

coloca el siguiente comando para añadir el proyecto a un origin remoto 
```shell
git remote add origin https://github.com/Dilanss/Project.git
```

>[!IMPORTANT]
>Ten en cuenta que se debe tener un proyecto de git inicializado

### Crear brazos y subir cambios a un brazo

Mira las siguientes instrucciones para crear un brazo, moverse entre el y subir cambios a un determinado brazo:

```shell
git branch otrobrazo
git checkout otrobrazo
```

Ahora editamos algun archivo y hacemos commit a los cambios 
```shell
git add .
git commit -m "commit desde otro brazo"
git push origin otrobrzo
```

Ahora puedes ver los cambios en otro brazo en github
>[!TIP]
>Asegurate de estar en el brazo correcto siempre que estas trabajando y haciendo commits

```shell
# El siguiente comando nos permite ver en que brazo estamos trabajando actualmente
git branch 
```


>[!IMPORTANT]
>Siempre haz commit antes de moverte a otro brazo


### Bajar cambios desde github

```shell
    git pull origin main
```

Se puede cambiar el nombre del brazo dependiendo del brazo del que estoy 
y del brazo del que quiero descargar archivos.

### Comandos que te pueden ayudar

```shell
    git status
    git log --oneline
    git fetch 
    git fetch -a 
    git branch -a
```