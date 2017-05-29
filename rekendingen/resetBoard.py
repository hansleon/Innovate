# roep deze functie aan om het spel opnieuw klaar te zetten
    def resetBoard(self):

        passant = False
        playerWhite = "White"
        playerBlack = "Black"

        # dit zet de array op volgorde zodat erdoor heen kan worden gegaan op volgorde van de for loop
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


        eindX = 1
        eindY = 1
        count = 1

        
        for pos in whiteConverted:
            place = list(white[pos])
            
            print(place[0], place[-1], x, y, nul, nul, nul, nul)
            # self.chielsMethod(place[1], place[-1], eindX, eindY, nul, nul, nul, nul, passant, playerWhite)
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
            place = list(white[pos])
            print(place[0], place[-1], x, y, nul, nul, nul, nul)

            # self.chielsMethod(place[1], place[-1], eindX, eindY, nul, nul, nul, nul, passant, playerBlack)

            eindX += 1
            count += 1
            if eindX is 9:
                eindX = 1
            if count is 9:
                eindY -= 1

        return(whiteConverted, blackConverted
