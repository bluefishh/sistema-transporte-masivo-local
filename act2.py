import csv
import heapq
import math
import networkx as nx
import matplotlib.pyplot as plt
import os

# Coordenadas de las estaciones, plano cartesiano 2D
coordenadas = {
    "A": (0, 0),
    "B": (2, 1),
    "C": (1, 3),
    "D": (5, 2),
    "E": (3, 3),
    "F": (2, 5),
    "G": (4, 4),
    "H": (6, 5)
}

# Cargar grafo (es bidireccional)
def cargar_grafo(archivo_csv):
    grafo = {}
    with open(archivo_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            origen = row["origen"]
            destino = row["destino"]
            tiempo = int(row["tiempo"])
            accesible = row["accesible"].lower() == "true"
            congestion = row["congestion"].lower()

            grafo.setdefault(origen, []).append({
                "destino": destino,
                "tiempo": tiempo,
                "accesible": accesible,
                "congestion": congestion
            })
            grafo.setdefault(destino, []).append({
                "destino": origen,
                "tiempo": tiempo,
                "accesible": accesible,
                "congestion": congestion
            })
    return grafo

# Motor de inferencia (reglas)
def costo_transicion(arista, accesibilidad_requerida):
    if accesibilidad_requerida and not arista["accesible"]:
        return None
    factor = {"bajo": 1.0, "medio": 1.3, "alto": 1.6}
    return arista["tiempo"] * factor.get(arista["congestion"], 1.0)

# Función para mostrar detalles del tiempo de viaje
def mostrar_detalles_ruta(grafo, ruta):
    print("\n=== DETALLES DEL TIEMPO DE VIAJE ===")
    tiempo_total = 0
    
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i + 1]
        
        # Buscar la arista correspondiente
        arista_encontrada = None
        for arista in grafo.get(origen, []):
            if arista["destino"] == destino:
                arista_encontrada = arista
                break
        
        if arista_encontrada:
            tiempo_base = arista_encontrada["tiempo"]
            congestion = arista_encontrada["congestion"]
            accesible = arista_encontrada["accesible"]
            
            # Calcular factor de congestión
            factor_congestion = {"bajo": 1.0, "medio": 1.3, "alto": 1.6}
            factor = factor_congestion.get(congestion.lower(), 1.0)
            tiempo_real = tiempo_base * factor
            
            print(f"{origen} → {destino}:")
            print(f"  • Tiempo base: {tiempo_base} min")
            print(f"  • Congestión: {congestion.capitalize()} (factor x{factor})")
            print(f"  • Accesible: {'Sí' if accesible else 'No'}")
            print(f"  • Tiempo real: {tiempo_real:.2f} min")
            print()
            
            tiempo_total += tiempo_real
    
    print(f"TIEMPO TOTAL DEL RECORRIDO: {tiempo_total:.2f} minutos")
    print("=" * 45)

# Heurística
def heuristica(nodo, destino):
    x1, y1 = coordenadas[nodo]
    x2, y2 = coordenadas[destino]
    return math.dist((x1, y1), (x2, y2))

# Algoritmo A*
def a_star_explorar(grafo, inicio, meta, accesibilidad_requerida=False):
    open_list = []
    heapq.heappush(open_list, (heuristica(inicio, meta), 0, inicio, [inicio]))

    visitados = set()
    rutas_exploradas = []

    while open_list:
        f, g, nodo, camino = heapq.heappop(open_list)

        if nodo in visitados:
            continue
        visitados.add(nodo)

        if nodo == meta:
            rutas_exploradas.append((camino, g))

        for arista in grafo.get(nodo, []):
            vecino = arista["destino"]
            if vecino in visitados:
                continue

            costo = costo_transicion(arista, accesibilidad_requerida)
            if costo is None:
                continue

            g_nuevo = g + costo
            f_nuevo = g_nuevo + heuristica(vecino, meta)
            heapq.heappush(open_list, (f_nuevo, g_nuevo, vecino, camino + [vecino]))

    return rutas_exploradas

# Grafo dibujado
def dibujar_grafo(grafo, ruta_optima):
    G = nx.Graph()
    for nodo, vecinos in grafo.items():
        for arista in vecinos:
            G.add_edge(nodo, arista["destino"], weight=arista["tiempo"])

    pos = coordenadas
    plt.figure(figsize=(7, 6))

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

    nx.draw_networkx_edges(G, pos, edge_color="gray")

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if ruta_optima:
        edges_path = list(zip(ruta_optima, ruta_optima[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges_path, edge_color="red", width=3)

    plt.title("MAPA SISTEMA TRANSPORTE MASIVO LOCAL")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    archivo_csv = os.path.join(directorio_script, "datos.csv")
    
    grafo = cargar_grafo(archivo_csv)

    print("##################### SISTEMA TRANSPORTE MASIVO LOCAL #####################")
    inicio = input("Ingrese punto de inicio: ").strip().upper()
    meta = input("Ingrese punto de destino: ").strip().upper()
    accesibilidad = input("¿Necesita tener en cuenta la accesibilidad? (s/n): ").strip().lower() == "s"

    rutas = a_star_explorar(grafo, inicio, meta, accesibilidad)

    if not rutas:
        print("\nNo se encontraron rutas posibles con las condiciones.")
    else:
        rutas.sort(key=lambda x: x[1])
        mejor = rutas[0]

        print("\nMejor ruta encontrada:")
        print(" -> ".join(mejor[0]))
        print("Costo total:", round(mejor[1], 2), "minutos")
        
        # Mostrar detalles del tiempo para la mejor ruta
        mostrar_detalles_ruta(grafo, mejor[0])

        if len(rutas) > 1:
            print("\nOtras rutas posibles diferentes a la dada:")
            for i, (r, c) in enumerate(rutas[1:], 1):
                print(f"\nRuta alternativa {i}:")
                print(" -> ".join(r), "| costo:", round(c, 2), "minutos")
                mostrar_detalles_ruta(grafo, r)

        dibujar_grafo(grafo, mejor[0])
