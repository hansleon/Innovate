    def Moveh(self, startx, starty, endx, endy, posx, posy):
        posx, posy = self.Beweegposxy(posx, posy, startx, starty)
        movementx = endx - startx
        movementy = endy - starty
        if(movementx == 2 and movementy == 4):
            posx, posy = self.Beweegposxy(posx, posy, posx + 1, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, posy + 4)
            posx, posy = self.Beweegposxy(posx, posy, posx + 1, posy)
        if(movementx == 4 and movementy == 2):
            posx, posy = self.Beweegposxy(posx, posy, posx, posy + 1)
            posx, posy = self.Beweegposxy(posx, posy, posx + 4, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, posy + 1)
        if(movementx == 4 and movementy == -2):
            posx, posy = self.Beweegposxy(posx, posy, posx , posy - 1)
            posx, posy = self.Beweegposxy(posx, posy, posx + 4, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, posy - 1)
        if(movementx == 2 and movementy == -4):
            posx, posy = self.Beweegposxy(posx, posy, posx + 1, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, posy - 4)
            posx, posy = self.Beweegposxy(posx, posy, posx + 1, posy) 
        if(movementx == -2 and movementy == -4):
            posx, posy = self.Beweegposxy(posx, posy, posx - 1, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, posy - 4)
            posx, posy = self.Beweegposxy(posx, posy, posx - 1, posy)
        if(movementx == -4 and movementy == -2):
            posx, posy = self.Beweegposxy(posx, posy, posx, posy - 1)
            posx, posy = self.Beweegposxy(posx, posy, posx - 4, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, posy - 1) 
        if(movementx == -4 and movementy == 2):
            posx, posy = self.Beweegposxy(posx, posy, posx, posy + 1)
            posx, posy = self.Beweegposxy(posx, posy, posx - 4, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, posy + 1)
        if(movementx == -2 and movementy == 4):
            posx, posy = self.Beweegposxy(posx, posy, posx - 1, posy)
            posx, posy = self.Beweegposxy(posx, posy, posx, posy + 4)
            posx, posy = self.Beweegposxy(posx, posy, posx - 1, posy)
