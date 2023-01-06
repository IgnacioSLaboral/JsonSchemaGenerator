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

#schema["properties"]["data"]["items"]["properties"]["adress"]["properties"]["agregar"]


def generate_json_schema(keys, mandatory, types):
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
    for key, is_mandatory, data_type in zip(keys, mandatory, types):

        # Si la key es "data", es un array y cada elemento es un objeto
        if key == "data":
            schema["properties"][key] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["data"],
                    "properties": {}
                }
            }
        if key != "data":
            current_level = schema["properties"]
            listaKeys = key.split(".")
            n = listaKeys[0]
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
                    "required": []
                }
            elif data_type == "Object[]":
                current_level["properties"][listaKeys[-1]] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [],
                    "properties": {}
                }
            }

            if is_mandatory:
                current_level["required"].append(listaKeys[-1])





            """schema["properties"][key]["items"]["properties"]["id"] = {
                "type" : "string"
            }
            schema["properties"][key]["items"]["required"].append("id")"""

            """listaKeys = key.split(".")
            for keyAnt in listaKeys:"""
            #print(schema)


    # Retornamos el esquema
    return schema

keys = ["data", "data.id", "data.address", "data.address.state", "data.address.state.id", "data.address.state.name", "data.address.city", "data.address.zipCode", "data.address.country", "data.address.country.id", "data.address.country.name", "data.address.geolocation", "data.address.geolocation.latitude", "data.address.geolocation.longitude", "data.distance", "data.description", "data.estimatedWaitingTime", "data.availableServices", "data.availableServices.id", "data.isOpen", "data.hasDigitalAppointment", "data.branchType", "data.branchType.id", "data.branchType.description", "data.atmsInBranch", "data.atmsInBranch.id", "data.atmsInBranch.number", "data.links", "data.links.id", "data.links.rel", "data.links.href", "data.links.method"]
#keys = ["data", "data.id"]
mandatory = [True, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, False, False, True, False, False, False, True, False, False, False, True, True, True, True, True]
#mandatory = [True, True ]
types = ["Object[]", "String", "Object", "Object", "String", "String", "String", "String", "Object", "String", "String", "Object", "Number", "Number", "Number", "String", "Number", "Object[]", "String", "Boolean", "Boolean", "Object", "Enum", "String", "Object[]", "Enum", "Number", "Object[]", "String", "String", "String", "Enum"]
#types = ["Object[]", "String"]
schema = generate_json_schema(keys,mandatory,types)
print(schema)


