import urllib.request
import json
import time
import string

class gameID:
    def __init__(self):
        boole = True
        while boole:
            time.sleep(3)
            try:
                path ='/media/pi/schaakbord/gameid.txt'
                days = open(path,'r')
                lijst = days.read()
                while not lijst:
                    path ='/media/pi/schaakbord/gameid.txt'
                    days = open(path,'r')
                    lijst = days.read()
                    print(lijst)
                    print("file is empty")
                    time.sleep(3)
                else:
                    main(lijst)
                    print("started")
                    boole = False
            except Exception: 
                print("Path is not correct")

class main:

    def __init__(self, gameID):
        
        print(gameID)
                       
        # Deze variabel wordt op true gezet wanneer het bord moet worden gestopt.
        stopBoard = False

        # De path van de file die je wilt lezen (Hierin staat het gameID)
        #path = "gameID.txt"

        # Hiermee open je het bestand en geef je aan dat je het wilt lezen (r = read)
        #gameIDFile = open(path,"r")

        # Deze try-except checked of er om de een of andere manier geen json kan worden opgehaalt, dit kan zijn omdat de gameID fout is maar ook wanneer geen internet beschikbaar is
        try:
            with urllib.request.urlopen("https://nl.lichess.org/api/game/" + gameID +"?with_moves=1") as url:
                data = json.loads(url.read().decode())
        except:
            print("De gameID is niet valid.\n")
            stopBoard = True

            
        # Deze twee arrays zijn om de posities van de witte en zwarte pionnen op te slaan.
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
        
        # Wanneer het bord niet mag worden gestart moet ook niks geprint worden (DEBUGGING)
        if stopBoard != True:
            self.printChessBoard(white, black)

        # Er wordt bijgehouden welke zet we nu zijn, dit is om te voorkomen dat we doorgaan terwijl we nog geen nieuwe zet hebben
        currentMove = 0;

        # We slaan op welke speler aan de beurt is, wit, zwart, wit, zwart etc
        player = "white"
        
        # Deze while loop speelt het spel af, deze is oneindig tot er een break in wordt gebruikt
        while True:

            # Deze variabel staat op True wanneer het bord moet stoppen
            if stopBoard:
                input("Press Enter to continue...")
                break

            # Hier wordt de connectie gemaakt en informatie opgehaalt
            with urllib.request.urlopen("https://nl.lichess.org/api/game/" + gameID +"?with_moves=1") as url:
                data = json.loads(url.read().decode())

            # Hier worden alle moves die zijn opgeslagen in een variabel string gezet
            moves = data["moves"]

            # De moves worden gesplit op spaties en het wordt dus een array
            moves = moves.split(" ")

            # Alleen wanneer we de move die we moeten doen wordt het uitgevoerd
            if currentMove < len(moves):
                # De calcCord methode wordt uitgevoerd
                cords = self.calcCor(moves[currentMove], player, white, black, graveyardPos)

                print(cords)

                # We checken op bijzonderheden als een rokade (#) of promotiee (&)
                if "#" in cords:

                    # Wanneer er een rokade is moeten twee pionnen worden verplaatst, we splitten de coördinaten eerst op de #
                    cords = cords.split("#")

                    # Hier splitten we de eerste twee coordinaten op de -, deze worden behandeld als een gewone zet
                    cord = cords[0].split("-")

                    # Hier splitten we de laatste twee coördinaten op de -, deze worden hieronder weer verwerkt
                    cordRokade = cords[1].split("-")

                    # We splitten de rokade code op in de begin en eind positie
                    cordOne = cordRokade[0]
                    cordTwo = cordRokade[1]

                    # We kijken of de speler wit of zwart is en verzetten daarna de 2e pion
                    if player == "white":
                        
                        for pawn in white:

                            # We kijken welke pion op de beginpositie staat en die zetten we naar de eindpositie
                            if white[pawn][0] == cordOne:
                                
                                white[pawn][0] = cordTwo
                            
                    elif player == "black":

                        # We kijken welke pion op de beginpositie staat en die zetten we naar de eindpositie
                        for pawn in black:
                            
                            if black[pawn][0] == cordOne:
                                
                                black[pawn][0] = cordTwo                  
                        

                # Wanneer er een & wordt gebruikt is er sprake van promotie
                elif "&" in cords:

                    # We splitsen de coördinaten op op  de &
                    cords = cords.split("&")

                    # We splitsen de eerste helft van de array op op de -, deze coördinaten worden behandelt als een gewone zet
                    cord = cords[0].split("-")

                    # van de tweede helft wordt de = afgehaalt en blijft alleen een letter over
                    promo = cords[1][1]

                    # Met dit variabel wordt geteld hoeveel varianten er van dit soort pion zijn (soort als in bijv. queen of loper)
                    number = 1

                    # We checken of de speler wit of zwart is
                    if player == "white":
                        
                        # We loopen door de witte pionnen heen
                        for pawn in white:

                            # Wanneer de een pion de van de soort promo is wordt number opgeteld
                            if promo in white[pawn][1]:
                                number += 1
                    
                    elif player == "black":

                        # We loopen door de zwarte pionnen heen
                        for pawn in black:

                            # Wanneer de een pion de van de soort promo is wordt number opgeteld
                            if promo in black[pawn][1]:
                                number += 1

                    # We voegen de letter in promo en de cijfer in number aan elkaar toe om het duidelijk te maken dat het bijvoorbeeld een tweede queen is
                    promo = promo + str(number)

                    # We checken de kleur van de speler weer
                    # Wanneer de speler wit is
                    if player == "white":

                        # We loopen door alle pionnen heen
                        for pawn in white:

                            # We kijken welke pion op de coördinaten staat
                            if white[pawn][0] == cord[0]:

                                # We promoveren de pion
                                white[pawn][1] = promo

                    # Wanneer de speler zwart is
                    elif player == "black":

                        # We loopen door alle pionnen heen
                        for pawn in black:

                            # We kijken welke pion op de coördinaten staat
                            if black[pawn][0] == cord[0]:

                                # We promoveren de pion
                                black[pawn][1] = promo
                                
                # Wanneer er een X wordt gebruikt is er sprake van passant
                elif "X" in cords:

                    # We splitsen de coördinaten op op  de X
                    cords = cords.split("X")

                    # We splitsen de eerste helft van de array op op de -, deze coördinaten worden behandelt als een gewone zet
                    cord = cords[0].split("-")

                    eindX = cord[1][0]
                    eindY = cord[1][2]

                    if player == "white":

                        passantCord = str(eindX) + " " + str(int(eindY) - 1)

                        for pawn in black:

                            if black[pawn][0] == passantCord:

                                black[pawn][0] = graveyardPos[pawn]
                                
                        
                    elif player == "black":

                        passantCord = str(eindX) + " " + str(int(eindY) + 1)

                        for pawn in white:

                            if white[pawn][0] == passantCord:

                                white[pawn][0] = graveyardPos[pawn]
                                
                else:
                    
                    cord = cords.split("-")


                # Beide cords worden opgeslagen in variabelen
                cordOne = cord[0]
                cordTwo = cord[1]
                
                # Er wordt door zowel de white als de black array geloopt
                for pawnWhite, pawnBlack in zip(white, black):

                    # Eerst wordt gekeken of de beurt gezet is door wit of zwart
                    if player == "white":

                        # Er wordt gechecked of de positie waar de pion naar verplaatst bezet is door een zwarte pion
                        if black[pawnBlack][0] == cordTwo:

                            # Als de positie bezet is door een pion wordt die pion in de "Graveyard" op zijn eigen plek gezet en wordt de eventuele promotie weggehaalt
                            black[pawnBlack][1] = pawnBlack
                            black[pawnBlack][0] = graveyardPos[pawnBlack]

                        # Wanneer de plek vrijgemaakt is kunnen we de pion die moet worden verplaatst verplaatsen
                        if white[pawnWhite][0] == cordOne:
                            white[pawnWhite][0] = cordTwo

                    elif player == "black":

                        # Er wordt gechecked of de positie waar de pion naar verplaatst bezet is door een witte pion        
                        if white[pawnWhite][0] == cordTwo:

                            ## Als de positie bezet is door een pion wordt die pion in de "Graveyard" op zijn eigen plek gezet en wordt de eventuele promotie weggehaalt
                            white[pawnWhite][1] = pawnWhite
                            white[pawnWhite][0] = graveyardPos[pawnWhite]

                        # Wanneer de plek vrijgemaakt is kunnen we de pion die moet worden verplaatst verplaatsen
                        if black[pawnBlack][0] == cordOne:
                            black[pawnBlack][0] = cordTwo
                

                # Wanneer de zet is gedaan gaan we naar de volgende move
                currentMove += 1

                # Wanneer de zet is gedaan switchen we van kant
                if player == "white":
                    player = "black"
                else:
                    player = "white"

                # De printChessBoard is een debug method, deze printen we voor een visuele representatie
                self.printChessBoard(white, black)

            else:
                if data["status"] != "started":
                    print("Game is done.")
                    input("Press Enter to continue...")
                    break
                

    # De printChessBoard() method geeft een visuele representatie van de posities van alle pionnen
    def printChessBoard(self, white, black):

        # ---------------------------------------------------------------------
        # Dit eerste stuk is voor het maken van de string van het complete bord
        # ---------------------------------------------------------------------
        
        # schaakbord is de string waarin alle posities worden toegevoegd
        board = ""

        # variabel y is de y positie van de pionen
        y = 8

        # We loopen door alle y mogelijkheden beginnent bovenin (aangezien het printen van de string linksboven begint)
        while y > 0:
            
            # variabel x is de x positie van de pionen
            x = 1

            # We loopen door alle x mogelijkheden beginnent links (aangezien het printen van de string linksboven begint)
            while x <= 8:

                # Deze for-loop looped door alle witte en zwarte stukken door om te kijken of de plek bezet is
                for pawnWhite, pawnBlack in zip(white, black):
                    # Wanneer de plek van de pion gelijk is aan de plek van de geconcate string van de variabelen x en y wordt deze toegevoegd aan de string en wordt spaceIsset op true gezet
                    if white[pawnWhite][0] == str(x) + " " + str(y):
                        board += "w" + white[pawnWhite][1]
                        break
                    elif black[pawnBlack][0] == str(x) + " " + str(y):
                        board += "b" + black[pawnBlack][1]
                        break

                # Wanneer de for loop niet wordt gebreaked (De plek is dus leeg) wordt "--" ingevuld
                else:
                    board += "---"

                # Tussen elke positie wordt een spatie geadd, zo is het visueel beter leesbaar
                board += " "

                # Wanneer de loop wordt doorlopen doen we x + 1 naar de volgende x positie te gaan    
                x += 1

            # Tussen elke y wordt een enter geplaats, dit is voor visueel effect
            board += "\n"
            
            # We doen y - 1 aangezien we bij 8 beginnen, dit is omdat een schaakbord eigenlijk links onderin met 1, 1 begint en wij dus links bovenin met 1, 8 beginnen
            y -= 1

        # -----------------------------------------------------------------------------
        # Dit stuk van de method is voor het maken van de string van de twee graveyards
        # -----------------------------------------------------------------------------

        graveyard = ""

        # variabel y is de y positie van de pionen
        y = 8

        # We loopen door alle y mogelijkheden beginnent bovenin (aangezien het printen van de string linksboven begint)
        while y > 0:

            # variabel x is de x positie van de pionen
            x = 9

            # We loopen door alle x mogelijkheden beginnent links (aangezien het printen van de string linksboven begint)
            while x <= 10:

                for pawn in white:
                    if white[pawn][0] == str(x) + " " + str(y):
                        graveyard += pawn
                        break
                else:
                    graveyard += "--"
                

                # Tussen elke positie wordt een spatie geadd, zo is het visueel beter leesbaar 
                if x == 9:
                    graveyard += " "
                else:
                    graveyard += " <w - b> "
                
                # Wanneer de loop wordt doorlopen doen we x + 1 naar de volgende x positie te gaan    
                x += 1

            # variabel x is de x positie van de pionen
            x = 9
            
            # We loopen door alle x mogelijkheden beginnent links (aangezien het printen van de string linksboven begint)
            while x <= 10:

                # Omdat de pionnen altijd op de buitenste rij staat (buitenste als in verst van het bord) wordt voor zwart 9 en 10 omgedraait.
                for pawn in black:
                    if x == 9:
                        xGraveyard = 10
                    elif x == 10:
                        xGraveyard = 9
                    if black[pawn][0] == str(xGraveyard) + " " + str(y):
                        graveyard += pawn
                        break
                else:
                    graveyard += "--"
                    
                # Tussen elke positie wordt een spatie geadd, zo is het visueel beter leesbaar 
                if x == 9:
                    graveyard += " "
                
                # Wanneer de loop wordt doorlopen doen we x + 1 naar de volgende x positie te gaan    
                x += 1

            # Tussen elke y wordt een enter geplaats, dit is voor visueel effect
            graveyard += "\n"

            # We doen y - 1 aangezien we bij 8 beginnen, dit is omdat een schaakbord eigenlijk links onderin met 1, 1 begint en wij dus links bovenin met 1, 8 beginnen
            y -= 1

            
        # Hier worden de twee strings geprint

        # De string schaakbord wordt geprint en laat visueel de positie van elke pion op het bord zien
        print("Board:")
        print(board)

        # De string graveyard wordt geprint en laat visueel de positie van elke geslagen pion zien
        print("graveyards:")
        print(graveyard)

    def calcCor(self, move, player, whiteBoard, blackBoard, graveyard):
        
        i = 0

        slaan = False
        
        startX = 0
        startY = 0
        eindX = 0
        eindY = 0

        graveyardX = 0
        graveyardY = 0
        
        nul = 0
        
        grave = 0
        graveX = 0
        graveY = 0
        
        promotieY = 0
        promotieLetter = 0
        
        passantX = 0
        passantY = 0
        
        rokade = 0
        
        passant = False
        
        returnString = "0"
        
        promotie = False

        if "#" in move:
            print("de game is over en moet gereset worden")
            move = move[:-1]



        # problemen met schaak staan voorkomen
        if "+" in move:
            move = move[:-1]

        # promotie controleren
        if "=" in move:
            promotie = True
            moveLetter = list(move)
            promotieLetter = moveLetter[-1]
            move = move[:-1]
            promotiePawn = promotieLetter + "1"
            promotieY = graveyard[promotiePawn][:-1]

        # prepareert coordinaten van de eindpositie in stringvorm
        place = list(move)
        place[0] = self.letterToNumber(place[0])
        moveStr = str(place[-2]) + " " + str(place[-1])
            
        if player == "black":
            playerBoard = blackBoard
        else:
            playerBoard = whiteBoard

        slagen = False
        if "x" in move:
            slagen = True

        if "+" in move:
            move = move[:-1]

        if "B" in move:
            
            moveSplit = list(move)

            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            for pawn in playerBoard:

                if "B" in playerBoard[pawn][1]:
                    
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    stopLoop = False

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY
                    
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:
                        
                        pawnXTemp += 1
                        pawnYTemp += 1

                        if (pawnXTemp < 9) or (pawnYTemp < 9):
                        
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):
                                
                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawnBlack][0][0]) == str(pawnXTemp) and str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            if stopLoop:
                                break
                                    

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:
                        
                        pawnXTemp -= 1
                        pawnYTemp += 1
                        
                        if (pawnXTemp > 0) or (pawnYTemp < 9):
                        
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):
                                
                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawnBlack][0][0]) == str(pawnXTemp) and str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            if stopLoop:
                                break
                                

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        pawnXTemp += 1
                        pawnYTemp -= 1
                        
                        if (pawnXTemp < 9) or (pawnYTemp > 0):
                        
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):
                                
                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawnBlack][0][0]) == str(pawnXTemp) and str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            if stopLoop:
                                break
                                

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        pawnXTemp -= 1
                        pawnYTemp -= 1
                        
                        if (pawnXTemp > 0) or (pawnYTemp > 0):
                        
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):
                                
                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawnBlack][0][0]) == str(pawnXTemp) and str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            if stopLoop:
                                break
                                
                            
            pawnType = "B"
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player,promotieLetter, i))

        
        elif "R" in move:

            moveSplit = list(move)

            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            for pawn in playerBoard:

                if "R" in playerBoard[pawn][1]:
                    
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    stopLoop = False
                    
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY
                    
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        pawnXTemp += 1

                        if pawnXTemp < 9:

                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):

                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawnBlack][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:
                        
                        pawnXTemp -= 1

                        if pawnXTemp > 0:
                            
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):

                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawnBlack][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        pawnYTemp += 1

                        if pawnYTemp < 9:
                            
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):

                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawnBlack][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break
                                    

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:
                        
                        pawnYTemp -= 1

                        if pawnYTemp > 0:
                            
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):

                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawnBlack][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False
                            

            pawnType = "R"
            
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player, promotieLetter, i))

        elif "Q" in move:

            moveSplit = list(move)
            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            for pawn in playerBoard:

                if "Q" in playerBoard[pawn][1]:

                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    stopLoop = False

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY
                    
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:
                        
                        pawnXTemp += 1
                        pawnYTemp += 1

                        if (pawnXTemp < 9) or (pawnYTemp < 9):
                        
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):
                                
                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            if stopLoop:
                                break
                                    

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:
                        
                        pawnXTemp -= 1
                        pawnYTemp += 1
                        
                        if (pawnXTemp > 0) or (pawnYTemp < 9):
                        
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):
                                
                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            if stopLoop:
                                break
                                

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        pawnXTemp += 1
                        pawnYTemp -= 1
                        
                        if (pawnXTemp < 9) or (pawnYTemp > 0):
                        
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):
                                
                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            if stopLoop:
                                break
                                

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        pawnXTemp -= 1
                        pawnYTemp -= 1
                        
                        if (pawnXTemp > 0) or (pawnYTemp > 0):
                        
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):
                                
                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False
                    
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        pawnXTemp += 1

                        if pawnXTemp < 9:

                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):

                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawnBlack][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:
                        
                        pawnXTemp -= 1

                        if pawnXTemp > 0:
                            
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):

                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawnBlack][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        pawnYTemp += 1

                        if pawnYTemp < 9:
                            
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):

                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawnBlack][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break
                                    

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False

                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:
                        
                        pawnYTemp -= 1

                        if pawnYTemp > 0:
                            
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            for pawnWhite, pawnBlack in zip(whiteBoard, blackBoard):

                                if str(whiteBoard[pawnWhite][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawnWhite][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawnBlack][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawnBlack][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

            pawnType = "Q"        
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player, promotieLetter, i))


        elif "N" in move:

            moveSplit = list(move)

            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            for pawn in playerBoard:

                if "N" in playerBoard[pawn][1]:

                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

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

            pawnType = "N"
            
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player, promotieLetter, i))
                        
        elif "K" in move:

            moveSplit = list(move)

            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            for pawn in playerBoard:

                if "K" in playerBoard[pawn][1]:

                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    if pawnX + 1 == movementX and pawnY == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX + 1 == movementX and pawnY +1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX + 1 == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX == movementX and pawnY + 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX - 1 == movementX and pawnY + 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX - 1 == movementX and pawnY == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    elif pawnX - 1 == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1

            pawnType = "K"                        
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player, promotieLetter, i))
        
        else:

            if promotie:
                move = move[:-1]
                moveSplit = list(move)

            if move == "O-O":
                rokade = 1
                if player == "white":
                    return("5 1-7 1#8 1-6 1")
                    # self.chielsmethod(nul, nul, nul, nul, nul, nul, nul, 1, nul, nul)
                else:
                    return("5 8-7 8#8 8-6 8")
                # self.chielsmethod(nul, nul, nul, nul, nul, nul, nul, 1, nul, nul)

            if move == "O-O-O":
                rokade = 2
                if player == "white":
                    return("5 1-3 1#1 1-4 1")
                    # self.chielsmethod(nul, nul, nul, nul, nul, nul, nul, 2, nul, nul)
                else:
                    return("5 8-3 8#1 8-4 8")
                    # self.chielsmethod(nul, nul, nul, nul, nul, nul, nul, 2, nul, nul)

            moveSplit = list(move)
            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])

            amountOfPawns = 0

            i = 1
            
            for pawn in playerBoard:
                    
                if "P" in playerBoard[pawn][1]:
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    if slagen != True:
                    
                        if "white" in player:
                        
                            if pawnX == movementX and pawnY + 1 == movementY:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            if pawnX == movementX and pawnY + 2 == movementY:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            i += 1

                        if "black" in player:
                            
                            if pawnX == movementX and pawnY - 1 == movementY:
                                
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break
                        
                            if pawnX == movementX and pawnY - 2 == movementY:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            i += 1

                    else:

                        if "white" in player:
                                  
                            if pawnX + 1 == movementX and pawnY + 1 == movementY and pawnX < 9 and pawnY < 9:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            if pawnX - 1 == movementX and pawnY + 1 == movementY and pawnX > 0 and pawnY < 9:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            i += 1

                        if "black" in player:
                            
                            if pawnX + 1 == movementX and pawnY - 1 == movementY and pawnX < 9 and pawnY > 0:
                                
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break
                        
                            if pawnX - 1 == movementX and pawnY - 1 == movementY and pawnX > 0 and pawnY > 0:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            i += 1
                                
       
            pawnType = "P"
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player, promotieLetter, i))
                                
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
          
    def pieceCheck(self, amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player, promotieLetter, i):
        
        eindX = movementX
        eindY = movementY

        startX = startX
        startY = startY

        graveyardX = 0
        graveyardY = 0
        
        if amountOfPawns > 1:
            
            if "x" in move:
                
                checkMove = move[1:-3]                        
                
            else:

                checkMove = move[1:-1]
                checkMove = checkMove[0]

            if checkMove.isalpha():
                
                checkMove = self.letterToNumber(checkMove)

                for pawn in playerBoard:

                    if pawnType in playerBoard[pawn][1]:

                        if (playerBoard[pawn][0][:-2] != "9") | (playerBoard[pawn][0][:-2] != "10"):

                            if str(checkMove) == playerBoard[pawn][0][:-2]:

                                startX = int(playerBoard[pawn][0][:-2])
                                startY = int(playerBoard[pawn][0][-1])
                                
            else:

                for pawn in playerBoard:

                    if pawnType in playerBoard[pawn][1]:
                        
                        if checkMove == playerBoard[pawn][0][-1]:

                            startX = int(playerBoard[pawn][0][:-2])
                            startY = int(playerBoard[pawn][0][-1])
                                                
        else:
            
            for pawn in playerBoard:

                    if pawnType in playerBoard[pawn][1]:

                        if pawnType == "P":

                            pawnNumber = pawnType + str(i)

                            if pawnNumber in playerBoard[pawn][1]:

                                startX = int(playerBoard[pawn][0][:-2])
                                startY = int(playerBoard[pawn][0][-1])
            
        if slagen == True:

            endCords = str(movementX) + " " + str(movementY)

            passant = True

            for whitePawn, blackPawn in zip(whiteBoard, blackBoard):
                
                if whiteBoard[whitePawn][0] == endCords or blackBoard[blackPawn][0] == endCords:
                    passant = False
                    break

            if player == "black":
                enemyBoard = blackBoard
            elif player == "white":
                enemyBoard = whiteBoard
                
            for pawn in enemyBoard:

                defeatCords = str(eindX) + " " + str(eindY)

                if enemyBoard[pawn][0] == defeatCords:

                    graveyardPos = graveyard[pawn]
                    
                    graveyardX = int(graveyardPos[:-2])

                    if graveyardX == 10:

                        graveyardY = int(graveyardPos[3])
                        
                    else:
                        
                        graveyardY = int(graveyardPos[2])

        if passant:
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY) + "X"
            return(returnVar)
        
        elif promotieY != 0:
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY) + "&=" + promotieLetter
            return(returnVar)
        
        else:
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY)
            return(returnVar)
        
gameID()
