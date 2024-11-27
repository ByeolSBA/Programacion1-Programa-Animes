import json
from animeflv import AnimeFLV

class Perfil:
    """Perfil de usuario"""
    def __init__(self, nombre, capitulos=None):
        self.nombre = nombre
        self.capitulos = capitulos if capitulos else []

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "nombre": self.nombre,
            "capitulos": self.capitulos
        }

    @staticmethod
    def from_dict(data):
        return Perfil(data["nombre"], data["capitulos"])

# Método de ordenamiento Shell Sort
def shell_sort(episodes):
    n = len(episodes)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = episodes[i]
            j = i
            while j >= gap and episodes[j - gap].id > temp.id:
                episodes[j] = episodes[j - gap]
                j -= gap
            episodes[j] = temp
        gap //= 2

def buscar_serie(api):
    nombre_serie = input("Escribe el nombre de la serie: ")
    elements = api.search(nombre_serie)

    # Mostrar resultados de la búsqueda
    for i, element in enumerate(elements):
        print(f"{i} - {element.title}")

    try:
        selection = int(input("Selecciona una serie: "))
        return elements[selection].id
    except (IndexError, ValueError):
        print("Selección inválida.")
        return None

def ver_episodios(api, serie_id):
    info = api.get_anime_info(serie_id)
    episodes = info.episodes

    # Ordenar episodios con el metodo shell sort
    shell_sort(episodes)

    # Mostrar episodios ordenados
    for j, episode in enumerate(episodes):
        print(f"{j} | Episodio - {episode.id}")

    try:
        index_episode = int(input("Selecciona el episodio: "))
        capitulo = episodes[index_episode].id
        return api.get_links(serie_id, capitulo)
    except (IndexError, ValueError):
        print("Selección de episodio inválida.")
        return None

def mostrar_enlaces(results):
    if results:
        for result in results:
            print(f"{result.server} {result}")
    else:
        print("No se encontraron enlaces.")

# Guardar perfil en archivo JSON
def guardar_perfil(usuario, capitulos, nombre_archivo="perfiles.json"):
    perfiles = cargar_perfiles(nombre_archivo)
    perfiles[usuario] = capitulos
    with open(nombre_archivo, "w") as archivo:
        json.dump(perfiles, archivo, indent=4)
    print(f"Perfil de {usuario} guardado.")

# Cargar perfiles desde archivo JSON
def cargar_perfiles(nombre_archivo="perfiles.json"):
    try:
        with open(nombre_archivo, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo} no encontrado. Se creará uno nuevo.")
        return {}

# Crear lista de capítulos o series
def gestionar_capitulos(capitulos):
    print("\nLista actual de capítulos o series:")
    for i, capitulo in enumerate(capitulos, start=1):
        print(f"{i}. {capitulo}")

    print("\nOpciones:")
    print("1. Agregar un capítulo o serie")
    print("2. Eliminar un capítulo o serie")
    print("3. Regresar al menú principal")
    
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        nuevo_capitulo = input("Escribe el nombre del nuevo capítulo o serie: ")
        capitulos.append(nuevo_capitulo)
        print(f"'{nuevo_capitulo}' ha sido agregado.")
    elif opcion == "2":
        try:
            index = int(input("Escribe el número del capítulo o serie a eliminar: ")) - 1
            if 0 <= index < len(capitulos):
                eliminado = capitulos.pop(index)
                print(f"'{eliminado}' ha sido eliminado.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")
    elif opcion == "3":
        print("Regresando al menú principal.")
    else:
        print("Opción no válida.")

# Menú interactivo
def menu_principal():
    print("\nMenú principal:")
    print("1. Buscar serie")
    print("2. Gestionar capítulos")
    print("3. Salir")

# Cargar datos desde archivo JSON
def main():
    # Cargar perfiles existentes
    perfiles = cargar_perfiles()

    # Elejir perfil
    if perfiles:
        print("\nPerfiles disponibles:")
        for usuario in perfiles:
            print(f"- {usuario}")
        print("Crear un nuevo perfil (cualquier otra tecla)")
        opcion = input("¿Quieres continuar con un perfil existente o crear uno nuevo? (Escribe 'nuevo' para crear uno nuevo): ").strip().lower()

        if opcion == "nuevo":
            usuario = input("Por favor, ingresa tu nombre: ")
            print(f"¡Bienvenido, {usuario}!")
            capitulos = []  
        else:
            usuario = input("Selecciona el perfil con el que deseas continuar: ").strip()
            if usuario in perfiles:
                capitulos = perfiles[usuario]
                print(f"¡Bienvenido de nuevo, {usuario}!")
            else:
                print("Perfil no encontrado, creando uno nuevo.")
                usuario = input("Por favor, ingresa tu nombre: ")
                print(f"¡Bienvenido, {usuario}!")
                capitulos = []  
    else:
        usuario = input("No se encontraron perfiles, por favor, ingresa tu nombre para crear uno: ")
        print(f"¡Bienvenido, {usuario}!")
        capitulos = []  # 

    # Usar el perfil y su lista de capítulos
    with AnimeFLV() as api:
        while True:
            menu_principal()
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                serie_id = buscar_serie(api)
                if serie_id:
                    results = ver_episodios(api, serie_id)
                    mostrar_enlaces(results)
            elif opcion == "2":
                gestionar_capitulos(capitulos)
            elif opcion == "3":
                # Guardar el perfil antes de salir
                guardar_perfil(usuario, capitulos)
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida.")

if __name__ == "__main__":
    main()
