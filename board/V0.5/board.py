import urllib.request
import json
import time
import string


class main:

    def __init__(self):

        # Deze variabel wordt op true gezet wanneer het bord moet worden gestopt.
        stopBoard = False

        # De path van de file die je wilt lezen (Hierin staat het gameID)
        path = "gameID.txt"

        # Hiermee open je het bestand en geef je aan dat je het wilt lezen (r = read)
        gameIDFile = open(path,"r")

        # Hier lees je de inhoud van de file
        gameID = gameIDFile.read()

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

            # Er zit een delay van 3 seconden op om te voorkomen dat de site het als spam gaat zien
            time.sleep(3)

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
                # cords = self.calcCord(moves[currentMove], player, white, black, graveyard)
                # cords = "3 2-3 4" #Debug placeholder
                cords = "3 2-3 4&=Q"

                

                # De coordinaten worden gesplit op de -, hieruit krijg je een array met de start [0] en eind [1] cords
                if "#" in cords:
                    cords = cords.split("#")
                    cord = cords[0].split("-")
                    print(1)
                elif "&" in cords:
                    cords = cords.split("&")
                    cord = cords[0].split("-")
                    promo = cords[1][1]
                    print(promo)
                    number = 1
                    for pawn in white:
                        if promo in white[pawn][1]:
                            number += 1
                    promo = promo + str(number)
                else:
                    cord = cords.split("-")
                    print(3)


                # Beide cords worden opgeslagen in variabelen
                cordOne = cord[0]
                cordTwo = cord[1]
                
                # Er wordt door zowel de white als de black array geloopt
                for pawnWhite, pawnBlack in zip(white, black):

                    # Eerst wordt gekeken of de beurt gezet is door wit of zwart
                    if player == "white":

                        # Er wordt gechecked of de positie waar de pion naar verplaatst bezet is door een zwarte pion
                        if black[pawnBlack][0] == cordTwo:

                            # Als de positie bezet is door een pion wordt die pion in de "Graveyard" op zijn eigen plek gezet
                            black[pawnBlack][0] = graveyardPos[pawnBlack]

                        # Wanneer de plek vrijgemaakt is kunnen we de pion die moet worden verplaatst verplaatsen
                        if white[pawnWhite][0] == cordOne:
                            white[pawnWhite][0] = cordTwo
                            if cordpromo:
                                promo = cordpromo[1] + "2"
                                white[pawnWhite][1] = promo
                                print(white)

                    elif player == "black":

                        # Er wordt gechecked of de positie waar de pion naar verplaatst bezet is door een witte pion        
                        if white[pawnWhite][0] == cordTwo:

                            # Als de positie bezet is door een pion wordt die pion in de "Graveyard" op zijn eigen plek gezet
                            white[pawnWhite][0] = graveyardPos[pawnWhite]

                        # Wanneer de plek vrijgemaakt is kunnen we de pion die moet worden verplaatst verplaatsen
                        if black[pawnBlack][0] == cordOne:
                            black[pawnBlack][0] = cordTwo
                            if cordpromo:
                                promo = cordpromo[1] + "2"
                                black[pawnBlack][1] = promo
                                print(black)
                

                # Wanneer de zet is gedaan gaan we naar de volgende move
                currentMove += 1

                # Wanneer de zet is gedaan switchen we van kant
                if player == "white":
                    player = "black"
                else:
                    player = "white"

                # De printChessBoard is een debug method, deze printen we voor een visuele representatie
                self.printChessBoard(white, black)
                

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
                        board += white[pawnWhite][1]
                        break
                    elif black[pawnBlack][0] == str(x) + " " + str(y):
                        board += black[pawnBlack][1]
                        break

                # Wanneer de for loop niet wordt gebreaked (De plek is dus leeg) wordt "--" ingevuld
                else:
                    board += "--"

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
        
        
main()
