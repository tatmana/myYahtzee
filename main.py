#Card Order
#00 ACES
#01 TWOS
#02 THREES
#03 FOURS
#04 FIVES
#05 SIXES
#06 3 OF A KIND
#07 4 OF A KIND
#08 FULL HOUSE
#09 SM STRAIGHT
#10 LG STRAIGHT
#11 YAHTZEE!
#12 CHANCE


import random


def rollDice(numDice):          #Rolls the requested number of dice and returns a list
    result = []
    for i in range (numDice):
        result.append(random.randint(1,6))
    return result


def printBoard(userCard,computerCard):          #Prints the scoreboard
    scoreCategories = [
        "ACES        ",
        "TWOS        ",
        "THREES      ",
        "FOURS       ",
        "FIVES       ",
        "SIXES       ",
        "3 OF A KIND ",
        "4 OF A KIND ",
        "FULL HOUSE  ",
        "SM STRAIGHT ",
        "LG STRAIGHT ",
        "YAHTZEE!    ",
        "CHANCE      "
    ]

    print("\u0332".join("Line  | Scorecard  Player | Computer"))
    for i in range (13):
        if i < 9:           #Prints single digit
            print(i+1, "    |", scoreCategories[i], end="")
        else:                  #Prints double digit
            print(i+1, "   |", scoreCategories[i], end="")
        if userCard[i] == -1:   #If card slot is empty prints blank space
            print("      | ", end="")
        elif userCard[i] >= 0 and userCard[i] <= 9:     #If card slot contains single digit
            print("  ", userCard[i], " |", end="")
        else:                                           #If card slot contains double digit
            print(" ", userCard[i], " |", end="")

        if computerCard[i] == -1:       #Prints comptuer card data
            print("")
        elif computerCard[i] >= 0 and computerCard[i] <= 9:
            print("  ", computerCard[i])
        else:
            print(" ", computerCard[i])

def printDice(dice,myDice,keep=0):      #Prints the value of the dice rolled and their position
    print("You have rolled",len(dice), "dice. Please pick the dice you would like to keep:\n"
                                         "Type the di position seperated by a space. \n"
                                    "Position: ",end="")
    if not keep:
        for i in range (len(dice)):
            print(" ", i+1, " |",end="")
        print("\nDi Value: ",end="")
        for i in range (len(dice)):
            print(" ", dice[i], " |",end="")

    print("\n\nKeeping: ", end="")
    for i in range (len(myDice)):
        print(" ", myDice[i], " |",end="")

def askKeepers(dice):           #Asks for amd validates user input
    checkInput = 1
    while checkInput:
        userInput = input("\nPlease enter your choice: ").rstrip()
        keepList = userInput.split(" ")         #Splits input into list.
        if keepList[0] != "":
            #keepList = [eval(n) for n in keepList]
            for i in range(len(keepList)):         #Make sure number is in correct dice picking range.
                if int(keepList[i]) > 0 and int(keepList[i]) <= len(dice):
                    checkInput = 0
            if len(keepList) > len(set(keepList)):
                print("Duplicate entry detected. Try again!")
                checkInput = 1
        else:
            checkInput = 0

    return keepList


def userTurn():             #Let's the user roll and pick dice. Returns list of 5 dice.
    keepDice = []
    rollsLeft = 3

    while rollsLeft:                #Keep rolling until no more rolls left
        dice = rollDice(5 - len(keepDice))
        printDice(dice, keepDice)
        keepList = askKeepers(dice)
        if keepList[0] == '':       #User hits enter, no dice kept, rolls again.
            print("Roll again.")
        else:
            for i in range(len(keepList)):
                keepDice.append(dice[int(keepList[i])-1])


        rollsLeft += -1

        if len(keepDice) == 5:
            rollsLeft = 0

    count = 0               #Moves left over dice into keepDice
    while len(keepDice) < 5:
        if str(count+1) not in keepList:
            keepDice.append(dice[count])
        count += 1

    return keepDice

def chooseScore(userCard,userDice):      #Prints the board and lets the user choose where to enter points and updates userCard
    tmpCard= scoreDice(userDice)
    openSpaceCard = [-1] * 13
    blankCard = [-1] *13
    correctChoice = 0
    for i in range(13):
        if userCard[i] == -1 and tmpCard[i] > 0:
            openSpaceCard[i] = tmpCard[i]
    printBoard(openSpaceCard,blankCard)
    printDice(userDice, userDice,1)
    while not correctChoice:
        userChoice = int(input("\nPlease enter the row number for where to keep these points: "))
        if userChoice < 14 and userChoice > 0:
            if tmpCard[userChoice-1] < 0 and userCard[userChoice-1] < 0:
                userCard[userChoice-1] = 0
                correctChoice = 1
            elif userCard[userChoice-1] >= 0:
                print ("Choice already taken. Try again.")
            else:
                userCard[userChoice-1] = tmpCard[userChoice-1]
                correctChoice = 1


def scoreDice(userDice):        #Accepts dice roll and returns a list of scores
    tmpCard = [-1]*13

    for i in range(13):                 #Creates a tmp score card for all options of dice held
        if i <= 5:                      #For the 1 to 6 numbers
            if userDice.count(i+1) > 0:
                tmpCard[i] = userDice.count(i+1) * (i + 1)
        elif i == 6:                    #For the 3 of a kind
            for x in range(6):
                if userDice.count(x+1) >= 3:
                    tmpCard[i] = sum(userDice)
        elif i == 7:                    #Four of a kind
            for x in range(6):
                if userDice.count(x+1) >= 4:
                    tmpCard[i] = sum(userDice)
        elif i == 8:                    #Full house
            for x in range(6):
                if userDice.count(x+1) >= 3:
                    tmpDice = userDice.copy()
                    tmpDice.remove(x + 1)
                    tmpDice.remove(x + 1)
                    tmpDice.remove(x + 1)
                    for y in range (6):
                        if tmpDice.count(y+1) >= 2:
                            tmpCard[i] = 25
        elif i == 9:
            if 3 in userDice:
                if 4 in userDice:
                    if 1 in userDice and 2 in userDice:
                        tmpCard[i] = 30
                    elif 2 in userDice and 5 in userDice:
                        tmpCard[i] = 30
                    elif 5 in userDice and 6 in userDice:
                        tmpCard[i] = 30
        elif i == 10:                       #Long straight
            if 2 in userDice:
                if 3 in userDice:
                    if 4 in userDice:
                        if 5 in userDice:
                            if 6 in userDice:
                                tmpCard[i] = 40
                            elif 1 in userDice:
                                tmpCard[i] = 40
        elif i == 11:                      #Yahtzee
            for x in range(6):
                if userDice.count(x+1) == 5:
                    tmpCard[i] = 50
        elif i == 12:
            tmpCard[i] = sum(userDice)

    return tmpCard

def chooseScoreComputer(computerCard):      #Handles computer scoring
    computerDice = rollDice(5)
    scoreOptions = scoreDice(computerDice)
    highScorePosition = 0
    for i in range (13):            #Finds the highest value spot that isn't taken.
        if scoreOptions[i] >= scoreOptions[highScorePosition] and computerCard[i] == -1:
            highScorePosition = i
    computerCard[highScorePosition] = scoreOptions[highScorePosition]       #Saves the spot.
    print("\n\nComputer Rolls: ", end="")
    for i in range(len(computerDice)):
        print(" ", computerDice[i], " |", end="")
    print(" and chooses option %i to store %i points!" %((highScorePosition+1),(scoreOptions[highScorePosition])))

def finalScores(userCard,computerCard):         #Prints final card and scores with bonus and winner
    userBonus = isBonus(userCard)
    computerBonus = isBonus(computerCard)
    userScore = sum(userCard)
    computerScore = sum(computerCard)
    print ("\n\nFinal Scores!")
    printBoard(userCard,computerCard)
    print ("User bonus: %i    " %userBonus)
    print ("User Score: %i    " %userScore)
    print ("Computer bonus: %i" %computerBonus)
    print ("Computer score: %i" %computerScore)
    if computerScore > userScore:
        print("Computer wins!")
    elif computerScore < userScore:
        print("User wins!")
    else:
        print("Tie!")


def isBonus(card):  #Checks if there is a bonus and returns 35 if so.
    count = 0
    for i in range(6):
        count += card[i]
    if count >= 63:
        return 35
    else:
        return 0

def main():
    userCard = [-1]*13
    computerCard = [-1]*13
    for i in range(13):
        userDice = userTurn()
        chooseScore(userCard,userDice)
        chooseScoreComputer(computerCard)
        printBoard(userCard,computerCard)
    finalScores(userCard,computerCard)

main()