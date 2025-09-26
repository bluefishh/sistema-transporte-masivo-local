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

# Instrucciones de Uso
1. Clonar el repositorio.
2. Instalar las dependencias:
   ```bash
   pip install networkx matplotlib
   ```
3. Ejecutar el script principal:
   ```bash
   python act2.py
   ```
4. Seguir las instrucciones en pantalla para ingresar los puntos de inicio y destino.
5. Visualizar el grafo y el camino óptimo encontrado.
6. Revisar el archivo `act2.py` para entender la implementación del algoritmo A* y cómo se modela el sistema de transporte.