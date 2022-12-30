Este modulo ofrece un algoritmo para el guardado de informacion en el entorno local, usando archivos "csv".

El programa trabaja con archivos "csv" delimitados por comas.

El programa "main.py" solo trabaja dentro de una carpeta llamada "data_base", por lo cual si se lo saca, o modifica el nombre de la misma
habra un error en la ruta de los metodos y funciones.

Cada base de datos creada sera la instancia de la clase llamada "Data_Base", a la cual se le debera pasar en los argumentos un nombre y usando
validación de la siguiente manera "app = Data_Base(nombre = "nombre", validacion = "validacion"). la validacion es un segundo argumento 
obligatorio que sirve para armar sub-clases y poder manejar diferentes bases de datos con mismos nombres. aunque se puede poner mas argumentos
estos no seran usados, no es recomendable.

Para crear una tabla, asosiada a una base de datos, debera usarse el metodo: "db.crear_tabla()", el cual recibe dos argumentos

    1) nombre = "nombre", el cual sera el nombre de la base de datos.
    2) list_head = [], una lista que debera tener elementos tipo str, en la cual cada elemento representa la cabecera de cada columna de csv.
        el mismo no podra estar vacio.

Para agregar filas a una tabla de la base de datos existen dos metodos, similares pero con una distincion entre ellos.

    1) db.agregar_datos_estatico() el cual agregara una fila a la tabla de la base de datos una unica vez al ejecutar el programa y luego por
        más que el programa se vuelva a ejecutar, no volvera a agregar más lineas a la tabla. su declaracion es acumulativa, lo que quiere 
        decir que se agregaran dos lineas con este metodo solo si hay dos llamadas al metodo.

    2) db.agregar_datos() cumple la misma funcion que el anterior metodo, pero este; a diferencia; si agrega una fila al csv por cada ejecucion
        del programa
    
    los parametros de estas dos funciones son iguales y son los siguientes:

        1) nombre = "nombre" que sera el nombre de la tabla de la base de datos en la que se quiere agregar la fila.
        2) lista = [] una lista que contendra las columans de la fila a agregar, donde cada elemento de la lista corresponde a cada columna.

Para actualizar los datos en una casilla del csv se usa el metodo bd.actualizar() el cual acepta los siguientes parametros:

    1) nombre = "nombre" que es el nombre de la tabla a actualizar los datos.
    2) actualizacion = ["fila", "columna", "nuevo_valor"], "fila" es la posicion de vertical de la casilla y empieza desde 1 sin 
        contar la linea head. 

Para un retorno de los datos en el csv hay dos opciones:

    1) la propia funcion incorporada "leer()" que acepta como parametro el nombre del archivo csv y devuelve una lista con sus filas.
    2) el metodo bd.consultar_datos() el cual tiene dos parametros de entrada:

        1) nombre = "nombre" de la lista a retornar sus filas.
        2) modo = ["modo", "fila", "columna"]. "modo" es el parametro que indica el modo de retorno de datos:

            1) modo "casilla": retorna el valor de una casilla, incluida las cabeceras. en este modo es obligatorio especificar la fila y
                la columna de la casilla, contando 1 desde la fila cabecera.
            2) modo "completo", solo hace falta pasarle a la lista el elemento modo y retornara todas las lineas del csv en cuestion.

Para borrar una tabla se usa el metodo bd.borrar_tabla(), el cual recive el nombre de la tabla como parametro "nombre = "nombre""

Para borrar una base de datos se usa la funcion bd.borrar_bd() la cual recive como parametro el nombre de la base de datos "nombre = "nombre""


********************************************************************************************************************************************************************************
                                                            ACTUALIZACION
********************************************************************************************************************************************************************************

1) se agregaron mejoras en el manejo de excepciones:

    -se agrego mas y nuevas excepciones

2) se arreglo el metodo "db.crear_lista()"

3) se agrego el metodo "db.eliminar_linea()", el cual recive dos argumentos:

    1) nombre = "nombre_tabla"
    2) fila = "desde-hacia", si solo se quiere borrar una linea, ingrese un solo numero respectivo sin el guion.

********************************************************************************************************************************************************************************
                                                            Interface
********************************************************************************************************************************************************************************

La interface grafica se encuentra en la carpeta "APP", con el nombre de "app_bd.py", la cual proporciona una mirada mas cofortable de la informacion de las tablas.

Tambien ofrece la posibilidad de hacer una conversion de .csv a .pdf o .xslx, pudiendo guardar el archivo de forma local o exportarlo via mail (gmail).

A la vez desde la interface se puede tanto agregar, eliminar o modificar elementos de la base de datos.
