import urllib.request
import json
import time
import string

class main:

    def __init__(self):

        gameID = "dhIhdq4r"

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

        currentMove = 0;

        currentPlayer = "white"

        while True:

            time.sleep(3)

            with urllib.request.urlopen("https://nl.lichess.org/api/game/" + gameID +"?with_moves=1") as url:
                data = json.loads(url.read().decode())

            moves = data["moves"]

            moves = moves.split(" ")
            
            if currentMove < len(moves):

                if currentPlayer == "white":
                    self.calcCor(moves[currentMove], currentPlayer, white)
                else:
                    self.calcCor(moves[currentMove], currentPlayer, black)

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

    def calcCor(self, move, player, playerBoard):
      # print(move, player, playerBoard)
        
        

        
            

        # controleert of de zet een pion is die niets speciaals doet
        if len(move) == 2:
            i = 0;

            # gaat door de schaakstukken-array heen en vuurt pas code af als hij bij de pionnen is
            for pawn in playerBoard:
                if i >= 8:

                    place = list(move)
                    place[0] = self.letterToNumber(place[0])

                    # controleert of het een witte pion is die beweegt
                    if player == "white":
                        
                        # prepareert de strings voor de if statement omdat als je dit in de if statement doet krijg je syntax errors
                        place1 = int(place[1]) - 1 
                        placeCheck1 = str(place[0]) + " " + str(place1)
                        place2 = int(place[1]) - 2
                        placeCheck2 = str(place[0]) + " " + str(place2)

                        # vergelijkt de strings met posities van de pionnen
                        if placeCheck1 == playerBoard[pawn]:
                            print("placeCheck1 is gelijk aan playerBoardpawn], beweegt 1 vakje en startpositie is wit " + playerBoard[pawn])
                        elif placeCheck2 == playerBoard[pawn]:
                            print("placeCheck2 is gelijk aan playerBoard[pawn], beweegt 2 vakjes en startpositie is wit " + playerBoard[pawn])

                    # controleert of het een zwarte pion is die beweegt
                    if player == "black":
                        
                        # prepareert de strings voor de if statement omdat als je dit in de if statement doet krijg je syntax errors
                        place1 = int(place[1]) + 1 
                        placeCheck1 = str(place[0]) + " " + str(place1)
                        place2 = int(place[1]) + 2
                        placeCheck2 = str(place[0]) + " " + str(place2)
                        
                        if placeCheck1 == playerBoard[pawn]:
                            print("placeCheck1 is gelijk aan playerboar[pawn], beweegt 1 vakje en startpositie is zwart " + playerBoard[pawn])
                        elif placeCheck2 == playerBoard[pawn]:
                            print("placeCheck2 is gelijk aan playerBoard[pawn], beweegt 2 vakjes en startpositie is zwart " + playerBoard[pawn])
                i += 1

        # controleert of het stuk dat gezet wordt een loper is
        if "B" in move:
            print(" het is een bishop")

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

        
main()
