from tabulate import tabulate
# Para simplificar consideramos llamamos cantidadRestriccion tanto al volumen como al peso.
problema1 = {
    "restricciones":{
        "cantidadRestringida":4200
    },
    "articulos":[
        {
            "id": 1,
            "valor": 20,
            "cantidadRestriccion": 150
        },
        {
            "id": 2,
            "valor": 40,
            "cantidadRestriccion": 325
        },
        {
            "id": 3,
            "valor": 50,
            "cantidadRestriccion": 600
        },
        {
            "id": 4,
            "valor": 36,
            "cantidadRestriccion": 805
        },
        {
            "id": 5,
            "valor": 25,
            "cantidadRestriccion": 430
        },
        {
            "id": 6,
            "valor": 64,
            "cantidadRestriccion": 1200
        },
        {
            "id": 7,
            "valor": 54,
            "cantidadRestriccion": 770
        },
        {
            "id": 8,
            "valor": 18,
            "cantidadRestriccion": 60
        },
        {
            "id": 9,
            "valor": 46,
            "cantidadRestriccion": 930
        },
        {
            "id": 10,
            "valor": 28,
            "cantidadRestriccion": 353
        }
    ]
}

problema2 = {
    "restricciones":{
        "cantidadRestringida":3000
    },
    "articulos":[
        {
            "id": 1,
            "valor": 72,
            "cantidadRestriccion": 1800
        },
        {
            "id": 2,
            "valor": 36,
            "cantidadRestriccion": 600
        },
        {
            "id": 3,
            "valor": 60,
            "cantidadRestriccion": 1200
        },
    ]  
}

def goloso(problema):
    problema = {
        "restricciones": problema["restricciones"],
        "articulos": problema["articulos"],
        "valorRelativo": []
    }

    def calcularValorRestriccionRelativo(articulo):
        return articulo["valor"] / articulo["cantidadRestriccion"]
    
    def seleccionarArticulos(articulos):
        for articulo in articulos:
            articulo["valorRelativo"] = calcularValorRestriccionRelativo(articulo)
        problema["articulos"] = sorted(articulos, key=calcularValorRestriccionRelativo, reverse=True)

    def resolver(problema):
        restriccionAcumulada = 0
        solucion = []
        for articulo in problema["articulos"]:
            if articulo["cantidadRestriccion"] + restriccionAcumulada <= problema["restricciones"]["cantidadRestringida"]:
                restriccionAcumulada += articulo["cantidadRestriccion"]
                solucion.append(articulo)
        return solucion
                

    seleccionarArticulos(problema["articulos"])

    return resolver(problema)

def exhaustivo(problema):
    print('')

print('\n')
print("==================== Algoritmo Greedy ============================")
print("==================== Problema 1  =================================")
print(tabulate(goloso(problema1), headers="keys",tablefmt="fancy_grid", floatfmt=".4f"))

print('\n')
print("==================== Algoritmo Greedy ============================")
print("==================== Problema 2  =================================")
print(tabulate(goloso(problema2), headers="keys",tablefmt="fancy_grid", floatfmt=".4f"))

print('\n')
print("==================== Algoritmo Exhaustivo ============================")
print("==================== Problema 1  =================================")

