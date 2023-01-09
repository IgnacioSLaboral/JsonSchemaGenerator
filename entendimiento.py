import json
from jsonschema import Draft7Validator, ErrorTree, validate, SchemaError, ValidationError
import collections


#Recibo las keys por las que debo pasar y los tipos de dichas keys, devuelvo el nivel en el cual se debe agregar la información
def setear_nivel(key, tipos, current_level, ultimo):
    """print(" pruebita ")
    print(key)
    print(current_level)
    print(tipos)
    print(" ")"""
    if ultimo:
        #print("entro aca")
        if tipos[key] == "Object[]":
            current_level = current_level[key.split(".")[-1]]["items"]
        elif tipos[key] == "Object":
            current_level = current_level[key.split(".")[-1]]
    else:
        #print("entro aca2")
        if tipos[key] == "Object[]":
            current_level = current_level[key.split(".")[-1]]["items"]["properties"]
            #print(current_level)
        elif tipos[key] == "Object":
            current_level = current_level[key.split(".")[-1]]["properties"]


    return current_level


def generate_json_schema(keys, mandatory, types, enum):
    # Creamos el diccionario del esquema JSON
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "required" : []
    }
    tipos = {}
    for k in range(0,len(keys)):
        tipos[keys[k]] = types[k]

    # Iteramos sobre cada key y construimos el esquema
    for key, is_mandatory, data_type, enum in zip(keys, mandatory, types, enum):
        current_level = schema["properties"]
        listaKeys = key.split(".")
        print(listaKeys)
        n = listaKeys[0]
        # Si el largo de la lista es igual a 1, significa que estamos en la base del schema, por lo tanto
        # No debemos hacer cambios sobre ListaKeys[-1], de esta forma diferenciamos los que si son hijos de los que son padres
        if len(listaKeys)==1:
            if data_type == "String" or data_type == "Number":
                current_level[listaKeys[0]] = {
                    "type": data_type.lower()
                }
            elif data_type == "Object":
                current_level[listaKeys[0]] = {
                    "type": data_type.lower(),
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            elif data_type == "Object[]":
                current_level[listaKeys[0]] = {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [],
                        "properties": {}
                        ,
                        "additionalProperties": False
                    }
                }

            elif data_type == "Enum":
                current_level["properties"][listaKeys[0]] = {
                     "enum": enum
                }

            elif data_type == "Boolean":
                current_level["properties"][listaKeys[0]] = {
                    "type": "boolean"
                }

            if is_mandatory:
                schema["required"].append(listaKeys[0])

        #Si son hijos, hacemos el mismo proceso
        else:
            for nivel in range(0,len(listaKeys)-1):
                if nivel != 0:
                    n = n + "." + listaKeys[nivel]
                if len(listaKeys)-2 == nivel:
                    current_level = setear_nivel(n, tipos, current_level,True)
                else:
                    current_level = setear_nivel(n, tipos, current_level,False)
            #current_level = schema["properties"]["data"]["items"]
            if data_type == "String" or data_type == "Number":
                current_level["properties"][listaKeys[-1]] = {
                    "type" : data_type.lower()
                }
            elif data_type == "Object":
                current_level["properties"][listaKeys[-1]] = {
                    "type": data_type.lower(),
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            elif data_type == "Object[]":
                current_level["properties"][listaKeys[-1]] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [],
                    "properties": {}
                    ,
                    "additionalProperties": False
                }
            }

            elif data_type == "Enum":
                current_level["properties"][listaKeys[-1]] = {
                     "enum": enum
                }

            elif data_type == "Boolean":
                current_level["properties"][listaKeys[-1]] = {
                    "type": "boolean"
                }



            if is_mandatory:
                current_level["required"].append(listaKeys[-1])

    # Retornamos el esquema
    return schema



keys = ["data", "data.id", "data.address", "data.address.state", "data.address.state.id", "data.address.state.name", "data.address.city", "data.address.zipCode", "data.address.country", "data.address.country.id", "data.address.country.name", "data.address.geolocation", "data.address.geolocation.latitude", "data.address.geolocation.longitude", "data.distance", "data.description", "data.estimatedWaitingTime", "data.availableServices", "data.availableServices.id", "data.isOpen", "data.hasDigitalAppointment", "data.branchType", "data.branchType.id", "data.branchType.description", "data.atmsInBranch", "data.atmsInBranch.id", "data.atmsInBranch.number", "data.links", "data.links.id", "data.links.rel", "data.links.href", "data.links.method"]
#keys = ["data", "data.id"]
mandatory = [True, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, False, False, True, False, False, False, True, False, False, False, False, True, True, True, True, True]
#mandatory = [True, True ]
types = ["Object[]", "String", "Object", "Object", "String", "String", "String", "String", "Object", "String", "String", "Object", "Number", "Number", "Number", "String", "Number", "Object[]", "String", "Boolean", "Boolean", "Object", "Enum", "String", "Object[]", "Enum", "Number", "Object[]", "String", "String", "String", "Enum"]
#types = ["Object[]", "String"]
enum = ["","","","","","","","","","","","","","","","","","","","","","",["Pepito1","Pepito2"],"","",["prueba","prueba2"],"","","","","",["Pepito","pepito2"]]




#---------------------------GENERACION SCHEMA--------------------------

schema = generate_json_schema(keys,mandatory,types,enum)
print(schema)




#------------------------------VALIDACION-------------------------------



f = open('response.json')

# returns JSON object as
# a dictionary
data = json.load(f)

validator = Draft7Validator(schema)
#errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

errors = validator.iter_errors(data)  # get all validation errors
for error in errors:
    print(error.message)
    print('.'.join(str(v) for v in error.path))
    print(error.validator)
    print('------')

