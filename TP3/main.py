import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import random
from typing import List, Tuple
import csv

# Capitales
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

# Coordenadas aproximadas 
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


# Tabla de distancias entre capitales (en km)
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

# Funciones Basicas
def calcular_distancia_total(ruta: List[int]) -> float:    
    distancia = 0
    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % len(ruta)]
        distancia += MATRIZ_DISTANCIAS[ciudad_actual][ciudad_siguiente]
    return distancia

def mostrar_ruta(ruta: List[int], distancia: float, titulo: str = "Ruta"):    
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

# Heuristica ciudad mas cercana no visitada
def vecino_mas_cercano(ciudad_inicio: int) -> Tuple[List[int], float]:
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
N = 50                 # Tamaño de la población (número de cromosomas)
M = 200                # Número de generaciones (cantidad de ciclos)
PROB_CROSSOVER = 0.8   # Probabilidad de aplicar crossover
PROB_MUTACION = 0.2    # Probabilidad de aplicar mutación (inversión)
NUM_CIUDADES = len(CAPITALES)  # 24

# Estado global 
mejor_ruta_historia: List[float] = []
poblacion_global: List[List[int]] = []

# ======= FUNCIONES DEL AG =======
def crear_individuo() -> List[int]:    
    individuo = list(range(NUM_CIUDADES))
    random.shuffle(individuo)
    return individuo

def crear_poblacion_inicial() -> List[List[int]]:
    return [crear_individuo() for _ in range(N)]

def fitness(individuo: List[int]) -> float:
    distancia = calcular_distancia_total(individuo)
    return 1 / distancia if distancia > 0 else 0

def seleccion_torneo(poblacion: List[List[int]], k: int = 3) -> List[int]:
    torneo = random.sample(poblacion, k)
    return max(torneo, key=fitness)

def crossover_ciclico(padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:    
    n = len(padre1)
    hijo1 = [-1] * n
    hijo2 = [-1] * n
    visitados = [False] * n
    es_ciclo_par = True

    for inicio in range(n):
        if not visitados[inicio]:
            indice = inicio
            ciclo = []
            while not visitados[indice]:
                visitados[indice] = True
                ciclo.append(indice)
                valor = padre1[indice]
                indice = padre2.index(valor)

            if es_ciclo_par:
                for idx in ciclo:
                    hijo1[idx] = padre1[idx]
                    hijo2[idx] = padre2[idx]
            else:
                for idx in ciclo:
                    hijo1[idx] = padre2[idx]
                    hijo2[idx] = padre1[idx]

            es_ciclo_par = not es_ciclo_par

    # Rellenar huecos (-1) con los valores que faltan (manteniendo permutación)
    def rellenar(hijo, padre):
        faltantes = [g for g in padre if g not in hijo]
        for i in range(n):
            if hijo[i] == -1:
                hijo[i] = faltantes.pop(0)
        return hijo

    hijo1 = rellenar(hijo1, padre2)
    hijo2 = rellenar(hijo2, padre1)
    return hijo1, hijo2

def mutacion_inversion(individuo: List[int]) -> List[int]:    
    if random.random() < PROB_MUTACION:
        individuo = individuo.copy()
        i, j = sorted(random.sample(range(len(individuo)), 2))
        individuo[i:j+1] = list(reversed(individuo[i:j+1]))
    return individuo

def evolucionar() -> Tuple[List[int], float]:
    global poblacion_global, mejor_ruta_historia

    poblacion = crear_poblacion_inicial()
    poblacion_global = poblacion
    mejor_ruta_historia = []

    registros = []
    mejor_global = float("inf")

    for generacion in range(M):
        distancias = [calcular_distancia_total(ind) for ind in poblacion]
        idx_mejor = distancias.index(min(distancias))
        mejor_recorrido = poblacion[idx_mejor]
        mejor_distancia = distancias[idx_mejor]
        mejor_ruta_historia.append(mejor_distancia)

        # Guardar mejor global
        if mejor_distancia < mejor_global:
            mejor_global = mejor_distancia

        # Registrar datos para CSV
        registros.append({
            "gen": generacion + 1,
            "mejor_dist": mejor_distancia,
            "mejor_recorrido": "-".join(map(str, mejor_recorrido))
        })

        # Nueva población con elitismo
        fitness_poblacion = [(ind, fitness(ind)) for ind in poblacion]
        fitness_poblacion.sort(key=lambda x: x[1], reverse=True)

        nueva_poblacion = [fitness_poblacion[0][0], fitness_poblacion[1][0]]

        while len(nueva_poblacion) < N:
            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)

            if random.random() < PROB_CROSSOVER:
                hijo1, hijo2 = crossover_ciclico(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()

            hijo1 = mutacion_inversion(hijo1)
            hijo2 = mutacion_inversion(hijo2)
            nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion[:N]

    # Guardar CSV final
    with open("evolucion.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["gen", "mejor_dist", "mejor_recorrido"])
        writer.writeheader()
        writer.writerows(registros)

    # Resultado final
    fitness_final = [(ind, fitness(ind)) for ind in poblacion]
    fitness_final.sort(key=lambda x: x[1], reverse=True)
    mejor_final = fitness_final[0][0]
    distancia_final = calcular_distancia_total(mejor_final)

    poblacion_global = poblacion

    return mejor_final, distancia_final



# Visualizacion
def visualizar_ruta(ruta: List[int], titulo: str = "Ruta TSP", figsize=(25, 6.2),
                    mostrar_regreso=True):
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
    lat0, lon0 = COORDENADAS[ruta[0]]
    lats.append(lat0)
    lons.append(lon0)

    # Dibujar líneas con flechas
    for i in range(len(ruta)):
        ciudad1 = ruta[i]
        ciudad2 = ruta[(i + 1) % len(ruta)]
        lat1, lon1 = COORDENADAS[ciudad1]
        lat2, lon2 = COORDENADAS[ciudad2]

        ax.plot([lon1, lon2], [lat1, lat2], color=color_linea,
                linewidth=1.8, alpha=0.7, zorder=1)

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
    ax.grid(True, alpha=0.25, linestyle='--')

    # Títulos
    ax.set_xlabel('Longitud', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitud', fontsize=12, fontweight='bold')
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=12)

    # Leyenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='*', color='w', markerfacecolor=color_inicio,
               markersize=12, label='Inicio/Fin', markeredgecolor='white', markeredgewidth=1.5),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_punto,
               markersize=8, label='Ciudades intermedias', markeredgecolor='white', markeredgewidth=1),
        Line2D([0], [0], color=color_linea, linewidth=1.8, label='Recorrido')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1),
              fontsize=10, framealpha=0.9, borderaxespad=0.)

    # Texto del recorrido
    lista_capitales = [CAPITALES[i] for i in ruta]
    if mostrar_regreso:
        lista_capitales.append(CAPITALES[ruta[0]])

    recorrido_texto = "Recorrido:\n" + "\n".join(
        [f"{i+1}. {nombre}" for i, nombre in enumerate(lista_capitales)]
    )
    plt.text(1.05, 0.02, recorrido_texto, transform=ax.transAxes,
             fontsize=9, va='bottom', ha='left',
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9),
             fontweight='bold')

    plt.tight_layout()
    plt.subplots_adjust(right=0.72)
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

#Menu
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

def mostrar_menu():    
    print(f"\n{'='*70}")
    print(" PROBLEMA DEL VIAJANTE")
    print(f"{'='*70}")
    print("1) Vecino más cercano desde una provincia específica")
    print("2) Mejor vecino más cercano (probar todas las provincias)")
    print("3) Algoritmo Genético")
    print("0) Salir")
    print(f"{'='*70}")

def menu_principal():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            listar_provincias()
            try:
                ciudad = int(input("Ingrese el número de la ciudad de inicio (0-23): "))
                if 0 <= ciudad < len(CAPITALES):
                    
                    ruta, distancia = vecino_mas_cercano(ciudad)

                    visualizar_ruta(ruta, f"Vecino más cercano - Inicio: {CAPITALES[ciudad]}\nDistancia: {distancia:.2f} km")
                else:
                    print("Ciudad inválida. Debe ser un número entre 0 y 23.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")
        
        elif opcion == '2':

            ruta, distancia, ciudad_inicio = mejor_vecino_mas_cercano()
            visualizar_ruta(ruta, f"Mejor Vecino Más Cercano\nInicio: {CAPITALES[ciudad_inicio]} - Distancia: {distancia:.2f} km")
        
        elif opcion == '3':            
            ruta, distancia = evolucionar()            
            visualizar_ruta(ruta, f"Algoritmo Genético\nDistancia: {distancia:.2f} km")
            graficar_convergencia(mejor_ruta_historia)
        
        elif opcion == '0':
            break
        
        else:
            print("\nOpción inválida. Por favor, intente nuevamente.")


if __name__ == "__main__":
    menu_principal()