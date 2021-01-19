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

def findPath(city1, city2, romEdges, romCoords, romNames, romMap):
    path = []
    openset = queue.PriorityQueue()
    openset.put((0, city1))
    opensetlist = {city1:0}
    das = {city1:""}
    closedset = set([city1])
    #for entry in romCoords.keys():
    #  print(entry, "Item: ", romCoords.get(entry))
    while not openset.empty():
        entry = openset.get()
        node = entry[1]
        nodeletter = entry[1][0]
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
                returnlist.append((node, previous, distance))
                sumdistance += distance
                previous = node
            returnlist = returnlist[::-1]
            for line in returnlist:
                print("Travel from ", line[0], " to ", line[1], ". Distance is ", line[2], " km.")
            print("Sum of distances: ", sumdistance, " km")
            return
        if romEdges.get(nodeletter):
            for edge in romEdges.get(nodeletter):
                if edge not in closedset:
                    nodecoords = romCoords.get(node)
                    newcoords = romCoords.get(romNames.get(edge))
                    distance = haversine(nodecoords[1], nodecoords[0], newcoords[1], newcoords[0])
                    if romNames.get(edge) not in opensetlist.keys():
                        openset.put((distance+currentdistance, romNames.get(edge)))
                        opensetlist[romNames.get(edge)] = distance+currentdistance
                        das[romNames.get(edge)] = node
                    elif opensetlist.get(romNames.get(edge)) > distance+currentdistance:
                        opensetlist[romNames.get(edge)] = distance+currentdistance
                        openset.put((distance+currentdistance, romNames.get(edge)))
                        das[romNames.get(edge)] = node
        closedset.add(node[0])

def main():
    input = sys.argv[1::]
    romNameFile = open("romNames.txt", "r+")
    romEdgesFile = open("romEdges.txt", "r+")
    romCoordFile = open("romNodes.txt", "r+")
    romNames = {}
    romEdges = {}
    romCoords = {}
    for line in romNameFile:
        name = line.strip("\n")
        romNames[name[0]] = name
    for line in romEdgesFile:
        edge = line.strip("\n")
        if edge[0] not in romEdges.keys():
            romEdges[edge[0]] = [edge[2]]
        else:
            romEdges[edge[0]].append(edge[2])
        if edge[2] not in romEdges.keys():
            romEdges[edge[2]] = [edge[0]]
        else:
            romEdges[edge[2]].append(edge[0])
    for line in romCoordFile:
        coords = line.strip("\n")
        romCoords[romNames.get(coords[0])] = (coords[2:9], coords[10:])
    #for entry in romCoords.keys():
    #    print(entry, "Item: ", romEdges.get(entry))
    ########################################################################################
    frame = Tk()
    romMap = Canvas(frame, width=1000, height=1000)
    romMap.pack()
    #Create Cities Labels
    for entry in romCoords.keys():
        citycoords = romCoords.get(entry)
        romMap.create_text(int((float(citycoords[1])%20)*100), int(500-(float(citycoords[0])%43)*100), text=entry)
    #Create Lines
    for entry in romEdges.keys():
        listOfConnections = romEdges.get(entry)
        city1coords = romCoords.get(romNames.get(entry))
        count = 0
        for x in range (0, len(listOfConnections)):
            city2name = romNames.get(listOfConnections[count])
            count+=1
            city2coords = romCoords.get(city2name)
            romMap.create_line(int((float(city1coords[1]) % 20) * 100), int(500-(float(city1coords[0]) % 43) * 100), int((float(city2coords[1]) % 20) * 100), int(500-(float(city2coords[0]) % 43) * 100))
    frame.mainloop()
    sumdistance = 0
    ########################################################################################
    #for entry in romEdges.keys():
        #count = 0
        #listOfConnections = romEdges.get(entry)
        #city1 = romCoords.get(romNames.get(entry))
        #while len(listOfConnections) > count:
        #    city2name = romNames.get(listOfConnections[count])
        #    city2 = romCoords.get(city2name)
        #    distance = haversine(city1[1],city1[0],city2[1],city2[0])
        #    sumdistance+=distance
            #print("Distance from ",city1," to ",city2,": ", distance, "km")
        #    count+=1
        #count = 0
    #print("Sum of distances: ", sumdistance, " km")
    #print(input[0])
    #print(input[1])
    findPath(input[0], input[1], romEdges, romCoords, romNames, romMap)

if __name__ == "__main__":
    main()
