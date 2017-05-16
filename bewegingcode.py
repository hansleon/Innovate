class Movement:
    
    def __init__(self):


        #beginpunt x as van het schaakstuk
        #beginpunt y as van het schaakstuk
        #eindpunt x as van het schaakstuk
        #eindpunt y as van het schaakstuk
        #word een stuk geslagen ja/nee
        #eindpunt x as geslagen stuk
        #eindpunt y as geslagen stuk
        #is er een promotie en welk stuk word het en is het stuk aanwezig eerste getal geeft aan welk stuk het is,
        #is het stuk nog niet geslagen vul dan 0 in. Zo ja vul de y in van de positie van dit stuk
        #rokade 0 is geen, 1 is korte rokade, 2 is lange rokade
        #startx, starty, endx, endy, slag, slagx, slagy, promotie, rokade, beurt in string, posx, posy.
        #posx en posy zijn fixt en worden steeds gereturned voor de volgende stap

        posx = 0
        posy = 0
        
        posx, posy = self.Set(7,4,8,6,0,0,0,0,"white", posx ,posy)
        #posx, posy = self.Set(7,7,7,8,9,4,0,0,"black", posx ,posy)

    def Set(self, inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy, promotie, rokade, beurt, posx, posy):
        startx, starty, endx, endy, slagx, slagy = self.Omrekenen(inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy, beurt)
        #check voor rokade, promotie, slag. Zo nee, doe de move, zo ja voer de de taak uit
        if(rokade == 0):
            
            if(promotie == 0):
                
                #als de inputslagx of inputslagy niet nul is betekend het dat er coördinaten zijn voor een plek in de graveyard.
                #hierdoor weet het systeem dat er een slag is.
                if(inputslagx != 0 or inputslagy != 0):

                    #de slag functie word later uitgelegt
                    posx, posy = self.Slag(endx, endy, posx, posy, slagx, slagy, 0 , beurt)

                #in deze functie word de stap gezet
                posx, posy = self.Move(posx, posy, startx, starty, endx, endy, beurt)

            #als er wel een promotie is gaat de code hier verder.
            if(promotie != 0):
                
                #de pion word eerst naar de laatste positie gebracht
                posx, posy = self.Move(posx, posy, startx, starty, endx, endy, beurt)
                
                #het variable promotie is de y coördinaat van de graveyard waar het geslagen stuk heen moet
                y3 = promotie * 2

                #voor elke partij word hier de coördinaten gegeven van bepaalde posities
                if(beurt == "white"):
                    #x is de x-as positie tussen het scaakbord en de witte graveyard
                    x = 4

                    #x2 is de x-as positie waar de geslagen stukken staan in de witte graveyard
                    x2 = 2

                    #y is de y-as positie die boven het bord langs loopt
                    y = 18

                    #y2 is de y-as positie waar het nieuwe stuk word neer gezet
                    y2 = 16

                    #deze variable zorgt dat het geslagen stuk niet naar de tegenpartij zijn graveyard gaat
                    #dit is nodig omdat de slag functie normaal gesproken het stuk naar de andere beurt, ten opzichte van de huidige beurt, zijn graveyard te sturen
                    beurtint = 1
                    
                if(beurt == "black"):
                    #hier geld alles precies het zelfde alleen dan voor zwart
                    x = 22
                    x2 = 24
                    y = 0
                    y2 = 2
                    beurtint = 2

                posx, posy = self.Slag(endx, endy, posx, posy, slagx, slagy, beurtint, beurt)
                posx, posy = self.Beweegposxy(posx, posy, x2, y3)
                self.Elektromagneet(1)
                
                posx, posy = self.Beweegposxy(posx, posy, x, posy)
                posx, posy = self.Beweegposxy(posx, posy, posx, y)
                posx, posy = self.Beweegposxy(posx, posy, endx, posy)
                posx, posy = self.Beweegposxy(posx, posy, posx, y2)
                self.Elektromagneet(0)
        
        #rokade 1 is korte rokade
        #rokade 2 is de lange rokade
        #X-as positie bepaalt voor koning en toren
        if(rokade == 1):
            #x1 = x as plek waar de koning moet komen te staan
            x1 = 18

            #x2 = x as plek waar de toren staat
            x2 = 20

            #x3 = x as plek waar de toeren moet komen te staan
            x3 = 16

        #hier geld het zelfde als bij de vorige if statement
        if(rokade == 2):
            x1 = 10
            x2 = 6
            x3 = 12

        #Y-as positie bepaalt voor koning en toren
        if(beurt == "white"):
            #de y-as hoogte waarop de stukken staan en moeten komen
            y1 = 2

            #de y-as hoogte waar langs de stukken langs elkaar kunnen gaan
            y2 = 0

        #hier geld weer het zelfde als wit
        if(beurt == "black"):
            y1 = 16
            y2 = 18

        #hier word de rokade uitgevoerd met de zojuist geselecteerde coördinaten
        if(rokade != 0):
            #14 is in x-as positie van de koning
            posx, posy = self.Beweegposxy(posx, posy, 14, y1)
            self.Elektromagneet(1)
            
            posx, posy = self.Beweegposxy(posx, posy, x1, y1)
            self.Elektromagneet(0)
            
            posx, posy = self.Beweegposxy(posx, posy, x2, y1)
            self.Elektromagneet(1)
            
            posx, posy = self.Beweegposxy(posx, posy, x2, y2)
            posx, posy = self.Beweegposxy(posx, posy, x3, y2)
            posx, posy = self.Beweegposxy(posx, posy, x3, y1)
            self.Elektromagneet(0)
        return posx, posy



    
    #input voor de Slag methode:
    #endx en endy is de xy - coördinaat waar het stuk van de partij dat aan de beurt is heen moet
    #posx en posy is de xy - coördinaat waar de elektromagneet staat
    #slagx, slagy is de xy - coördinaat van de graveyard waar het geslagen stuk heen moet
    #beurt is nodig voor de promotie functie zodat het stuk terug gaat naar zijn eigen graveyard inplaat van naar de tegenstander
    #beurtstring geeft aan wie de huidige beurt heeft, wit of zwart
    def Slag(self, endx, endy, posx, posy, slagx, slagy, beurt, beurtstring):

            posx, posy = self.Beweegposxy(posx, posy, endx, endy)
            self.Elektromagneet(1)
            
            posx, posy = self.Beweegposxy(posx, posy, posx, endy + 1)

            if(beurt == 0):

                #als de huidige beurt wit aan zet is moet het stuk dus naar de zwarte graveyard toe en andersom
                if(beurtstring == "white"):
                    posx, posy = self.Beweegposxy(posx, posy, 22, posy)
                    
                if(beurtstring == "black" ):
                    posx, posy = self.Beweegposxy(posx, posy, 4, posy)

                #x is de x-as coördinaat van het geslagen stuk in de graveyard
                x = slagx

            
            if(beurt == 1):
                #4 is de x-coördinaat tussen het schaakbord en de witte graveyard
                #hier moet het stuk langs als het een promotie heeft gehad
                posx, posy = self.Beweegposxy(posx, posy, 4, posy)
                x = 0
                
            if(beurt == 2):
                #hier geld het zelfde maar dan voor zwart
                posx, posy = self.Beweegposxy(posx, posy, 22, posy)
                x = 26

            #hier word de rest van de beweging afgemaakt om er voor te zorgen dat het geslagen stuk op de goede plek komt
            posx, posy = self.Beweegposxy(posx, posy, posx, slagy + 1)
            posx, posy = self.Beweegposxy(posx, posy, x, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, slagy)
            self.Elektromagneet(0)
            
            return posx, posy

    #input voor de Move methode
    #posx en posy is de xy-coördinaat van de huidige plek van de elektromagneet
    #startx en starty is de xy-coördinaat van de start positie van de zet
    #endx en endy is de xy-coördinaat van de eind positie van de zet
    def Move(self, posx, posy, startx, starty, endx, endy, beurt):


        #zet de elektromagneet onder het juiste stuk
        posx, posy = self.Beweegposxy(posx, posy, startx, starty)
            
        #eerst word er gecheckt of de zet een paard is, dit moet omdat het paard een andere beweging maakt
        moveh, posx, posy = self.Moveh(startx, starty, endx, endy, posx, posx)

        #als de self.Moveh functie false returned kan de zet als nog gedaan worden
        if(moveh == False):


            #zet de elektromagneet aan
            self.Elektromagneet(1)

            #beweegt de elektromagneet naar de eindbestemming
            posx, posy = self.Beweegposxy(posx, posy, endx, endy)

            #zet de elektromagneet uit
            self.Elektromagneet(0)
            
        return posx, posy

    #input voor de Moveh methode
    #startx en starty is de xy-coördinaat van de huidige plek van de elektromagneet
    #endx en endy is de xy-coördinaat van de eind positie van de zet
    #posx en posy is de xy-coördinaat van de huidige plek van de elektromagneet
    def Moveh(self, startx, starty, endx, endy, posx, posy):

        #berekent de xy coördinaat waar het stuk moet eindigen
        movementx = endx - startx
        movementy = endy - starty

        #hier word gecheckt of de zet een paarde sprong is
        if((movementx == 2 and movementy == 4) or (movementx == 4 and movementy == 2)
           or (movementx == 4 and movementy == 2) or (movementx == 4 and movementy == -2)
           or (movementx == 2 and movementy == -4) or (movementx == -2 and movementy == -4)
           or (movementx == -4 and movementy == -2) or (movementx == -4 and movementy == 2)
           or (movementx == -2 and movementy == 4)):

            #hier word doormiddel van elke sprong die het paard kan maken
            #de juiste zetten uitgevoert die nodig zijn voor de huidige paardesprong
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
            return True, posx, posy
        else:
            return False, posx, posy
        

    #input voor de Omreken methode
    #inputstartx en inputstarty is de xy-coördinaat van het spelbord, deze kan alleen maar tussen de 1, 8 zitten(9 en 10 zijn voor de graveyard).
    #inputendx en inputendy is de xy-coördinaat van het spelbord, deze kan alleen maar tussen de 1 - 8 zitten
    #beurt geeft aan wie er aan de beurt is
    def Omrekenen(self, inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy, beurt):
        startx = (inputstartx + 2) * 2
        starty = inputstarty * 2
        
        endx = (inputendx + 2) * 2
        endy = inputendy * 2
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

    #input voor de Beweegposxy funtie
    #posx em posy is huidige xy-coördinaat van de elektromagneet
    #x, y
    def Beweegposxy(self, posx, posy, x, y):
        movementx = x - posx
        movementy = y - posy
        posx += movementx
        posy += movementy
        
        self.Motorx(movementx)
        self.Motory(movementy)
        print("posx = " + str(posx) + " posy = " + str(posy))
        return posx, posy

    def Motorx(self, x):
        print("motor x-as beweeg " + str(x))

    def Motory(self, y):
        print("motor y-as beweeg " + str(y))

    def Elektromagneet(self, status):
        if(status == 0):
            print("Deactiveer de elektromagneet")
        elif(status == 1):
            print("Activeer de elektromagneet")
        else:
            print("Error onjuiste data")

Movement()
