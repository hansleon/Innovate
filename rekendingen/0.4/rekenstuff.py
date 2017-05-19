import urllib.request
import json
import time
import string

class main:

    def __init__(self):

        gameID = "P8yYWJFL"

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

            time.sleep(3)

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

        slaan = "0"


        
        # #######################################################################################################
        #                                                                                                       #
        #   voordat de non-pionnen worden gecontroleerd moet er worden gekeken of een pion wordt gepromoveerd.  #
        #                                                                                                       #
        # #######################################################################################################
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

                    # prepareert string
                    place = list(move)
                    place[0] = self.letterToNumber(place[0])

                    # controleert of het een wit stuk is die beweegt
                    if player == "white":
                        
                        # prepareert de strings voor de if statement omdat als je dit in de if statement doet krijg je syntax errors
                        place1 = int(place[1]) - 1 
                        placeCheck1 = str(place[0]) + " " + str(place1)
                        place2 = int(place[1]) - 2
                        placeCheck2 = str(place[0]) + " " + str(place2)

                        # vergelijkt de strings met posities van de pionnen
                        if placeCheck1 == playerBoard[pawn][0]:
                            print("de controle voor 1 stapje werkt , beweegt 1 vakje en startpositie is wit " + playerBoard[pawn][0])
                        elif placeCheck2 == playerBoard[pawn][0]:
                            print("de controle voor 2 stapjes werkt, beweegt 2 vakjes en startpositie is wit " + playerBoard[pawn][0])

                    # controleert of het een zwart stuk is die beweegt
                    if player == "black":
                        
                        # prepareert de strings voor de if statement omdat als je dit in de if statement doet krijg je syntax errors
                        place1 = int(place[1]) + 1 
                        placeCheck1 = str(place[0]) + " " + str(place1)
                        place2 = int(place[1]) + 2
                        placeCheck2 = str(place[0]) + " " + str(place2)
                        
                        if placeCheck1 == playerBoard[pawn][0]:
                            print("placeCheck1 is gelijk aan playerboar[pawn], beweegt 1 vakje en startpositie is zwart " + playerBoard[pawn][0])
                        elif placeCheck2 == playerBoard[pawn][0]:
                            print("placeCheck2 is gelijk aan playerBoard[pawn], beweegt 2 vakjes en startpositie is zwart " + playerBoard[pawn][0])
                i += 1
        #########################################################################
        #                                                                       # 
        #                                                                       #
        #                                                                       #
        #                                                                       #
        # RICK LEES HIER MADAFUCKA                                              #
        #                                                                       #
        # als je deze elif kopieert maar dan de B verandert voor R or N voor    #
        # toren of paard dan kun je daarbinnen alles schrijven                  #
        #                                                                       #
        #                                                                       #
        #                                                                       #
        #                                                                       #
        #                                                                       #
        #########################################################################
        elif "B" in move:
                            
            # prepareer vergelijking voor 
            place = list(move)
            place[-2] = self.letterToNumber(place[-2])
            
            moveCor = str(place[-2]) + " " + str(place[-1])

            # prepareert de move string voor positiecontrole en controleert welke speciale dingen de zet bevat
            if "x" in move:
                if player is "white":
                    for piece in lackBoard:
                        print(blackBoard[piece], moveCor)
                        if blackBoard[piece] in moveCor:
                            print("charlieeeeee", moveCor)
                if player is "black":
                    for piece in whiteBoard:
                        print(whiteBoard[piece], moveCor)
                        if whiteBoard[piece] in moveCor:
                            print("charlie that hurts", moveCor)
            
            # controleert of de bishop op een zwart of wit vlak staat
            if self.letterToNumber(place[-2]) % 2 == 1:
                if int(place[-1]) % 2 == 1:
                    print("hij staat op een zwart vlak en is dus B1")
                else:
                    print("hij staat op een wit vlak en is dus B2")
            else:
                if int(place[-1]) % 2 == 1:
                    print("hij staat op een wit vlak en is dus B1")
                else:
                    print("hij staat op een zwart vlak en is dus B2")
            
            
            
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
        nul = 0
        
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
        nul = 0
                
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
