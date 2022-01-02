#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan David Monsalve
"""

import requests


def PokeAPI(url, params):
    """Metodo que realiza consumo REST tipo GET a la API de PokeRest. Retorna
    un objeto tipo JSON. 
    Parametros: 
        url: URL de la API que se desea consultar
        params: parametros para la consulta
    Retorna:
    JSON object con todos los pokemons registrados por la API
    """
    r = requests.get(url, params)
    return r.json()


def ObtenerCantidadPokemonesConAT_y_2A(pokemons):
    """Metodo que calcula la cantidad de pokemones que cumplan con tener 2 a´s 
    como minimo y contenga "at" dentro de su nombre. Retorna la cantidad de pokemones
    que cumplen con las condiciones anteriormente mencionadas. 
    Parametros: 
        pokemons: listado de todos los pokemones encontrados por la API
    Retorna:
        int: cantidad de pokemones que cumplen las condiciones
    """
    counter = 0
    for pokemon in pokemons:
        sortedWord = sorted(pokemon["name"])
        if(sortedWord[0] == "a" and sortedWord[1] == "a" and "at" in pokemon["name"]):
            counter+=1
    return counter

def ObtenerCantidadEspeciesRaichuPuedeProcrear(eggGroups):
    """Metodo que calcula la cantidad de especies que el pokemon Raichu
    puede procrear. 
    Parametros: 
        eggGroups: listado de todos los egg groups a los que pertenece Raichu.
    Retorna:
        int: cantidad de pokemones que craichu puede procrear
    """
    counter = 0
    dic = {}
    for egg_group in eggGroups:
        speciesFromEggGroup = PokeAPI(egg_group["url"],None)["pokemon_species"]
        for species in speciesFromEggGroup: 
            name = species["name"]
            if(name!= "raichu" and name not in dic):
                dic[name] = 1
                counter+=1
    return counter

def ObtenerMaximoyMinimoPesoPokemonesTipoFightingGeneracionUno(fightingList, FirstGenList):
    """Metodo que calcula el peso maximo y minimo encontrados entre todos los pokemones
    que sean de typo Fighting, sean de primera generacion, y tengan un id menor a 151.
    Parametros: 
        fightingList: listado de todos los pokemones que son de tipo fighting.
        FirstGenList: listado de todos los pokemones que son de primera generacion.
    Retorna:
        list: listado de 2 valores que contiene el peso maximo y minimo encontrados.
    """
    Weightlist = []
    dicPokemonsWithAllConditions = {}
    for pokemon in fightingList:
        detail = pokemon["pokemon"]
        pokemonId = int(detail["url"].split("/")[6])
        if(pokemonId <= 151 and detail["name"] not in dicPokemonsWithAllConditions):
            dicPokemonsWithAllConditions[detail["name"]] = pokemonId
            
    for pokemon in FirstGenList:
        pokemonId = int(pokemon["url"].split("/")[6])
        if(pokemonId <= 151 and pokemon["name"] not in dicPokemonsWithAllConditions):
            dicPokemonsWithAllConditions[pokemon["name"]] = pokemonId
                    
    minWeight= 10000000000
    maxWeight= 0
    
    for pokemon in dicPokemonsWithAllConditions: 
        pokemonId = dicPokemonsWithAllConditions[pokemon] 
        URL = "https://pokeapi.co/api/v2/pokemon/"+str(pokemonId)+"/"
        pokemonsWeight = PokeAPI(URL,None)["weight"]
        if(pokemonsWeight < minWeight):
            minWeight = pokemonsWeight
        if(pokemonsWeight > maxWeight):
            maxWeight = pokemonsWeight
            
            
    return [maxWeight, minWeight]

  

def mostrar_menu():
    """Imprime las opciones de ejecucion solicitadas en la prueba tecnica.
    """
    print("\nSeleccione los resultados que desea visualizar")
    print("1. Obten cuantos pokemones poseen en sus nombres “at” y tienen 2 “a” en su nombre, incluyendo la primera del “at”.")
    print("2. ¿Con cuantas especies de pokemon puede procrear raichu? (2 Pokémon pueden procrear si están dentro del mismo egg group). Tu respuesta debe ser un numero.")
    print("3. Entrega el maximo y minimo peso de los pokemon de tipo fighting de primera generacion (cuyo id sea menor o igual a 151). Tu respuesta debe ser una lista con el siguiente formato: [1234, 12], en donde 1234 corresponde al maximo peso y 12 al minimo.")
    print("4. Salir de la aplicacion")
    
def iniciar_aplicacion():
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("- - - - - - - - - - - - - Juan David Monsalve - - - - - - - - - - - - -")
    print("- - - - - - - - - - - - - HOUM - Prueba tecnica - - - - - - - - - - - -")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    """Ejecuta el programa para el usuario."""
    continuar = True
    mostrar_menu()
    while continuar:
        opcion_seleccionada = int(input("Por favor seleccione una opcion: "))
        if opcion_seleccionada == 1:
            URL = "https://pokeapi.co/api/v2/pokemon"
            PARAMS = {'limit':10000000}
            allPokemons = PokeAPI(URL,PARAMS)["results"]
            cantidad = ObtenerCantidadPokemonesConAT_y_2A(allPokemons)
            print(cantidad)
        elif opcion_seleccionada == 2:
            URL = "https://pokeapi.co/api/v2/pokemon-species/26/"
            raichuEggGroups = PokeAPI(URL,None)["egg_groups"]
            cantidad = ObtenerCantidadEspeciesRaichuPuedeProcrear(raichuEggGroups)
            print(cantidad)
        elif opcion_seleccionada == 3:
            URL = "https://pokeapi.co/api/v2/type/2"
            pokemonsTypeFighting = PokeAPI(URL,None)["pokemon"]
            URL = "https://pokeapi.co/api/v2/generation/1/"
            pokemonsFirstGen = PokeAPI(URL,None)["pokemon_species"]
            lista = ObtenerMaximoyMinimoPesoPokemonesTipoFightingGeneracionUno(pokemonsTypeFighting,pokemonsFirstGen)
            print(lista)
        elif opcion_seleccionada == 4:
            continuar = False
        else:
            print("Por favor seleccione una opcion valida.")


# PROGRAMA PRINCIPAL
iniciar_aplicacion()
    
    
    
    
    
    
    
