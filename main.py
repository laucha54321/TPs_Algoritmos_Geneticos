import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import csv
import json

# Cargo las variables desde el archivo JSON
with open("variables.json", "r", encoding="utf-8") as file:
    variables = json.load(file)

PROBABILIDAD_DE_CROSSOVER = variables["PROBABILIDAD_DE_CROSSOVER"]
PROBABILIDAD_DE_MUTACION = variables["PROBABILIDAD_DE_MUTACION"]
LONGITUD_DE_LOS_VECTORES = variables["LONGITUD_DE_LOS_VECTORES"]
TAMAÑO_DE_LA_POBLACION = variables["TAMAÑO_DE_LA_POBLACION"]
CANTIDAD_DE_ITERACIONES = variables["CANTIDAD_DE_ITERACIONES"]
COEF = variables["COEF"]
TAMAÑO_TORNEO = variables["TAMAÑO_TORNEO"]
N_ELITISMO = variables["N_ELITISMO"]



Vector = list[int]
Poblacion = list[Vector]

def generarVector(longitud: int = 30) -> Vector:
    """
    Genera un vector binario aleatorio de longitud especificada.
    """
    return [random.choice([0, 1]) for _ in range(longitud)]

def generarPoblacion(longitud: int = 10) -> Poblacion:
    """
    Genera una población de vectores binarios.
    """
    return [generarVector(LONGITUD_DE_LOS_VECTORES) for _ in range(longitud)]

def crossover(vector1: Vector, vector2: Vector) -> tuple[Vector, Vector]:
    """
    Realiza un crossover entre dos vectores padres para generar dos vectores hijos.
    """
    def cruzarVector(vect1: list[int], vect2: list[int]) -> tuple[Vector, Vector]:
        posicionSplit = random.randint(1, len(vect1) - 1)
        vect1Left, vect1Right = vect1[:posicionSplit], vect1[posicionSplit:]
        vect2Left, vect2Right = vect2[:posicionSplit], vect2[posicionSplit:]
        return vect1Left + vect2Right, vect2Left + vect1Right

    if random.random() < PROBABILIDAD_DE_CROSSOVER:
        return cruzarVector(vector1, vector2)
    return vector1, vector2

def mutacionInvertida(vector: Vector) -> Vector:
    """
    Aplica la mutación por inversa a un individuo (vector).
    """
    if random.random() < PROBABILIDAD_DE_MUTACION:
        i = random.randint(0, len(vector) - 2)
        j = random.randint(i + 1, len(vector) - 1)
        vector[i:j+1] = vector[i:j+1][::-1]
    return vector

def binarioDecimal(vector: Vector) -> int:
    """
    Convierte un vector binario a su equivalente decimal.
    """
    return sum(bit * (2 ** (len(vector) - 1 - i)) for i, bit in enumerate(vector))

def fitness(decimal: float) -> float:
    """
    Calcula el valor de fitness: (decimal / COEF) al cuadrado.
    """
    return (decimal / COEF) ** 2

def fitnessPromedioPoblacion(poblacion: list[Vector]) -> float:
    """
    Calcula el fitness promedio de una población.
    """
    return sum(fitness(binarioDecimal(p)) for p in poblacion) / len(poblacion)

def fitnessMaxPoblacion(poblacion: list[Vector]) -> float:
    """
    Calcula el valor máximo de fitness en la población.
    """
    return max(fitness(binarioDecimal(p)) for p in poblacion)

def fitnessMinPoblacion(poblacion: list[Vector]) -> float:
    """
    Calcula el valor mínimo de fitness en la población.
    """
    return min(fitness(binarioDecimal(p)) for p in poblacion)

def printInfoPoblacion(poblacion: list[Vector]) -> None:
    """
    Imprime información estadística sobre una población.
    """
    print("\n######## Datos de la Poblacion ########\n")
    for i, p in enumerate(poblacion, 1):
        print(f"Fitness Vector {i}: {fitness(binarioDecimal(p)):.6f}")
    print(f"\nPromedio: {fitnessPromedioPoblacion(poblacion):.6f}")
    print(f"Max: {fitnessMaxPoblacion(poblacion):.6f}")
    print(f"Min: {fitnessMinPoblacion(poblacion):.6f}\n")

def ruleta(poblacion: Poblacion) -> list[tuple[Vector, Vector]]:
    """
    Selección por ruleta: devuelve pares de padres binarios según fitness relativo.
    """
    def calcularFitnessRelativo(poblacionDecimal: list[float]) -> list[float]:
        listaFitness = [fitness(ind) for ind in poblacionDecimal]
        total = sum(listaFitness)
        return [f / total for f in listaFitness]

    def calcularFitnessAcumulado(fitnessRelativo: list[float]) -> list[float]:
        acumulado = [0.0]
        for fr in fitnessRelativo:
            acumulado.append(acumulado[-1] + fr)
        return acumulado

    def seleccionar_individuo(fitnessAcumulado: list[float]) -> int:
        r = random.random()
        for i in range(len(fitnessAcumulado) - 1):
            if fitnessAcumulado[i] <= r < fitnessAcumulado[i + 1]:
                return i
        return len(fitnessAcumulado) - 2

    poblacionDecimal = [binarioDecimal(ind) for ind in poblacion]
    fitnessRel = calcularFitnessRelativo(poblacionDecimal)
    fitnessAcum = calcularFitnessAcumulado(fitnessRel)

    pares = []
    num_pares = (len(poblacion) - N_ELITISMO) // 2  # Ajustar para elitismo
    for _ in range(num_pares):
        idx1 = seleccionar_individuo(fitnessAcum)
        idx2 = seleccionar_individuo(fitnessAcum)
        while idx2 == idx1:
            idx2 = seleccionar_individuo(fitnessAcum)
        pares.append((poblacion[idx1], poblacion[idx2]))

    return pares

def torneo(poblacion: Poblacion) -> list[tuple[Vector, Vector]]:
    """
    Selección por torneo: devuelve pares de padres binarios según fitness.
    """
    def seleccionar_individuo() -> Vector:
        participantes = random.sample(poblacion, TAMAÑO_TORNEO)
        return max(participantes, key=lambda p: fitness(binarioDecimal(p)))

    pares = []
    num_pares = (len(poblacion) - N_ELITISMO) // 2  # Ajustar para elitismo
    for _ in range(num_pares):
        padre1 = seleccionar_individuo()
        padre2 = seleccionar_individuo()
        while padre2 == padre1:
            padre2 = seleccionar_individuo()
        pares.append((padre1, padre2))

    return pares

def cruzarPoblacion(padresPares: list[tuple[Vector, Vector]], poblacion: Poblacion) -> Poblacion:
    """
    Realiza crossover y mutación sobre los pares de padres, incorporando elitismo.
    """
    nueva_poblacion: Poblacion = []
    
    # Elitismo: conservar los N_ELITISMO mejores individuos
    fitness_pares = [(fitness(binarioDecimal(p)), p) for p in poblacion]
    fitness_pares.sort(reverse=True)
    elite = [individuo for _, individuo in fitness_pares[:N_ELITISMO]]
    nueva_poblacion.extend(elite)

    # Generar hijos mediante crossover y mutación
    for padre1, padre2 in padresPares:
        hijo1, hijo2 = crossover(padre1, padre2)
        nueva_poblacion.extend([mutacionInvertida(hijo1), mutacionInvertida(hijo2)])

    # Asegurar que la población tenga el tamaño correcto
    return nueva_poblacion[:TAMAÑO_DE_LA_POBLACION]

def guardarDatosPoblacionCSV(poblacion: list[Vector], generacion: int, nombre_archivo: str = "resultados.csv") -> None:
    modo = 'w' if generacion == 0 else 'a'
    with open(nombre_archivo, mode=modo, newline='') as archivo:
        writer = csv.writer(archivo)
        if generacion == 0:
            writer.writerow(["gen", "min", "avg", "max", "mejor"])

        fitness_pares = [(fitness(binarioDecimal(p)), p) for p in poblacion]
        min_fitness = min(f for f, _ in fitness_pares)
        avg_fitness = sum(f for f, _ in fitness_pares) / len(poblacion)
        max_fitness, mejor_vector = max(fitness_pares, key=lambda x: x[0])
        mejor_cromosoma = ''.join(str(bit) for bit in mejor_vector)

        writer.writerow([generacion, min_fitness, avg_fitness, max_fitness, mejor_cromosoma])

def entrenamiento(pobl: Poblacion, iteraciones: int, use_torneo: bool = False) -> None:
    """
    Aplica el algoritmo genético iterando crossover y mutación.
    """
    generations = list(range(iteraciones))
    avg, min_, max_ = [], [], []

    for i in range(iteraciones):
        printInfoPoblacion(pobl)
        avg.append(fitnessPromedioPoblacion(pobl))
        max_.append(fitnessMaxPoblacion(pobl))
        min_.append(fitnessMinPoblacion(pobl))

        guardarDatosPoblacionCSV(pobl, i, "poblacion_ruleta.csv")
        padres_pares = torneo(pobl) if use_torneo else ruleta(pobl)
        pobl = cruzarPoblacion(padres_pares, pobl)        

    mejor = max(pobl, key=lambda x: fitness(binarioDecimal(x)))
    print("Mejor cromosoma final:", mejor)
    print("Valor decimal:", binarioDecimal(mejor))
    print("Fitness:", fitness(binarioDecimal(mejor)))

    # Gráfico de evolución
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(generations, avg, label='Average')
    ax.plot(generations, max_, label='Max')
    ax.plot(generations, min_, label='Min')

    metodo = "TORNEO" if use_torneo else "RULETA"
    titulo = f"{metodo} - Pobl Size: {TAMAÑO_DE_LA_POBLACION} - Vect Len: {LONGITUD_DE_LOS_VECTORES} - Cant Iter: {CANTIDAD_DE_ITERACIONES} - Prob.Mutacion: {PROBABILIDAD_DE_MUTACION} - Prob. Crossover: {PROBABILIDAD_DE_CROSSOVER} - Elitismo: {N_ELITISMO}"
    ax.set_title(titulo)
    ax.set_xlabel("Generación")
    ax.set_ylabel("Fitness")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    pobl = generarPoblacion(TAMAÑO_DE_LA_POBLACION)
    entrenamiento(pobl, CANTIDAD_DE_ITERACIONES, use_torneo=False)  