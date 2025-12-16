import numpy as np
import heapq
from PIL import Image

def load_image_and_grayscale(path):
    """
    Charge une image et la convertit en un tableau NumPy 2D (niveaux de gris).
    """
    try:
        img = Image.open(path).convert('L')  # Convert to grayscale
        return np.array(img)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        return None

def build_graph(image_array):
    """
    Construit la représentation du graphe (dictionnaire d'adjacence) à partir du tableau NumPy.
    Les sommets sont les tuples (i, j).
    Les arêtes connectent les 4 voisins.
    Poids = |I(u) - I(v)|.
    """
    rows, cols = image_array.shape
    graph = {}
    
    for r in range(rows):
        for c in range(cols):
            u = (r, c)
            neighbors = []
            
            # Directions: Haut, Bas, Gauche, Droite
            deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for dr, dc in deltas:
                nr, nc = r + dr, c + dc
                
                # Vérifier les limites de l'image
                if 0 <= nr < rows and 0 <= nc < cols:
                    v = (nr, nc)
                    # Poids = différence absolue d'intensité
                    weight = abs(int(image_array[r, c]) - int(image_array[nr, nc]))
                    neighbors.append((v, weight))
            
            graph[u] = neighbors
            
    print(graph)  
    return graph

def dijkstra_shortest_path(graph, start_coords, end_coords):
    """
    Implémente l'algorithme de Dijkstra.
    Retourne la liste des coordonnées du chemin le plus court et la distance totale.
    """
    # File de priorité : (distance, sommet_courant)
    pq = [(0, start_coords)]
    
    # Distances minimales trouvées
    distances = {node: float('inf') for node in graph}
    distances[start_coords] = 0
    
    # Pour reconstruire le chemin : predecessors[v] = u
    predecessors = {node: None for node in graph}
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_node == end_coords:
            break
        
        if current_dist > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstruction du chemin
    path = []
    node = end_coords
    
    if distances[end_coords] == float('inf'):
        print("Aucun chemin trouvé.")
        return [], float('inf')
        
    while node is not None:
        path.append(node)
        node = predecessors[node]
    
    path.reverse()
    return path, distances[end_coords]
