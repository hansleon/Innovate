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

            
        # Deze twee arrays met lists erin laten de current position van de pionnen zien en hun plek in de "graveyard" ([0] is de current positie [1] is de "graveyard" positie)
        white = {
            "K1" : ["5 1", "10 5"],
            "Q1" : ["4 1", "10 4"],
            "B1" : ["3 1", "10 3"],
            "B2" : ["6 1", "10 6"],
            "N1" : ["2 1", "10 2"],
            "N2" : ["7 1", "10 7"],
            "R1" : ["1 1", "10 1"],
            "R2" : ["8 1", "10 8"],
            "P1" : ["1 2", "9 1"],
            "P2" : ["2 2", "9 2"],
            "P3" : ["3 2", "9 3"],
            "P4" : ["4 2", "9 4"],
            "P5" : ["5 2", "9 5"],
            "P6" : ["6 2", "9 6"],
            "P7" : ["7 2", "9 7"],
            "P8" : ["8 2", "9 8"],
            }

        black = {
            "K1" : ["5 8", "9 5"],
            "Q1" : ["4 8", "9 4"],
            "B1" : ["3 8", "9 3"],
            "B2" : ["6 8", "9 6"],
            "N1" : ["2 8", "9 2"],
            "N2" : ["7 8", "9 7"],
            "R1" : ["1 8", "9 1"],
            "R2" : ["8 8", "9 8"],
            "P1" : ["1 7", "10 1"],
            "P2" : ["2 7", "10 2"],
            "P3" : ["3 7", "10 3"],
            "P4" : ["4 7", "10 4"],
            "P5" : ["5 7", "10 5"],
            "P6" : ["6 7", "10 6"],
            "P7" : ["7 7", "10 7"],
            "P8" : ["8 7", "10 8"],
            }

        self.printChessBoard(white, black)

        # Er wordt bijgehouden welke zet we nu zijn, dit is om te voorkomen dat we doorgaan terwijl we nog geen nieuwe zet hebben
        currentMove = 0;

        # We slaan op welke speler aan de beurt is, wit, zwart, wit, zwart etc
        player = "white"

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
                # cords = self.calcCord(moves[currentMove], player, white, black)
                cords = "3 2-3 4" #Debug placeholder

                # De coordinaten worden gesplit op de -, hieruit krijg je een array met de start [0] en eind [1] cords
                cords = cords.split("-")

                # Beide cords worden opgeslagen in variabelen
                cordOne = cords[0]
                cordTwo = cords[1]
                
                # Er wordt door zowel de white als de black array geloopt
                for pawnWhite, pawnBlack in zip(white, black):

                    # Eerst wordt gekeken of de beurt gezet is door wit of zwart
                    if player == "white":

                        # Er wordt gechecked of de positie waar de pion naar verplaatst bezet is door een zwarte pion
                        if black[pawnBlack][0] == cordTwo:

                            # Als de positie bezet is door een pion wordt die pion in de "Graveyard" op zijn eigen plek gezet
                            black[pawnBlack][0] = black[pawnBlack][1]

                        # Wanneer de plek vrijgemaakt is kunnen we de pion die moet worden verplaatst verplaatsen
                        if white[pawnWhite][0] == cordOne:
                            white[pawnWhite][0] = cordTwo

                    elif player == "black":

                        # Er wordt gechecked of de positie waar de pion naar verplaatst bezet is door een witte pion        
                        if white[pawnWhite][0] == cordTwo:

                            # Als de positie bezet is door een pion wordt die pion in de "Graveyard" op zijn eigen plek gezet
                            white[pawnWhite][0] = white[pawnWhite][1]

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
                    if white[pion][0] == str(x) + " " + str(y):
                        schaakbord += pion
                        spaceIsset = True

                # We checken of de positie niet al bezet is door een witte pion (Voorkomt dat de loop onnodig wordt doorlopen)
                if spaceIsset == False:
                    # We loopen door alle pionnen van black heen om te kijken welke pion op de x y coördinaten zit
                    for pion in black:

                        # Wanneer de plek van de pion gelijk is aan de plek van de geconcate string van de variabelen x en y wordt deze toegevoegd aan de string en wordt spaceIsset op true gezet
                        if black[pion][0] == str(x) + " " + str(y):
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
                    if white[pawnWhite][0] == str(x) + " " + str(y):
                        graveyardWhite += pawnWhite
                        spaceIssetWhite = True

                    if black[pawnBlack][0] == str(x) + " " + str(y):
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
