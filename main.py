import random
from guardarVectores import guardarVectoresJson

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

Vector = list[int]
Poblacion = list[Vector]

poblacion = [[1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1], [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1], [0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0]]


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

def ruleta(poblacion: Poblacion)-> list[Vector,Vector]:
    """  
    Realiza la selección de padres mediante el método de ruleta (roulette wheel selection).
    
    Este método asigna a cada individuo de la población una probabilidad de ser elegido proporcional a su valor de fitness relativo. Luego, se generan pares de padres seleccionando aleatoriamente posiciones dentro del rango [0, 1), que corresponden a sectores acumulados de la ruleta definidos por el fitness relativo.

    Args:
        poblacion (Poblacion): Lista de individuos (vectores binarios) sobre los que se aplicará la selección.

    Returns:
        List[Tuple[Vector, Vector]]: Lista de pares de individuos seleccionados para cruzamiento, en formato binario.
    """ 

    def calcularPoblacionDecimal(poblacion: Poblacion):
        """
        Convierte cada individuo binario de la población en su representación decimal.

        Returns:
            list[float]: Lista de valores decimales correspondientes a la población binaria.
        """
        poblacionDecimal: list[float] = []
        for p in poblacion: 
            poblacionDecimal.append(binarioDecimal(p))
        return poblacionDecimal

    def calcularFitnessAcumulado(poblacionDecimal: list[int]) -> list[float]:
        """
        Calcula el fitness acumulado de la población para el método de ruleta.

        A partir del fitness relativo de cada individuo, construye una lista que representa el acumulado progresivo, comenzando en 0. Este acumulado permite asignar a cada individuo una "porción" de la ruleta proporcional a su fitness.

        Args:
            poblacionDecimal (list[float]): Poblacion representada en su forma decimal.

        Returns:
            list[float]: Lista de valores acumulados desde 0 hasta 1.
        """
        fitnessAcumulado: list[float] = []
        fitnessAcumulado.append(0)
        fitnessRelativo = fitnessRelativoPoblacion(poblacionDecimal)
        acumulado: float = 0
        for p in fitnessRelativo:
            acumulado += p
            fitnessAcumulado.append(acumulado)
        return fitnessAcumulado

    def calcularParesPadres(fitnessAcumulado: list[float], poblacionDecimal: list[int])->list[list[float]]:
        """
        Selecciona pares de padres (en decimal) basándose en el fitness acumulado.

        Args:
            fitnessAcumulado (list[float]): Lista de fitness acumulado de la población. Define los rangos de selección dentro de la ruleta.
            poblacionDecimal (list[float]): Población representada en su forma decimal.

        Returns:
            list[list[float]]: Lista de pares de padres seleccionados según el método de ruleta.
        """
        padresParesDecimal: list[float] = []
        for _ in range(CANTIDAD_DE_PARES):
            par: list[float] = []
            padre1 = random.random()
            padre2 = random.random()
            for p in range(len(fitnessAcumulado)):
                if fitnessAcumulado[p] <= padre1 <= fitnessAcumulado[p+1]:
                    par.append(poblacionDecimal[p])
                if fitnessAcumulado[p] <= padre2 <= fitnessAcumulado[p+1]:
                    par.append(poblacionDecimal[p])
            padresParesDecimal.append(par)
        return padresParesDecimal

    def calcularParesPadresBinario(padresParesDecimal: list[int]) -> list[Vector,Vector]:
        """
        Convierte los pares de padres seleccionados (en decimal) a su forma binaria original.
        Args:
            list[list[int]]: Pares de individuos seleccionados en su forma decimal.
        Returns:
            list[list[Vector]]: Pares de individuos seleccionados en su forma binaria.
        """
        padresParesBinario: list[int] = []
        for par in padresParesDecimal:
            parBinario: list[int] = []
            for padre in par:
                parBinario.append(poblacion[poblacionDecimal.index(padre)])
            padresParesBinario.append(parBinario)
        return padresParesBinario

    # Calculo la cantidad de pares que vamos a tener para luego cruzar. 
    CANTIDAD_DE_PARES = int(len(poblacion)/2)
    # Transformo la poblacion Binaria a Decimal para usarla en las demas funciones
    poblacionDecimal: list[float] = calcularPoblacionDecimal(poblacion) 
    # Calculo el fitness acumulado para poder utilizarlo para definir las porciones de la ruleta.
    fitnessAcumulado: list[float] = calcularFitnessAcumulado(poblacionDecimal)

    # Calculo los Pares de padres a partir utilizando el fitness acumulado como posicion en la ruleta.
    padresParesDecimal: list[float] = calcularParesPadres(fitnessAcumulado,poblacionDecimal)
    # Transormo los pares de padres en Decimal a Binario.
    padresParesBinario: list[int] = calcularParesPadresBinario(padresParesDecimal)


    return padresParesBinario
        
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


def torneo (poblacion, fitness):
    """
    Selecciona un individuo usando el método de torneo.

    Args:
        poblacion (lista): lista con los individuos.
        fitness (lista): lista con los valores de fitness de cada individuo.

    Returns:
        individuo ganador: el individuo con el mejor fitness dentro del torneo.
    """

    participantes = random.sample(list(zip(poblacion, fitness)), TAMAÑO_TORNEO)
    ganador = participantes[0]
    for participante in participantes:
        if participante[1] > ganador[1]:
            ganador = participante

    return ganador[0]


def entrenamiento(pobl: Poblacion, iteraciones: int):
    """
    Aplica el algoritmo genetico iterando haciendo crossover y generando las nuevas poblaciones.

    Args:
        pobl (Poblacion): poblacion inicial del algoritmo.
        iteraciones (int): La cantidad de iteraciones que se van a ejecutar. 
    """
    generations = list(range(iteraciones))
    avg = []
    min_ = []
    max_ = []
    for i in range(iteraciones):
        printInfoPoblacion(pobl)
        avg.append(fitnessPromedioPoblacion(pobl))
        max_.append(fitnessMaxPoblacion(pobl))
        min_.append(fitnessMinPoblacion(pobl))

        guardarDatosPoblacionCSV(pobl,i,"poblacion_ruleta.csv")

        pobl = ruleta(pobl)
        pobl = cruzarPoblacion(pobl)



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

    # Mostrar 8 decimales en el eje Y
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))

    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()

def guardarDatosPoblacionCSV(poblacion: list[Vector], generacion: int, nombre_archivo: str = "resultados.csv") -> None:
    modo = 'w' if generacion == 0 else 'a'
    with open(nombre_archivo, mode=modo, newline='') as archivo:
        writer = csv.writer(archivo)
        
        # Escribir encabezado si es la primera generación
        if generacion == 0:
            writer.writerow(["gen", "ind", "fit", "avg", "max", "min"])

        promedio = fitnessPromedioPoblacion(poblacion)
        maximo = fitnessMaxPoblacion(poblacion)
        minimo = fitnessMinPoblacion(poblacion)

        for i, p in enumerate(poblacion):
            fit = fitness(binarioDecimal(p))
            writer.writerow([generacion, i+1, fit, promedio, maximo, minimo])   

pobl = generarPoblacion(10)
#pobl = generarPoblacion(TAMAÑO_DE_LA_POBLACION)
entrenamiento(pobl, CANTIDAD_DE_ITERACIONES)