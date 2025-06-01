import random
from guardarVectores import guardarVectoresJson

PROBABILIDAD_DE_CROSSOVER = 0.75
LONGITUD_DE_LOS_VECTORES = 30
TAMAÑO_DE_LA_POBLACION = 10
COEF = 2**30 - 1

Vector = list[int]
Poblacion = list[Vector]


# Genera un vector aleatorio de longitud 30 por defecto
def generarVector(longitud: int=30)->Vector:
    return [random.choice([0, 1]) for _ in range(longitud)]

# Utiliza la funcion generarVector para generar una poblacion de vectores, longitud en este caso es el tamaño de la poblacion.
def generarPoblacion(longitud: int = 10) -> Poblacion:
    pobl = []
    for i in range(longitud):
        pobl.append(generarVector())
    return pobl

# Crossover devuelve los dos pares de vectores resultados del crossover o devuelve los dos padres directamente en caso de no haber crossover.
def crossover(vector1: Vector, vector2: Vector):

    # Cruzamos un solo par de vectores en esta funcion
    def cruzarVector(vect1: list[int], vect2:list[int]):
        posicionSplit = int(random.random() * len(vect1) + 1)
        
        # Separamos los vectores vect1 y vect2 en dos partes (Left y Right)
        vect1Right = vect1[posicionSplit:]
        vect1Left = vect1[:posicionSplit]
        vect2Right = vect2[posicionSplit:]
        vect2Left = vect2[:posicionSplit]

        # Unimos las partes, generando los nuevos vectores hijos que son cruza de sus padres
        vect1Hijo = vect1Left + vect2Right
        vect2Hijo = vect2Left + vect1Right

        print("\n ################# CRUZAR VECTORES #################\n \nPosicion del Split: ", posicionSplit,"\n\nPadre1: ",vect1,"\nPadre2: ", vect2,"\n\nHijo1: ",vect1Hijo,"\nHijo2: ",vect2Hijo,"\n\n")
        return vect1Hijo, vect2Hijo

    if(random.random()>PROBABILIDAD_DE_CROSSOVER):
        ## Aca hacemos el crossover si aplica
        vect1, vect2 = cruzarVector(vect1,vect2)
        return vect1, vect2
    
    else:
        return vect1, vect2

# Transforma el vector de binario a un valor decimal
def binarioDecimal(vector: Vector) -> int:
    decimal=0
    for i in range(len(vector)):
            if vector[i] == 1:
                decimal += 2 ** (len(vector) - 1 - i)
    return decimal

# Funcion de fitness dada en la consigna, hay que aplicarla al vector transformado a decimal con la funcion binarioDecimal()
def fitness(decimal):
    return (decimal / COEF) ** 2

# Calcula el fitness promedio de la poblacion que se le pasa como parametro
def fitnessPromedioPoblacion(poblacion):
    promedio = 0
    for p in poblacion:
        promedio += fitness(binarioDecimal(p))
    promedio = promedio / len(poblacion)
    return promedio

# Calcula el individuo con fitness mas alto en la poblacion que se le pasa como parametro.
def fitnessMaxPoblacion(poblacion):
    max = fitness(binarioDecimal(poblacion[0]))
    for p in poblacion:
        if(max < fitness(binarioDecimal(p))):
            max = fitness(binarioDecimal(p))
    return max

# Calcula el individuo con el peor fitness en la poblacion que se le paso como parametro.
def fitnessMinPoblacion(poblacion):
    min = fitness(binarioDecimal(poblacion[0]))
    for p in poblacion:
        if(min > fitness(binarioDecimal(p))):
            min = fitness(binarioDecimal(p))
    return min

# Te hace un print con los fitness, promedios, maximos y minimos de la poblacion que se la pasa como paramtetro.
def printInfoPoblacion(poblacion):
    print("\n######## Datos de la Poblacion ########\n")
    i=0
    for p in poblacion:
        i += 1
        print("Fitness Vector ", i, ": ",fitness(binarioDecimal(p)))
    print("\nPromedio: ",fitnessPromedioPoblacion(poblacion))
    print("Max: ",fitnessMaxPoblacion(poblacion))
    print("Min: ",fitnessMinPoblacion(poblacion))
    print("\n")

# Devuelve una lista con los pares de vectores a cruzar.
def ruleta(poblacion: Poblacion)-> list[list[Vector]]:

    def calcularPoblacionDecimal(poblacion: Poblacion):
        poblacionDecimal: list[float] = []
        for p in poblacion: 
            poblacionDecimal.append(binarioDecimal(p))
        return poblacionDecimal

    def calcularFitnessAcumulado(poblacionDecimal) -> list[float]:
        fitnessAcumulado: list[float] = []
        fitnessAcumulado.append(0)
        fitnessRelativo = fitnessRelativoPoblacion(poblacionDecimal)
        acumulado: float = 0
        for p in fitnessRelativo:
            acumulado += p
            fitnessAcumulado.append(acumulado)
        return fitnessAcumulado

    def calcularParesPadres(fitnessAcumulado: list[float], poblacionDecimal: list[int]):
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
        
#Calcula el Fitness Relativo de cada individuo de la poblacion(decimal) que se pasa como parametro. 
def fitnessRelativoPoblacion(poblacion: Poblacion) -> list[float]:
    listaFitness: list[float] = []

    for individuo in poblacion:
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

pobl = generarPoblacion(TAMAÑO_DE_LA_POBLACION)
padresPares = ruleta(pobl)

print(padresPares)