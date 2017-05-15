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
        #het tweede getal geeft aan waar dit stuk staat als hij bestaat
        #rokade 0 is geen, 1 is korte rokade, 2 is lange rokade
        #startx, starty, endx, endy, slag, slagx, slagy, promotie, rokade, beurt in string, posx, posy.
        #posx en posy zijn fixt en worden steeds gereturned voor de volgende stap
        posx = 0
        posy = 0
        posx, posy = self.Set(7,4,8,6,0,0,0,0,"white", posx ,posy)
        #posx, posy = self.Set(7,7,7,8,9,4,0,0,"black", posx ,posy)

    def Set(self, inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy, promotie, rokade, beurt, posx, posy):
        startx, starty, endx, endy, slagx, slagy = self.Omrekenen(inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy, beurt)
        if(rokade == 0):
            
            if(promotie == 0):
                
                if(inputslagx != 0 or inputslagy != 0):

                    posx, posy = self.slag(endx, endy, posx, posy, slagx, slagy, 0 , beurt)
                moveh = self.Moveh(startx, starty, endx, endy, posx, posx)        
                if(moveh == False):
                    posx, posy = self.Move(posx, posy, startx, starty, endx, endy, beurt)
            if(promotie != 0):
                posx, posy = self.Move(posx, posy, startx, starty, endx, endy, beurt)
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
                    endx, endy, posx, posy, slagx, slagy, beurt, beurtstring
                posx, posy = self.Slag(endx, endy, posx, posy, slagx, slagy, beurtint, beurt)
                posx, posy = self.Beweegposxy(posx, posy, x2, y3)
                self.Elektromagneet(1)
                posx, posy = self.Beweegposxy(posx, posy, x, posy)
                posx, posy = self.Beweegposxy(posx, posy, posx, y)
                posx, posy = self.Beweegposxy(posx, posy, endx, posy)
                posx, posy = self.Beweegposxy(posx, posy, posx, y2)
                self.Elektromagneet(0)
        
                    
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



            
    def slag(self, endx, endy, posx, posy, slagx, slagy, beurt, beurtstring):
            posx, posy = self.Beweegposxy(posx, posy, endx, endy)
            self.Elektromagneet(1)
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
            self.Elektromagneet(0)
            return posx, posy

    def Move(self, posx, posy, startx, starty, endx, endy, beurt):
        #zet de elektromagneet onder het juiste stuk
        posx, posy = self.Beweegposxy(posx, posy, startx, starty)

        #zet de elektromagneet aan
        self.Elektromagneet(1)

        #beweegt de elektromagneet naar de eindbestemming
        posx, posy = self.Beweegposxy(posx, posy, endx, endy)

        #zet de elektromagneet uit
        self.Elektromagneet(0)
        return posx, posy

    def Moveh(self, startx, starty, endx, endy, posx, posy):
        posx, posy = self.Beweegposxy(posx, posy, startx, starty)
        movementx = endx - startx
        movementy = endy - starty
        if((movementx == 2 and movementy == 4) or (movementx == 4 and movementy == 2)
           or (movementx == 4 and movementy == 2) or (movementx == 4 and movementy == -2)
           or (movementx == 2 and movementy == -4) or (movementx == -2 and movementy == -4)
           or (movementx == -4 and movementy == -2) or (movementx == -4 and movementy == 2)
           or (movementx == -2 and movementy == 4)):
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
