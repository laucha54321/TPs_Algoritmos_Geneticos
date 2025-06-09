import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

poblacion = [[1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1], [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1], [0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0]]

# Constants
PROBABILIDAD_DE_CROSSOVER = 0.75
PROBABILIDAD_DE_MUTACION = 0.05
LONGITUD_DE_LOS_VECTORES = 30
TAMAÑO_DE_LA_POBLACION = 10
CANTIDAD_DE_ITERACIONES = 20
COEF = 2**30 - 1
TAMAÑO_TORNEO = 3
N_ELITISMO = 4

Vector = list[int]
Poblacion = list[Vector]

def generarVector(longitud: int = 30) -> Vector:
    return [random.choice([0, 1]) for _ in range(longitud)]

def generarPoblacion(longitud: int = 10) -> Poblacion:
    return [generarVector(LONGITUD_DE_LOS_VECTORES) for _ in range(longitud)]

def crossover(vector1: Vector, vector2: Vector) -> tuple[Vector, Vector]:
    def cruzarVector(vect1: Vector, vect2: Vector) -> tuple[Vector, Vector]:
        posicionSplit = random.randint(1, len(vect1) - 1)
        vect1Hijo = vect1[:posicionSplit] + vect2[posicionSplit:]
        vect2Hijo = vect2[:posicionSplit] + vect1[posicionSplit:]
        return vect1Hijo, vect2Hijo

    if random.random() < PROBABILIDAD_DE_CROSSOVER:
        return cruzarVector(vector1, vector2)
    return vector1, vector2

def mutacionInvertida(vector: Vector) -> Vector:
    if random.random() < PROBABILIDAD_DE_MUTACION:
        i = random.randint(0, len(vector) - 2)
        j = random.randint(i + 1, len(vector) - 1)
        vector[i:j+1] = vector[i:j+1][::-1]
    return vector

def binarioDecimal(vector: Vector) -> int:
    return sum(2 ** (len(vector) - 1 - i) for i, bit in enumerate(vector) if bit == 1)

def fitness(decimal: float) -> float:
    return (decimal / COEF) ** 2

def fitnessPromedioPoblacion(poblacion: Poblacion) -> float:
    return sum(fitness(binarioDecimal(p)) for p in poblacion) / len(poblacion)

def fitnessMaxPoblacion(poblacion: Poblacion) -> float:
    return max(fitness(binarioDecimal(p)) for p in poblacion)

def fitnessMinPoblacion(poblacion: Poblacion) -> float:
    return min(fitness(binarioDecimal(p)) for p in poblacion)

def printInfoPoblacion(poblacion: Poblacion) -> None:
    print("\n######## Datos de la Poblacion ########\n")
    for i, p in enumerate(poblacion, 1):
        print(f"Fitness Vector {i}: {fitness(binarioDecimal(p)):.8f}")
    print(f"\nPromedio: {fitnessPromedioPoblacion(poblacion):.8f}")
    print(f"Max: {fitnessMaxPoblacion(poblacion):.8f}")
    print(f"Min: {fitnessMinPoblacion(poblacion):.8f}\n")

def fitnessRelativoPoblacion(poblacionDecimal: list[float]) -> list[float]:
    fitness_values = [fitness(ind) for ind in poblacionDecimal]
    total_fitness = sum(fitness_values)
    if total_fitness == 0:  # Avoid division by zero
        return [1.0 / len(poblacionDecimal)] * len(poblacionDecimal)
    return [f / total_fitness for f in fitness_values]

def ruleta(poblacion: Poblacion) -> list[list[Vector]]:
    poblacionDecimal = [binarioDecimal(p) for p in poblacion]
    fitnessAcumulado = [0]
    for f in fitnessRelativoPoblacion(poblacionDecimal):
        fitnessAcumulado.append(fitnessAcumulado[-1] + f)

    CANTIDAD_DE_PARES = len(poblacion) // 2
    padresParesBinario = []
    for _ in range(CANTIDAD_DE_PARES):
        par = []
        for _ in range(2):
            r = random.random()
            for i in range(len(fitnessAcumulado) - 1):
                if fitnessAcumulado[i] <= r < fitnessAcumulado[i + 1]:
                    par.append(poblacion[i])
                    break
        padresParesBinario.append(par)
    return padresParesBinario

def cruzarPoblacion(padresPares: list[list[Vector]]) -> Poblacion:
    poblacionResultante = []    
    for par in padresPares:
        hijo1, hijo2 = crossover(par[0], par[1])
        poblacionResultante.append(mutacionInvertida(hijo1))
        poblacionResultante.append(mutacionInvertida(hijo2))
    return poblacionResultante

def ruletaElitismo(poblacion: Poblacion, n_elit: int) -> Poblacion:
    """Roulette with elitism, preserving top n_elit and generating 6 offspring."""
    if not poblacion:
        return generarPoblacion(TAMAÑO_DE_LA_POBLACION, max_decimal=1024)
    
    # Select top n_elit individuals
    fitness_values = [(fitness(binarioDecimal(p)), p) for p in poblacion]
    fitness_values.sort(reverse=True)
    elite = [ind for _, ind in fitness_values[:n_elit]]
    
    # Non-elite population for selection
    non_elite_poblacion = [p for p in poblacion if p not in elite]
    if not non_elite_poblacion:
        non_elite_poblacion = poblacion  # Fallback to full population if elite takes all
    
    # Generate exactly 6 offspring (3 pairs)
    nueva_poblacion = []
    for _ in range(3):  # Need 3 pairs to produce 6 offspring
        poblacionDecimal = [binarioDecimal(p) for p in non_elite_poblacion]
        fitnessAcumulado = [0]
        for f in fitnessRelativoPoblacion(poblacionDecimal):
            fitnessAcumulado.append(fitnessAcumulado[-1] + f)
        
        parents = []
        for _ in range(2):  # Select 2 parents for a pair
            r = random.random()
            for i in range(len(fitnessAcumulado) - 1):
                if fitnessAcumulado[i] <= r < fitnessAcumulado[i + 1]:
                    parents.append(non_elite_poblacion[i])
                    break
            else:
                parents.append(non_elite_poblacion[-1])
        
        if len(parents) == 2:
            hijo1, hijo2 = crossover(parents[0], parents[1])
            nueva_poblacion.append(mutacionInvertida(hijo1))
            nueva_poblacion.append(mutacionInvertida(hijo2))
    
    # Combine elite with new offspring
    result = elite + nueva_poblacion
    
    # Ensure population size is exactly 10
    while len(result) < TAMAÑO_DE_LA_POBLACION:
        new_vector = generarVector(N_ELITISMO, max_decimal=1024)
        if tuple(new_vector) not in {tuple(v) for v in result}:
            result.append(new_vector)
    
    return result[:TAMAÑO_DE_LA_POBLACION]   

def moving_average(data, window_size=3):
    """Calcula el promedio móvil para suavizar una serie de datos."""
    if len(data) < window_size:
        return data  # no smooth if not enough data
    return [
        sum(data[max(0, i - window_size + 1):i + 1]) / len(data[max(0, i - window_size + 1):i + 1])
        for i in range(len(data))
    ]

def entrenamiento(pobl: Poblacion, iteraciones: int):
    generations = list(range(iteraciones))
    avg = []
    min_ = []
    max_ = []
    for _ in range(iteraciones):
        printInfoPoblacion(pobl)
        avg.append(fitnessPromedioPoblacion(pobl))
        max_.append(fitnessMaxPoblacion(pobl))
        min_.append(fitnessMinPoblacion(pobl))
        pobl = ruletaElitismo(pobl, N_ELITISMO)


    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(generations, avg, label='Average')
    ax.plot(generations, max_, label='Max')
    ax.plot(generations, min_, label='Min')
    titulo = (f"Pobl Size: {TAMAÑO_DE_LA_POBLACION} - Vect Len: {LONGITUD_DE_LOS_VECTORES} "
              f"- Cant Iter: {CANTIDAD_DE_ITERACIONES} - Prob.Mutacion: {PROBABILIDAD_DE_MUTACION} "
              f"- Prob. Crossover: {PROBABILIDAD_DE_CROSSOVER}")
    ax.set_title(titulo)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    x = generarPoblacion()
    print(x)
    printInfoPoblacion(x)

    pobl = poblacion
    entrenamiento(pobl, CANTIDAD_DE_ITERACIONES)