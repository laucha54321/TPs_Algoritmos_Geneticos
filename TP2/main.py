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
    posibilidades = []
    soluciones  = []

    def generarPosibilidades(articulos, solucionActual, indice):
        if indice == len(articulos):
            posibilidades.append(solucionActual.copy())
            return

        # No incluir el artículo actual
        generarPosibilidades(articulos, solucionActual, indice + 1)

        # Incluir el artículo actual
        solucionActual.append(articulos[indice])
        generarPosibilidades(articulos, solucionActual, indice + 1)
        solucionActual.pop()  # Backtrack

    generarPosibilidades(problema["articulos"], [], 0)

    for posibilidad in posibilidades:
        valorTotal = sum(art["valor"] for art in posibilidad)
        cantidadRestriccionTotal = sum(art["cantidadRestriccion"] for art in posibilidad)
        if cantidadRestriccionTotal <= problema["restricciones"]["cantidadRestringida"]:
            soluciones.append((posibilidad, valorTotal, cantidadRestriccionTotal))

    return soluciones

def formatearExahustivo(problema):

    soluciones = exhaustivo(problema)
    soluciones_ordenadas = sorted(soluciones, key=lambda x: x[1],reverse=True)
    soluciones_ordenadas = soluciones_ordenadas[:10]  # Tomar las 10 mejores soluciones

    maxid = max(item['id'] for items, _, _ in soluciones_ordenadas for item in items)

    # Build table rows
    tabla = []
    for items, total, cantidad in soluciones_ordenadas:
        ids_included = {item['id'] for item in items}
        fila = ["X" if i in ids_included else "" for i in range(1, maxid + 1)]
        fila.append(total)
        fila.append(cantidad)
        tabla.append(fila)

    # Headers: item IDs + Total
    headers = [str(i) for i in range(1, maxid + 1)] + ["Valor Total"] + ["Cantidad Restriccion"]

    return tabla, headers

def formatearGoloso(problema):
    solucion_greedy = goloso(problema)
    # Construir tabla
    tabla = []
    for articulo in solucion_greedy:
        tabla.append({
            "ID": articulo["id"],
            "Valor": articulo["valor"],
            "Cantidad Restricción": articulo["cantidadRestriccion"],
            "Valor Relativo": articulo["valorRelativo"]
        })
    
    # Calcular totales
    valor_total = sum(a["valor"] for a in solucion_greedy)
    cantidad_total = sum(a["cantidadRestriccion"] for a in solucion_greedy)
    
    # Agregar fila de totales
    tabla.append({
        "ID": "TOTAL",
        "Valor": valor_total,
        "Cantidad Restricción": cantidad_total,
        "Valor Relativo": ""
    })

    return tabla

print('\n')
print("==================================================================")
print("|                    Solucion Unica                              |")
print("|                    Algoritmo Greedy                            |")
print("|                    Problema 1                                  |")
print("==================================================================")
print(tabulate(formatearGoloso(problema1), headers="keys",tablefmt="fancy_grid", floatfmt=".4f"))

tabla, headers = formatearExahustivo(problema1)
print('\n')
print("==================================================================")
print("|                    Conjunto Solucion                           |")
print("|                    Algoritmo Exhaustivo                        |")
print("|                    Problema 1 (10 mejores)                     |")
print("==================================================================")
print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="center", numalign="right"))

print('\n')
print("==================================================================")
print("|                    Solucion Unica                              |")
print("|                    Algoritmo Greedy                            |")
print("|                    Problema 2                                  |")
print("==================================================================")
print(tabulate(formatearGoloso(problema2), headers="keys",tablefmt="fancy_grid", floatfmt=".4f"))

tabla, headers = formatearExahustivo(problema2)
print('\n')
print("==================================================================")
print("|                    Conjunto Solucion                           |")
print("|                    Algoritmo Exhaustivo                        |")
print("|                    Problema 2                                  |")
print("==================================================================")
print(tabulate(tabla, headers, tablefmt="grid", stralign="center", numalign="right"))
print('\n')