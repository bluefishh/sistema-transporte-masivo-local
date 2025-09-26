# Mapa del Sistema de Transporte Masivo Local

Este proyecto modela un sistema de transporte masivo local utilizando grafos, donde los puntos representan estaciones y las conexiones (aristas) incluyen tiempos de viaje, accesibilidad y reglas de congestión.

## Características

- **Algoritmo A\***: Implementación del algoritmo A* con heurística dinámica basada en la distancia euclidiana (coordenadas 2D en x e y) deducidas con el teorema de Pitágoras, se hace através de la librería `matplotlib`.
- **Visualización**: Utiliza `networkx` y `matplotlib` para representar gráficamente el sistema de transporte.
- **Reglas**: Considera tiempos, accesibilidad y congestión en las conexiones.

## Requisitos

- [networkx](https://networkx.org/)
- [matplotlib](https://matplotlib.org/)
- Python 3.x