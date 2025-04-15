import json
import datetime

def guardarVectoresJson(lista_vectores, nombre_base="vectores", formato_compacto=True):
    """
    Guarda una lista de vectores en un archivo JSON con timestamp en el nombre.
    
    Args:
        lista_vectores (list): Lista de vectores a guardar.
        nombre_base (str): Nombre base del archivo JSON. Por defecto es "vectores".
        formato_compacto (bool): Si es True, guarda el JSON sin formato de líneas nuevas.
        
    Returns:
        str: Nombre del archivo generado si la operación fue exitosa, None en caso contrario.
    """
    try:
        # Obtener fecha y hora actual para el nombre del archivo
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{nombre_base}_{timestamp}.json"
        
        with open(nombre_archivo, 'w') as archivo:
            if formato_compacto:
                # Formato compacto sin saltos de línea adicionales
                json.dump(lista_vectores, archivo, indent=None, separators=(',', ':'))
            else:
                # Formato con indentación para mejor legibilidad
                json.dump(lista_vectores, archivo, indent=4)
                
        print(f"Vectores guardados exitosamente en '{nombre_archivo}'")
        return nombre_archivo
    except Exception as e:
        print(f"Error al guardar los vectores: {e}")
        return None