import random
from guardarVectores import guardarVectoresJson

PROBABILIDAD_DE_CROSSOVER = 0.75
LONGITUD_DE_LOS_VECTORES = 30
TAMAÑO_DE_LA_POBLACION = 10
COEF = 2**30 - 1


# Genera un vector aleatorio de longitud 30 por defecto
def generarVector(longitud=30):
    return [random.choice([0, 1]) for _ in range(longitud)]

# Utiliza la funcion generarVector para generar una poblacion de vectores, longitud en este caso es el tamaño de la poblacion.
def generarPoblacion(longitud=10):
    pobl = []
    for i in range(longitud):
        pobl.append(generarVector())
    return pobl

# Crossover devuelve los dos pares de vectores resultados del crossover o devuelve los dos padres directamente en caso de no haber crossover.
def crossover(vect1, vect2):

    # Cruzamos un solo par de vectores en esta funcion
    def cruzarVector(vect1, vect2):
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
def binarioDecimal(vector):
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


''' 
Tenemos que Desarollar:
    * La funcion que obtiene los fitness relativos a la poblacion.
    
    * La ruleta que va a tener distintos pesos para cada vector dependiendo del fitness. 
    INPUT: no estoy seguro como manejar este tema. Podemos usar una tupla por cada uno de poblacion seleccionada? Por ejemplo: {[vect1, 0.35], [vect2, 0.35], [vect3,0.30]}
    Tenemos que tener en cuenta que esta funcion va a tener que poder recibir distintas longitudes de lista ya que la cantidad de vectores seleccionados puede variar.
    OUTPUT: Tuplas con los vectores a cruzar? {[vect1, vect2], [vect2, vect2], [vect3,vect1]}
    

Por ahora creo que eso seria lo mas principal, despues vamos a tener que integrar y loopear todo, pero hagamos el desarollo de estas cosas para una sola instancia y despues vemos como loopeamos llamando a las funciones. 
'''

# Generar un vector binario
# vector = generarVector(LONGITUD_DE_LOS_VECTORES)

# Convertir binario a decimal
# x_decimal = binarioDecimal(vector)

# Mostrar el vector binario ysu conversion a decimal
# print(f"binario: {vector}")
# print(f"decimal: {x_decimal}")

# Calcular fitness
# fitness_value = fitness(x_decimal)

# Mostrar el fitness calculado
#print(f"Fitness de {x_decimal} es: {fitness_value}")


pobl = generarPoblacion(TAMAÑO_DE_LA_POBLACION)
printInfoPoblacion(pobl)

#print(crossover(generarVector(),generarVector()))