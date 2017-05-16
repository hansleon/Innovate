class Main:
    def __init__(self):
	
        #global maken
        global beginx
        global beginy
        global beurt
		
        #beginx en beginy geven de huidige positie aan van de elektromagneet
        self.beginx = 0
        self.beginy = 0
        self.beurt = 0
        
        #beginpunt x as van het schaakstuk
        #beginpunt y as van het schaakstuk
        #eindpunt x as van het schaakstuk
        #eindpunt y as van het schaakstuk
        #word een stuk geslagen ja/nee
        #eindpunt x as geslagen stuk
        #eindpunt y as geslagen stuk
        #is er een promotie en welk stuk word het, 0 voor nee, 1 voor koningin, 2 voor paard, 3 voor toren, 4 voor loper
        #rokade 0 is geen, 1 is korte rokade, 2 is lange rokade
        #op dit punt zijn er 3 zetten geweest
        
        
        #self.Ifslas(5,2,5,4,False,0,0,0,0,self.beurt)
        self.Ifslas(4,7,4,5,False,0,0,0,0,self.beurt)
        self.Ifslas(5,4,7,8,True,10,6,0,0,self.beurt)
        
    def Ifslas(self, inputstartx, inputstarty, inputendx, inputendy, slag, inputslagx, inputslagy, promotie, rokade, beurt):
	
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
                    print(endx)
                    print(self.beginx)
                    #voert de beweging uit
                    self.beweegxy(movementx, movementy)

                    #activeren van de elektromagneet
                    print("activeerelektromagneet")

                    #beweging om tussen de stukken door te gaan
                    self.beweegxy(0,1)
					
                    if(beurt%2 == 0):
					
                        #beweging om naar de linkerkant te gaan in het geval van een slag voor wit
                        #slag voor zwart moet nog gemaakt worden
                        #deze regel klopt voor geen hoer
                        print(movementx)
                        self.beweegxy(4 - self.beginx , 0)

                        #beweging om naar de hoogte van het gewenste vak te gaan
                        self.beweegxy(0, slagy - endy)

                        #beweging om naar het juiste vak te bewegen op de graveyard
                        #eerste if word geactiveerd als het een pion is en de tweede als het een ander stuk is
                        if(inputslagx == 9):
                            self.beweegxy(-4,0)
                        if(inputslagx == 10):
                            self.beweegxy(-2,0)
                    else:
					
                        #beweging om naar de linkerkant te gaan in het geval van een slag voor wit
                        #slag voor zwart moet nog gemaakt worden
                        print(movementx)
                        self.beweegxy(12 + movementx , 0)

                        #beweging om naar de hoogte van het gewenste vak te gaan
                        self.beweegxy(0, slagy - endy)

                        #beweging om naar het juiste vak te bewegen op de graveyard
                        #eerste if word geactiveerd als het een pion is en de tweede als het een ander stuk is
                        if(inputslagx == 9):
                            self.beweegxy(4,0)
                        if(inputslagx == 10):
                            self.beweegxy(2,0)

                    #beweging om recht in het vak te komen
                    self.beweegxy(0,-1)

                    #deactiveren van de elektromagneet
                    print("deactiveerelektromagneet")

                    #positie x as elektromagneet bepalen, de eerste voor als het stuk een pion is de tweede voor als het een ander stuk is
                    if(inputslagx == 9):
                        self.beginx = 0
                    if(inputslagx == 10):
                        self.beginx = 2

                    #positie y as elektromagneet bepalen
                    self.beginy = inputslagy *2

                #als al de andere dingen zoals promotie of rokade behandeld is word de zet uitgevoerd
                self.SetMoverShort(inputstartx, inputstarty, inputendx, inputendy)

    def SetMoverShort(self, inputstartx, inputstarty, inputendx, inputendy):

        #omreken van de x en y coördinaten
        startx = (inputstartx + 2) * 2
        starty = inputstarty * 2
        endx = (inputendx + 2) * 2
        endy = inputendy * 2

        #de beweging van het vorige punt van de elektromagneet naar het start punt van het stuk
        movementx = startx - self.beginx
        movementy = starty - self.beginy

        #activeren van de beweging
        self.beweegxy(movementx, movementy)

        #activeren van de elektromagneet
        print("activeerelektromagneet")

        #de beweging van het begin van de zet naar het eind van de zet berekenen
        movementx = endx - startx  
        movementy = endy - starty

        #activeren van de beweging        
        self.beweegxy(movementx, movementy)
        print("deactiveerelektromagneet")

        #de huidige positie van de elektromagneet door geven
        self.beginx = endx
        self.beginy = endy
        self.beurt += 1
		
    #als de motor niks hoeft te doen word deze ook niet geactiveerd
    def beweegxy(self, x, y):
        if(x != 0):
            print("motor1 beweeg " + str(x))
        if(y != 0):
            print("motor2 beweeg " + str(y))
        
    
Main()
        
