import urllib.request
import json
import time
import string

class main:

    def __init__(self):

        gameID = "W00IKbpo"

        # De start posities van alle witte pionnen wordt in deze associative array gezet
        white = {
            "K1" : ["5 1", "K1"],
            "Q1" : ["4 1", "Q1"],
            "B1" : ["3 1", "B1"],
            "B2" : ["6 1", "B2"],
            "N1" : ["2 1", "N1"],
            "N2" : ["7 1", "N2"],
            "R1" : ["1 1", "R1"],
            "R2" : ["8 1", "R2"],
            "P1" : ["1 2", "P1"],
            "P2" : ["2 2", "P2"],
            "P3" : ["3 2", "P3"],
            "P4" : ["4 2", "P4"],
            "P5" : ["5 2", "P5"],
            "P6" : ["6 2", "P6"],
            "P7" : ["7 2", "P7"],
            "P8" : ["8 2", "P8"]
            }

        black = {
            "K1" : ["5 8", "K1"],
            "Q1" : ["4 8", "Q1"],
            "B1" : ["3 8", "B1"],
            "B2" : ["6 8", "B2"],
            "N1" : ["2 8", "N1"],
            "N2" : ["7 8", "N2"],
            "R1" : ["1 8", "R1"],
            "R2" : ["8 8", "R2"],
            "P1" : ["1 7", "P1"],
            "P2" : ["2 7", "P2"],
            "P3" : ["3 7", "P3"],
            "P4" : ["4 7", "P4"],
            "P5" : ["5 7", "P5"],
            "P6" : ["6 7", "P6"],
            "P7" : ["7 7", "P7"],
            "P8" : ["8 7", "P8"],
            }

        # De graveyardPos array wordt gebruikt om te kijken welk stuk op welke positie moet komen te staan wanneer geslagen, rij x 9 voor pionnen x 10 voor andere stukken
        graveyardPos = {
            "K1" : "10 4",
            "Q1" : "10 5",
            "B1" : "10 3",
            "B2" : "10 6",
            "N1" : "10 2",
            "N2" : "10 7",
            "R1" : "10 1",
            "R2" : "10 8",
            "P1" : "9 1",
            "P2" : "9 2",
            "P3" : "9 3",
            "P4" : "9 4",
            "P5" : "9 5",
            "P6" : "9 6",
            "P7" : "9 7",
            "P8" : "9 8",
            }

        currentMove = 0;

     ##########   self.resetBoard(black, white)
        
        currentPlayer = "white"

        while True:

            time.sleep(2)

            with urllib.request.urlopen("https://nl.lichess.org/api/game/" + gameID +"?with_moves=1") as url:
                data = json.loads(url.read().decode())

            moves = data["moves"]

            moves = moves.split(" ")
            
            if currentMove < len(moves):

                if currentPlayer == "white":
                    self.calcCor(moves[currentMove], currentPlayer, white, black, graveyardPos)
                else:
                    self.calcCor(moves[currentMove], currentPlayer, white, black, graveyardPos)

                currentMove += 1

                if currentPlayer == "white":
                    currentPlayer = "black"
                else:
                    currentPlayer = "white"


                

    # De printChessBoard() method geeft een visuele representatie van de posities van alle pionnen
    def printChessBoard(self, white, black):
        
        # schaakbord is de string waarin alle posities worden toegevoegd
        schaakbord = ""

        # variabel y is de y positie van de pionen
        y = 8

        # We loopen door alle y mogelijkheden beginnent bovenin (aangezien het printen van de string linksboven begint)
        while y > 0:
            
            # variabel x is de x positie van de pionen
            x = 1

            # We loopen door alle x mogelijkheden beginnent links (aangezien het printen van de string linksboven begint)
            while x <= 8:
                
                # spaceIsset is een variabel waarmee wordt gecontrolleerd of een plek bezet is, is een plek niet bezet dan wordt er "--" ingevuld
                spaceIsset = False

                # We loopen door alle pionnen van white heen om te kijken welke pion op de x y coördinaten zit
                for pion in white:

                    # Wanneer de plek van de pion gelijk is aan de plek van de geconcate string van de variabelen x en y wordt deze toegevoegd aan de string en wordt spaceIsset op true gezet
                    if white[pion] == str(x) + " " + str(y):
                        schaakbord += pion
                        spaceIsset = True

                # We checken of de positie niet al bezet is door een witte pion (Voorkomt dat de loop onnodig wordt doorlopen)
                if spaceIsset == False:
                    # We loopen door alle pionnen van black heen om te kijken welke pion op de x y coördinaten zit
                    for pion in black:

                        # Wanneer de plek van de pion gelijk is aan de plek van de geconcate string van de variabelen x en y wordt deze toegevoegd aan de string en wordt spaceIsset op true gezet
                        if black[pion] == str(x) + " " + str(y):
                            schaakbord += pion
                            spaceIsset = True

                # Wanneer een positie helemaal niet bezet is wordt "--" ingevuld
                if spaceIsset == False:
                       schaakbord += "--"

                # Tussen elke positie wordt een spatie geadd, zo is het visueel beter leesbaar
                schaakbord += " "

                # Wanneer de loop wordt doorlopen doen we x + 1 naar de volgende x positie te gaan    
                x += 1

            # Tussen elke y wordt een enter geplaats, dit is voor visueel effect
            schaakbord += "\n"
            
            # We doen y - 1 aangezien we bij 8 beginnen, dit is omdat een schaakbord eigenlijk links onderin met 1, 1 begint en wij dus links bovenin met 1, 8 beginnen
            y -= 1

        # De string schaakbord wordt geprint en laat visueel de positie van elke pion zien
        print(schaakbord)

    def calcCor(self, move, player, whiteBoard, blackBoard, graveyard):

        slaan = False
        nul = 0
        grave = 0
        graveX = 0
        graveY = 0
        promotieY = 0
        rokade = 0
        returnString = "0"

        # problemen met schaak staan voorkomen
        if "+" in move:
            move = move[:-1]

        # prepareert coordinaten van de eindpositie in stringvorm
        place = list(move)
        place[0] = self.letterToNumber(place[0])
        moveStr = str(place[-2]) + " " + str(place[-1])
            
        if player == "black":
            playerBoard = blackBoard
        else:
            playerBoard = whiteBoard
        # controleert of de zet een pion is die niets speciaals doet
        if len(move) == 2:
            i = 0;

            # gaat door de schaakstukken-array heen en vuurt pas meer code af als hij bij de pionnen is
            for pawn in playerBoard:
                if i >= 8:

                    startList = list(playerBoard[pawn][0])
                    startX = startList[0]
                    startY = startList[2]

                    returnString = str(startX) + str(" ")+ str(startY)
                    
                    # controleert of het een wit stuk is die beweegt
                    if player == "white":
                        
                        # prepareert de strings voor de if statement omdat als je dit in de if statement doet krijg je syntax errors
                        place1 = int(place[1]) - 1 
                        placeCheck1 = str(place[0]) + " " + str(place1)
                        place2 = int(place[1]) - 2
                        placeCheck2 = str(place[0]) + " " + str(place2)

                        returnString = returnString + str("-") + str(place[0]) + str(" ") + str(place[1])
                        
                        # controleert hoeveel stappen de pion heeft gezet
                        if placeCheck1 == playerBoard[pawn][0]:
                            print(startX, startY, place[0], place[1], slaan, graveX, graveY, promotieY, rokade, "returnstring is ", returnString)
                            # self.chielsMethod(startX, startY, place[0], place[1], slaan, graveX, graveY, promotieY, rokade)
                            # return(returnString)
                        elif placeCheck2 == playerBoard[pawn][0]:
                            print(startX, startY, place[0], place[1], slaan, graveX, graveY, promotieY, rokade, "returnstring is ", returnString)
                            # self.chielsMethod(startX, startY, place[0], place[1], slaan, graveX, graveY, promotieY, rokade)
                            # return(returnString)

                    # controleert of het een zwart stuk is die beweegt
                    if player == "black":
                        
                        # prepareert de strings voor de if statement omdat als je dit in de if statement doet krijg je syntax errors
                        place1 = int(place[1]) + 1 
                        placeCheck1 = str(place[0]) + " " + str(place1)
                        place2 = int(place[1]) + 2
                        placeCheck2 = str(place[0]) + " " + str(place2)

                        returnString = returnString + str("-") + str(place[0]) + str(" ") + str(place[1])
                        
                        # controleert hoeveel stappen de pion heeft gezet
                        if placeCheck1 == playerBoard[pawn][0]:
                            print(startX, startY, place[0], place[1], slaan, graveX, graveY, promotieY, rokade, "returnstring is ", returnString)
                            # self.chielsMethod(startX, startY, place[0], place[1], slaan, graveX, graveY, promotieY, rokade)
                            # return(returnString)
                            
                        elif placeCheck2 == playerBoard[pawn][0]:
                            print(startX, startY, place[0], place[1], slaan, graveX, graveY, promotieY, rokade, "returnstring is ", returnString)
                            # self.chielsMethod(startX, startY, place[0], place[1], slaan, graveX, graveY, promotieY, rokade)
                            # return(returnString)
                i += 1



        ##############################################################################################
        #                                                                                            #
        #                                                                                            #
        #                                                                                            #
        # hier moet promoveren worden gedaan, anders gaat de controle voor de andere stukken fout    #
        #                                                                                            #
        #                                                                                            #
        #                                                                                            #
        ##############################################################################################
        elif "=" in move:
            print("er wordt een pion gepormoveerd")
        
        # controleert of de zet die gedaan is een loper is

        
        elif "B" in move:

            slagen = False
            if "x" in move:
                slagen = True

            if "+" in move:
                move = move[:-1]

            moveSplit = list(move)

            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            startX = 0
            startY = 0
            eindX = 0
            eindY = 0

            graveyardX = 0
            graveyardY = 0

            for pawn in playerBoard:

                if "B" in playerBoard[pawn][1]:

                    pawnX = int(playerBoard[pawn][0][0])
                    pawnY = int(playerBoard[pawn][0][2])

                    pawnX = int(playerBoard[pawn][0][0])
                    pawnY = int(playerBoard[pawn][0][2])

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY
                    
                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x += 1
                        y += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x -= 1
                        y += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x -= 1
                        y += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x -= 1
                        y -= 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                            
                if amountOfPawns > 1:

                    if "x" in move:
                        
                        checkMove = move[1:-3]                        
                        
                    else:

                        checkMove = move[1:-2]

                    if len(checkMove) == 1:
                        if checkMove.isalpha():
                            
                            checkMove = self.letterToNumber(checkMove)

                            for pawn in playerBoard:

                                if "B" in playerBoard[pawn][1]:

                                    if (playerBoard[pawn][0][:-2] != "9") | (playerBoard[pawn][0][:-2] != "10"):

                                        if str(checkMove) == playerBoard[pawn][0][:-2]:

                                            startX = int(playerBoard[pawn][0][0])
                                            startY = int(playerBoard[pawn][0][2])
                                            eindX = movementX
                                            eindY = movementY
                                            
                        else:

                            for pawn in playerBoard:

                                if "B" in playerBoard[pawn][1]:
                                    
                                    if checkMove == playerBoard[pawn][0][-1]:

                                        startX = int(playerBoard[pawn][0][0])
                                        startY = int(playerBoard[pawn][0][2])
                                        eindX = movementX
                                        eindY = movementY
                                        
                    else:

                        x = self.letterToNumber(checkMove[0])
                        y = checkMove[1]

                        for pawn in playerBoard:

                            if "B" in playerBoard[pawn][1]:

                                print(playerBoard[pawn][0][:-2], playerBoard[pawn][0][-1])
                                print(x, y)
                                
                                if (str(x) == playerBoard[pawn][0][:-2]) & (y == playerBoard[pawn][0][-1]):

                                    startX = int(playerBoard[pawn][0][0])
                                    startY = int(playerBoard[pawn][0][2])
                                    eindX = movementX
                                    eindY = movementY
                        
                    
                if slagen == True:

                    if player == "white":
                        enemyBoard = blackBoard
                    elif player == "black":
                        enemyBoard = whiteBoard

                    for pawn in enemyBoard:

                        if enemyBoard[pawn][0] == str(eindX) + " " + str(eindY):

                            graveyardPos = graveyard[pawn]
                            
                            graveyardX = int(graveyardPos[:-2])

                            if graveyardX == 10:

                                graveyardY = int(graveyardPos[3])
                                
                            else:
                                
                                graveyardY = int(graveyardPos[2])

            print(startX, startY, eindX, eindY, slagen, graveyardY)

        # controleert of de zet een dame is 
        elif "Q" in move:


            
            
        elif "R" in move:

            slagen = False
            if "x" in move:
                slagen = True

            if "+" in move:
                move = move[:-1]

            moveSplit = list(move)

            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            startX = 0
            startY = 0
            eindX = 0
            eindY = 0

            graveyardX = 0
            graveyardY = 0

            for pawn in playerBoard:

                if "R" in playerBoard[pawn][1]:

                    pawnX = int(playerBoard[pawn][0][0])
                    pawnY = int(playerBoard[pawn][0][2])

                    rookx = pawnX
                    rooky = pawnY
                    
                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                            
                    rookx = pawnX
                    rooky = pawnY
                    

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x -= 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                            
                    rookx = pawnX
                    rooky = pawnY
                    

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        y += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                            
                    rookx = pawnX
                    rooky = pawnY
                    

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        y -= 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                        

                        
                if amountOfPawns > 1:

                    if "x" in move:
                        
                        checkMove = move[1:-3]                        
                        
                    else:

                        checkMove = move[1:-2]

                    if len(checkMove) == 1:
                        if checkMove.isalpha():
                            
                            checkMove = self.letterToNumber(checkMove)

                            for pawn in playerBoard:

                                if "R" in playerBoard[pawn][1]:

                                    if (playerBoard[pawn][0][:-2] != "9") | (playerBoard[pawn][0][:-2] != "10"):

                                        if str(checkMove) == playerBoard[pawn][0][:-2]:

                                            startX = int(playerBoard[pawn][0][0])
                                            startY = int(playerBoard[pawn][0][2])
                                            eindX = movementX
                                            eindY = movementY
                                            
                        else:

                            for pawn in playerBoard:

                                if "R" in playerBoard[pawn][1]:
                                    
                                    if checkMove == playerBoard[pawn][0][-1]:

                                        startX = int(playerBoard[pawn][0][0])
                                        startY = int(playerBoard[pawn][0][2])
                                        eindX = movementX
                                        eindY = movementY
                                        
                    else:

                        x = self.letterToNumber(checkMove[0])
                        y = checkMove[1]

                        for pawn in playerBoard:

                            if "R" in playerBoard[pawn][1]:

                                print(playerBoard[pawn][0][:-2], playerBoard[pawn][0][-1])
                                print(x, y)
                                
                                if (str(x) == playerBoard[pawn][0][:-2]) & (y == playerBoard[pawn][0][-1]):

                                    startX = int(playerBoard[pawn][0][0])
                                    startY = int(playerBoard[pawn][0][2])
                                    eindX = movementX
                                    eindY = movementY
                        
                    
                if slagen == True:

                    if player == "white":
                        enemyBoard = blackBoard
                    elif player == "black":
                        enemyBoard = whiteBoard

                    for pawn in enemyBoard:

                        if enemyBoard[pawn][0] == str(eindX) + " " + str(eindY):

                            graveyardPos = graveyard[pawn]
                            
                            graveyardX = int(graveyardPos[:-2])

                            if graveyardX == 10:

                                graveyardY = int(graveyardPos[3])
                                
                            else:
                                
                                graveyardY = int(graveyardPos[2])

            print(startX, startY, eindX, eindY, slagen, graveyardY)

        elif "Q" in move:

            slagen = False
            if "x" in move:
                slagen = True

            if "+" in move:
                move = move[:-1]

            moveSplit = list(move)

            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            startX = 0
            startY = 0
            eindX = 0
            eindY = 0

            graveyardX = 0
            graveyardY = 0

            for pawn in playerBoard:

                if "Q" in playerBoard[pawn][1]:

                    pawnX = int(playerBoard[pawn][0][0])
                    pawnY = int(playerBoard[pawn][0][2])

                    queenX = pawnX
                    queenY = pawnY
                    
                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                            
                    queenX = pawnX
                    queenY = pawnY
                    

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x -= 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                            
                    queenX = pawnX
                    queenY = pawnY
                    

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        y += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                            
                    queenX = pawnX
                    queenY = pawnY
                    

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        y -= 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x += 1
                        y += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1

                    queenX = pawnX
                    queenY = pawnY

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x -= 1
                        y += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1

                    queenX = pawnX
                    queenY = pawnY

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x -= 1
                        y += 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1

                    queenX = pawnX
                    queenY = pawnY

                    while pawnX < 9 and pawnX > 0 and pawnY < 9 and pawnY > 0:
                        x -= 1
                        y -= 1
                        if pawnX == movementX and pawnY == movementY:
                            startX = pawnX
                            startY = pawnY
                            eindX = movementX
                            eindY = movementY
                            amountOfPawns += 1
                        

                        
                if amountOfPawns > 1:

                    if "x" in move:
                        
                        checkMove = move[1:-3]                        
                        
                    else:

                        checkMove = move[1:-2]

                    if len(checkMove) == 1:
                        if checkMove.isalpha():
                            
                            checkMove = self.letterToNumber(checkMove)

                            for pawn in playerBoard:

                                if "Q" in playerBoard[pawn][1]:

                                    if (playerBoard[pawn][0][:-2] != "9") | (playerBoard[pawn][0][:-2] != "10"):

                                        if str(checkMove) == playerBoard[pawn][0][:-2]:

                                            startX = int(playerBoard[pawn][0][0])
                                            startY = int(playerBoard[pawn][0][2])
                                            eindX = movementX
                                            eindY = movementY
                                            
                        else:

                            for pawn in playerBoard:

                                if "Q" in playerBoard[pawn][1]:
                                    
                                    if checkMove == playerBoard[pawn][0][-1]:

                                        startX = int(playerBoard[pawn][0][0])
                                        startY = int(playerBoard[pawn][0][2])
                                        eindX = movementX
                                        eindY = movementY
                                        
                    else:

                        x = self.letterToNumber(checkMove[0])
                        y = checkMove[1]

                        for pawn in playerBoard:

                            if "R" in playerBoard[pawn][1]:

                                print(playerBoard[pawn][0][:-2], playerBoard[pawn][0][-1])
                                print(x, y)
                                
                                if (str(x) == playerBoard[pawn][0][:-2]) & (y == playerBoard[pawn][0][-1]):

                                    startX = int(playerBoard[pawn][0][0])
                                    startY = int(playerBoard[pawn][0][2])
                                    eindX = movementX
                                    eindY = movementY
                        
                    
                if slagen == True:

                    if player == "white":
                        enemyBoard = blackBoard
                    elif player == "black":
                        enemyBoard = whiteBoard

                    for pawn in enemyBoard:

                        if enemyBoard[pawn][0] == str(eindX) + " " + str(eindY):

                            graveyardPos = graveyard[pawn]
                            
                            graveyardX = int(graveyardPos[:-2])

                            if graveyardX == 10:

                                graveyardY = int(graveyardPos[3])
                                
                            else:
                                
                                graveyardY = int(graveyardPos[2])

            print(startX, startY, eindX, eindY, slagen, , graveyardY)


        if "N" in move:

            slagen = False
            if "x" in move:
                slagen = True

            if "+" in move:
                move = move[:-1]

            moveSplit = list(move)

            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            startX = 0
            startY = 0
            eindX = 0
            eindY = 0

            graveyardX = 0
            graveyardY = 0

            for pawn in playerBoard:

                if "N" in playerBoard[pawn][1]:

                    pawnX = int(playerBoard[pawn][0][0])
                    pawnY = int(playerBoard[pawn][0][2])

                    if pawnX + 2 == movementX and pawnY + 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX + 2 == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX - 2 == movementX and pawnY + 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX - 2 == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX + 1 == movementX and pawnY + 2 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX + 1 == movementX and pawnY - 2 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX - 1 == movementX and pawnY + 2 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX - 1 == movementX and pawnY - 2 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1

                        
                if amountOfPawns > 1:

                    if "x" in move:
                        
                        checkMove = move[1:-3]                        
                        
                    else:

                        checkMove = move[1:-2]

                    if len(checkMove) == 1:
                        if checkMove.isalpha():
                            
                            checkMove = self.letterToNumber(checkMove)

                            for pawn in playerBoard:

                                if "N" in playerBoard[pawn][1]:

                                    if (playerBoard[pawn][0][:-2] != "9") | (playerBoard[pawn][0][:-2] != "10"):

                                        if str(checkMove) == playerBoard[pawn][0][:-2]:

                                            startX = int(playerBoard[pawn][0][0])
                                            startY = int(playerBoard[pawn][0][2])
                                            eindX = movementX
                                            eindY = movementY
                                            
                        else:

                            for pawn in playerBoard:

                                if "N" in playerBoard[pawn][1]:
                                    
                                    if checkMove == playerBoard[pawn][0][-1]:

                                        startX = int(playerBoard[pawn][0][0])
                                        startY = int(playerBoard[pawn][0][2])
                                        eindX = movementX
                                        eindY = movementY
                                        
                    else:

                        x = self.letterToNumber(checkMove[0])
                        y = checkMove[1]

                        for pawn in playerBoard:

                            if "N" in playerBoard[pawn][1]:

                                print(playerBoard[pawn][0][:-2], playerBoard[pawn][0][-1])
                                print(x, y)
                                
                                if (str(x) == playerBoard[pawn][0][:-2]) & (y == playerBoard[pawn][0][-1]):

                                    startX = int(playerBoard[pawn][0][0])
                                    startY = int(playerBoard[pawn][0][2])
                                    eindX = movementX
                                    eindY = movementY
                        
                    
                if slagen == True:

                    if player == "white":
                        enemyBoard = blackBoard
                    elif player == "black":
                        enemyBoard = whiteBoard

                    for pawn in enemyBoard:

                        if enemyBoard[pawn][0] == str(eindX) + " " + str(eindY):

                            graveyardPos = graveyard[pawn]
                            
                            graveyardX = int(graveyardPos[:-2])

                            if graveyardX == 10:

                                graveyardY = int(graveyardPos[3])
                                
                            else:
                                
                                graveyardY = int(graveyardPos[2])

                
                    







            print(startX, startY, eindX, eindY, slagen, graveyardY)

        elif "K" in move:
            playerBoardSplit = playerBoard["K1"][0].split(" ")

        
            
                
    # convert de letters van de x as naar cijfers
    def letterToNumber(self, letter):

        if letter == "a":
            return 1
        elif letter == "b":
            return 2
        elif letter == "c":
            return 3
        elif letter == "d":
            return 4
        elif letter == "e":
            return 5
        elif letter == "f":
            return 6
        elif letter == "g":
            return 7
        elif letter == "h":
            return 8
        else:
            return False

    # roep deze functie aan om het spel opnieuw klaar te zetten
    def resetBoard(self, black, white):

        # dit zet de array op volgorde zodat erdoor heen kan worden gegaan op volgorde van de for loop
        whiteConverted = {
            "R1" : white["R1"],
            "N1" : white["N1"],
            "B1" : white["B1"],
            "Q1" : white["Q1"],
            "K1" : white["K1"],
            "B2" : white["B2"],
            "N2" : white["N2"],
            "R2" : white["R2"],
            "P1" : white["P1"],
            "P2" : white["P2"],
            "P3" : white["P3"],
            "P4" : white["P4"],
            "P5" : white["P5"],
            "P6" : white["P6"],
            "P7" : white["P7"],
            "P8" : white["P8"],
            }

        blackConverted = {
            "R1" : black["R1"],
            "N1" : black["N1"],
            "B1" : black["B1"],
            "Q1" : black["Q1"],
            "K1" : black["K1"],
            "B2" : black["B2"],
            "N2" : black["N2"],
            "R2" : black["R2"],
            "P1" : black["P1"],
            "P2" : black["P2"],
            "P3" : black["P3"],
            "P4" : black["P4"],
            "P5" : black["P5"],
            "P6" : black["P6"],
            "P7" : black["P7"],
            "P8" : black["P8"],
            }


        x = 1
        y = 1
        count = 1

        
        for pos in whiteConverted:
            place = list(white[pos])
            
            print(place[0], place[-1], x, y, nul, nul, nul, nul)
            # self.chielsMethod(place[1], place[-1], x, y, nul, nul, nul, nul)

            x += 1
            count += 1
            if x is 9:
                x = 1
            if count is 9:
                y += 1

        x = 1
        y = 8
        count = 1
                
        for pos in whiteConverted:
            place = list(white[pos])
            print(place[0], place[-1], x, y, nul, nul, nul, nul)
            
            # self.chielsMethod(place[1], place[-1], x, y, nul, nul, nul, nul)

            x += 1
            count += 1
            if x is 9:
                x = 1
            if count is 9:
                y -= 1
                    
main()
