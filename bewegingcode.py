class Main:
    def __init__(self):
        #alle globale variabelen
        global posx
        global posy
        global beurt
        global beurt2
        global startx
        global starty
        global endx
        global endy
        global slagx
        global slagy

        #alle variabelen een waarde meegeven
        self.posx = 0
        self.posy = 0
        self.beurt = 0
        self.beurt2 = ""
        self.startx = 0
        self.starty = 0
        self.endx = 0
        self.endy = 0
        self.slagx = 0
        self.slagy = 0

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
        #startx, starty, endx, endy, slag, slagx, slagy, promotie, rokade

        self.set(7,7,7,8,False,9,5,2,0)
        self.set(2,2,2,1,False,9,1,7,0)

    def set(self, inputstartx, inputstarty, inputendx, inputendy, slag, inputslagx, inputslagy, promotie, rokade):

        #rekent alle inputCoördinaten om naar coöordinaten die nodig zijn voor het bord
        
        #zorgt de beurt per zet verandert
        self.beurt += 1
        if((self.beurt & 1) == 0):
            self.beurt2 = "black"
        if((self.beurt & 1) == 1):
            self.beurt2 = "white"

        self.omrekenen(inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy)
   
        #kijkt of er een rokade gebeurt, zo nee checkt hij of er een promotie is,
        #daarna kijkt hij of er een slag is. als al deze dingen False zijn dan
        #word het stuk van a naar b verplaatst
        if(rokade == 0):
            
            if(promotie == 0):
                
                if(slag == True):

                    self.slag(0)
                                         
                self.move()
##############################################################################
##############################################################################
## promotie functie
## eerst moet in deze functie de pion naar zijn doel worden gebracht
## daarna checkt het bord of het stuk al geslagen is of niet
## zo ja: dan plaatst hij de pion in de graveyard en haalt het goede stuk op uit de graveyard
## zo nee: dan gebeurt er niks en functioneert de pion als nieuw stuk                
                
            if(promotie != 0):
                self.move()
                promotie *= 2
                y3 = promotie
                if(self.beurt2 == "white"):
                    x = 4
                    x2 = 2
                    y = 18
                    y2 = 16
                    beurt = 1
                if(self.beurt2 == "black"):
                    x = 22
                    x2 = 24
                    y = 0
                    y2 = 2
                    beurt = 2
                self.slag(beurt)
                self.beweegposxy(x2,y3)
                self.elektromagneet(1)
                self.beweegposxy(x,self.posy)
                self.beweegposxy(self.posx, y)
                self.beweegposxy(self.endx, self.posy)
                self.beweegposxy(self.posx, y2)
                self.elektromagneet(0)
                    
                    
                



##############################################################################
##############################################################################
## rokade functie.
## de eerste 2 if statements bepalen de x locatie waar de toren en koning
## staan of heen moeten
## de tweede 2 if statements bepalen de y locatie waar de toren en koning
## staan of heen moeten

        if(rokade == 1):
            x1 = 18
            x2 = 20
            x3 = 16
        if(rokade == 2):
            x1 = 10
            x2 = 6
            x3 = 12   
        if(self.beurt2 == "white"):
            y1 = 2
            y2 = 0
        if(self.beurt2 == "black"):
            y1 = 16
            y2 = 18
        if(rokade != 0): 
            self.beweegposxy(14,y1)
            self.elektromagneet(1)
            
            self.beweegposxy(x1,y1)
            self.elektromagneet(0)
            
            self.beweegposxy(x2,y1)
            self.elektromagneet(1)
            
            self.beweegposxy(x2,y2)
            self.beweegposxy(x3,y2)
            self.beweegposxy(x3,y1)
            self.elektromagneet(0)

    def slag(self, beurt):
        self.beweegposxy(self.endx, self.endy)
        self.elektromagneet(1)
        self.beweegposxy(self.posx, self.endy + 1)

        if(beurt == 0):
            if(self.beurt2 == "white"):
                self.beweegposxy(22, self.posy)
            if(self.beurt2 == "black" ):
                self.beweegposxy(4, self.posy)
            x = self.slagx
        if(beurt == 1):
            self.beweegposxy(4, self.posy)
            x = 0   
        if(beurt == 2):
            self.beweegposxy(22, self.posy)
            x = 26
        self.beweegposxy(self.posx, self.slagy + 1)
        self.beweegposxy(x, self.posy)
        self.beweegposxy(self.posx, self.slagy)
        self.elektromagneet(0)
##############################################################################
##############################################################################
##          alle functie nodig voor het bewegen van de schaakstukken        ##
##############################################################################
##############################################################################

    #bij deze functie word een schaakstuk van startxy naar endxy gebracht
    def move(self):
        #zet de elektromagneet onder het juiste stuk
        self.beweegposxy(self.startx,self.starty)

        #zet de elektromagneet aan
        self.elektromagneet(1)

        #beweegt de elektromagneet naar de eindbestemming
        self.beweegposxy(self.endx,self.endy)

        #zet de elektromagneet uit
        self.elektromagneet(0)

    #omreken tabel voor de coördinaten
    def omrekenen(self, inputstartx, inputstarty, inputendx, inputendy, inputslagx, inputslagy):
        self.startx = (inputstartx + 2) * 2
        self.starty = inputstarty * 2
        
        self.endx = (inputendx + 2) * 2
        self.endy = inputendy * 2
        print("beurt = " + str(self.beurt2))
        if(inputslagx == 9):
            if(self.beurt2 == "black"):
                self.slagx = 0
            if(self.beurt2 == "white"):
                self.slagx = 26
        if(inputslagx == 10):
            if(self.beurt2 == "black"):
                self.slagx = 2
            if(self.beurt2 == "white"):
                self.slagx = 24
        self.slagy = inputslagy * 2
    
    ###de parameters voor deze functies bepalen de nieuwe locatie 
    ###waar de elektromagneet heen moet
    def beweegposxy(self, x, y):
        movementx = x - self.posx
        movementy = y - self.posy
        self.posx += movementx
        self.posy += movementy
        
        self.beweegxy(movementx, movementy)
        print("posx = " + str(self.posx) + " posy = " + str(self.posy))

    def beweegxy(self, x, y):
        self.motorx(x)
        self.motory(y)

    ###de parameters voor de volgende twee functies bepalen 
    ###de afstand over de x en de y as
    ###
    def motorx(self, x):
        print("motor x-as beweeg " + str(x))

    def motory(self, y):
        print("motor y-as beweeg " + str(y))

    def elektromagneet(self, status):
        if(status == 0):
            print("Deactiveer de elektromagneet")
        elif(status == 1):
            print("Activeer de elektromagneet")
        else:
            print("Error onjuiste data")

        
Main()
