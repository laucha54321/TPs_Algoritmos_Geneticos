import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import random
from typing import List, Tuple

# ==================== DATOS DE LAS CAPITALES ====================
CAPITALES = {
    0: "Ciudad de Buenos Aires",
    1: "Córdoba",
    2: "Corrientes",
    3: "Formosa",
    4: "La Plata",
    5: "La Rioja",
    6: "Mendoza",
    7: "Neuquén",
    8: "Paraná",
    9: "Posadas",
    10: "Rawson",
    11: "Resistencia",
    12: "Río Gallegos",
    13: "S.F.d V.d. Catamarca",
    14: "S.M. de Tucumán",
    15: "S.S. de Jujuy",
    16: "Salta",
    17: "San Juan",
    18: "San Luis",
    19: "Santa Fe",
    20: "Santa Rosa",
    21: "Sgo. Del Estero",
    22: "Ushuaia",
    23: "Viedma"
}

# Coordenadas aproximadas (latitud, longitud) para visualización
COORDENADAS = {
    0: (-34.6037, -58.3816),   # CABA
    1: (-31.4201, -64.1888),   # Córdoba
    2: (-27.4806, -58.8341),   # Corrientes
    3: (-26.1775, -58.1781),   # Formosa
    4: (-34.9215, -57.9545),   # La Plata
    5: (-29.4131, -66.8558),   # La Rioja
    6: (-32.8895, -68.8458),   # Mendoza
    7: (-38.9516, -68.0591),   # Neuquén
    8: (-31.7333, -60.5297),   # Paraná
    9: (-27.3671, -55.8961),   # Posadas
    10: (-43.3002, -65.1023),  # Rawson
    11: (-27.4514, -58.9867),  # Resistencia
    12: (-51.6230, -69.2168),  # Río Gallegos
    13: (-28.4696, -65.7795),  # Catamarca
    14: (-26.8083, -65.2176),  # Tucumán
    15: (-24.1858, -65.2995),  # Jujuy
    16: (-24.7821, -65.4232),  # Salta
    17: (-31.5375, -68.5364),  # San Juan
    18: (-33.2950, -66.3356),  # San Luis
    19: (-31.6333, -60.7000),  # Santa Fe
    20: (-36.6197, -64.2895),  # Santa Rosa
    21: (-27.7834, -64.2642),  # Santiago del Estero
    22: (-54.8019, -68.3030),  # Ushuaia
    23: (-40.8119, -62.9962)   #Viedma
}

# ==================== MATRIZ DE DISTANCIAS REAL ====================
# Matriz proporcionada por el usuario (en kilómetros)
MATRIZ_DISTANCIAS = np.array([
    [0, 646, 792, 933, 53, 986, 985, 989, 375, 834, 1127, 794, 2082, 979, 1080, 1334, 1282, 1005, 749, 393, 579, 939, 2373, 799],
    [646, 0, 677, 824, 698, 340, 466, 907, 348, 919, 1321, 669, 2281, 362, 517, 809, 745, 412, 293, 330, 577, 401, 2618, 1047],
    [792, 677, 0, 157, 830, 814, 1131, 1534, 500, 291, 1845, 13, 2819, 691, 633, 742, 719, 1039, 969, 498, 1136, 535, 3131, 1527],
    [933, 824, 157, 0, 968, 927, 1269, 1690, 656, 263, 1999, 161, 2974, 793, 703, 750, 741, 1169, 1117, 654, 1293, 629, 3284, 1681],
    [53, 698, 830, 968, 0, 1038, 1029, 1005, 427, 857, 1116, 833, 2064, 1030, 1132, 1385, 1333, 1053, 795, 444, 602, 991, 2350, 789],
    [986, 340, 814, 927, 1038, 0, 427, 1063, 659, 1098, 1548, 802, 2473, 149, 330, 600, 533, 283, 435, 640, 834, 311, 2821, 1311],
    [985, 466, 1131, 1269, 1029, 427, 0, 676, 790, 1384, 1201, 1121, 2081, 569, 756, 1023, 957, 152, 235, 775, 586, 713, 2435, 1019],
    [989, 907, 1534, 1690, 1005, 1063, 676, 0, 1053, 1709, 543, 1529, 1410, 1182, 1370, 1658, 1591, 824, 643, 1049, 422, 1286, 1762, 479],
    [375, 348, 500, 656, 427, 659, 790, 1053, 0, 658, 1345, 498, 2320, 622, 707, 959, 906, 757, 574, 19, 642, 566, 2635, 1030],
    [834, 919, 291, 263, 857, 1098, 1384, 1709, 658, 0, 1851, 305, 2914, 980, 924, 1007, 992, 1306, 1200, 664, 1293, 827, 3207, 1624],
    [1127, 1321, 1845, 1999, 1116, 1548, 1201, 543, 1345, 1951, 0, 1843, 975, 1647, 1827, 2120, 2054, 1340, 1113, 1349, 745, 1721, 1300, 327],
    [794, 669, 13, 161, 833, 802, 1121, 1529, 498, 305, 1843, 0, 2818, 678, 620, 729, 706, 1029, 961, 495, 1132, 523, 3130, 1526],
    [2082, 2281, 2819, 2974, 2064, 2473, 2081, 1410, 2320, 2914, 975, 2818, 0, 2587, 2773, 3063, 2997, 2231, 2046, 2325, 1712, 2677, 359, 1294],
    [979, 362, 691, 793, 1030, 149, 569, 1182, 622, 980, 1647, 678, 2587, 0, 189, 477, 410, 430, 540, 602, 915, 166, 2931, 1391],
    [1080, 517, 633, 703, 1132, 330, 756, 1370, 707, 924, 1827, 620, 2773, 189, 0, 293, 228, 612, 727, 689, 1088, 141, 3116, 1562],
    [1334, 809, 742, 750, 1385, 600, 1023, 1658, 959, 1007, 2120, 729, 3063, 477, 293, 0, 67, 874, 1017, 942, 1382, 414, 3408, 1855],
    [1282, 745, 719, 741, 1333, 533, 957, 1591, 906, 992, 2054, 706, 2997, 410, 228, 67, 0, 808, 950, 889, 1316, 353, 3341, 1790],
    [1005, 412, 1039, 1169, 1053, 283, 152, 824, 757, 1306, 1340, 1029, 2231, 430, 612, 874, 808, 0, 284, 740, 686, 583, 2585, 1141],
    [749, 293, 969, 1117, 795, 435, 235, 643, 574, 1200, 1113, 961, 2046, 540, 727, 1017, 950, 284, 0, 560, 412, 643, 2392, 882],
    [393, 330, 498, 654, 444, 640, 775, 1049, 19, 664, 1349, 495, 2325, 602, 689, 942, 889, 740, 560, 0, 641, 547, 2641, 1035],
    [579, 577, 1136, 1293, 602, 834, 586, 422, 642, 1293, 745, 1132, 1712, 915, 1088, 1382, 1316, 686, 412, 641, 0, 977, 2044, 477],
    [939, 401, 535, 629, 991, 311, 713, 1286, 566, 827, 1721, 523, 2677, 166, 141, 414, 353, 583, 643, 547, 977, 0, 3016, 1446],
    [2373, 2618, 3131, 3284, 2350, 2821, 2435, 1762, 2635, 3207, 1300, 3130, 359, 2931, 3116, 3408, 3341, 2585, 2392, 2641, 2044, 3016, 0, 1605],
    [799, 1047, 1527, 1681, 789, 1311, 1019, 479, 1030, 1624, 327, 1526, 1294, 1391, 1562, 1855, 1790, 1141, 882, 1035,	477, 1446, 1605, 0]
])

# ==================== FUNCIONES AUXILIARES ====================
def calcular_distancia_total(ruta: List[int]) -> float:
    """Calcula la distancia total de una ruta (incluyendo regreso)"""
    distancia = 0
    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % len(ruta)]
        distancia += MATRIZ_DISTANCIAS[ciudad_actual][ciudad_siguiente]
    return distancia

def mostrar_ruta(ruta: List[int], distancia: float, titulo: str = "Ruta"):
    """Muestra la información de una ruta"""
    print(f"\n{'='*70}")
    print(f"{titulo}")
    print(f"{'='*70}")
    print(f"Ciudad de partida: {CAPITALES[ruta[0]]}")
    print(f"\nRecorrido completo:")
    for i, ciudad_id in enumerate(ruta, 1):
        print(f"  {i:2d}. {CAPITALES[ciudad_id]}")
    print(f"  {len(ruta)+1:2d}. {CAPITALES[ruta[0]]} (regreso)")
    print(f"\nDistancia total: {distancia:.2f} km")
    print(f"{'='*70}\n")

# ==================== HEURÍSTICA: VECINO MÁS CERCANO ====================
def vecino_mas_cercano(ciudad_inicio: int) -> Tuple[List[int], float]:
    """
    Implementa la heurística del vecino más cercano
    Desde cada ciudad va a la ciudad más cercana no visitada
    """
    n = len(CAPITALES)
    visitadas = [False] * n
    ruta = [ciudad_inicio]
    visitadas[ciudad_inicio] = True
    ciudad_actual = ciudad_inicio
    
    # Visitar todas las ciudades
    for _ in range(n - 1):
        distancia_minima = float('inf')
        ciudad_mas_cercana = -1
        
        # Buscar la ciudad más cercana no visitada
        for ciudad in range(n):
            if not visitadas[ciudad]:
                distancia = MATRIZ_DISTANCIAS[ciudad_actual][ciudad]
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    ciudad_mas_cercana = ciudad
        
        ruta.append(ciudad_mas_cercana)
        visitadas[ciudad_mas_cercana] = True
        ciudad_actual = ciudad_mas_cercana
    
    distancia_total = calcular_distancia_total(ruta)
    return ruta, distancia_total

def mejor_vecino_mas_cercano() -> Tuple[List[int], float, int]:
    """
    Prueba la heurística desde todas las ciudades y retorna la mejor
    """
    mejor_ruta = None
    mejor_distancia = float('inf')
    mejor_inicio = 0
    
    for ciudad_inicio in range(len(CAPITALES)):
        ruta, distancia = vecino_mas_cercano(ciudad_inicio)
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_ruta = ruta
            mejor_inicio = ciudad_inicio
    
    return mejor_ruta, mejor_distancia, mejor_inicio

# ==================== ALGORITMO GENÉTICO ====================
class AlgoritmoGenetico:
    def __init__(self, tam_poblacion=50, num_generaciones=200, 
                 prob_crossover=0.8, prob_mutacion=0.2):
        self.tam_poblacion = tam_poblacion
        self.num_generaciones = num_generaciones
        self.prob_crossover = prob_crossover
        self.prob_mutacion = prob_mutacion
        self.num_ciudades = len(CAPITALES)
        self.mejor_ruta_historia = []
        
    def crear_individuo(self) -> List[int]:
        """Crea un cromosoma (permutación aleatoria de ciudades)"""
        individuo = list(range(self.num_ciudades))
        random.shuffle(individuo)
        return individuo
    
    def crear_poblacion_inicial(self) -> List[List[int]]:
        """Crea la población inicial de cromosomas"""
        return [self.crear_individuo() for _ in range(self.tam_poblacion)]
    
    def fitness(self, individuo: List[int]) -> float:
        """
        Calcula el fitness de un individuo
        Mayor fitness = mejor (inverso de la distancia)
        """
        distancia = calcular_distancia_total(individuo)
        return 1 / distancia if distancia > 0 else 0
    
    def seleccion_torneo(self, poblacion: List[List[int]], k=3) -> List[int]:
        """Selección por torneo"""
        torneo = random.sample(poblacion, k)
        return max(torneo, key=self.fitness)
    
    def crossover_ciclico(self, padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Implementa crossover cíclico (Cycle Crossover - CX)
        Preserva la posición de los genes de los padres
        """
        n = len(padre1)
        hijo1 = [-1] * n
        hijo2 = [-1] * n
        
        # Encontrar ciclos
        visitados = [False] * n
        es_ciclo_par = True
        
        for inicio in range(n):
            if not visitados[inicio]:
                # Comenzar un nuevo ciclo
                indice = inicio
                ciclo = []
                
                while not visitados[indice]:
                    visitados[indice] = True
                    ciclo.append(indice)
                    # Buscar el valor de padre1[indice] en padre2
                    valor = padre1[indice]
                    indice = padre2.index(valor)
                
                # Alternar entre padres para cada ciclo
                if es_ciclo_par:
                    for idx in ciclo:
                        hijo1[idx] = padre1[idx]
                        hijo2[idx] = padre2[idx]
                else:
                    for idx in ciclo:
                        hijo1[idx] = padre2[idx]
                        hijo2[idx] = padre1[idx]
                
                es_ciclo_par = not es_ciclo_par
        
        return hijo1, hijo2
    
    def mutacion_swap(self, individuo: List[int]) -> List[int]:
        """Mutación por intercambio de dos genes"""
        if random.random() < self.prob_mutacion:
            individuo = individuo.copy()
            i, j = random.sample(range(len(individuo)), 2)
            individuo[i], individuo[j] = individuo[j], individuo[i]
        return individuo
    
    def mutacion_inversion(self, individuo: List[int]) -> List[int]:
        """Mutación por inversión de un segmento"""
        if random.random() < self.prob_mutacion:
            individuo = individuo.copy()
            i, j = sorted(random.sample(range(len(individuo)), 2))
            individuo[i:j+1] = reversed(individuo[i:j+1])
        return individuo
    
    def evolucionar(self) -> Tuple[List[int], float]:
        """Ejecuta el algoritmo genético completo"""
        print(f"\n{'='*70}")
        print("INICIANDO ALGORITMO GENÉTICO")
        print(f"{'='*70}")
        print(f"Parámetros:")
        print(f"  - Tamaño de población: {self.tam_poblacion}")
        print(f"  - Número de generaciones: {self.num_generaciones}")
        print(f"  - Probabilidad de crossover: {self.prob_crossover}")
        print(f"  - Probabilidad de mutación: {self.prob_mutacion}")
        print(f"{'='*70}\n")
        
        # Crear población inicial
        poblacion = self.crear_poblacion_inicial()
        self.mejor_ruta_historia = []
        
        for generacion in range(self.num_generaciones):
            # Evaluar población
            fitness_poblacion = [(ind, self.fitness(ind)) for ind in poblacion]
            fitness_poblacion.sort(key=lambda x: x[1], reverse=True)
            
            # Guardar mejor individuo
            mejor_individuo = fitness_poblacion[0][0]
            mejor_distancia = calcular_distancia_total(mejor_individuo)
            self.mejor_ruta_historia.append(mejor_distancia)
            
            # Mostrar progreso cada 20 generaciones
            if (generacion + 1) % 20 == 0 or generacion == 0:
                print(f"Generación {generacion + 1:3d}: Mejor distancia = {mejor_distancia:.2f} km")
            
            # Crear nueva población
            nueva_poblacion = []
            
            # Elitismo: mantener los mejores 2 individuos
            nueva_poblacion.extend([fitness_poblacion[0][0], fitness_poblacion[1][0]])
            
            # Generar resto de la población
            while len(nueva_poblacion) < self.tam_poblacion:
                # Selección
                padre1 = self.seleccion_torneo(poblacion)
                padre2 = self.seleccion_torneo(poblacion)
                
                # Crossover
                if random.random() < self.prob_crossover:
                    hijo1, hijo2 = self.crossover_ciclico(padre1, padre2)
                else:
                    hijo1, hijo2 = padre1.copy(), padre2.copy()
                
                # Mutación (alternando entre swap e inversión)
                hijo1 = self.mutacion_swap(hijo1)
                hijo2 = self.mutacion_inversion(hijo2)
                
                nueva_poblacion.extend([hijo1, hijo2])
            
            # Recortar si excede el tamaño
            poblacion = nueva_poblacion[:self.tam_poblacion]
        
        # Retornar mejor solución final
        fitness_final = [(ind, self.fitness(ind)) for ind in poblacion]
        fitness_final.sort(key=lambda x: x[1], reverse=True)
        mejor_final = fitness_final[0][0]
        distancia_final = calcular_distancia_total(mejor_final)
        
        print(f"\n{'='*70}")
        print(f"ALGORITMO GENÉTICO FINALIZADO")
        print(f"{'='*70}\n")
        
        return mejor_final, distancia_final

# ==================== VISUALIZACIÓN MEJORADA ====================
def visualizar_ruta(ruta: List[int], titulo: str = "Ruta TSP", figsize=(28, 9),
                    guardar=None, mostrar_regreso=True) -> List[str]:
    """
    Visualiza la ruta del TSP en un mapa proporcional.
    Muestra la leyenda fuera del mapa (más espaciada) y agrega el recorrido numerado.
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Colores y estilos
    color_linea = '#2E86AB'
    color_punto = '#A23B72'
    color_inicio = '#F18F01'
    color_texto = '#333333'

    # Obtener coordenadas
    lons, lats = [], []
    for i in range(len(ruta)):
        lat, lon = COORDENADAS[ruta[i]]
        lats.append(lat)
        lons.append(lon)
    # incluir el regreso para los límites
    lat0, lon0 = COORDENADAS[ruta[0]]
    lats.append(lat0)
    lons.append(lon0)

    # Dibujar líneas con flechas
    for i in range(len(ruta)):
        ciudad1 = ruta[i]
        ciudad2 = ruta[(i + 1) % len(ruta)]
        lat1, lon1 = COORDENADAS[ciudad1]
        lat2, lon2 = COORDENADAS[ciudad2]

        # Línea
        ax.plot([lon1, lon2], [lat1, lat2], color=color_linea,
                linewidth=1.8, alpha=0.7, zorder=1)

        # Flecha
        mid_lon = (lon1 + lon2) / 2
        mid_lat = (lat1 + lat2) / 2
        dx = lon2 - lon1
        dy = lat2 - lat1
        arrow = FancyArrowPatch((mid_lon - dx*0.09, mid_lat - dy*0.09),
                               (mid_lon + dx*0.09, mid_lat + dy*0.09),
                               arrowstyle='->', mutation_scale=14,
                               color=color_linea, linewidth=1.6,
                               alpha=0.9, zorder=2)
        ax.add_patch(arrow)

    # Dibujar ciudades y etiquetas
    for idx, ciudad_id in enumerate(ruta):
        lat, lon = COORDENADAS[ciudad_id]
        if idx == 0:
            ax.plot(lon, lat, marker='*', color=color_inicio,
                    markersize=18, zorder=5, markeredgecolor='white', markeredgewidth=1.8)
        else:
            ax.plot(lon, lat, 'o', color=color_punto,
                    markersize=9, zorder=5, markeredgecolor='white', markeredgewidth=1)

        nombre_corto = CAPITALES[ciudad_id].replace("S.F.d V.d. ", "").replace("S.M. de ", "").replace("S.S. de ", "")
        texto = f'[{idx+1}] {nombre_corto}'
        ax.text(lon, lat, texto, fontsize=8, fontweight='bold',
                color=color_texto, ha='left', va='bottom', zorder=6,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                          edgecolor='gray', alpha=0.85))

    # Ajustar proporciones del mapa
    lon_min, lon_max = min(lons), max(lons)
    lat_min, lat_max = min(lats), max(lats)
    pad_lon = (lon_max - lon_min) * 0.12
    pad_lat = (lat_max - lat_min) * 0.12
    ax.set_xlim(lon_min - pad_lon, lon_max + pad_lon)
    ax.set_ylim(lat_min - pad_lat, lat_max + pad_lat)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.25, linestyle='--')

    # Títulos
    ax.set_xlabel('Longitud', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitud', fontsize=12, fontweight='bold')
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=12)

    # Leyenda (más separada horizontalmente del mapa)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='*', color='w', markerfacecolor=color_inicio,
               markersize=12, label='Inicio/Fin', markeredgecolor='white', markeredgewidth=1.5),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_punto,
               markersize=8, label='Ciudades intermedias', markeredgecolor='white', markeredgewidth=1),
        Line2D([0], [0], color=color_linea, linewidth=1.8, label='Recorrido')
    ]

    # bbox_to_anchor define el desplazamiento (x, y): cuanto mayor sea x, más lejos del gráfico
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.18, 1),
              fontsize=10, framealpha=0.9, borderaxespad=0.)

    # Crear lista de recorrido
    lista_capitales = [CAPITALES[i] for i in ruta]
    if mostrar_regreso:
        lista_capitales.append(CAPITALES[ruta[0]])

    # Texto del recorrido dentro del gráfico (debajo de la leyenda, más espaciado)
    recorrido_texto = "Recorrido:\n" + "\n".join(
        [f"{i+1}. {nombre}" for i, nombre in enumerate(lista_capitales)]
    )
    plt.text(1.18, 0.02, recorrido_texto, transform=ax.transAxes,
             fontsize=9, va='bottom', ha='left',
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9),
             fontweight='bold')

    # Ajustar espacio (reservar más a la derecha para las leyendas)
    plt.tight_layout()
    plt.subplots_adjust(right=0.72)

    # Guardar si se pidió
    if guardar:
        plt.savefig(guardar, dpi=200, bbox_inches='tight')

    plt.show()


def graficar_convergencia(historia: List[float]):
    """Grafica la evolución del algoritmo genético"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    generaciones = list(range(1, len(historia) + 1))
    
    ax.plot(generaciones, historia, linewidth=2.5, color='#2E86AB')
    ax.fill_between(generaciones, historia, alpha=0.3, color='#2E86AB')
    
    # Marcar mejor valor
    mejor_gen = historia.index(min(historia)) + 1
    mejor_dist = min(historia)
    ax.plot(mejor_gen, mejor_dist, 'r*', markersize=20, 
            label=f'Mejor: {mejor_dist:.2f} km (Gen. {mejor_gen})',
            markeredgecolor='white', markeredgewidth=2)
    
    ax.set_xlabel('Generación', fontsize=13, fontweight='bold')
    ax.set_ylabel('Distancia (km)', fontsize=13, fontweight='bold')
    ax.set_title('Convergencia del Algoritmo Genético', 
                fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, loc='upper right')
    
    plt.tight_layout()
    plt.show()

# ==================== MENÚ PRINCIPAL ====================
def mostrar_menu():
    """Muestra el menú principal"""
    print(f"\n{'='*70}")
    print(" PROBLEMA DEL VIAJANTE - CAPITALES DE ARGENTINA")
    print(f"{'='*70}")
    print("a) Vecino más cercano desde una provincia específica")
    print("b) Mejor vecino más cercano (probar todas las provincias)")
    print("c) Algoritmo Genético")
    print("d) Comparar todos los métodos")
    print("e) Mostrar matriz de distancias")
    print("s) Salir")
    print(f"{'='*70}")

def listar_provincias():
    """Lista todas las provincias disponibles"""
    print(f"\n{'='*70}")
    print("CAPITALES DE PROVINCIAS ARGENTINAS")
    print(f"{'='*70}")
    for i in range(0, len(CAPITALES), 2):
        if i + 1 < len(CAPITALES):
            print(f"{i:2d}. {CAPITALES[i]:30s}  {i+1:2d}. {CAPITALES[i+1]}")
        else:
            print(f"{i:2d}. {CAPITALES[i]}")
    print(f"{'='*70}\n")

def menu_principal():
    """Función principal con menú interactivo"""
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip().lower()
        
        if opcion == 'a':
            listar_provincias()
            try:
                ciudad = int(input("Ingrese el número de la ciudad de inicio (0-23): "))
                if 0 <= ciudad < len(CAPITALES):
                    print(f"\nCalculando ruta desde {CAPITALES[ciudad]}...")
                    ruta, distancia = vecino_mas_cercano(ciudad)
                    mostrar_ruta(ruta, distancia, 
                               f"HEURÍSTICA: VECINO MÁS CERCANO (desde {CAPITALES[ciudad]})")
                    visualizar_ruta(ruta, f"Vecino más cercano - Inicio: {CAPITALES[ciudad]}\nDistancia: {distancia:.2f} km")
                else:
                    print("Ciudad inválida. Debe ser un número entre 0 y 22.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")
        
        elif opcion == 'b':
            print("\nBuscando la mejor ruta con vecino más cercano...")
            print("(Probando desde todas las ciudades)")
            ruta, distancia, ciudad_inicio = mejor_vecino_mas_cercano()
            mostrar_ruta(ruta, distancia, 
                        f"MEJOR VECINO MÁS CERCANO (óptimo local desde {CAPITALES[ciudad_inicio]})")
            visualizar_ruta(ruta, f"Mejor Vecino Más Cercano\nInicio: {CAPITALES[ciudad_inicio]} - Distancia: {distancia:.2f} km")
        
        elif opcion == 'c':
            ag = AlgoritmoGenetico(tam_poblacion=50, num_generaciones=200, 
                                  prob_crossover=0.8, prob_mutacion=0.2)
            ruta, distancia = ag.evolucionar()
            mostrar_ruta(ruta, distancia, "ALGORITMO GENÉTICO (solución optimizada)")
            visualizar_ruta(ruta, f"Algoritmo Genético\nDistancia: {distancia:.2f} km")
            graficar_convergencia(ag.mejor_ruta_historia)
        
        elif opcion == 'd':
            print("\n" + "="*70)
            print("COMPARACIÓN DE TODOS LOS MÉTODOS")
            print("="*70)
            
            # Vecino más cercano (mejor)
            print("\n1. Ejecutando Vecino Más Cercano...")
            ruta_vmc, dist_vmc, inicio_vmc = mejor_vecino_mas_cercano()
            print(f"   ✓ Mejor distancia: {dist_vmc:.2f} km")
            print(f"   ✓ Mejor inicio: {CAPITALES[inicio_vmc]}")
            
            # Algoritmo genético
            print("\n2. Ejecutando Algoritmo Genético...")
            ag = AlgoritmoGenetico(tam_poblacion=50, num_generaciones=200)
            ruta_ag, dist_ag = ag.evolucionar()
            print(f"   ✓ Distancia final: {dist_ag:.2f} km")
            
            # Resumen
            print("\n" + "="*70)
            print("RESUMEN DE RESULTADOS")
            print("="*70)
            print(f"Vecino Más Cercano:    {dist_vmc:.2f} km")
            print(f"Algoritmo Genético:    {dist_ag:.2f} km")
            mejora = ((dist_vmc - dist_ag) / dist_vmc) * 100
            if mejora > 0:
                print(f"\nMejora del AG: {mejora:.2f}% ✓")
            else:
                print(f"\nDiferencia: {abs(mejora):.2f}%")
            print("="*70)
            
            # Visualizar ambas
            visualizar_ruta(ruta_vmc, f"Vecino Más Cercano\nInicio: {CAPITALES[inicio_vmc]} - Distancia: {dist_vmc:.2f} km")
            visualizar_ruta(ruta_ag, f"Algoritmo Genético\nDistancia: {dist_ag:.2f} km")
            graficar_convergencia(ag.mejor_ruta_historia)
        
        elif opcion == 'e':
            print(f"\n{'='*70}")
            print("MATRIZ DE DISTANCIAS ENTRE CAPITALES (en kilómetros)")
            print(f"{'='*70}\n")
            print("Mostrando primeras 10 ciudades:\n")
            
            # Encabezado
            print("     ", end="")
            for i in range(min(10, len(CAPITALES))):
                print(f"{i:6d}", end="")
            print()
            
            # Filas
            for i in range(min(10, len(CAPITALES))):
                print(f"{i:2d} - ", end="")
                for j in range(min(10, len(CAPITALES))):
                    print(f"{int(MATRIZ_DISTANCIAS[i][j]):6d}", end="")
                print(f"  {CAPITALES[i][:25]}")
            
            print(f"\n{'='*70}")
            input("\nPresione Enter para continuar...")
        
        elif opcion == 's':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("\nOpción inválida. Por favor, intente nuevamente.")

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    menu_principal()