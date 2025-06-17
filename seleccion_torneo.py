import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import csv
import json


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

# Generadores
def generarVector(longitud: int=30)->Vector:
    """
    Genera un vector binario aleatorio de longitud especificada.

    Args:
        longitud (int, optional): Longitud del vector a generar. Por defecto es 30.

    Returns:
        Vector: Lista de 0s y 1s representando un individuo binario.
    """
    return [random.choice([0, 1]) for _ in range(longitud)]

def generarPoblacion(longitud: int = 10) -> Poblacion:
    """
    Genera una población de vectores binarios.

    Utiliza la función generarVector() para crear una lista de individuos, donde cada individuo es un vector binario. El parámetro longitud representa la cantidad de individuos en la población.

    Args:
        longitud (int, optional): Número de vectores a generar. Por defecto es 10.

    Returns:
        Poblacion: Lista de vectores binarios.
    """
    pobl = []
    for i in range(longitud):
        pobl.append(generarVector())
    return pobl

def crossover(vector1: Vector, vector2: Vector):
    '''
    Realiza un crossover entre dos vectores padres para generar dos vectores hijos. Si no se cumple la probabilidad de crossover, devuelve los padres sin modificar.

    Args:
        vector1 (Vector): Primer vector padre.
        vector2 (Vector): Segundo vector padre.

    Returns:
        Tuple[Vector, Vector]: Dos vectores resultantes del crossover o los padres originales.
    '''
    def cruzarVector(vect1: list[int], vect2:list[int]):
        '''
        Realiza el crossover simple (single-point) entre dos vectores.

        Args:
            vect1 (Vector): Primer vector padre.
            vect2 (Vector): Segundo vector padre.

        Returns:
            Tuple[Vector, Vector]: Dos vectores hijos resultantes del crossover.
        '''
        posicionSplit = int(random.random() * len(vect1) + 1)
        
        # Separamos los vectores vect1 y vect2 en dos partes (Left y Right)
        vect1Right = vect1[posicionSplit:]
        vect1Left = vect1[:posicionSplit]
        vect2Right = vect2[posicionSplit:]
        vect2Left = vect2[:posicionSplit]

        # Unimos las partes, generando los nuevos vectores hijos que son cruza de sus padres
        vect1Hijo = vect1Left + vect2Right
        vect2Hijo = vect2Left + vect1Right

        return vect1Hijo, vect2Hijo

    if(random.random()< PROBABILIDAD_DE_CROSSOVER):
        ## Aca hacemos el crossover si aplica
        vector1, vector2 = cruzarVector(vector1,vector2)
        return vector1, vector2
    
    else:
        return vector1, vector2

def mutacionInvertida(vector: Vector) -> Vector:
    """
    Aplica la mutación por inversa a un individuo (vector).

    Args:
        vector (Vector): Individuo representado como lista de valores .

    Returns:
        Vector: El individuo mutado.
    """

    if random.random() < PROBABILIDAD_DE_MUTACION:
        i = random.randint(0, len(vector) - 2)
        j = random.randint(i + 1, len(vector) - 1)
        sublista = vector[i:j+1]
        sublista.reverse()
        vector[i:j+1] = sublista
    return vector

def binarioDecimal(vector: Vector) -> int:
    '''
    Convierte un vector de bits (0s y 1s) que representa un número binario en su equivalente decimal.

    Args:
        vector (Vector): Lista de bits, donde el índice 0 es el bit más significativo.

    Returns:
        int: Valor decimal equivalente al número binario.
    '''
    decimal=0
    for i in range(len(vector)):
            if vector[i] == 1:
                decimal += 2 ** (len(vector) - 1 - i)
    return decimal

def fitness(decimal:float)->float:
    '''
    Calcula el valor de fitness de un número decimal según la función dada: (decimal / COEF) al cuadrado.

    Args:
        decimal (float): Valor decimal obtenido del vector binario.

    Returns:
        float: Resultado de la función de fitness.
    '''
    return (decimal / COEF) ** 2

def fitnessPromedioPoblacion(poblacion:list[Vector])->float:
    '''
    Calcula el fitness promedio de una población de vectores binarios.

    Args:
        poblacion (List[Vector]): Lista de vectores binarios.

    Returns:
        float: Valor promedio de fitness de la población.
    '''
    promedio = 0
    for p in poblacion:
        promedio += fitness(binarioDecimal(p))
    promedio = promedio / len(poblacion)
    return promedio

def fitnessMaxPoblacion(poblacion:list[Vector])->float:
    '''
    Calcula el valor máximo de fitness entre los individuos de la población.

    Args:
        poblacion (List[Vector]): Lista de vectores binarios.

    Returns:
        float: El fitness más alto encontrado en la población.
    '''
    max = fitness(binarioDecimal(poblacion[0]))
    for p in poblacion:
        if(max < fitness(binarioDecimal(p))):
            max = fitness(binarioDecimal(p))
    return max

def fitnessMinPoblacion(poblacion: list[Vector])->float:
    '''
    Calcula el valor mínimo de fitness entre los individuos de la población.

    Args:
        poblacion (List[Vector]): Lista de vectores binarios.

    Returns:
        float: El fitness más bajo encontrado en la población.
    '''
    min = fitness(binarioDecimal(poblacion[0]))
    for p in poblacion:
        if(min > fitness(binarioDecimal(p))):
            min = fitness(binarioDecimal(p))
    return min

def fitnessRelativoPoblacion(poblacionDecimal: Poblacion) -> list[float]:
    """
    Calcula el fitness relativo de cada individuo de la población.

    El fitness relativo es el valor del fitness de un individuo dividido por la suma total del fitness de la población. Esto permite expresar el aporte proporcional de cada individuo al total, útil para selección por ruleta.

    Args:
        poblacion (Poblacion): Lista de individuos en valores decimales.

    Returns:
        list[float]: Lista de valores de fitness relativo (suma = 1.0).
    """
    listaFitness: list[float] = []

    for individuo in poblacionDecimal:
        fitIndividuo = fitness(individuo)
        listaFitness.append(fitIndividuo)
   
    total = 0
    for f in listaFitness:
        total += f
  

    listaRelativos: list[float] = []
    for f in listaFitness:
        fitRelativo = f / total
        listaRelativos.append(fitRelativo)

    return listaRelativos

def cruzarPoblacion(padresPares:list[Vector, Vector])->Poblacion:
    """
    Con los pares de padres genera la siguiente generacion de individuos

    Args:
        padresPares (list[Vecto, Vector]): Pares de padres de la poblacion.
    Returns:
        Poblacion: Siguiente generacion de vectores despues de ser cruzados.
    """
    poblacionResultante: list[Vector, Vector] = []

    for par in padresPares:
        hijosPares = []
        hijosPares.append(crossover(par[0],par[1]))
        for a in hijosPares:
            poblacionResultante.append(a[0])
            poblacionResultante.append(a[1])
    
    for i in range(len(poblacionResultante)):
        poblacionResultante[i] = mutacionInvertida(poblacionResultante[i])

    return poblacionResultante

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
    with open(nombre_archivo, mode=modo, newline='') as archivo:
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
        guardarDatosPoblacionCSV(pobl,i,"poblacion_torneo.csv")

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
    ax.plot(generations, avg, label='Average')
    ax.plot(generations, max_, label='Max')
    ax.plot(generations, min_, label='Min')

    # Title and labels
    titulo = f"Pobl Size: {TAMAÑO_DE_LA_POBLACION} - Vect Len: {LONGITUD_DE_LOS_VECTORES} - Cant Iter: {CANTIDAD_DE_ITERACIONES} - Prob.Mutacion: {PROBABILIDAD_DE_MUTACION} - Prob. Crossover: {PROBABILIDAD_DE_CROSSOVER}"
    ax.set_title(titulo)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))

    ax.legend()
    ax.grid(True)




  

    plt.tight_layout()
    plt.show()

poblacion = [[1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1], [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1], [0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0]]


# Ejemplo de uso
if __name__ == "__main__":
    poblacion_inicial = generarPoblacion(10)
    seleccion_torneo(poblacion_inicial, CANTIDAD_DE_ITERACIONES)
