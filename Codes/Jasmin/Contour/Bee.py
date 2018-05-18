# Object Bee
# a Bee has an id, a position (x, y), a speed (x, y) and an history of the all last positions (x, y)
class Bee(object):

# declaration and initalisation of the variables
    id = 0
    positionX = 0 # current poistion x
    positionY = 0 # current poistion y
    speedX = 0 # current speed x
    speedY = 0 # current speed y
    historyPosition = [] ## all last poistions
    state = 0 # 0: creating bee, 1: fling bee, 2: entering bee 3: lost bee
    counter = 0 # after 100 frames as a lost bee, delete bee
    update = False

    # constructor
    def __init__(self, id, positionX, positionY, speedX, speedY, state, counter, update):
        self.id = id
        self.positionX = positionX
        self.positionY = positionY
        self.speedX = speedX
        self.speedY = speedY
        self.state = state
        self.counter = counter
        self.update = update

    # Method for bee object

    # input : the object Bee
    # output : show in the terminal the information of the bee
    # example : Bee : 113, position ( 22, 33), speed (1, 1)
    def screen(self):
        print("Bee no = " + str(self.id) + ", position (" + str(self.positionX) + ", " + str(self.positionY) + "), speed (" + str(self.speedX) + ", " + str(self.speedY) + ")" + "\n")
        # print("Bee no = ", self.id, ', position: ', self.positionX,self.positionY,' Speed: ', self.speedX,',',self.speedY,' Current state: ', self.state)
    # input :
    #            the object Bee
    #            new positionX : current position x-axis
    #            new positionY : current position y-axis
    # function
    #            - add the last position to the history table
    #            - change the position with the current value
    def newPosition(self, positionX, positionY):
        self.historyPosition.append( [self.positionX, self.positionY])
        self.positionX = positionX
        self.positionY = positionY
