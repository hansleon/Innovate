import urllib.request
import json
import time
import string
import sys


class main:

    def __init__(self):

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
            input("Press Enter to continue...")
            sys.exit("")

            
        # De start posities van alle witte pionnen wordt in deze associative array gezet
        white = {
            "K1" : "5 1",
            "Q1" : "4 1",
            "B1" : "3 1",
            "B2" : "6 1",
            "N1" : "2 1",
            "N2" : "7 1",
            "R1" : "1 1",
            "R2" : "8 1",
            "P1" : "1 2",
            "P2" : "2 2",
            "P3" : "3 2",
            "P4" : "4 2",
            "P5" : "5 2",
            "P6" : "6 2",
            "P7" : "7 2",
            "P8" : "8 2",
            }

        # De start posities van alle zwarte pionnen wordt in deze associative array gezet
        black = {
            "K1" : "5 8",
            "Q1" : "4 8",
            "B1" : "3 8",
            "B2" : "6 8",
            "N1" : "2 8",
            "N2" : "7 8",
            "R1" : "1 8",
            "R2" : "8 8",
            "P1" : "1 7",
            "P2" : "2 7",
            "P3" : "3 7",
            "P4" : "4 7",
            "P5" : "5 7",
            "P6" : "6 7",
            "P7" : "7 7",
            "P8" : "8 7",
            }

        self.printChessBoard(white, black)

        # Er wordt bijgehouden welke zet we nu zijn, dit is om te voorkomen dat we doorgaan terwijl we nog geen nieuwe zet hebben
        currentMove = 0;

        # We slaan op welke speler aan de beurt is, wit, zwart, wit, zwart etc
        currentPlayer = "white"

        # Deze while loop speelt het spel af, deze is oneindig tot er een break in wordt gebruikt
        while True:

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
                # cords = self.calcCord(moves[currentMove], currentPlayer, black)
                cords = "3 2-3 4" #Debug placeholder

                # De coordinaten worden gesplit op de -, hieruit krijg je een array met de start [0] en eind [1] cords
                cords = cords.split("-")

                # Beide cords worden opgeslagen in variabelen
                cordOne = cords[0]
                cordTwo = cords[1]
                
                if currentPlayer == "white":

                    # Er wordt door alle zwarte pionnen geloopt        
                    for pawn in black:

                        # We kijken of er een pion zich bevindt op de einddatum, deze pion wordt geslagen en wordt naar de "graveyard" verplaatst (De graveyard is x 9 tot 10 en y 1 tot 8)
                        if black[pawn] == cordTwo:

                            # Elke pion krijgt zijn eigen positie in de graveyard
                            if pawn == "K1":
                                black[pawn] = "9 5"
                            elif pawn == "Q1":
                                black[pawn] = "9 4"
                            elif pawn == "B1":
                                black[pawn] = "9 3"
                            elif pawn == "B2":
                                black[pawn] = "9 6"
                            elif pawn == "N1":
                                black[pawn] = "9 2"
                            elif pawn == "N2":
                                black[pawn] = "9 7"
                            elif pawn == "R1":
                                black[pawn] = "9 1"
                            elif pawn == "R2":
                                black[pawn] = "9 8"
                            elif pawn == "P1":
                                black[pawn] = "10 1"
                            elif pawn == "P2":
                                black[pawn] = "10 2"
                            elif pawn == "P3":
                                black[pawn] = "10 3"
                            elif pawn == "P4":
                                black[pawn] = "10 4"
                            elif pawn == "P5":
                                black[pawn] = "10 5"
                            elif pawn == "P6":
                                black[pawn] = "10 6"
                            elif pawn == "P7":
                                black[pawn] = "10 7"
                            elif pawn == "P8":
                                black[pawn] = "10 8"

                    # Er wordt door alle witte pionnen geloopt
                    for pawn in white:

                        # Hier checken we welke pion zich op de begincoördinaten bevindt, deze verplaatsen we naar de einddatum
                        if white[pawn] == cordOne:
                            white[pawn] = cordTwo

                # Dit is bijna gelijk aan de IF maar dan voor de zwarte pionnen        
                else:

                    # Er wordt door alle witte pionnen geloopt             
                    for pawn in white:

                        # We kijken of er een pion zich bevindt op de einddatum, deze pion wordt geslagen en wordt naar de "graveyard" verplaatst (De graveyard is x 9 tot 10 en y 1 tot 8)
                        if white[pawn] == cordTwo:

                            # Elke pion krijgt zijn eigen positie in de graveyard
                            if pawn == "K1":
                                white[pawn] = "10 5"
                            elif pawn == "Q1":
                                white[pawn] = "10 4"
                            elif pawn == "B1":
                                white[pawn] = "10 3"
                            elif pawn == "B2":
                                white[pawn] = "10 6"
                            elif pawn == "N1":
                                white[pawn] = "10 2"
                            elif pawn == "N2":
                                white[pawn] = "10 7"
                            elif pawn == "R1":
                                white[pawn] = "10 1"
                            elif pawn == "R2":
                                white[pawn] = "10 8"
                            elif pawn == "P1":
                                white[pawn] = "9 1"
                            elif pawn == "P2":
                                white[pawn] = "9 2"
                            elif pawn == "P3":
                                white[pawn] = "9 3"
                            elif pawn == "P4":
                                white[pawn] = "9 4"
                            elif pawn == "P5":
                                white[pawn] = "9 5"
                            elif pawn == "P6":
                                white[pawn] = "9 6"
                            elif pawn == "P7":
                                white[pawn] = "9 7"
                            elif pawn == "P8":
                                white[pawn] = "9 8"

                    # Er wordt door alle witte pionnen geloopt
                    for pawn in black:

                        # Hier checken we welke pion zich op de begincoördinaten bevindt, deze verplaatsen we naar de einddatum
                        if black[pawn] == cordOne:
                            black[pawn] = cordTwo

                # Wanneer de zet is gedaan gaan we naar de volgende move
                currentMove += 1

                # Wanneer de zet is gedaan switchen we van kant
                if currentPlayer == "white":
                    currentPlayer = "black"
                else:
                    currentPlayer = "white"

                # De printChessBoard is een debug method, deze printen we voor een visuele representatie
                self.printChessBoard(white, black)
                

    # De printChessBoard() method geeft een visuele representatie van de posities van alle pionnen
    def printChessBoard(self, white, black):

        # ---------------------------------------------------------
        # Dit eerste stuk is voor het printen van het complete bord
        # ---------------------------------------------------------
        
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
        print("Board:")
        print(schaakbord)


        # ----------------------------------------------------------------------------------------------------------
        # Dit stuk van de method is voor het printen van de 2 "Graveyards" hierin worden de geslagen stukken bewaard
        # ----------------------------------------------------------------------------------------------------------

        # In deze twee strings worden alle posities gevuld, deze strings wordt uiteindelijk geprint
        graveyardWhite = ""
        graveyardBlack = ""

        # variabel y is de y positie van de pionen
        y = 8

        # We loopen door alle y mogelijkheden beginnent bovenin (aangezien het printen van de string linksboven begint)
        while y > 0:

            # variabel x is de x positie van de pionen
            x = 9

            # We loopen door alle x mogelijkheden beginnent links (aangezien het printen van de string linksboven begint)
            while x <= 10:

                # spaceIsset is een variabel waarmee wordt gecontrolleerd of een plek bezet is, is een plek niet bezet dan wordt er "--" ingevuld, dit moet voor beide kleuren gebeuren
                spaceIssetWhite = False
                spaceIssetBlack = False

                # We loopen door alle pionnen van white heen om te kijken welke pion op de x y coördinaten zit
                for pawnWhite, pawnBlack in zip(white, black):

                    # Wanneer de plek van de pion gelijk is aan de plek van de geconcate string van de variabelen x en y wordt deze toegevoegd aan de string en wordt spaceIsset op true gezet
                    if white[pawnWhite] == str(x) + " " + str(y):
                        graveyardWhite += pawnWhite
                        spaceIssetWhite = True

                    if black[pawnBlack] == str(x) + " " + str(y):
                        graveyardBlack += pawnBlack
                        spaceIssetBlack = True

                # Wanneer een positie helemaal niet bezet is wordt "--" ingevuld
                if spaceIssetWhite == False:
                    graveyardWhite += "--"
                if spaceIssetBlack == False:
                    graveyardBlack += "--"

                # Tussen elke positie wordt een spatie geadd, zo is het visueel beter leesbaar 
                graveyardWhite += " "
                graveyardBlack += " "

                # Wanneer de loop wordt doorlopen doen we x + 1 naar de volgende x positie te gaan    
                x += 1

            # Tussen elke y wordt een enter geplaats, dit is voor visueel effect
            graveyardWhite += "\n"
            graveyardBlack += "\n"

            # We doen y - 1 aangezien we bij 8 beginnen, dit is omdat een schaakbord eigenlijk links onderin met 1, 1 begint en wij dus links bovenin met 1, 8 beginnen
            y -= 1

        # De strings graveyard worden geprint en laten visueel de positie van elke pion zien
        print("Graveyard \nWhite:")
        print(graveyardWhite)

        print("Graveyard \nBlack:")
        print(graveyardBlack)

            


        
main()
