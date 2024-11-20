import json
from animeflv import AnimeFLV

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

# Guardar lista en archivo JSON
def guardar_en_json(lista, nombre_archivo="capitulos.json"):
    with open(nombre_archivo, "w") as archivo:
        json.dump(lista, archivo, indent=4)
    print(f"Datos guardados en {nombre_archivo}.")

# Cargar lista desde archivo JSON
def cargar_desde_json(nombre_archivo="capitulos.json"):
    try:
        with open(nombre_archivo, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo} no encontrado. Se creará uno nuevo.")
        return []

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
        guardar_en_json(capitulos)
    elif opcion == "2":
        try:
            index = int(input("Escribe el número del capítulo o serie a eliminar: ")) - 1
            if 0 <= index < len(capitulos):
                eliminado = capitulos.pop(index)
                print(f"'{eliminado}' ha sido eliminado.")
                guardar_en_json(capitulos)
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
    capitulos = cargar_desde_json()

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
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida.")

if __name__ == "__main__":
    main()
