import gpiozero
import time
#define GPIO pins to control each direction of the switch
motor1 = gpiozero.LED(17)
motor2 = gpiozero.LED(18)
#read awning state from file
file = open(r"e:\Python Scripts\awningstate.txt", "r")
amount_total=int(file.read())
#It take about 28 complete revolutions to extend the awning to shade the door for the puppies
#It takes about 78 revolution to extend the awning fully
#function to retract the awning
def retract(amount):
    motor1.on()
    print("Retracting")
    time.sleep(amount)
    motor1.off()
    print("Stopped")
#funtion to extend the awning
def extend(amount):
    motor2.on()
    print("Extending")
    time.sleep(amount)
    motor2.off()
    print("Stopped")
#function to display the current state of the awning
def current_state(amount_total):
    if amount_total >= 156:
        return "Your awning should be fully extended."
    elif amount_total < 156 and amount_total > 64:
        return "Your awning is between dog shade and fully extended."
    elif amount_total <= 64 and amount_total >= 56:
        return "Your awning should be at the dog shade position."
    else:
        return "Your awning is too close to the full-in or full-out position for full automatic movement."

print("START")
#is the awning in the proper position, if not input correction********************
#correct = input("Is this correct? y or n ")
#if correct == "n"
    #amount_total = input("What is the correct position?")

operation = input("Would you like to move the awning? (y or n):\n")
while operation == "y":
    print(current_state(amount_total))
    print(amount_total)
    direction = input("In or Out? (i or o):\n").lower()
#this section asks how far to move the awning IN, after considering its current distance
    if amount_total >= 156 and direction == "i":
        distance = input("Where would you like the awning to move? (f for full-in)(d for dog-shade)(s for a-smiggen):\n").lower()
        if distance == "f":
            amount = 156
        elif distance == "d":
            amount = 100
        elif distance == "s":
            amount = 2
        else:
            print("Incorrect distance command.")
    elif amount_total < 156 and amount_total > 56 and direction == "i":        
        distance = input("Where would you like the awning to move? (f for full-in)(d for dog-shade)(s for a smiggen):\n").lower()
        if distance == "f":
            amount = amount_total
        elif distance == "d":
            amount = amount_total - 56
        elif distance == "s":
            amount = 2
        else:
            print("Incorrect distance command.")
    elif amount_total <= 56 and direction == "i":        
        distance = input("Where would you like the awning to move? (f for full-in)(s for a smiggen):\n").lower()
        if distance == "f":
            amount = amount_total
        elif distance == "s":
            amount = 2
        else:
            print("Incorrect distance command.")
#this section asks how far to move the awning OUT, after considering its current distance
    elif amount_total >= 156 and direction == "o":
        distance = input("Where would you like the awning to move? (s for a smiggen):\n").lower()
        if distance == "s":
            amount = 2
        else:
            print("Incorrect distance command.")
    elif amount_total < 156 and amount_total > 56 and direction == "o":        
        distance = input("Where would you like the awning to move? (f for full-out)(s for a smiggen):\n").lower()
        if distance == "f":
            amount = 156 - amount_total
        elif distance == "s":
            amount = 2
        else:
            print("Incorrect distance command.")
    elif amount_total <= 56 and direction == "o":        
        distance = input("Where would you like the awning to move? (f for full-out)(d for dog-shade)(s for a smiggen):\n").lower()
        if distance == "f":
            amount = 156 - amount_total
        elif distance == "d":
            amount = 56 - amount_total
        elif distance == "s":
            amount = 2
        else:
            print("Incorrect distance command.")                       
    print(amount)
    print(amount_total)
    if direction == "i":
        retract(amount)
        amount_total -= amount
    elif direction == "o":
        extend(amount)
        amount_total += amount
    else:
        print("Incorrect directional command.")

    operation = input("Would you like to move the awning again? (y or n):\n ").lower()
print("Operations Complete, please restart to move the awning again.")
#write out the ending state of the awning for use the next time it is ran
amount_total=str(amount_total)
file=open(r"e:\Python Scripts\awningstate.txt", mode= "w", encoding="utf-8")
file.write(amount_total)
file.close()