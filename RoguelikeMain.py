import random

#set windowsize
from os import system
system('mode con: cols=150 lines=60')
"""
Student Name:    Mark Moulton
Program Title:  First semester Roguelike 
Description:    An example of where my skill level is during the start of school, fall 2020 semester
                to be rewritten each semester to keep track of my improvement
"""
#initialize global variables
global_wall = " "
global_floor = "."
global_player = "@"
global_kobold = "k"
global_stairUp = "U"
global_stairDown = "D"
global_dungeonArray = [[]]
global_roomArray = []
global_floorArray = []
global_stairDownArray = []
global_stairUpArray = []
global_enemyArray = []
global_playerLocation = []

global_turnCounter = 0

global_playerMaxHP = 15
global_playerCurrentHP = 15
global_playerDamage = 5

global_healthRegenRate = 10

global_enemyMaxHP = 5
global_enemyCurrentHP = 5
global_enemyDamage = 3

global_width = 100
global_height = 50

global_min_rooms = 7
global_max_rooms = 15

global_min_room_size = 3
global_max_room_size = 15

def generateDungeon(width, height):
    global global_dungeonArray
    #initialize map with just walls
    global_dungeonArray = [[global_wall for x in range(width)] for y in range(height)]
    #Create x amount of rooms within a 2D array
    global_dungeonArray = generateRooms(global_dungeonArray)
    #Create hallways to connect between each room
    global_dungeonArray = generateHallways(global_dungeonArray, global_roomArray)
    #Create a stairway to the next floor
    global_dungeonArray = generateStairway(global_dungeonArray, global_roomArray)
    #spawn player
    global_dungeonArray = spawnPlayer(global_dungeonArray, global_roomArray)
    #spawn enemies
    global_dungeonArray = spawnEnemies(global_dungeonArray, global_roomArray)
    #initialize all arrays to track tiles
    trackAllTiles(global_dungeonArray)


def generateRooms(dungeonArray):
    #random number of rooms
    numberOfRooms = random.randint(global_min_rooms, global_max_rooms)
    #for each room
    for rooms in range(numberOfRooms):
        #get a random size
        roomSizeX = random.randint(global_min_room_size, global_max_room_size)
        roomSizeY = random.randint(global_min_room_size, global_max_room_size)
        #get a random x,y coordinate
        roomStartPosX = random.randint(1,len(dungeonArray))
        roomStartPosY = random.randint(1, len(dungeonArray[0]))
        #make sure the room will fit inside the dungeon
        if roomStartPosX + roomSizeX < len(dungeonArray) and roomStartPosY + roomSizeY < len(dungeonArray[0]):
            #for each tile in the x coordinate
            for xsize in range(roomSizeX):
                #run through each y coordinate
                for ysize in range(roomSizeY):
                    #and place a floor tile at their combined x,y coordinate
                    dungeonArray[roomStartPosX + xsize][roomStartPosY + ysize] = global_floor
            #store the room by its initial tile
            addRoom(roomStartPosX, roomStartPosY, rooms, roomSizeX, roomSizeY)
        #else:
            #if the room size doesn't fit, just put a single floor tile at the starting position
            #dungeonArray[roomStartPosX-1][roomStartPosY-1] = global_floor
        #store the room by its initial tile
        #addRoom(roomStartPosX, roomStartPosY)
    return dungeonArray

def generateHallways(dungeonArray, roomArray):
    #for each room in the array (minus 1 because once the second last room connects to the last room, its all connected)
    for room in range(len(roomArray) - 1):
        #if the x coordinates of a room don't line up
        if getX(roomArray[room]) != getX(roomArray[room+1]):
            #decide which room has a lower x coordinate (this < that)
            if getX(roomArray[room]) < getX(roomArray[room+1]):
                thisSpace = roomArray[room]
                thatSpace = roomArray[room+1]
            else:
                thisSpace = roomArray[room+1]
                thatSpace = roomArray[room]
            #while x coordinate of this < that, set the next x coordinate to a floor and set this to the next x coordinate
            while getX(thisSpace) != getX(thatSpace):
                dungeonArray[getX(thisSpace)+1][getY(thisSpace)] = global_floor
                thisSpace = str(getX(thisSpace)+1) + "," + str(getY(thisSpace))
        #if y coordinates don't line up
        if getY(roomArray[room]) != getY(roomArray[room+1]):
            #set lower y to this
            if getY(roomArray[room]) < getY(roomArray[room+1]):
                thisSpace = roomArray[room]
                thatSpace = roomArray[room+1]
            else:
                thisSpace = roomArray[room+1]
                thatSpace = roomArray[room]
            #line up x coordinates because we've already done that, otherwise it starts from the initial position again!
            if getX(thisSpace) < getX(thatSpace):
                thisSpace = str(getX(thatSpace)) + "," + str(getY(thisSpace))
            #place floors and move closer to that
            while getY(thisSpace) != getY(thatSpace):
                dungeonArray[getX(thisSpace)][getY(thisSpace)+1] = global_floor
                thisSpace = str(getX(thisSpace)) + "," + str(getY(thisSpace)+1)
    return dungeonArray

def generateStairway(dungeonArray, roomArray):
    #set stairs to the final room
    stairs = roomArray[-1]
    #move x,y coordinate out 1 so it won't spawn in a corner every single time
    stairs = str(getX(stairs) + random.randint(0,getRoomSizeX(roomArray[-1])-1)) + "," + str(getY(stairs) + random.randint(0,getRoomSizeY(roomArray[-1])-1))
    #change the tile at x,y of stairs to be a staircase in the dungeon array
    dungeonArray[getX(stairs)][getY(stairs)] = global_stairDown
    return dungeonArray

def spawnPlayer(dungeonArray, roomArray):
    #set spawn point to first room
    playerSpawn = roomArray[0]
    #move x,y coordinates out 1 to avoid corner spawns
    playerSpawn = str(getX(playerSpawn) + random.randint(0,getRoomSizeX(roomArray[0])-1)) + "," + str(getY(playerSpawn) + random.randint(0,getRoomSizeY(roomArray[0])-1))
    #change tile at x,y of stairs to be the player
    dungeonArray[getX(playerSpawn)][getY(playerSpawn)] = global_player
    return dungeonArray

def spawnEnemies(dungeonArray, roomArray):
    #for each room other than first and last
    for room in range(1, len(roomArray) - 1):
        #set spawn point
        enemySpawn = roomArray[room]
        #randomly set x,y within room size
        enemySpawn = str(getX(roomArray[room]) + random.randint(0,getRoomSizeX(roomArray[room])-1)) + "," + str(getY(roomArray[room]) + random.randint(0,getRoomSizeY(roomArray[room])-1))
        #change tile at x,y to be an enemy
        dungeonArray[getX(enemySpawn)][getY(enemySpawn)] = global_kobold
    return dungeonArray

def trackAllTiles(dungeonArray):
    #run through dungeon array and get the position of everything
    for y in range(len(dungeonArray)):
        for x in range(len(dungeonArray[y])):
            #get and set thisTiles x,y
            thisTile = str(x) + "," + str(y)
            tile = dungeonArray[y][x]
            #sort all tiles into their appropriate global arrays to track positions of everything
            if tile == global_player:
                #initialize player with extra stats
                global_playerLocation.append(thisTile  + "," + str(global_playerMaxHP) + "," + str(global_playerCurrentHP) + "," + str(global_playerDamage))
            elif tile == global_kobold:
                #initialize enemies with extra stats
                global_enemyArray.append(thisTile + "," + str(global_enemyMaxHP) + "," + str(global_enemyCurrentHP) + "," + str(global_enemyDamage))
            elif tile == global_stairDown:
                global_stairDownArray.append(thisTile)
            elif tile == global_stairUp:
                global_stairUpArray.append(thisTile)
            #if tile is not a wall, add it to the floor (this accounts tiles player and enemies are standing on)
            if tile != global_wall:
                global_floorArray.append(thisTile)

def displayDungeon(dungeonArray):
    print("\n Semester 1 Roguelike \n")
    #for every y coordinate in every x coordinate, print the tile! idk why 2d arrays display [y][x]
    for y in range(len(dungeonArray)):
        for x in range(len(dungeonArray[y])):
            print(dungeonArray[y][x], end = "")
        print("")
    print("HP: " + str(getCurrentHP(global_playerLocation[0])) + "/" + str(getMaxHP(global_playerLocation[0])))
    print("You are the @. Kobolds are k. Stairs going down are D.")
    print(global_stairDownArray)
    print(global_playerLocation)

def addRoom(x, y, room, sizex, sizey):
    #if a room already exists on x,y don't add a second one
    if (global_roomArray.count(str(x) + "," + str(y)) == 0):
        global_roomArray.append(str(x) + "," + str(y) + "," + str(room) + "," + str(sizex) + "," + str(sizey))

def getX(room):
    #returns x of "x,y" string
    x = room.split(",")
    return int(x[0])

def getY(room):
    #returns y of "x,y" string
    y = room.split(",")
    return int(y[1])

def getRoomNumber(room):
    #returns roomnum of "x,y,roomnum,sizex,sizey" string
    num = room.split(",")
    return int(num[2])

def getRoomSizeX(room):
    #returns sizex of "x,y,room,sizex,sizey" string
    x = room.split(",")
    return int(x[3])

def getRoomSizeY(room):
    #returns sizey of "x,y,room,sizex,sizey" string
    y = room.split(",")
    return int(y[4])

def getMaxHP(creature):
    #returns hp of "x,y,MaxHP, current HP,damage" string
    hp = creature.split(",")
    return int(hp[2])

def getCurrentHP(creature):
    #returns hp of "x,y,MaxHP, current HP,damage" string
    hp = creature.split(",")
    return int(hp[3])

def getDamage(creature):
    #returns damage of "x,y,MaxHP,current HP,damage" string
    damage = creature.split(",")
    return int(damage[4])

def getNewPosition(creature, direction):
    if direction.lower() == "up":
        return str(getX(creature)) + "," + str(getY(creature) - 1)
    elif direction.lower() == "left":
        return str(getX(creature) - 1) + "," + str(getY(creature))
    elif direction.lower() == "down":
        return str(getX(creature)) + "," + str(getY(creature) + 1)
    elif direction.lower() == "right":
        return str(getX(creature) + 1) + "," + str(getY(creature))

def setOldPosToFloor(oldPos):
    global global_dungeonArray

    #check if old position was a staircase and put the appropriate staircase
    if str(getX(oldPos)) + "," + str(getY(oldPos)) == global_stairDownArray[0]:
        global_dungeonArray[getY(oldPos)][getX(oldPos)] = global_stairDown
    #elif oldPos == global_stairUpArray[0]:
    #    global_dungeonArray[getY(oldPos)][getX(oldPos)] = global_stairUp
    else:
        #else it was just a floor tile
        global_dungeonArray[getY(oldPos)][getX(oldPos)] = global_floor

def moveCreature(creature, newPos):
    global global_dungeonArray
    global global_playerLocation
    global global_enemyArray

    newDungeonPos = global_dungeonArray[getY(newPos)][getX(newPos)]
    #if a floor tile at newPos direction exists
    if global_floorArray.count(newPos) == 1:
        #check if it's empty (floor or stairs)
        if newDungeonPos == global_floor or newDungeonPos == global_stairDown or newDungeonPos == global_stairUp:
            #check if it's the player or enemy moving
            if global_dungeonArray[getY(creature)][getX(creature)] == global_player:
                #move player there
                global_dungeonArray[getY(newPos)][getX(newPos)] = global_player
                #update player location
                global_playerLocation[0] = newPos + "," + str(getMaxHP(creature)) + "," + str(getCurrentHP(creature)) + "," + str(getDamage(creature))
            else:
                #if its not a player its an enemy because nothing else moves
                global_dungeonArray[getY(newPos)][getX(newPos)] = global_kobold
                #update enemy location
                global_enemyArray[global_enemyArray.index(creature)] = newPos + "," + str(getMaxHP(creature)) + "," + str(getCurrentHP(creature)) + "," + str(getDamage(creature))
            #replace creature who moved with floor tile or stairs
            setOldPosToFloor(creature)
        #if its not an empty floor, check if its creature, if it's a creature, attack
        elif newDungeonPos == global_kobold or newDungeonPos == global_player:
            attackTarget(newPos, creature)

def attackTarget(target, attacker):
    global global_playerLocation
    global global_enemyArray
    global global_dungeonArray

    player = global_playerLocation[0]

    #check whether the attacker is a player or an enemy
    if global_dungeonArray[getY(attacker)][getX(attacker)] == global_kobold:
        global_playerLocation[0] = str(getX(player)) + "," + str(getY(player)) + "," + str(getMaxHP(player)) + "," + str(adjustHealth(player, getDamage(attacker))) + "," + str(getDamage(player))
        if (getCurrentHP(player) <= 0):
            creatureDeath(player)
            for x in range(100):
                print("GAME OVER", end=" ")
    else:
        enemy = creatureFromPosition(target, global_enemyArray)
        i = global_enemyArray.index(enemy)
        global_enemyArray[i] = str(getX(target)) + "," + str(getY(target)) + "," + str(getMaxHP(enemy)) + "," + str(adjustHealth(enemy, getDamage(player))) + "," + str(getDamage(enemy))
        if getCurrentHP(global_enemyArray[i]) <= 0:
            creatureDeath(global_enemyArray[i])
            global_enemyArray.pop(i)

def creatureDeath(creature):
    global global_dungeonArray
    #if they were on floor make it floor
    global_dungeonArray[getY(creature)][getX(creature)] = global_floor

    #if they were on the stairs make it stairs
    if global_stairDownArray.count(str(getY(creature)) + "," + str(getX(creature)) == 1):
        global_dungeonArray[getY(creature)][getX(creature)] = global_stairDown

def adjustHealth(creature, amount):
    hp = getCurrentHP(creature) - amount
    return hp

def creatureFromPosition(pos, creatureArray):
    i = [x for x in creatureArray if pos in x]
    return i[0]

def checkForStairs():
    if str(getX(global_playerLocation[0])) + "," + str(getY(global_playerLocation[0])) == global_stairDownArray[0]:
        clearGlobals()
        generateDungeon(global_width, global_height)

def playerInput():
    this = input("w,a,s,d to move in a direction, e to interact with staircase, attack by walking into enemies")
    #initialize newPos
    newPos = "0"
    #handle accepted inputs
    if this.lower() == "w":
        newPos = getNewPosition(global_playerLocation[0], "up")
    elif this.lower() == "a":
        newPos = getNewPosition(global_playerLocation[0], "left")
    elif this.lower() == "s":
        newPos = getNewPosition(global_playerLocation[0], "down")
    elif this.lower() == "d":
        newPos = getNewPosition(global_playerLocation[0], "right")
    elif this.lower() == "e":
        checkForStairs()
    elif this.lower() == "r":
        clearGlobals()
        generateDungeon(global_width, global_height)

    if newPos != "0":
        moveCreature(global_playerLocation[0], newPos)

def enemyTurn():
    for enemy in range(len(global_enemyArray)):
        print(global_enemyArray[enemy])

def clearGlobals():
    #clear arrays when generating a new floor
    global_dungeonArray.clear()
    global_enemyArray.clear()
    global_playerLocation.clear()
    global_roomArray.clear()
    global_stairDownArray.clear()
    global_stairUpArray.clear()
    global_floorArray.clear()
    


def main():
    global global_turnCounter
    global global_playerLocation
    print("\nWelcome to First Semester RL")
    dungeonWidth = global_width #int(input("Enter the width of the dungeon you want: "))
    dungeonHeight = global_height #int(input("Enter the height of the dungeon you want: "))
    generateDungeon(dungeonWidth, dungeonHeight)

    while True:
        displayDungeon(global_dungeonArray)
        playerInput()
        global_turnCounter += 1
        if global_turnCounter % global_healthRegenRate == 0:
            regen = adjustHealth(global_playerLocation[0], -1)
            if regen <= getMaxHP(global_playerLocation[0]):
                global_playerLocation[0] = str(getX(global_playerLocation[0])) + "," + str(getY(global_playerLocation[0])) + "," + str(getMaxHP(global_playerLocation[0])) + "," + str(regen) + "," + str(getDamage(global_playerLocation[0]))
        enemyTurn()


if __name__ == "__main__":
    main()