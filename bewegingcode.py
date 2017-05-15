class Main:
    def __init__(self):

	
        #global maken
        global beginx
        global beginy
        global beurt
        global elekx
        global eleky
        
        #beginx en beginy geven de huidige positie aan van de elektromagneet
        self.beginx = 0
        self.beginy = 0
        self.beurt = 1
        self.elekx = 0
        self.eleky = 0


        #beginpunt x as van het schaakstuk
        #beginpunt y as van het schaakstuk
        #eindpunt x as van het schaakstuk
        #eindpunt y as van het schaakstuk
        #word een stuk geslagen ja/nee
        #eindpunt x as geslagen stuk
        #eindpunt y as geslagen stuk
        #is er een promotie en welk stuk word het en is het stuk aanwezig eerste getal geeft aan welk stuk het is,
        #0 voor nee, 1 voor koningin, 2 voor paard, 3 voor toren, 4 voor loper
        #rokade 0 is geen, 1 is korte rokade, 2 is lange rokade
        #op dit punt zijn er 3 zetten geweest
        self.Ifslag(3,7,3,8,False,9,6,1,0,self.beurt)
        self.Ifslag(3,7,3,8,False,9,6,1,0,self.beurt)
        #self.Ifslag(5,4,5,8,True,9,1,1,0,self.beurt)


    def Ifslag(self, inputstartx, inputstarty, inputendx, inputendy, slag, inputslagx, inputslagy, promotie, rokade, beurt):
        if(self.beurt%2 == 0):
            beurt = "black"
        if(self.beurt%2 != 0):
            beurt = "white"
        self.beurt = self.beurt + 1
        #als er een rokade is word deze eerste behandeld
        if(rokade == 0):
		
            #als er een promotie is word deze eerste behandeld
            if(promotie == 0):
			
                #als er een slag is wordt die eerst gedaan
                if(slag == True):
				
                    #omrekenen van coördinaten van de api naar coördinaten van ons schaakbord
                    slagy = inputslagy * 2
                    startx = (inputstartx + 2) * 2
                    starty = inputstarty * 2
                    endx = (inputendx + 2) * 2
                    endy = inputendy * 2

                    #b
                    movementx = endx - self.beginx
                    movementy = endy - self.beginy
                    #voert de beweging uit
                    self.beweegxy(movementx, movementy)
                    
                    #activeren van de elektromagneet
                    self.elektromagneet(1)

                    #beweging om tussen de stukken door te gaan
                    self.beweegxy(0,1)
					
                    if(self.beurt%2 == 0):
					
                        #beweging om naar de linkerkant te gaan in het geval van een slag voor wit
                        self.beweegxy(4 - self.elekx, 0)

                        #beweging om naar de hoogte van het gewenste vak te gaan
                        self.beweegxy(0, slagy - endy)

                        #beweging om naar het juiste vak te bewegen op de graveyard
                        #eerste if word geactiveerd als het een pion is en de tweede als het een ander stuk is
                        if(inputslagx == 9):
                            self.beweegxy(-4,0)
                        if(inputslagx == 10):
                            self.beweegxy(-2,0)
                    if(self.beurt%2 != 0):
                        self.beweegxy(22 - self.elekx, 0)
                        self.beweegxy(slagy-endy)
                        if(inputslagx == 9):
                            self.beweegxy(4,0)
                        if(inputslagx == 10):
                            self.beweegxy(2,0)
                    #beweging om recht in het vak te komen
                    self.beweegxy(0,-1)

                    #deactiveren van de elektromagneet
                    self.elektromagneet(0)

                    #positie x as elektromagneet bepalen, de eerste voor als het stuk een pion is de tweede voor als het een ander stuk is
                    if(inputslagx == 9):
                        self.beginx = 0
                    if(inputslagx == 10):
                        self.beginx = 2

                    #positie y as elektromagneet bepalen
                    self.beginy = inputslagy *2

                #als al de andere dingen zoals promotie of rokade behandeld is word de zet uitgevoerd
                self.SetMoverShort(inputstartx, inputstarty, inputendx, inputendy)

############################################################
############################################################                
############################################################
                ###Promotie code###
############################################################
############################################################
############################################################

    
            if(promotie != 0):
                print(self.elekx)
                print(self.eleky)
                print(inputstartx)
                print(inputstarty)
                print(inputendx)
                print(inputendy)
                self.SetMoverShort(inputstartx, inputstarty, inputendx, inputendy)
                print("done")
                geslagen = True
                
            if(promotie == 1):
                #promotie is koningin
                #check of het stuk al eerder geslagen is of niet
                if(geslagen == True):
                    slagx = (inputslagx + 2) * 2
                    slagy = (inputslagy * 2)
                    self.elektromagneet(1)
                    #eerst pion weg brengen
                    #daarna nieuw koningin ophalen
                    #breng pion naar zijn plek
                    if(beurt == "white"):
                        self.beweegxy(0,2)
                        self.beweegxy(4 - self.elekx,0)
                    if(beurt == "black"):
                        self.beweegxy(0,-2)
                        self.beweegxy(22 - self.elekx,0)
                    self.beweegxy(0,slagy - self.eleky + 1)
                    self.beweegxy(-4,0)
                    self.beweegxy(0,-1)
                    self.elektromagneet(0)
            #if(promotie == 2):
                #promotie is paard
            #if(promotie == 3):
                #promotie is een toren
            #if(promotie == 4)
                #promotie is een loper

############################################################
############################################################                
############################################################
                ###Rokade code###should fucking work
############################################################
############################################################
############################################################
                
        #korte rokade               
        if(rokade == 1):

            #zet elektromagneet onder de koning en activeer de elektromagneet
            movementx = 14 - self.elekx
            
            if(beurt == "white"):
                movementy = 2 - self.eleky
            if(beurt == "black"):
                movementy = 16 - self.eleky
                
            self.beweegxy(movementx, movementy)
            self.elektromagneet(1)

            #zet de koning op het juiste vlak voor de korte rokade dat is voor wit (2,18) voor zwart (16,18)
            self.beweegxy(4,0)

            #Deactiveer elektromagneet
            self.elektromagneet(0)

            #zet de elektromagneet onder de toren 
            self.beweegxy(2,0)

            #Activeer elektromagneet
            self.elektromagneet(1)

            #zet de toren 2 omlaag voor wit of 2 omhoof voor zwart
            #daarna beweegt hij naar de goede x
            #daarna beweegt hij naar de goede Y
            #dit moet om de koning te omzeilen
            #de eerste if is voor als wit aan de beurt is;
            #de tweede voor als zwart aan de beurt is 
            
            if(beurt == "white"):
                self.beweegxy(0,-2)
                self.beweegxy(-4,0)
                self.beweegxy(0,2)
                
            if(beurt == "black"):
                self.beweegxy(0,2)
                self.beweegxy(-4,0)
                self.beweegxy(0,-2)

            #deactiveer elektromagneet
            self.elektromagneet(0)
           
        #lange rokade
        if(rokade == 2):
            movementx = 14 - self.elekx
            
            if(beurt == "white"):
                movementy = 2 - self.eleky
            if(beurt == "black"):
                movementy = 16 - self.eleky
                
            self.beweegxy(movementx, movementy)
            self.elektromagneet(1)
            
            self.beweegxy(-4,0)
            self.elektromagneet(0)
            
            self.beweegxy(-4,0)
            self.elektromagneet(1)
            
            if(beurt == "white"):
                self.beweegxy(0,-2)
                self.beweegxy(6,0)
                self.beweegxy(0,2)
                
            if(beurt == "black"):
                self.beweegxy(0,2)
                self.beweegxy(6,0)
                self.beweegxy(0,-2)
                
            self.elektromagneet(0)

############################################################
############################################################                
############################################################
                ###beweging code###
############################################################
############################################################
############################################################


                 
    def SetMoverShort(self, inputstartx, inputstarty, inputendx, inputendy):
        #omreken van de x en y coördinaten
        startx = (inputstartx + 2) * 2
        starty = inputstarty * 2
        endx = (inputendx + 2) * 2
        endy = inputendy * 2
        print(startx)
        print(starty)
        print(endx)
        print(endy)
        #de beweging van het vorige punt van de elektromagneet naar het start punt van het stuk
        movementx = startx - self.beginx
        movementy = starty - self.beginy

        #activeren van de beweging
        self.beweegxy(movementx, movementy)
        
        #activeren van de elektromagneet
        self.elektromagneet(1)

        #de beweging van het begin van de zet naar het eind van de zet berekenen
        movementx = endx - startx  
        movementy = endy - starty

        #activeren van de beweging        
        self.beweegxy(movementx, movementy)

        #deactiveren van de elektromagneet
        self.elektromagneet(0)

        #de huidige positie van de elektromagneet door geven
        self.beginx = endx
        self.beginy = endy
        self.beurt += 1
		
    #als de motor niks hoeft te doen word deze ook niet geactiveerd
    def beweegxy(self, x, y):
        self.elekx += x
        self.eleky += y
        if(x != 0):
            print("motor1 beweeg " + str(x))
        if(y != 0):
            print("motor2 beweeg " + str(y))
        print(str(self.elekx),str(self.eleky))

    def elektromagneet(self, status):
        if(status == 0):
            print("Deactiveer de elektromagneet")
        if(status == 1):
            print("Activeer de elektromagneet")
                  
    
Main()
        

