import time

class gameID:
    #een loop methode om de kijken wanneer de usb met game-id er in komt.
    def __init__(self):# wanneer het schaakspel over is moet deze methode weer aangeroepen worden.
        boole = True
        # boole is True tot dat het programma een usb met valid game-id gevonden heeft.
        while boole:
            time.sleep(3)
            # sleep om het systeem niet te overbelasten
            try:
                # eerste check
                path ='/media/pi/....../gameid.txt'
                days = open(path,'r')
                lijst = days.read()
                while not lijst:
                    # blijven checken voor usb / path / inhoud
                    path ='/media/pi/w_10_pro_x64/cool.txt'
                    days = open(path,'r')
                    lijst = days.read()
                    print(lijst)
                    print("file is empty")
                    time.sleep(3)
                else:
                    #Main(lijst)
                    print("started")
                    boole = False
            except Exception: # exception wanneer er een error komt.
                print("Path is not correct")
        
gameID()
