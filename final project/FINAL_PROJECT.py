# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 19:20:21 2021

@author: Güven
"""

import pandas as pd
import tkinter as tk
from tkinter.ttk import Combobox
from PIL import Image,ImageTk
import numpy as np
import folium
import webbrowser

form = tk.Tk()
form.title("Travelling World")
form.geometry("700x600")
form.resizable(False,False)
photo = ImageTk.PhotoImage(Image.open("background2.jpg"))
labelback = tk.Label(form,image=photo)
labelback.pack()

title = tk.Label(form,text = "START LOCATION").place(x=0,y=0)
ct1 = tk.Label(form,text = "City").place(x=0,y=20)

data = pd.read_table("airports.txt",sep=',')

cities = []
for i in range(len(data["city"])):
    cities.append(data["city"][i])

coord_list = []

name_list = []        
curr_coord_lat = []
curr_coord_long = [] 


variable_cities = tk.StringVar()
city_box = Combobox(form,values=cities,height=10,textvariable = variable_cities).place(x = 0,y = 40)

def get1():
    name_list.append(variable_cities.get())
    this_city=data[data["city"]==variable_cities.get()]
    airport = this_city["name"]
    
    variable_airports = tk.StringVar()
    air_box = Combobox(form,values=list(airport),height=10,textvariable = variable_airports).place(x = 220,y = 40)
    air1 = tk.Label(form,text="Airport").place(x=220,y =20)
    def get2():
        
        airp = data[data["name"]==variable_airports.get()]
        
        start_lat = float(airp["lat"])
        start_long = float(airp["long"])
        curr_coord_lat.append(start_lat)
        curr_coord_long.append(start_long)
        
        location = (float(airp["lat"]),float(airp["long"]))
        
        loc1 = tk.Label((form),text="Location").place(x=450, y=20)
        label_loc1 = tk.Label(form,text=location).place(x=450,y=40)
    button_get2 = tk.Button(form,text="Choose",command = get2).place(x = 370,y = 40)
          
button_get1 = tk.Button(form,text="Choose",command = get1).place(x = 160,y = 40)

ct2 = tk.Label(form,text = "Select cities to visit").place(x=0,y=120)
variable_cities2 = tk.StringVar()
city_box2 = Combobox(form,values=cities,height=10,textvariable = variable_cities2).place(x = 0,y =140)

def getct1():
    this_city=data[data["city"]==variable_cities2.get()]
    name_list.append(variable_cities2.get())
    airport2 = this_city["name"]
    
    variable_airports2 = tk.StringVar()
    air_box2 = Combobox(form,values=list(airport2),height=10,textvariable = variable_airports2).place(x = 220,y = 140)
    air1 = tk.Label(form,text="Select the airports you will be visiting").place(x=220,y =120)
    
    def getct2():
        airp1 = data[data["name"]==variable_airports2.get()]
        curr_lat = float(airp1["lat"])
        curr_long = float(airp1["long"])
        curr_coord_lat.append(curr_lat)
        curr_coord_long.append(curr_long)
        location1 = (float(airp1["lat"]),float(airp1["long"]))
        
        loc2 = tk.Label((form),text="Location").place(x=450, y=120)
        label_loc1 = tk.Label(form,text=location1).place(x=450,y=140)
        label_loc1.destroy()
    button_getct2 = tk.Button(form,text="Choose",command = getct2).place(x = 370,y = 140)

button_getct1 = tk.Button(form,text="Choose",command = getct1).place(x = 160,y = 140)

button_continue = tk.Button(form,text="Continue",command = lambda: form.destroy()).place(x=600,y=200)
          
form.mainloop()
##################################################################################################
# https://ichi.pro/tr/python-da-2-cografi-konum-arasindaki-mesafe-nasil-hesaplanir-162644696480676
cities2 = pd.DataFrame(data={
   'City': name_list,
   'Lat' : curr_coord_lat,
   'Lon' : curr_coord_long
})

def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res, 2)
i = 0
distances_km = []
for row in cities2.itertuples(index=False):
   distances_km.append(
       haversine_distance(curr_coord_lat[i], curr_coord_long[i], cities2['Lat'], cities2['Lon'])
   )
   
   i = i +1

cities2['Distance'] = distances_km
###################################################################################################

sort_name = [name_list[0]]
distances_list = []
name = name_list[0]

def sort_airline(name):    
    for i in range(len(cities2["City"])-1):
        name2 = (cities2[cities2["City"] == name])
        dist = list(list(name2["Distance"])[0])
        dist.sort()
        
        j = name_list.index(name)
        name_cont = cities2[cities2["Distance"][j]==dist[1]]
        name = list(name_cont["City"])[0]
        
        if sort_name.count(name)>0:
            for value in range(2,len(dist)):
                
                if sort_name.count(name)>0:
                    name_cont = cities2[cities2["Distance"][j]==dist[value]]
                    name = list(name_cont["City"])[0]
            distances_list.append(dist[value])
            sort_name.append(name)
        
        else:
            distances_list.append(dist[1])
            sort_name.append(name)

sort_airline(name)   
#print(sort_name)
sort_coord = []
latit1 = []
long1 = []

for coord in range(len(sort_name)):
    ct = cities2[cities2["City"] == sort_name[coord]]
    latitude = list(ct["Lat"])[0]
    latit1.append(latitude)
    longitude = list(ct["Lon"])[0]
    long1.append(longitude)
    sort_coord.append((latitude,longitude))

coordinates=sort_coord

m = folium.Map(location=[curr_coord_lat[0], curr_coord_long[0]], zoom_start=4)

#line going from dfw to lga
aline=folium.PolyLine(locations=coordinates,weight=2,color = 'blue')

m.add_children(folium.Marker(location=[curr_coord_lat[0],curr_coord_long[0]], 
                             popup=f"START LOCATION {name_list[0]}", icon=folium.Icon(color="red")))

i = 0
for latit, long, ad in zip(latit1, long1, sort_name):
    
    m.add_children(folium.Marker(location=[latit,long], popup=f"{i+1}. Cıty {sort_name[i]}" ))
    i = i+1
m.add_children(aline)    

m.save('map.html')


form2 = tk.Tk()
form2.title("AVARAGE DİSTANCES(mil)")
form2.geometry("500x500")
form2.resizable(False,False)
photo1 = ImageTk.PhotoImage(Image.open("background4.jpg"))
labelback1 = tk.Label(form2,image=photo1)
labelback1.pack()

for val1 in range(len(distances_list)):
    
    labeldist1 = tk.Label(form2,text=f"{sort_name[val1]}-->{sort_name[val1+1]} => {distances_list[val1]/1.609344} mil ").place(x=0,y=20+(val1*20))

def Link():
    webbrowser.open("map.html")

button1 = tk.Button(form2, text = "OPEN MAP URL", command = Link).place(x=200,y=470)

form2.mainloop()