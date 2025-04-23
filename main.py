import random
from guardarVectores import guardarVectoresJson

PROBABILIDAD_DE_CROSSOVER = 0.75
LONGITUD_DE_LOS_VECTORES = 30
TAMAÑO_DE_LA_POBLACION = 10


def generarVector(longitud=30):
# Genera un vector aleatorio de longitud 30 por defecto
    return [random.choice([0, 1]) for _ in range(longitud)]

def generarPoblacion(longitud=10):
# Utiliza la funcion generarVector para generar una poblacion de vectores, longitud en este caso es el tamaño de la poblacion.
    pobl = []
    for i in range(longitud):
        pobl.append(generarVector())
    return pobl

def crossover(vect1, vect2):
# Crossover devuelve los dos pares de vectores resultados del crossover o devuelve los dos padres directamente en caso de no haber crossover.

    def cruzarVector(vect1, vect2):
        # Cruzamos un solo par de vectores en esta funcion
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
    
''' 
Tenemos que Desarollar:
    * La funcion que convierte los vectores (binario) a decimal.
    INPUT: Vector de la forma [0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,1,0,1,0,0,1,1,0] con longitud variable. 
    OUTPUT: El numero correcto en decimal, por ejemplo 10. 

    * La funcion que evalua el fitness con el numero ya en decimal.
    INPUT: Numero Decimal por ejemplo 10.
    OUTPUT: Numero Decimal resultado de aplicar la funcion de fitness.

    * La funcion que obtiene los fitness relativos a la poblacion.
    
    * La ruleta que va a tener distintos pesos para cada vector dependiendo del fitness. 
    INPUT: no estoy seguro como manejar este tema. Podemos usar una tupla por cada uno de poblacion seleccionada? Por ejemplo: {[vect1, 0.35], [vect2, 0.35], [vect3,0.30]}
    Tenemos que tener en cuenta que esta funcion va a tener que poder recibir distintas longitudes de lista ya que la cantidad de vectores seleccionados puede variar.
    OUTPUT: Tuplas con los vectores a cruzar? {[vect1, vect2], [vect2, vect2], [vect3,vect1]}
    

Por ahora creo que eso seria lo mas principal, despues vamos a tener que integrar y loopear todo, pero hagamos el desarollo de estas cosas para una sola instancia y despues vemos como loopeamos llamando a las funciones. 
'''

print(crossover(generarVector(),generarVector()))