import datetime
####################################################################################################################
def propietarios():
    nombre_archivo = "propietario.txt"
    separador = ";"
    propietarios = {}
    with open(nombre_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            codpropietario = columnas[0]
            codmembresia = columnas[2]
            valores = [columna.strip() for columna in columnas[1:] if columna.strip()]
            codmembresia_repetido = False
            for prop in propietarios.values():
                if prop["codmembresia"] == codmembresia:
                    codmembresia_repetido = True
                    break
            if codpropietario not in propietarios and valores and not codmembresia_repetido:
                propietarios[codpropietario] = {"nombrepro": valores[0], "codmembresia": valores[1], "activo": valores[2]}
    return propietarios
####################################################################################################################
def administradores():
    nombre_archivo = "administrador.txt"
    separador = ";"
    administradores = {}
    with open(nombre_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            if len(columnas)>1:
                codadmin = columnas[0]
                valores = [columna.strip() for columna in columnas[1:] if columna.strip()]
                if codadmin not in administradores and valores:
                    administradores[codadmin] = {"nombreadmin": valores[0]}
    return administradores
####################################################################################################################
def canciones():
    nombre_archivo = "canciones.txt"
    separador = ";"
    canciones = {}
    with open(nombre_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            codcancion = columnas[0]
            valores = [columna.strip() for columna in columnas[1:] if columna.strip()]
            if codcancion not in canciones and valores:
                canciones[codcancion] = {"nombrecan": valores[0], "codart": valores[1], "codalbum": valores[2],"codgenero": valores[3],"codplaylist": valores[4]}
    return canciones
####################################################################################################################
def playlist():
    nombre_archivo = "playlist.txt"
    separador = ";"
    playlist = {}
    with open(nombre_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            codplaylist = columnas[0]
            valores = [columna.strip() for columna in columnas[1:] if columna.strip()]
            if codplaylist not in playlist and valores:
                playlist[codplaylist] = {"nombreplay": valores[0],"codpropietario": valores[1]}
    return playlist
####################################################################################################################
def album():
    nombre_archivo = "albumes.txt"
    separador = ";"
    albumes = {}
    with open(nombre_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            codalbum = columnas[0]
            valores = [columna.strip() for columna in columnas[1:] if columna.strip()]
            if codalbum not in albumes and valores:
                albumes[codalbum] = {"nombrealbum": valores[0], "codart": valores[1]}
    return albumes
####################################################################################################################
def artistas():
    nombre_archivo = "artista.txt"
    separador = ";"
    artistas = {}
    with open(nombre_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            codartista = columnas[0]
            valores = [columna.strip() for columna in columnas[1:] if columna.strip()]
            if codartista not in artistas and valores:
                artistas[codartista] = {"nombreart": valores[0],"codgenero": valores[1]}
    return artistas
####################################################################################################################
def genero():
    nombre_archivo = "genero.txt"
    separador = ";"
    generos = {}
    with open(nombre_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            codgenero = columnas[0]
            valores = [columna.strip() for columna in columnas[1:] if columna.strip()]
            if codgenero not in generos and valores:
                generos[codgenero] = {"nombregen": valores[0]}
    return generos
####################################################################################################################
