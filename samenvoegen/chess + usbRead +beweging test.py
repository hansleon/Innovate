import urllib.request
import json
import time
import string

#import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)


#x motor
GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

#y motor
GPIO.setup(12, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

#magneet
GPIO.setup(22, GPIO.OUT)

dirx = 26
stepx = 16
enablex = 25

diry = 12
stepy = 6
enabley = 24

GPIO.output(enablex, GPIO.HIGH)
GPIO.output(enabley, GPIO.HIGH)

class usbReader:
    
    def __init__(self):
        position = main.ReadPos(self)
        with open("xyaspos.txt", "w") as file:

            file.write(str(0) + " " + str(0))

        if(position != "0 0"):
            aantalstappenx = int((position.split( )[0]))
            aantalstappeny = int((position.split( )[1]))
            GPIO.output(dirx, GPIO.LOW)
            GPIO.output(diry, GPIO.LOW)
            if(aantalstappenx != 0):
                GPIO.output(enablex, GPIO.LOW)
                while aantalstappenx > 0:
                    GPIO.output(stepx, GPIO.HIGH)
                    time.sleep(0.0004)
                    GPIO.output(stepx, GPIO.LOW)
                    time.sleep(0.0004)
                    #print(aantalstappenx)
                    aantalstappenx -= 1
                GPIO.output(enablex, GPIO.HIGH)
            if(aantalstappeny != 0):
                GPIO.output(enabley, GPIO.LOW)
                while aantalstappeny > 0:
                    GPIO.output(stepy, GPIO.HIGH)
                    time.sleep(0.0004)
                    GPIO.output(stepy, GPIO.LOW)
                    time.sleep(0.0004)
                    #print(aantalstappeny)
                    aantalstappeny -= 1
                GPIO.output(enabley, GPIO.HIGH)
            

            
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
##                    #print(gameID)
##                    #print("file is empty")
##                    time.sleep(3)
##                else:
##                    main(gameID)
##                    #print("started")
##                    boole = False
##            except Exception: 
##                #print("Path is not correct")

        main("Gtdpklen")

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
            #print("De gameID is niet valid.\n")
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
        
        # Wanneer het bord niet mag worden gestart moet ook niks ge#print worden (DEBUGGING)
        if stopBoard != True:
            self.#printChessBoard(white, black)

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

                #print(cords)

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

                    promoInGraveyard = cords[-1]

                    cords = cords[:-1]

                    if promoInGraveyard == "F":

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

                    elif promoInGraveyard == "T":

                         # We splitsen de coördinaten op op  de &
                        cords = cords.split("&")

                        cord = cords[0]
                        cord = cord.split("-")

                        beginX = cord[0][0]
                        beginY = cord[0][2]

                        eindX = cord[1][0]
                        eindY = cord[1][2]

                        # van de tweede helft wordt de = afgehaalt en blijft alleen een letter over
                        promo = cords[1][1]

                        # Deze variabel is om te kijken of er al een stuk verplaatst is
                        foundOne = False

                        # We kijken of de speler wit of zwart is
                        if player == "white":

                            # We loopen door alle witte pionnen
                            for pawn in white:

                                # De begincoördinaten worden in een variable gezet
                                beginCord = beginX + " " + beginY

                                # Dit coördinaat kijk waar de pawn staat
                                pawnCord = white[pawn][0]

                                # We checken of de pion op de plek staat
                                if pawnCord == beginCord:

                                        # Zo ja, dan mag deze naar de graveyard
                                        white[pawn][0] = graveyardPos[pawn]

                                # We zoeken de pion waarnaar wordt gepromoveerd
                                if promo in pawn and not foundOne:

                                    # De x coördinaat wordt hiervan opgehaalt
                                    pawnCordX = pawnCord.split(" ")
                                    pawnCordX = pawnCordX[0]

                                    # We checken of deze in de graveyard zit
                                    if pawnCordX == "9" or pawnCordX == "10":

                                        # Zo ja, da 
                                        white[pawn][0] = eindX + " " + eindY

                                        # Er hoeft maar een pion te worden verplaatst (Er zijn bijv 2 paarden in de graveyard maar we zijn maar 1 nodig)
                                        foundOne = True

                        # We kijken of de speler wit of zwart is
                        elif player == "black":

                            # We loopen door alle zwarte pionnen
                            for pawn in black:

                                # De begincoördinaten worden in een variable gezet
                                beginCord = beginX + " " + beginY

                                # Dit coördinaat kijk waar de pawn staat
                                pawnCord = black[pawn][0]

                                # We checken of de pion op de plek staat
                                if pawnCord == beginCord:

                                        # Zo ja, dan mag deze naar de graveyard
                                        black[pawn][0] = graveyardPos[pawn]

                                # We zoeken de pion waarnaar wordt gepromoveerd
                                if promo in pawn and not foundOne:

                                    # De x coördinaat wordt hiervan opgehaalt
                                    pawnCordX = pawnCord.split(" ")
                                    pawnCordX = pawnCordX[0]

                                    # We checken of deze in de graveyard zit
                                    if pawnCordX == "9" or pawnCordX == "10":

                                        # Zo ja, da 
                                        black[pawn][0] = eindX + " " + eindY

                                        # Er hoeft maar een pion te worden verplaatst (Er zijn bijv 2 paarden in de graveyard maar we zijn maar 1 nodig)
                                        foundOne = True
                                
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

                # De #printChessBoard is een debug method, deze #printen we voor een visuele representatie
                self.#printChessBoard(white, black)

            # Wanneer we bij een stap zijn die nog niet is gezet (Het potje is dus afgelopen of nog bezig) checken we of het potje al klaar is
            elif data["status"] != "started":
                
                #print("Game is klaar.")
                #print("De game wordt gereset")

                # We runnen de reset functie om het bord naar originele posities te resetten
                newArrays = self.resetBoard(white, black, posx, posy)
                #print(posx, posy)
                white, black = newArrays
                self.#printChessBoard(white, black) 
                
                input("Press enter to continue...")
                break
                

    # De #printChessBoard() method geeft een visuele representatie van de posities van alle pionnen
    def #printChessBoard(self, white, black):

        # ---------------------------------------------------------------------
        # Dit eerste stuk is voor het maken van de string van het complete bord
        # ---------------------------------------------------------------------
        
        # schaakbord is de string waarin alle posities worden toegevoegd
        board = ""

        # variabel y is de y positie van de pionen
        y = 8

        # We loopen door alle y mogelijkheden beginnent bovenin (aangezien het #printen van de string linksboven begint)
        while y > 0:
            
            # variabel x is de x positie van de pionen
            x = 1

            # We loopen door alle x mogelijkheden beginnent links (aangezien het #printen van de string linksboven begint)
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

        # We loopen door alle y mogelijkheden beginnent bovenin (aangezien het #printen van de string linksboven begint)
        while y > 0:

            # variabel x is de x positie van de pionen
            x = 9

            # We loopen door alle x mogelijkheden beginnent links (aangezien het #printen van de string linksboven begint)
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
            
            # We loopen door alle x mogelijkheden beginnent links (aangezien het #printen van de string linksboven begint)
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

            
        # Hier worden de twee strings ge#print

        # De string schaakbord wordt ge#print en laat visueel de positie van elke pion op het bord zien
        #print("Board:")
        #print(board)

        # De string graveyard wordt ge#print en laat visueel de positie van elke geslagen pion zien
        #print("graveyards:")
        #print(graveyard)

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
            #print(move)
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

                    # Deze pawnX en Y zijn ervoor om te worden "increment", een bisschop beweegt steeds één vakje verticaal
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

                    # prepareert variabelen van startpositie van de pawn
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    # een variabele die later een loop stop zet als hij true is
                    stopLoop = False

                    # variabelen voor coordinaten die later worden gebruikt
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # een loop die af gaat zolang de waardes binnen de coordinaten van het schaakbord zijn.
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # telt 1 op bij de x-coordinaat zodat de rij rechts van de toren wordt gecontroleerd op stukken
                        pawnXTemp += 1

                        # kijkt og of de coordinaat nog in het schaakbord is
                        if pawnXTemp < 9:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken heen, pawn kan worden gebruikt worden voor zowel wit als zwart
                            for pawn in whiteBoard:

                                # controleert of wit een stuk op de positie van de eerder geprepareerde coordinaten staat
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):

                                    stopLoop = True

                                # controleert of er een zwart stuk op de positie van de eerder geprepareerde coordinaten staat   
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break

                    # coordinaten worden opnieuw opgeslagen
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt gereset 
                    stopLoop = False

                    # controleert of de coordinaten binnen een normaal schaakbord vallen
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # doet de x -1 zodat de rij links van de toren wordt gecheckt op stukken
                        pawnXTemp -= 1

                        # controleert of de x-coordinaat wel op een schaakbord ligt
                        if pawnXTemp > 0:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken heen, pawn kan worden gebruikt worden voor zowel wit als zwart
                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break

                    # coordinaten worden opnieuw opgeslagen 
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt gereset 
                    stopLoop = False

                    # controleert of de coordinaten op een normaal schaakbord passen
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # de y coordinaat wordt plus 1 gedaan zodat de rij boven de toren wordt gecontroleerd
                        pawnYTemp += 1

                        # kijkt of de waarde nog op een normaal schaakbord past
                        if pawnYTemp < 9:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan voor beide kanten van het bord worden gebruikt
                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break
                                    
                    # coordinaten worden gereset
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt gereset 
                    stopLoop = False

                    # kijkt of de stukken op een bordt passen 
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # de y gaat min 1 om de rij onder de toren to controleren
                        pawnYTemp -= 1

                        # kijkt of de positie nog op het schaakbordt is
                        if pawnYTemp > 0:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan voor beide kanten van het bord worden gebruikt
                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break
                            
                    # coordinaten worden gereset
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY
        
                    stopLoop = False
                            
            # variabele wordt geprepareert voor de motor methode 
            pawnType = "R"

            # gaat naar de volgende methode die de motor aanstuurt
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player, promotieLetter, i, posx, posy))

        # controleert of het stuk dat verplaatst wordt een dame is
        elif "Q" in move:

            # loopt door ieder stuk heen van de speler die op dat moment aan de beurt is
            for pawn in playerBoard:

                # controleert of het stuk dat gecontroleerd wordt een dame is, als dat niet zo is kan de loop door naar het volgende stuk
                if "Q" in playerBoard[pawn][1]:

                    # prepareert variabelen voor later
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    stopLoop = False

                    # tijdelijke coordinaten worden geprepareerd
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # controleert of de coordinaten in een normaal schaakbord passen
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # x en y gaan + 1 om de schuine rij naar rechtsboven te controleren
                        pawnXTemp += 1
                        pawnYTemp += 1

                        # kijkt of de coordinaten nog in het schaakbord zijn
                        if (pawnXTemp < 9) or (pawnYTemp < 9):

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan voor beide kanten van het bord worden gebruikt
                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break
                                    
                    # coordinaten worden gereset 
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt terug naar false gezet
                    stopLoop = False

                    # kijkt of de coordinaten in een schaakbord passen
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # x min 1 en y plus 1 om de schuine rij linksboven te controleren
                        pawnXTemp -= 1
                        pawnYTemp += 1

                        # kijkt of de coordinaten nog steeds in een schaakbordt zijn
                        if (pawnXTemp > 0) or (pawnYTemp < 9):

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan voor beide kanten van het bord worden gebruikt
                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break
                                
                    # coordinaten worden gereset 
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt terug naar false gezet 
                    stopLoop = False

                    # controleert of de coordinaten op een schaakbord passen 
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # x plus 1 en y min 1 controleert de schuine rij naar rechtsonder
                        pawnXTemp += 1
                        pawnYTemp -= 1

                        # controleert of de coordinaten nog op een schaakbord passen
                        if (pawnXTemp < 9) or (pawnYTemp > 0):

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan voor beide kanten van het bord worden gebruikt
                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break
                                
                    # De coordinaten worden gereset
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # Stoploop wordt weer op false gezet
                    stopLoop = False

                    # kijkt of de coordinaten binnen een schaakbord vallen
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # x en y min 1 controleert de schuine rij linksonder
                        pawnXTemp -= 1
                        pawnYTemp -= 1

                        # controleert of de coordinaten nog op een schaakbord vallen
                        if (pawnXTemp > 0) or (pawnYTemp > 0):

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan voor beide kanten van het bord worden gebruikt
                            for pawn in whiteBoard:
                                
                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = False

                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break

                    # de coordinaten worden gereset 
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt weer op false gezet 
                    stopLoop = False
                    
                    # controleert of de coordinaten nog in het schaakbord zijn 
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # x plus 1 controleert de rij naar rechts
                        pawnXTemp += 1

                        # controleert of het nog op een schaakbord past 
                        if pawnXTemp < 9:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan voor beide kanten van het bord worden gebruikt
                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                            # als stoploop true is moet de loop worden gestopt 
                            if stopLoop:
                                break

                    # de coordinaten worden gereset 
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt terug naar false gezet 
                    stopLoop = False

                    # er wordt gecontroleert of de coordinaten nog binnen een schaakbord vallen
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # x min 1 controleert de rij naar links
                        pawnXTemp -= 1

                        # controleert of de coordinaten nog op het schaakbord vallen
                        if pawnXTemp > 0:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan dan worden gebruikt voor wit en zwart
                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                            # als stoploop true is moet de loop worden afgebroken
                            if stopLoop:
                                break
                            
                    # de coordinaten worden gereset 
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt weer op false gezet 
                    stopLoop = False

                    # controleert of de coordinaten nog op een schaakbord zijn
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # y plus 1 controleert de rij boven de dame
                        pawnYTemp += 1

                        # controleert of de coordinaten nog in het schaakbord zijn
                        if pawnYTemp < 9:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan dan worden gebruikt voor wit en zwart
                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True

                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break
                                    
                    # de coordinaten worden gereset
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # stoploop wordt weer op false gezet 
                    stopLoop = False

                    # controleert of de coordinaten nog binnen een schaakbord vallen 
                    while pawnXTemp < 9 and pawnXTemp > 0 and pawnYTemp < 9 and pawnYTemp > 0:

                        # y min 1 controleert de rij onder de dame
                        pawnYTemp -= 1

                        # controleert of de coordinaten nog binnen het schaakbord vallen
                        if pawnYTemp > 0:
                            
                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns
                            if str(pawnXTemp) == str(movementX) and str(pawnYTemp) == str(movementY):
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1

                            # loopt door alle stukken van 1 speler heen, de waarde van pawn kan dan worden gebruikt voor wit en zwart
                            for pawn in whiteBoard:

                                if str(whiteBoard[pawn][0][:-2]) == str(pawnXTemp) and  str(whiteBoard[pawn][0][-1]) == str(pawnYTemp):
                                    stopLoop = True
                                    
                                elif str(blackBoard[pawn][0][:-2]) == str(pawnXTemp) and str(blackBoard[pawn][0][2]) == str(pawnYTemp):
                                    stopLoop = True
                            # als stoploop true is moet de loop worden gestopt
                            if stopLoop:
                                break
                            
                    # de coordinaten worden gereset
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

            # het stuk wordt in een variabele gezet 
            pawnType = "Q"

            # gaat naar de volgende methode die de motor aanstuurt
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player, promotieLetter, i, posx, posy))

        # kijkt of het een paard is dat bewogen wordt
        elif "N" in move:

            # loopt door elk stuk van de speler die aan de beurt is heen
            for pawn in playerBoard:

                # kijkt of het stuk waar doorheen geloopt een paard is.
                if "N" in playerBoard[pawn][1]:

                    # prepareert variabelen voor later
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    # controleert de eerste van de acht mogelijke zettten van een paard om te kijken of hij naar de eindpositie kan
                    if pawnX + 2 == movementX and pawnY + 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de tweede van de acht mogelijke zettten van een paard om te kijken of hij naar de eindpositie kan
                    elif pawnX + 2 == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de derde van de acht mogelijke zettten van een paard om te kijken of hij naar de eindpositie kan
                    elif pawnX - 2 == movementX and pawnY + 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de vierde van de acht mogelijke zettten van een paard om te kijken of hij naar de eindpositie kan
                    elif pawnX - 2 == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de vijfde van de acht mogelijke zettten van een paard om te kijken of hij naar de eindpositie kan
                    elif pawnX + 1 == movementX and pawnY + 2 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de zesde van de acht mogelijke zettten van een paard om te kijken of hij naar de eindpositie kan
                    elif pawnX + 1 == movementX and pawnY - 2 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de zevende van de acht mogelijke zettten van een paard om te kijken of hij naar de eindpositie kan
                    elif pawnX - 1 == movementX and pawnY + 2 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de achtste van de acht mogelijke zettten van een paard om te kijken of hij naar de eindpositie kan
                    elif pawnX - 1 == movementX and pawnY - 2 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1

            # slaat op welk stuk het is dat bewogen wordt
            pawnType = "N"

            # gaat naar de volgende methode die de motor aanstuurt
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player, promotieLetter, i, posx, posy))

        # controleert of het een koning is dat bewogen wordt, behalve rokade, dat wordt elders gedaan
        elif "K" in move:

            # loopt door elk stuk heen van de speler die aan de beurt is
            for pawn in playerBoard:

                # kijkt of het stuk in de loop een koning is
                if "K" in playerBoard[pawn][1]:

                    # prepareert variabelen voor later
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    # controleert de eerste van de acht mogelijke zettten van de koning om te kijken of hij naar de eindpositie kan
                    if pawnX + 1 == movementX and pawnY == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de tweede van de acht mogelijke zettten van de koning om te kijken of hij naar de eindpositie kan
                    elif pawnX + 1 == movementX and pawnY +1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de derde van de acht mogelijke zettten van de koning om te kijken of hij naar de eindpositie kan
                    elif pawnX + 1 == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de vierde van de acht mogelijke zettten van de koning om te kijken of hij naar de eindpositie kan
                    elif pawnX == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de vijfde van de acht mogelijke zettten van de koning om te kijken of hij naar de eindpositie kan
                    elif pawnX == movementX and pawnY + 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de zesde van de acht mogelijke zettten van de koning om te kijken of hij naar de eindpositie kan
                    elif pawnX - 1 == movementX and pawnY + 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de zevende van de acht mogelijke zettten van de koning om te kijken of hij naar de eindpositie kan
                    elif pawnX - 1 == movementX and pawnY == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1
                        
                    # controleert de achtste van de acht mogelijke zettten van de koning om te kijken of hij naar de eindpositie kan
                    elif pawnX - 1 == movementX and pawnY - 1 == movementY:
                        startX = pawnX
                        startY = pawnY
                        eindX = movementX
                        eindY = movementY
                        amountOfPawns += 1

            # slaat op dat het de koning is die bewoog
            pawnType = "K"

            # geeft alle info door aan de volgende functie die uiteindelijk de motor aanstuurt
            return(self.pieceCheck(amountOfPawns, move, playerBoard, graveyard, startX, startY, movementX, movementY, slagen, pawnType, whiteBoard, blackBoard, promotieY, rokade, False, player, promotieLetter, i, posx, posy))
        
        else:

            # controleert of er promotie plaatsvind en haalt dit uit de string
            if promotie:
                move = move[:-1]
                moveSplit = list(move)

            # controleert of een korte rokade plaatsvind
            if move == "O-O":
                rokade = 1

                # rokade is altijd hetzelfde, hier doet hij de korte rokade voor de witte speler met vaste waardes
                if player == "white":
                    # self.chielsmethod(0, 0, 0, 0, 0, 0, 0, rokade, 0, 0)
                    return("5 1-7 1#8 1-6 1", self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, rokade, False, player, posx, posy))

                # rokade is altijd hetzelfde, hier doet hij de korte rokade voor de zwarte speler met vaste waardes
                else:
                    # self.chielsmethod(0, 0, 0, 0, 0, 0, 0, rokade, 0, 0)
                    return("5 8-7 8#8 8-6 8", self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, rokade, False, player, posx, posy))
                    
            # controleert of er een lange rokade plaatsvind
            if move == "O-O-O":
                rokade = 2

                # rokade is altijd hetzelfde, hier doet hij de lange rokade voor de witte speler met vaste waardes
                if player == "white":
                    # self.chielsmethod(0, 0, 0, 0, 0, 0, 0, rokade, 0, 0)
                    return("5 1-3 1#1 1-4 1", self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, rokade, False, player, posx, posy))
                    
                # rokade is altijd hetzelfde, hier doet hij de lange rokade voor de zwarte speler met vaste waardes
                else:
                    # self.chielsmethod(0, 0, 0, 0, 0, 0, 0, rokade, 0, 0)
                    return("5 8-3 8#1 8-4 8", self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, rokade, False, player, posx, posy))
                    
            # prepareert een variabele voor later
            i = 1

            # loopt door elk stuk heen van de speler die aan de beurt is
            for pawn in playerBoard:

                # kijkt of het stuk waar de loop is een pion is
                if "P" in playerBoard[pawn][1]:

                    # prepareert variabelen voor later
                    pawnX = int(playerBoard[pawn][0][:-2])
                    pawnY = int(playerBoard[pawn][0][-1])

                    # slaat tijdelijke coordinaten op
                    pawnXTemp = pawnX
                    pawnYTemp = pawnY

                    # controleert of niet geslagen word
                    if slagen != True:

                        # controleert of wit aan de beurt is
                        if "white" in player:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns en stoppen de loop
                            if pawnX == movementX and pawnY + 1 == movementY:

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns en stoppen de loop
                            if pawnX == movementX and pawnY + 2 == movementY:

                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break
                            
                            # telt 1 bij i op
                            i += 1

                        # kijkt of zwart aan de beurt is
                        if "black" in player:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns en stoppen de loop
                            if pawnX == movementX and pawnY - 1 == movementY:
                                
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break
                        
                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns en stoppen de loop
                            if pawnX == movementX and pawnY - 2 == movementY:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            # telt 1 bij i op
                            i += 1

                    # als wel geslagen wordt gaat dit af
                    else:

                        # controleert of wit aan de beurt is
                        if "white" in player:

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns en stoppen de loop
                            if pawnX + 1 == movementX and pawnY + 1 == movementY and pawnX < 9 and pawnY < 9:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns en stoppen de loop
                            if pawnX - 1 == movementX and pawnY + 1 == movementY and pawnX > 0 and pawnY < 9:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break

                            # telt 1 bij i op
                            i += 1

                        # kijkt of zwart aan de beurt is 
                        if "black" in player:
                            
                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns en stoppen de loop
                            if pawnX + 1 == movementX and pawnY - 1 == movementY and pawnX < 9 and pawnY > 0:
                                
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break
                        
                            # We kijken of we de juiste positie gevonden hebben, dan zetten we de variabelen om en incrementen we amountOfPawns en stoppen de loop
                            if pawnX - 1 == movementX and pawnY - 1 == movementY and pawnX > 0 and pawnY > 0:
                                startX = pawnX
                                startY = pawnY
                                eindX = movementX
                                eindY = movementY
                                amountOfPawns += 1
                                break
                            
                            # telt 1 bij i op
                            i += 1
                            
            # slaat op dat het een pion is die beweegt
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

                # We kijken welke pion wordt geslagen en zorgen dat de coördinaten voor de pion in de graveyard wordt berekend
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

        # als passant geslagen wordt wordt daar hier de motor methode aangeroepen
        if passant:
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY) + "X"
            return(returnVar, self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, 0, True, player, posx, posy))

        # als promotie plaatsvind wordt hier de motor methode aangeroepen
        elif promotieY != 0:

            # We geven promoInGraveyard en pawnCordY een basis waarde.
            promoInGraveyard = "F"
            pawnCordY = 0

            # We loopen door de pionnen van de speler
            for pawn in playerBoard:

                # We kijken alleen naar de pionen van het type dat we willen hebben
                if promotieLetter in pawn:

                    # We halen de X en Y waarde op van deze pionnen
                    pawnCords = playerBoard[pawn][0]
                    pawnCord = pawnCords.split(" ")
                    pawnCordX = pawnCord[0]
                    pawnCordY = pawnCord[1]

                    # Wanneeer de X 9 of 10 is staat de pion in de graveyard
                    if pawnCordX == "9" or pawnCordX == "10":

                        # We zetten de promoInGraveyard op T van True en breaken de loop
                        promoInGraveyard = "T"
                        break

                    
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY) + "&=" + promotieLetter + promoInGraveyard
            return(returnVar, self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, pawnCordY, 0, False, player, posx, posy))

        # hier wordt de motor methode aangeoepen als er geen passant is en geen promotie
        else:
            
            returnVar = str(startX) + " " + str(startY) + "-" + str(eindX) + " " + str(eindY)
            return(returnVar, self.Set(startX, startY, eindX, eindY, graveyardX, graveyardY, 0, 0, False, player, posx, posy))

    # roep deze functie aan om het spel opnieuw klaar te zetten
    def resetBoard(self, white, black):

        # dit zet de arrays op volgorde van links naar rechts zodat met simpele tellers de eindposities kunnen worden bepaald
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
        
        # dit zijn de standaardposities van een ongespeeld schaakspel die worden teruggestuurd als deze method klaar is
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

        # dit zijn de graveyard posities van stukken als ze geslagen zijn
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

        # de tellers voor wit, en een variabele die aangeeft welke speler zijn stukken worden verplaatst.
        eindX = 1
        eindY = 1
        count = 1
        player = "white"
        graveX = 1
        graveY = 1
        

        # loopt door elk stuk heen die gereset moet worden
        for pos in whiteConverted:

            # variabelen die gereset moeten worden elke keer dat de loop af gaat
            finished = False
            noMove = False

            # variabelen die gebruikt worden om te controleren wat er gebeurt
            eindXY = whiteActual[pos][0]
            eindXYList = eindXY.split()
            eindX2 = eindXYList[0]
            eindY2 = eindXYList[-1]

            #als dit werkt dan staat er wat op de eindpositie van het stuk, deze methode zet dat stuk in de grave zodat er ruimte is voor het stuk dat naar de originele plaats moet
            for pos2 in whiteConverted:

                # variabele voor de controle klaarmaken
                startXY = whiteConverted[pos2][0]

                #als dit werkt dan staat er wat op de eindpositie van het stuk
                if startXY in eindXY:

                    #deze kijkt of het stuk verplaatst moet worden, als de if af gaat moet hij niet verplaatst worden
                    if pos in pos2:

                        # #print("0 0 0 0 0 0 0 0 False White - hier wordt niets verplaatst")

                        # deze variabelen geven aan voor de rest dat er niets meer gedaan hoeft te worden.
                        finished = True
                        noMove = True

                    # als de if niet af gaat moet het stuk verplaatst worden 
                    else:

                        # prepareert de variabelen voor de methode van het aansturen van de motors
                        graveXY = graveyardPos[pos2].split()
                        graveX = graveXY[0]
                        graveY = graveXY[-1]

                        # roept de motor methodes aan
                        # #print(0, 0, eindX, eindY, graveX, graveY, 0, 0, False, "white maakt plaats")
                        #self.Set(0, 0, eindX, eindY, graveX, graveY, 0, 0, False, "white")

                        # update de positie van het bewogen stuk in de array van wit
                        whiteConverted[pos2][0] = graveyardPos[pos2]
                        #print(whiteConverted[pos2][0], "is het er klaar voor?")

            
            # de loop die controleert of er zwarte stukken in de weg staan
            for pos2 in blackConverted:

                # variabele voor de controle klaarmaken
                startXY = blackConverted[pos2][0]

                #als dit werkt dan staat er wat op de eindpositie van het stuk, deze methode zet dat stuk in de grave zodat er ruimte is voor het stuk dat naar de originele plaats moet
                if startXY in eindXY:

                    # prepareert de variabelen voor de methode van het aansturen van de motors
                    graveXY = graveyardPos[pos2].split()
                    graveX = graveXY[0]
                    graveY = graveXY[-1]

                    # roept de motor methodes aan
                    #print(0, 0, eindX, eindY, graveX, graveY, 0, 0, False, "black maakt plaats")
                    #self.Set(0, 0, eindX, eindY, graveX, graveY, 0, 0, False, "black")

                    # update de positie van het bewogen stuk in de array van zwart
                    blackConverted[pos2][0] = graveyardPos[pos2]

            # als finished en noMove niet op true is gezet betekent het dat het stuk gewoon van positie a naar b kan worden gezet.                          
            if noMove is False:      
                
                if finished is False:

                    # prepareert de variabelen voor de motor methode
                    startXY = whiteConverted[pos][0].split()
                    startX = startXY[0]
                    startY = startXY[-1]
                    nextEindXY = str(eindX) + str(" ") + str(eindY)

                    # roept de motor methode aan 
                    # #print(startX, startY, eindX, eindY, 0, 0, 0, 0, False, "white")
                    # self.Set(startX, startY, eindX, eindY, 0, 0, 0, 0, False, "white")

                    # update de nieuwe positie van het stuk
                    whiteConverted[pos][0] = nextEindXY
                    
            # x houdt bij waar op de x-as het volgende stuk moet staan
            eindX += 1

            # als x 9 is moet y op 2 voor de witte pionnen, en x op 2 om in de goede rij te zitten
            if eindX is 9:
                eindX = 1
                eindY += 1
    
        #print(" ")
        #print("hier begint zwart")
        #print(" ")
        
        # de tellers voor zwart, en een variabele die aangeeft welke speler zijn stukken worden verplaatst.
        eindX = 1
        eindY = 8
        count = 1
        player = "black"
        graveX = 1
        graveY = 1
        

        # gaat door elk stuk heen die gereset moet worden
        for pos in blackConverted:

            # variabelen die gereset moeten worden elke keer dat de loop af gaat 
            finished = False
            noMove = False

            # variabelen die gebruikt worden om te controleren wat er gebeurt
            eindXY = blackActual[pos][0]
            eindXYList = eindXY.split()
            eindX2 = eindXYList[0]
            eindY2 = eindXYList[-1]

            # de loop die controleert of witte stukken in de weg staan        
            for pos2 in whiteConverted:

                # variabele voor de controle klaarmaken
                startXY = whiteConverted[pos2][0]

                #als dit werkt dan staat er wat op de eindpositie van het stuk, deze methode zet dat stuk in de grave zodat er ruimte is voor het stuk dat naar de originele plaats moet
                if startXY in eindXY:

                    # prepareert de variabelen voor de motor methode 
                    graveXY = graveyardPos[pos2].split()
                    graveX = graveXY[0]
                    graveY = graveXY[-1]

                    # roept de motor methode aan
                    # #print(0, 0, eindX, eindY, graveX, graveY, 0, 0, False, "white maakt plaats")
                    #self.Set(0, 0, eindX, eindY, graveX, graveY, 0, 0, False, "white")

                    # update de positie van het stuk dat verplaatst wordt
                    whiteConverted[pos2][0] = graveyardPos[pos2]

            
            # de loop die controleert of witte stukken in de weg staan
            for pos2 in blackConverted:

                # variabele voor de controle klaarmaken
                startXY = blackConverted[pos2][0]

                #als dit werkt dan staat er wat op de eindpositie van het stuk, deze methode zet dat stuk in de grave zodat er ruimte is voor het stuk dat naar de originele plaats moet
                if startXY in eindXY:

                    #deze kijkt of het stuk verplaatst moet worden, als de if af gaat moet hij niet verplaatst worden
                    if pos in pos2:
                        
                        # #print("0 0 0 0 0 0 0 0 False White - hier wordt niets verplaatst")

                        # deze variabelen geven aan dat voor de rest niets gedaan hoeft te worden
                        finished = True
                        noMove = True

                    # als de if niet af gaat moet een stuk verplaatst worden om plaats te maken
                    else:

                        # prepareert de variabelen voor de methode van het aansturen van de motors
                        graveXY = graveyardPos[pos2].split()
                        graveX = graveXY[0]
                        graveY = graveXY[-1]

                        # roept de motor methode aan
                        # #print(0, 0, eindX, eindY, graveX, graveY, 0, 0, False, "black maakt plaats") # misschien moet dit white zijn
                        #self.Set(0, 0, eindX, eindY, graveX, graveY, 0, 0, False, "black")

                        # update de posities van het bewogen stuk in de array
                        blackConverted[pos2][0] = graveyardPos[pos2]

            # als noMove en finished false zijn kan/moet het originele stuk nog bewogen worden
            if noMove is False:      

                if finished is False:

                    # prepareert de variabelen voor de motor methode
                    startXY = whiteConverted[pos][0].split()
                    startX = startXY[0]
                    startY = startXY[-1]
                    nextEindXY = str(eindX) + str(" ") + str(eindY)

                    # roept de motor methode aan 
                    # #print(startX, startY, eindX, eindY, 0, 0, 0, 0, False, "white")
                    # self.Set(startX, startY, eindX, eindY, 0, 0, 0, 0, False, "white")

                    # update de positie van het stuk in de array
                    blackConverted[pos][0] = nextEindXY
                    
            # x houdt bij waar op de x-as het volgende stuk moet staan
            eindX += 1

            # als x 9 is moet y op 2 voor de witte pionnen, en x op 2 om in de goede rij te zitten
            if eindX is 9:
                eindX = 1
                eindY -= 1


        # returnt de standaard posities zodat de main methode klaar is voor een volgend spel
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
        startx = int(startx)
        starty = int(starty)
        endx = int(endx)
        endy = int(endy)
        posx = int(posx)
        posy = int(posy)

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
        beweegx = endx - startx
        beweegy = endy - starty
        if((beweegx == beweegy) or (beweegx == -beweegy) or (-beweegx == beweegy)):
            if(beweegx > 0):
                posx, posy = self.Beweegposxy(posx, posy, posx + 1, posy)
            else:
                posx, posy = self.Beweegposxy(posx, poxy, posx - 1, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, endy + 1)
            posx, posy = self.Beweegposxy(posx, posy, endx, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, endy)

        else:
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
        # #print("");
        # #print("beurt = " + str(beurt))
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
        self.BeweegXY(movementx, movementy)
        #print("posx = " + str(posx) + " posy = " + str(posy))
        x = int((posx/2)-2)
        y = int((posy/2))
        # #print("x-as " + str(x) + " y-as " + str(y))
        return posx, posy

    def BeweegXY(self, x, y):
        position = self.ReadPos()
        aantalstappenx = int((position.split( )[0]))
        aantalstappeny = int((position.split( )[1]))
        #hoeveel stappen voor half vlak (205)
        stapx = 205
        stapy = 400
        i = 0
        j = 0
        
        directionx = 0
        directiony = 0
        #zet de driver aan als het de motor moet draaien
        if(x != 0):
            GPIO.output(enablex, GPIO.LOW)
            #print("enablex is on")
        if(y != 0):
            GPIO.output(enabley, GPIO.LOW)
            #print("enabley is on")
            
        #bepaalt de richting en het aantal stappen voor de x- as
        if(x > 0):
            GPIO.output(dirx, GPIO.HIGH)
            #print("dirx is HIGH")
            directionx = 1
            i = x * 1 * stapx
        if(x < 0):
            GPIO.output(dirx, GPIO.LOW)
            #print("dirx is LOW")
            directionx = -1
            x *= -1
            i = x * 1 * stapx

        #bepaalt de richting en het aantal stappen voor de y- as
        if(y > 0):
            GPIO.output(diry, GPIO.HIGH)
            #print("diry is HIGH")
            directiony = 1
            j = y * 1 * stapy
        if(y < 0):
            GPIO.output(diry, GPIO.LOW)
            #print("diry is LOW")
            directiony = -1
            y *= -1
            j = y * 1 * stapy

        #bepaalt hoevaak de loop zich moet herhalen aan de hand van de motor die het langst moet bewegen
        total = i
        if(j > i):
            total = j

        #de bewegigins loop
        while total > 0:

            #zet de motor 1 tik aan 
            if(i > 0):
                GPIO.output(stepx, GPIO.HIGH)
                #print("aan " + str(i))
            if(j > 0):
                GPIO.output(stepy, GPIO.HIGH)
                #print("aan " + str(j))
            time.sleep(0.0004)
            
            if(i > 0):
                GPIO.output(stepx, GPIO.LOW)
                #print("uit " + str(i))
                i -= 1
            else:
                GPIO.output(enablex, GPIO.HIGH)
                #print("enablex is LOW")
                directionx = 0
                
            if(j > 0):
                GPIO.output(stepy, GPIO.LOW)
                #print("uit " + str(j))
                j -= 1
            else:
                GPIO.output(enabley, GPIO.HIGH)
                #print("enabley is LOW")
                directiony = 0

            aantalstappenx += directionx
            aantalstappeny += directiony
            self.SavePos(aantalstappenx, aantalstappeny)
            time.sleep(0.0004)
            
            total -= 1
            
        GPIO.output(enablex, GPIO.HIGH)
        GPIO.output(enabley, GPIO.HIGH)

    def Elektromagneet(self, status, elektro):
        if(status == 0 and elektro == True):
            #print("Elektromagneet is LOW")
            GPIO.output(22, GPIO.LOW)
            elektro = False
        elif(status == 1 and elektro == False):
            #print("Elektromagneet is HIGH")
            GPIO.output(22, GPIO.HIGH)
            elektro = True
        return elektro    

    
    def SavePos(self, x, y):

        #print(x, y)
        try:
            with open("xyaspos.txt", "w") as file:
                
                file.write(str(x) + " " + str(y))

        except:
            #print(x, y )
    def ReadPos(self):

        with open("xyaspos.txt", "r") as file:
            position = file.read()



        return position
            
        
        
usbReader()
