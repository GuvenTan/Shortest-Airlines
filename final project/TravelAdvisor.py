# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 00:57:28 2021

@author: Güven
"""

import collections 
import csv 
import haversine 
import heapq




Airport = collections.namedtuple('Airport', 'code name country city latitude longitude')

Flight = collections.namedtuple('Flight','origin destination')


Route = collections.namedtuple('Route','price path')





def get_airports(path = 'airports.txt'):

	with open(path,'rt') as fd : 
		reader = csv.reader(fd)
		for row in reader : 
			name = row[1]
			country = row[3]
			code = row[4]	# IATA code (eg, 'ALP' for Aleppo)
			city = row[2]
			latitude = float(row[6])	#Negative is south
			longitude = float(row[7])	#Negative is West 
    
			yield Airport(code,name,country,city,latitude,longitude)


#Make it possible to easily look up airports by IATA code 


AIRPORTS = {airport.code : airport for airport in get_airports()}

def get_flights(path = 'routes.dat'):
	#Return a generator that yields direct Flight Object 

	with open(path,'rt') as fd : 
		reader = csv.reader(fd)
		for row in reader : 
			origin = row[2]		#IATA code for the origin airport 
			destination = row[4]	#IATA code for destination aiport 
			nstops = int(row[7])	#Number of stops ; zero for direct

			if not nstops : 
				yield Flight(origin,destination)