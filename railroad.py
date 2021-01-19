import sys
import time
import math
import queue
from tkinter import *

def haversine(long1, lat1, long2, lat2):
    long1 = math.radians(float(long1))
    long2 = math.radians(float(long2))
    lat1 = math.radians(float(lat1))
    lat2 = math.radians(float(lat2))
    dLat = lat2-lat1
    dLong = long2-long1
    radius = 6372.8
    a = math.sin(dLat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dLong/2)**2
    c = math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 2*radius*c

def findPath(city1, city2, romEdges, romCoords, romNames, romMap): #Passes in two IDs as cities
    openset = queue.PriorityQueue()
    openset.put((0, city1))
    opensetlist = {city1:0}
    das = {city1:""}
    closedset = set([city1])
    previous = ""
    count = 0
    city2coords = romCoords.get(city2)
    while not openset.empty():
        entry = openset.get()
        while entry in closedset:
            entry = openset.get()
        node = entry[1]
        currentdistance = entry[0]
        if node == city2:
            file = open("romDict.txt", "w")
            for key in das.keys():
                file.write(key)
                file.write(":")
                file.write(das.get(key))
                file.write("\n")
            previous = node
            file.write("\n")
            returnlist = []
            sumdistance = 0
            while node != city1:
                node = das.get(previous)
                nodecoords = romCoords.get(node)
                newcoords = romCoords.get(previous)
                distance = haversine(nodecoords[1], nodecoords[0], newcoords[1], newcoords[0])
                coord1 = 1200 - int((float(nodecoords[1]) + 60) * -15)
                coord2 = 700 - int((float(nodecoords[0]) - 14) * 15)
                coord3 = 1200 - int((float(newcoords[1]) + 60) * -15)
                coord4 = 700 - int((float(newcoords[0]) - 14) * 15)
                romMap.create_line(coord1, coord2, coord3, coord4, fill="red", width=2)
                returnlist.append((node, previous, distance))
                sumdistance += distance
                previous = node
                romMap.update()
            returnlist = returnlist[::-1]
            romMap.mainloop()
            for line in returnlist:
                print("Travel from ", line[0], " to ", line[1], ". Distance is ", line[2], " km.")
            print("Sum of distances: ", sumdistance, " km")
            return
        if romEdges.get(node):
            for edge in romEdges.get(node):
                if edge not in closedset:
                    nodecoords = romCoords.get(node)
                    newcoords = romCoords.get(edge)
                    distance = haversine(nodecoords[1], nodecoords[0], newcoords[1], newcoords[0])
                    coord1 = 1200 - int((float(nodecoords[1]) + 60) * -15)
                    coord2 = 700 - int((float(nodecoords[0]) - 14) * 15)
                    coord3 = 1200 - int((float(newcoords[1]) + 60) * -15)
                    coord4 = 700 - int((float(newcoords[0]) - 14) * 15)
                    estimate = haversine(nodecoords[1], nodecoords[0], city2coords[1], city2coords[0])
                    if edge not in opensetlist.keys():
                        openset.put((currentdistance+distance, edge))
                        opensetlist[edge] = currentdistance+distance
                        das[edge] = node
                        romMap.create_line(coord1, coord2, coord3, coord4, fill="blue", width=2)
                    elif opensetlist.get(edge) > currentdistance+distance:
                        opensetlist[edge] = currentdistance+distance
                        openset.put((currentdistance+distance, edge))
                        das[edge] = node
        closedset.add(node)
        if previous:
            for edge in romEdges.get(previous):
                nodecoords = romCoords.get(previous)
                newcoords = romCoords.get(edge)
                coord1 = 1200 - int((float(nodecoords[1]) + 60) * -15)
                coord2 = 700 - int((float(nodecoords[0]) - 14) * 15)
                coord3 = 1200 - int((float(newcoords[1]) + 60) * -15)
                coord4 = 700 - int((float(newcoords[0]) - 14) * 15)
                romMap.create_line(coord1, coord2, coord3, coord4, fill="green", width=2)
        previous = node
        if count % 10000 == 0:
            #romMap.update()
            print(count)
        count+=1
    file = open("romDict.txt", "w")
    for key in das.keys():
        file.write(key)
        file.write(":")
        file.write(das.get(key))
        file.write("\n")

def main():
    nameFile = open("rrNodeCity.txt", "r+")
    edgesFile = open("rrEdges.txt", "r+")
    coordFile = open("rrNodes.txt", "r+")
    romNames = {}
    romEdges = {}
    romCoords = {}
    nameToId = {}
    maxcoord1 = -1000
    mincoord1 = 1000
    maxcoord2 = -1000
    mincoord2 = 1000
    input = sys.argv[1:]
    for line in nameFile:
        name = line.strip("\n")
        romNames[name[:7]] = name[8:]
        nameToId[name[8:]] = name[:7]
    for line in edgesFile:
        edge = line.strip("\n")
        if edge[:7] not in romEdges.keys():
            romEdges[edge[:7]] = [edge[8:]]
        else:
            romEdges[edge[:7]].append(edge[8:])
        if edge[8:] not in romEdges.keys():
            romEdges[edge[8:]] = [edge[:7]]
        else:
            romEdges[edge[8:]].append(edge[:7])
    for line in coordFile:
        coordinates = line.strip("\n")
        coord1 = float(coordinates[8:17])
        coord2 = float(coordinates[18:])
        if coord1 > maxcoord1:
            maxcoord1 = coord1
        if coord2 > maxcoord2:
            maxcoord2 = coord2
        if coord1 < mincoord1:
            mincoord1 = coord1
        if coord2 < mincoord2:
            mincoord2 = coord2
        romCoords[coordinates[:7]] = (coordinates[8:17], coordinates[18:])
    frame = Tk()
    romMap = Canvas(frame, width=1520, height=1280)
    romMap.pack()
    lines = {}
    for entry in romEdges.keys():
        listOfConnections = romEdges.get(entry)
        city1coords = romCoords.get(entry)
        count = 0
        lines[entry] = {}
        for x in range(0, len(listOfConnections)):
            city2coords = romCoords.get(listOfConnections[count])
            coord1 = 1200 - int((float(city1coords[1])+60) * -15)
            coord2 = 700 - int((float(city1coords[0])-14) * 15)
            coord3 = 1200 - int((float(city2coords[1])+60) * -15)
            coord4 = 700 - int((float(city2coords[0])-14) * 15)
            line = romMap.create_line(coord1, coord2, coord3, coord4)
            lines[entry][listOfConnections[count]] = line
            count += 1
    if len(input) == 2:
        city1 = str(nameToId.get(input[0]))
        city2 = str(nameToId.get(input[1]))
    elif len(input) == 3:
        if nameToId.get(input[0] + " " + input[1]):
            city1 = str(nameToId.get(input[0] + " " + input[1]))
            city2 = str(nameToId.get(input[2]))
        else:
            city1 = str(nameToId.get(input[0]))
            city2 = str(nameToId.get(input[1] + " " + input[2]))
    else:
        city1 = str(nameToId.get(input[0] + " " + input[1]))
        city2 = str(nameToId.get(input[2] + " " + input[3]))
    findPath(city1,city2, romEdges, romCoords, romNames, romMap)

if __name__ == "__main__":
    main()
    print(haversine(-77.016880, 38.884060, -118.230620, 34.061870))

#Part 2:
#1)  Adapt your code to accept two cities on the command line and find the shortest path between them.
#    Your code should display the sequence of cities between the two (give station ID when city not available).
#    To the right of each city (other than the first one), the distance to that city from the prior one should be displayed.
#    The total path length should be printed at the end.
#2)  If not already done, update your code from step 1 to use A*.
#    Each time a vertex goes to the open set, it should be marked in some color (say blue).
#    Each time a vertex goes to the closed set, it should be marked in some color (say green).
#    The shortest path should be marked in red.
#3)  Update your code from Part 2 to use the data for North America
#tk.update_idletasks()
#    tk.update()