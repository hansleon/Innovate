import urllib.request
import json
import time
import string

class usbReader:
    
    def __init__(self):
##        boole = True
##        while boole:
##            time.sleep(3)
##            try:
##                path ='/media/pi/schaakbord/gameid.txt'
##                days = open(path,'r')
##                gameID = days.read()
##                while not gameID:
##                    path ='/media/pi/schaakbord/gameid.txt'
##                    days = open(path,'r')
##                    gameID = days.read()
##                    print(gameID)
##                    print("file is empty")
##                    time.sleep(3)
##                else:
##                    main(gameID)
##                    print("started")
##                    boole = False
##            except Exception: 
##                print("Path is not correct")

        main("WMoa4kd7")

class main:

    def __init__(self, gameID):

        posx = 0
        posy = 0

        # Deze variabel wordt op true gezet wanneer het bord moet worden gestopt.
        stopBoard = False

        # De path van de file die je wilt lezen (Hierin staat het gameID)
        # path = "gameID.txt"

        # Hiermee open je het bestand en geef je aan dat je het wilt lezen (r = read)
        # gameIDFile = open(path,"r")

        # Hier lees je de inhoud van de file
        # gameID = gameIDFile.read()

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
                cords, setCords = self.calcCor(moves[currentMove], player, white, black, graveyardPos, posx, posy)
                posx, posy = setCords

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
                        
                        # We kijken welke pion op de beginpositie staat en die zetten we naar de eindpositie
                        for pawn in white:

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
                    
                    # We halen de X en Y coördinaten uit het variabel cords
                    eindX = cord[1][0]
                    eindY = cord[1][2]

                    # We kijken of de speler wit of zwart is
                    if player == "white":
                        
                        # Wanneer passant wordt geslagen door wit is het altijd de pion op de eindY min 1
                        passantCord = str(eindX) + " " + str(int(eindY) - 1)

                        # We kijken welke zwarte pion hier staat en deze verplaatsen we naar de graveyard
                        for pawn in black:

                            if black[pawn][0] == passantCord:

                                black[pawn][0] = graveyardPos[pawn]
                                
                        
                    elif player == "black":

                        # Wanneer passant wordt geslagen door wit is het altijd de pion op de eindY min 1
                        passantCord = str(eindX) + " " + str(int(eindY) + 1)

                        # We kijken welke zwarte pion hier staat en deze verplaatsen we naar de graveyard
                        for pawn in white:

                            if white[pawn][0] == passantCord:

                                white[pawn][0] = graveyardPos[pawn]

                # Wanneer er niks speciaals is splitten we de coördinaten gewoon op de - en deze coördinaten behandelen we verder hieronder
                else:
                    
                    cord = cords.split("-")


                # Beide cords worden opgeslagen in variabelen
                cordOne = cord[0]
                cordTwo = cord[1]
                
                # Er wordt door zowel de white als de black array geloopt
                for pawn in white:

                    # Eerst wordt gekeken of de beurt gezet is door wit of zwart
                    if player == "white":

                        # Er wordt gechecked of de positie waar de pion naar verplaatst bezet is door een zwarte pion
                        if black[pawn][0] == cordTwo:

                            # Als de positie bezet is door een pion wordt die pion in de "Graveyard" op zijn eigen plek gezet en wordt de eventuele promotie weggehaalt
                            black[pawn][1] = pawn
                            black[pawn][0] = graveyardPos[pawn]

                        # Wanneer de plek vrijgemaakt is kunnen we de pion die moet worden verplaatst verplaatsen
                        if white[pawn][0] == cordOne:
                            white[pawn][0] = cordTwo

                    elif player == "black":

                        # Er wordt gechecked of de positie waar de pion naar verplaatst bezet is door een witte pion        
                        if white[pawn][0] == cordTwo:

                            ## Als de positie bezet is door een pion wordt die pion in de "Graveyard" op zijn eigen plek gezet en wordt de eventuele promotie weggehaalt
                            white[pawn][1] = pawn
                            white[pawn][0] = graveyardPos[pawn]

                        # Wanneer de plek vrijgemaakt is kunnen we de pion die moet worden verplaatst verplaatsen
                        if black[pawn][0] == cordOne:
                            black[pawn][0] = cordTwo
                

                # Wanneer de zet is gedaan gaan we naar de volgende move
                currentMove += 1

                # Wanneer de zet is gedaan switchen we van kant
                if player == "white":
                    player = "black"
                else:
                    player = "white"

                # De printChessBoard is een debug method, deze printen we voor een visuele representatie
                self.printChessBoard(white, black)

            # Wanneer we bij een stap zijn die nog niet is gezet (Het potje is dus afgelopen of nog bezig) checken we of het potje al klaar is
            elif data["status"] != "started":
                
                print("Game is klaar.")
                print("De game wordt gereset")

                # We runnen de reset functie om het bord naar originele posities te resetten
                newArrays = self.resetBoard(white, black, posx, posy)
                print(posx, posy)
                white, black = newArrays
                self.printChessBoard(white, black)
                
                input("Press enter to continue...")
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
                for pawn in white:
                    
                    # Wanneer de plek van de pion gelijk is aan de plek van de geconcate string van de variabelen x en y wordt deze toegevoegd aan de string en wordt spaceIsset op true gezet
                    if white[pawn][0] == str(x) + " " + str(y):
                        board += "w" + white[pawn][1]
                        break
                    
                    elif black[pawn][0] == str(x) + " " + str(y):
                        board += "b" + black[pawn][1]
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

    def calcCor(self, move, player, whiteBoard, blackBoard, graveyard, posx, posy):

        # We initialiseren alle variabelen zodat ze altijd een waarde hebben

        # i is voor de index van de pion
        i = 0

        # AmountOfPawns is een variabel waarin we het aantal mogelijkheden opslaan, dit is om te voorkomen dat de verkeerde pion wordt bewogen
        amountOfPawns = 0

        # Met deze variabelen geef je bijzonderheden mee
        slagen = False
        passant = False
        promotie = False

        # In deze variabelen worden de coördinaten van de beweging van de pion opgeslagen
        startX = 0
        startY = 0
        eindX = 0
        eindY = 0

        # Hierin worden de coördinaten van een pion opgeslagen wanneer hij geslagen is
        graveyardX = 0
        graveyardY = 0
        
        grave = 0
        graveX = 0
        graveY = 0

        # Wanneer er promotie is zijn dit gegevens die moeten worden meegegevens, promotieY is de positie van de pion in de graveyard en promotieLetter is waarnaar gepromoveerd wordt
        promotieY = 0
        promotieLetter = 0

        # Dit zijn de coördinaten van de pion die passant wordt geslagen
        passantX = 0
        passantY = 0
        
        rokade = 0
        returnString = "0"
        
        
        # Mat staan wordt anders verwerkt in de code, we halen daarom de # uit de move en doen hier verder niks mee
        if "#" in move:
            move = move[:-1]

        # Wanneer move een x bevat wordt iets geslagen, we zetten dus het variabel hiervoor
        if "x" in move:
            slagen = True

        # Voor ons systeem is schaakstaan niet echt van belang. We halen daarom de + uit de move en doen hier verder niks mee
        if "+" in move:
            move = move[:-1]

        # promotie controleren
        if "=" in move:
            promotie = True
            moveLetter = list(move)
            promotieLetter = moveLetter[-1]
            move = move[:-2]
            print(move)
            promotiePawn = promotieLetter + "1"
            promotieY = graveyard[promotiePawn][:-1]

        # prepareert coordinaten van de eindpositie in stringvorm
        place = list(move)
        place[0] = self.letterToNumber(place[0])
        moveStr = str(place[-2]) + " " + str(place[-1])

        # We checken of de speler zwart of wit is    
        if player == "black":
            playerBoard = blackBoard
        else:
            playerBoard = whiteBoard

        # We splitten de move op voor stringbewerking
        moveSplit = list(move)

        if "O-O" not in move:
            # We splitten de coördinaten op in een X en een Y
            movementX = int(self.letterToNumber(moveSplit[-2]))
            movementY = int(moveSplit[-1])


        # We kijken of de zet een bischop bevat    
        if "B" in move:

            # We loopen door alle pionnen van de speler die aan de beurt is
            for pawn in playerBoard:

                # We kijken alleen naar de pionnen waarbij de waarde in de array een B bevat (Dit is zodat gepromoveerde pionnen ook werken)
                if "B" in playerBoard[pawn][1]:

                    # We zetten pawnX en pawnY naar de coördinaten
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    # stopLoop is een variabel om ervoor te zorgen dat de buitenste loop wordt gestopt wanneer er een pion in het pad staat (Een bisschop kan niet over pionnen heen bewegen)
                    stopLoop = False

                    # Deze pawnX en Y zijn ervoor om te worden "increment", een bisschop beweegt steeds één vakje vertical
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # We loopen door alle mogelijkheden, wanneer het buiten het bord is stoppen we de loop
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # We "incrementen" de X en Y
                        pawnXTemp += 1
                        pawnYTemp += 1

                        # We kijken of de X en Y nog op het bord zitten
                        if (pawnXTemp < 9) or (pawnYTemp < 9):
                            
                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # We loopen door beide arrays om te kijken of de positie bezet is, wanneer deze bezet is zetten we stopLoop op True om de loop te stoppen
                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][0]) == str(pawnXTemp) and str(blackBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            # We stoppen de loop wanneer stopLoop True is
                            if stopLoop:
                                break
                                    

                    # We zetten de variabelen terug om ze weer te gebruiken
                    stopLoop = False
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # We loopen door alle mogelijkheden, wanneer het buiten het bord is stoppen we de loop
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # We "incrementen" de X en Y
                        pawnXTemp -= 1
                        pawnYTemp += 1

                        # We kijken of de X en Y nog op het bord zitten
                        if (pawnXTemp > 0) or (pawnYTemp < 9):

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # We loopen door beide arrays om te kijken of de positie bezet is, wanneer deze bezet is zetten we stopLoop op True om de loop te stoppen
                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][0]) == str(pawnXTemp) and str(blackBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            # We stoppen de loop wanneer stopLoop True is
                            if stopLoop:
                                break
                                

                    # We zetten de variabelen terug om ze weer te gebruiken
                    stopLoop = False
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY
                    

                    # We loopen door alle mogelijkheden, wanneer het buiten het bord is stoppen we de loop
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # We "incrementen" de X en Y
                        pawnXTemp += 1
                        pawnYTemp -= 1

                        # We kijken of de X en Y nog op het bord zitten
                        if (pawnXTemp < 9) or (pawnYTemp > 0):

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # We loopen door beide arrays om te kijken of de positie bezet is, wanneer deze bezet is zetten we stopLoop op True om de loop te stoppen
                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][0]) == str(pawnXTemp) and str(blackBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            # We stoppen de loop wanneer stopLoop True is
                            if stopLoop:
                                break
                                
                    # We zetten de variabelen terug om ze weer te gebruiken
                    stopLoop = False
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # We loopen door alle mogelijkheden, wanneer het buiten het bord is stoppen we de loop
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # We "incrementen" de X en Y
                        pawnXTemp -= 1
                        pawnYTemp -= 1

                        # We kijken of de X en Y nog op het bord zitten
                        if (pawnXTemp > 0) or (pawnYTemp > 0):

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # We loopen door beide arrays om te kijken of de positie bezet is, wanneer deze bezet is zetten we stopLoop op True om de loop te stoppen
                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][0]) == str(pawnXTemp) and str(blackBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            # We stoppen de loop wanneer stopLoop True is
                            if stopLoop:
                                break
                                
            # We geven de pawnType mee en returnen het resultaat uit de pieceCheck method die de uiteindelijke coördinaten en bijzonderheden bepaalt                
            pawnType = "B"
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player,promotieLetter, i, posx, posy))
        
        # Wanneer R in de move staat hebben we een Rook
        elif "R" in move:

            # We loopen door alle pionnen van de speler die aan de beurt is
            for pawn in playerBoard:

                # We kijken alleen naar de pionnen waarbij de waarde in de array een R bevat (Dit is zodat gepromoveerde pionnen ook werken)
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

                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    stopLoop = False
                            

            pawnType = "R"
            
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player, promotieLetter, i, posx, posy))

        elif "Q" in move:

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

                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
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

                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            if stopLoop:
                                break

                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

            pawnType = "Q"        
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player, promotieLetter, i, posx, posy))


        elif "N" in move:

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
            
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player, promotieLetter, i, posx, posy))
                        
        elif "K" in move:

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
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player, promotieLetter, i, posx, posy))
        
        else:

            if promotie:
                move = move[:-1]
                moveSplit = list(move)
                
            if move == "O-O":
                rokade = 1

                if player == "white":
                    # self.chielsmethod(0, 0, 0, 0, 0, 0, 0, rokade, 0, 0)
                    return("5 1-7 1#8 1-6 1", self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, rokade, False, player, posx, posy))
                    
                else:
                    # self.chielsmethod(0, 0, 0, 0, 0, 0, 0, rokade, 0, 0)
                    return("5 8-7 8#8 8-6 8", self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, rokade, False, player, posx, posy))
                    

            if move == "O-O-O":
                rokade = 2
                
                if player == "white":
                    # self.chielsmethod(0, 0, 0, 0, 0, 0, 0, rokade, 0, 0)
                    return("5 1-3 1#1 1-4 1", self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, rokade, False, player, posx, posy))
                    
                    
                else:
                    # self.chielsmethod(0, 0, 0, 0, 0, 0, 0, rokade, 0, 0)
                    return("5 8-3 8#1 8-4 8", self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, rokade, False, player, posx, posy))
                    

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
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player, promotieLetter, i, posx, posy))
                                
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
          
    def pieceCheck(self, amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, passant, player, promotieLetter, i, posx, posy):

        # We initialiseren alle variabelen
        eindX = movementX
        eindY = movementY

        startX = startX
        startY = startY

        graveyardX = 0
        graveyardY = 0

        # We kijken of er meerdere mogelijkheden zijn
        if amountOfPawns > 1:

            # Wanneer de move een x bevat moet de stringbewerking anders worden toegepast
            if "x" in move:
                
                checkMove = move[1:-3]                        
                
            else:

                checkMove = move[1:-1]
                checkMove = checkMove[0]
                
            # We kijken of de mogelijkheid moet worden berekent met met de X of Y coördinaat (X is in letter, Y in nummer)
            if checkMove.isalpha():

                # We zetten de letter om in een nummer
                checkMove = self.letterToNumber(checkMove)

                # We loopen door alle pionnen van dit type en kijken welke het kan zijn
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

            # We loopen door alle pionnen van dit type en kijken welke het kan zijn
            for pawn in playerBoard:

                    if pawnType in playerBoard[pawn][1]:

                        if pawnType == "P":

                            pawnNumber = pawnType + str(i)

                            if pawnNumber in playerBoard[pawn][1]:

                                startX = int(playerBoard[pawn][0][:-2])
                                startY = int(playerBoard[pawn][0][-1])

        # Wanneer een andere pion wordt geslagen kijken we ook waar deze moet staan   
        if slagen == True:

            # We zetten de eindpositie om naar één variabel
            endCords = str(eindX) + " " + str(eindY)

            # We zetten passant in eerste instantie op true
            passant = True

            # We kijken wat de array voor de tegenstander is en zetten deze in een variabel
            if player == "black":
                enemyBoard = whiteBoard
            elif player == "white":
                enemyBoard = blackBoard            
                
            # Er wordt door alle pionnen van de tegenstander geloopt   
            for pawn in enemyBoard:

                # We kijken welke pion wordt geslagne en zorgen dat de coördinaten voor de pion in de graveyard wordt berekent
                if enemyBoard[pawn][0] == endCords:

                    passant = False

                    graveyardPos = graveyard[pawn]
                    
                    graveyardX = int(graveyardPos[:-2])

                    if graveyardX == 10:

                        graveyardY = int(graveyardPos[3])
                        
                    else:
                        
                        graveyardY = int(graveyardPos[2])

                    break

            else:

                if passant:

                    if player == "black":
                        endCords = str(eindX) + " " + str(eindY + 1)
                    elif player == "white":
                        endCords = str(eindX) + " " + str(eindY - 1)

                        for pawn in enemyBoard:

                            # Er wordt door alle pionnen van de tegenstander geloopt   
                            for pawn in enemyBoard:

                                # We kijken welke pion wordt geslagen en zorgen dat de coördinaten voor de pion in de graveyard wordt berekent
                                if enemyBoard[pawn][0] == endCords:

                                    graveyardPos = graveyard[pawn]
                                    
                                    graveyardX = int(graveyardPos[:-2])

                                    if graveyardX == 10:

                                        graveyardY = int(graveyardPos[3])
                                        
                                    else:
                                        
                                        graveyardY = int(graveyardPos[2])

                                    break

                            

        # Ergens zit een bug waardoor startX 7 soms naar 9 wordt gezet, hiernaar moet nog worden gekeken
        if startX == 9:
            startX = 7

        print(passant)


        if passant:
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY) + "X"
            return(returnVar, self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, 0, True, player, posx, posy))
        
        elif promotieY != 0:
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY) + "&=" + promotieLetter
            return(returnVar, self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, 0, False, player, posx, posy))
        
        else:
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY)
            return(returnVar, self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, 0, False, player, posx, posy))

    # roep deze functie aan om het spel opnieuw klaar te zetten
    def resetBoard(self, white, black, posx, posy):
        print("resetboard")
        print(posx, posy)
        # dit zet de array op volgorde zodat erdoor heen kan worden gegaan op volgorde van de for loop
        whiteConverted = {
            "R1" : [white["R1"][0], "K1"],
            "N1" : [white["N1"][0], "Q1"],
            "B1" : [white["B1"][0], "B1"],
            "Q1" : [white["Q1"][0], "B2"],
            "K1" : [white["K1"][0], "N1"],
            "B2" : [white["B2"][0], "N2"],
            "N2" : [white["N2"][0], "R1"],
            "R2" : [white["R2"][0], "R2"],
            "P1" : [white["P1"][0], "P1"],
            "P2" : [white["P2"][0], "P2"],
            "P3" : [white["P3"][0], "P3"],
            "P4" : [white["P4"][0], "P4"],
            "P5" : [white["P5"][0], "P5"],
            "P6" : [white["P6"][0], "P6"],
            "P7" : [white["P7"][0], "P7"],
            "P8" : [white["P8"][0], "P8"]
            }

        blackConverted = {
            "R1" : [black["R1"][0], "K1"],
            "N1" : [black["N1"][0], "Q1"],
            "B1" : [black["B1"][0], "B1"],
            "Q1" : [black["Q1"][0], "B2"],
            "K1" : [black["K1"][0], "N1"],
            "B2" : [black["B2"][0], "N2"],
            "N2" : [black["N2"][0], "R1"],
            "R2" : [black["R2"][0], "R2"],
            "P1" : [black["P1"][0], "P1"],
            "P2" : [black["P2"][0], "P2"],
            "P3" : [black["P3"][0], "P3"],
            "P4" : [black["P4"][0], "P4"],
            "P5" : [black["P5"][0], "P5"],
            "P6" : [black["P6"][0], "P6"],
            "P7" : [black["P7"][0], "P7"],
            "P8" : [black["P8"][0], "P8"]
            }

        whiteActual = {
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

        blackActual = {
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



        eindX = 1
        eindY = 1
        count = 1
        elektro = False
        for pos in whiteConverted:
            place = list(white[pos][0])

            startX = place[0]
            startY = place[-1]

            if (int(startX) == int(eindX)) & (int(startY) == int(eindY)):
                print("Pion is nooit bewogen")
                                              
            else:
                print(startX, startY, posx, posy, eindX, eindY)
                startX = int(startX)
                startY = int(startY)
                eindX = int(eindX)
                eindY = int(eindY)
                posx, posy, elektro = self.Reset((startX+2)*2, startY*2, (eindX+2)*2, eindY*2, posx, posy, elektro)
            
            eindX += 1
            count += 1
            if eindX is 9:
                eindX = 1
            if count is 9:
                eindY += 1

        eindX = 1
        eindY = 8
        count = 1
                
        for pos in blackConverted:
            place = list(black[pos][0])

            startX = place[0]
            startY = place[-1]

            if (int(startX) == int(eindX)) & (int(startY) == int(eindY)):
                print("Pion is nooit bewogen")
            else:
                startX = int(startX)
                startY = int(startY)
                eindX = int(eindX)
                eindY = int(eindY)
                posx, posy, elektro = self.Reset((startX+2)*2, startY*2, (eindX+2)*2, eindY*2, posx, posy, elektro)
            
            eindX += 1
            count += 1
            if eindX is 9:
                eindX = 1
            if count is 9:
                eindY -= 1

        return(whiteActual, blackActual)

    def Set(self, inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy, promotie, rokade, passant, beurt, posx, posy):

        inputstartx = int(inputstartx)
        inputstarty = int(inputstarty)

        inputendx = int(inputendx)
        inputendy = int(inputendy)

        inputslagx = int(inputslagx)
        inputslagy = int(inputslagy)

        elektro = False
        startx, starty, endx, endy, slagx, slagy = self.Omrekenen(inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy, beurt)
        if(rokade == 0):
            
            if(promotie == 0):
                
                if(inputslagx != 0 and inputslagy != 0):

                    if(passant == True):

                        if(beurt == "white"):
                            endy -= 2

                        if(beurt == "black"):
                            endy += 2
                                          
                    posx, posy, elektro = self.Slag(endx, endy, posx, posy, slagx, slagy, 0 , beurt, elektro)

                posx, posy, moveh, elektro = self.Moveh(startx, starty, endx, endy, posx, posy, elektro)

                if(moveh == False):

                    if(passant):

                        if(beurt == "white"):
                            endy += 2

                        if(beurt == "black"):
                            endy -= 2

                    posx, posy, elektro = self.Move(posx, posy, startx, starty, endx, endy, beurt, elektro)

            if(promotie != 0):

                posx, posy, elektro = self.Move(posx, posy, startx, starty, endx, endy, beurt, elektro)
                promotie *= 2
                y3 = promotie

                if(beurt == "white"):
                    x = 4
                    x2 = 2
                    y = 18
                    y2 = 16
                    beurtint = 1

                if(beurt == "black"):
                    x = 22
                    x2 = 24
                    y = 0
                    y2 = 2
                    beurtint = 2
                    
                posx, posy, elektro = self.Slag(endx, endy, posx, posy, slagx, slagy, beurtint, beurt, elektro)
                posx, posy = self.Beweegposxy(posx, posy, x2, y3)
                elektro = self.Elektromagneet(1, elektro)
                posx, posy = self.Beweegposxy(posx, posy, x, posy)
                posx, posy = self.Beweegposxy(posx, posy, posx, y)
                posx, posy = self.Beweegposxy(posx, posy, endx, posy)
                posx, posy = self.Beweegposxy(posx, posy, posx, y2)
                elektro = self.Elektromagneet(0, elektro)
        
                    
        if(rokade == 1):
            x1 = 18
            x2 = 20
            x3 = 16

        if(rokade == 2):
            x1 = 10
            x2 = 6
            x3 = 12   

        if(beurt == "white"):
            y1 = 2
            y2 = 0

        if(beurt == "black"):
            y1 = 16
            y2 = 18

        if(rokade != 0): 
            posx, posy = self.Beweegposxy(posx, posy, 14, y1)
            elektro = self.Elektromagneet(1, elektro)
            
            posx, posy = self.Beweegposxy(posx, posy, x1, y1)
            elektro = self.Elektromagneet(0, elektro)
            
            posx, posy = self.Beweegposxy(posx, posy, x2, y1)
            elektro = self.Elektromagneet(1, elektro)
            
            posx, posy = self.Beweegposxy(posx, posy, x2, y2)
            posx, posy = self.Beweegposxy(posx, posy, x3, y2)
            posx, posy = self.Beweegposxy(posx, posy, x3, y1)
            elektro = self.Elektromagneet(0, elektro)
        return posx, posy



            
    def Slag(self, endx, endy, posx, posy, slagx, slagy, beurt, beurtstring, elektro):

        endx = int(endx)
        endy = int(endy)

        posx = int(posx)
        posy = int(posy)

        slagx = int(slagx)
        slagy = int(slagy)
        
        posx, posy = self.Beweegposxy(posx, posy, endx, endy)
        elektro = self.Elektromagneet(1, elektro)
        posx, posy = self.Beweegposxy(posx, posy, posx, endy + 1)

        if(beurt == 0):
            if(beurtstring == "white"):
                posx, posy = self.Beweegposxy(posx, posy, 22, posy)
            if(beurtstring == "black" ):
                posx, posy = self.Beweegposxy(posx, posy, 4, posy)
            x = slagx
        if(beurt == 1):
            posx, posy = self.Beweegposxy(posx, posy, 4, posy)
            x = 0   
        if(beurt == 2):
            posx, posy = self.Beweegposxy(posx, posy, 22, posy)
            x = 26
        posx, posy = self.Beweegposxy(posx, posy, posx, slagy + 1)
        posx, posy = self.Beweegposxy(posx, posy, x, posy)
        posx, posy = self.Beweegposxy(posx, posy, posx, slagy)
        elektro = self.Elektromagneet(0, elektro)
        return posx, posy, elektro

    def Reset(self, startx, starty, endx, endy, posx, posy, elektro):
        posx, posy = self.Beweegposxy(posx, posy, startx, starty)
        elektro = self.Elektromagneet(1, elektro)
        posx, posy = self.Beweegposxy(posx, posy, posx + 1, posy)
        posx, posy = self.Beweegposxy(posx, posy, posx, endy + 1) 
        posx, posy = self.Beweegposxy(posx, posy, endx, posy)
        posx, posy = self.Beweegposxy(posx, posy, posx, endy)
        elektro = self.Elektromagneet(0, elektro)
        return posx, posy, elektro
        

    def Move(self, posx, posy, startx, starty, endx, endy, beurt, elektro):

        endx = int(endx)
        endy = int(endy)

        posx = int(posx)
        posy = int(posy)

        startx = int(startx)
        starty = int(starty)
        
        posx, posy = self.Beweegposxy(posx, posy, startx, starty)
        
        #zet de elektromagneet aan
        elektro = self.Elektromagneet(1, elektro)
        
        #beweegt de elektromagneet naar de eindbestemming
        posx, posy = self.Beweegposxy(posx, posy, endx, endy)

        #zet de elektromagneet uit
        elektro = self.Elektromagneet(0, elektro)
        return posx, posy, elektro

    def Moveh(self, startx, starty, endx, endy, posx, posy, elektro):

        endx = int(endx)
        endy = int(endy)

        posx = int(posx)
        posy = int(posy)

        startx = int(startx)
        starty = int(starty)
        
        movementx = endx - startx
        movementy = endy - starty
        if((movementx == 2 and movementy == 4) or (movementx == 4 and movementy == 2)
           or (movementx == 4 and movementy == 2) or (movementx == 4 and movementy == -2)
           or (movementx == 2 and movementy == -4) or (movementx == -2 and movementy == -4)
           or (movementx == -4 and movementy == -2) or (movementx == -4 and movementy == 2)
           or (movementx == -2 and movementy == 4)):
            posx, posy = self.Beweegposxy(posx, posy, startx, starty)
            elektro = self.Elektromagneet(1, elektro)
            if(movementx == 2 or movementx == -2):
                x = movementx / 2
            else:
                x = 0
            if(movementx == 4 or movementx == -4):
                x2 = movementx
            else:
                x2 = 0
            if(movementy == 2 or movementy == -2):
                y = movementy / 2
            else:
                y = 0
            if(movementy == 4 or movementy == -4):
                y2 = movementy
            else:
                y2 = 0
            posx, posy = self.Beweegposxy(posx, posy, posx + x, posy + y)
            posx, posy = self.Beweegposxy(posx, posy, posx + x2, posy + y2)
            posx, posy = self.Beweegposxy(posx, posy, posx + x, posy + y)
            elektro = self.Elektromagneet(0, elektro)
            return posx, posy, True, elektro
        else:
            return posx, posy, False, elektro

    def Omrekenen(self, inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy, beurt):
     
        inputendx = int(inputendx)
        inputendy = int(inputendy)

        inputslagx = int(inputslagx)
        inputslagy = int(inputslagy)

        inputstartx = int(inputstartx)
        inputstarty = int(inputstarty)
                 
        startx = (inputstartx + 2) * 2
        starty = inputstarty * 2
        
        endx = (inputendx + 2) * 2
        endy = inputendy * 2
        print("");
        print("beurt = " + str(beurt))
        if(inputslagx == 9):
            if(beurt == "black"):
                slagx = 0
            if(beurt == "white"):
                slagx = 26
        if(inputslagx == 10):
            if(beurt == "black"):
                slagx = 2
            if(beurt == "white"):
                slagx = 24
        if(inputslagx == 0):
            slagx = 0
        slagy = inputslagy * 2
        return startx, starty, endx, endy, slagx, slagy

    def Beweegposxy(self, posx, posy, x, y):

        posx = int(posx)
        posy = int(posy)

        x = int(x)
        y = int(y)
        
        movementx = x - posx
        movementy = y - posy
        posx += movementx
        posy += movementy
        if(movementx != 0):
            self.Motorx(movementx)
        if(movementy != 0): 
            self.Motory(movementy)
        print("posx = " + str(posx) + " posy = " + str(posy))
        x = int((posx/2)-2)
        y = int((posy/2))
        print("x-as " + str(x) + " y-as " + str(y))
        return posx, posy

    def Motorx(self, x):
        print("motor x-as beweeg " + str(x))

    def Motory(self, y):
        print("motor y-as beweeg " + str(y))

    def Elektromagneet(self, status, elektro):
        if(status == 0 and elektro == True):
            print("Deactiveer de elektromagneet")
            elektro = False
        elif(status == 1 and elektro == False):
            print("Activeer de elektromagneet")
            elektro = True
        return elektro    

    
    

            
        
        
usbReader()
