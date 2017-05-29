# roep deze functie aan om het spel opnieuw klaar te zetten
def resetBoard(self, white, black):

    passant = False
    playerWhite = "White"
    playerBlack = "Black"

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
    nul = 0

    
    for pos in whiteConverted:
        place = list(white[pos][0])

        startX = place[0]
        startY = place[-1]
        print(startX, startY, eindX, eindY, nul, nul, nul, nul)
        
        # self.chielsMethod(startX, startY, eindX, eindY, nul, nul, nul, nul, passant, playerWhite)
        
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
        place = list(white[pos][0])

        startX = place[0]
        startY = place[-1]
        
        print(startX, startY, eindX, eindY, nul, nul, nul, nul)

        # self.chielsMethod(startX, startY, eindX, eindY, nul, nul, nul, nul, passant, playerBlack)

        eindX += 1
        count += 1
        if eindX is 9:
            eindX = 1
        if count is 9:
            eindY -= 1

    return(whiteActual, blackActual)
