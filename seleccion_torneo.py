import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import csv


# Constantes
PROBABILIDAD_DE_CROSSOVER = 0.75
PROBABILIDAD_DE_MUTACION = 0.05
LONGITUD_DE_LOS_VECTORES = 30
TAMAÑO_DE_LA_POBLACION = 10
CANTIDAD_DE_ITERACIONES = 10
COEF = 2**30 - 1
TAMAÑO_TORNEO = 3

Vector = list[int]
Poblacion = list[Vector]

# Generadores
def generarVector(longitud: int = 30) -> Vector:
    return [random.choice([0, 1]) for _ in range(longitud)]

def generarPoblacion(longitud: int = 10) -> Poblacion:
    return [generarVector() for _ in range(longitud)]

# Evaluación
def binarioDecimal(vector: Vector) -> int:
    return sum(bit * (2 ** (len(vector) - 1 - i)) for i, bit in enumerate(vector))

def fitness(decimal: float) -> float:
    return (decimal / COEF) ** 2

def fitnessPromedioPoblacion(poblacion: list[Vector]) -> float:
    return sum(fitness(binarioDecimal(p)) for p in poblacion) / len(poblacion)

def fitnessMaxPoblacion(poblacion: list[Vector]) -> float:
    return max(fitness(binarioDecimal(p)) for p in poblacion)

def fitnessMinPoblacion(poblacion: list[Vector]) -> float:
    return min(fitness(binarioDecimal(p)) for p in poblacion)

# Operadores genéticos
def crossover(vector1: Vector, vector2: Vector):
    if random.random() < PROBABILIDAD_DE_CROSSOVER:
        split = random.randint(1, len(vector1) - 1)
        hijo1 = vector1[:split] + vector2[split:]
        hijo2 = vector2[:split] + vector1[split:]
        return hijo1, hijo2
    else:
        return vector1, vector2

def mutacionInvertida(vector: Vector) -> Vector:
    if random.random() < PROBABILIDAD_DE_MUTACION:
        i = random.randint(0, len(vector) - 2)
        j = random.randint(i + 1, len(vector) - 1)
        vector[i:j+1] = reversed(vector[i:j+1])
    return vector

def cruzarPoblacion(padresPares: list[list[Vector]]) -> Poblacion:
    nueva_poblacion = []
    for padre1, padre2 in padresPares:
        hijo1, hijo2 = crossover(padre1, padre2)
        nueva_poblacion.append(mutacionInvertida(hijo1))
        nueva_poblacion.append(mutacionInvertida(hijo2))
    return nueva_poblacion

def printInfoPoblacion(poblacion: list[Vector])->None:
    """
    Imprime información estadística sobre una población.

    Muestra el fitness de cada individuo, junto con el promedio, el valor máximo y el mínimo del fitness en la población pasada como parámetro.

    Args:
        poblacion (list[Vector]): Lista de individuos representados en binario.
    """
    print("\n######## Datos de la Poblacion ########\n")
    i=0
    for p in poblacion:
        i += 1
        print("Fitness Vector ", i, ": ",fitness(binarioDecimal(p)))
    print("\nPromedio: ",fitnessPromedioPoblacion(poblacion))
    print("Max: ",fitnessMaxPoblacion(poblacion))
    print("Min: ",fitnessMinPoblacion(poblacion))
    print("\n")

def guardarDatosPoblacionCSV(poblacion: list[Vector], generacion: int, nombre_archivo: str = "resultados.csv") -> None:
    modo = 'w' if generacion == 0 else 'a'
    with open(nombre_archivo, mode='a', newline='') as archivo:
        writer = csv.writer(archivo)
        
        # Escribir encabezado si es la primera generación
        if generacion == 0:
            writer.writerow(["Generación", "Individuo", "Fitness", "Promedio", "Máximo", "Mínimo"])
        
        promedio = fitnessPromedioPoblacion(poblacion)
        maximo = fitnessMaxPoblacion(poblacion)
        minimo = fitnessMinPoblacion(poblacion)

        for i, p in enumerate(poblacion):
            fit = fitness(binarioDecimal(p))
            writer.writerow([generacion, i+1, fit, promedio, maximo, minimo])

# Selección por torneo
def torneo(poblacion: Poblacion, fitnesses: list[float]) -> Vector:
    participantes = random.sample(list(zip(poblacion, fitnesses)), TAMAÑO_TORNEO)
    return max(participantes, key=lambda x: x[1])[0]

def seleccion_torneo(pobl: Poblacion, iteraciones: int):
    generations = list(range(iteraciones))
    avg = []
    min_ = []
    max_ = []

    for i in range(iteraciones):
        printInfoPoblacion(pobl)
        avg.append(fitnessPromedioPoblacion(pobl))
        min_.append(fitnessMinPoblacion(pobl))
        max_.append(fitnessMaxPoblacion(pobl))

        #Guardar los datos
        guardarDatosPoblacionCSV(pobl,i,"poblacion_torneo")

        # Usar selección por torneo
        fits = [fitness(binarioDecimal(p)) for p in pobl]
        padres = [[torneo(pobl, fits), torneo(pobl, fits)] for _ in range(int(len(pobl)/2))]

        pobl = cruzarPoblacion(padres)

    mejor = max(pobl, key=lambda x: fitness(binarioDecimal(x)))
    print("Mejor cromosoma final:", mejor)
    print("Valor decimal:", binarioDecimal(mejor))
    print("Fitness:", fitness(binarioDecimal(mejor)))

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot lines
    ax.plot(generations, avg, label='Average', marker='o')
    ax.plot(generations, max_, label='Max', marker='^')
    ax.plot(generations, min_, label='Min', marker='v')

    # Title and labels
    titulo = f"Pobl Size: {TAMAÑO_DE_LA_POBLACION} - Vect Len: {LONGITUD_DE_LOS_VECTORES} - Cant Iter: {CANTIDAD_DE_ITERACIONES} - Prob.Mutacion: {PROBABILIDAD_DE_MUTACION} - Prob. Crossover: {PROBABILIDAD_DE_CROSSOVER}"
    ax.set_title(titulo)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")

    # Mostrar 8 decimales en el eje Y
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))

    ax.legend()
    ax.grid(True)




  

    plt.tight_layout()
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    poblacion_inicial = generarPoblacion(TAMAÑO_DE_LA_POBLACION)
    seleccion_torneo(poblacion_inicial, CANTIDAD_DE_ITERACIONES)
