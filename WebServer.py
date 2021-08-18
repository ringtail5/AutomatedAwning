#!/usr/bin python3

import os
import gpiozero
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# IP Address and port of Raspberry Pi
host_name = "192.168.1.29"
host_port = 80

#Define which GPIO pins are activated for motor movement
motor1 = gpiozero.LED(17)
motor2 = gpiozero.LED(18)

#read awning state from file
file = open(r"awningstate.txt", "r")
amount_total=int(file.read())
file.close()

#write awning state to file
def writefile(amount_total):
    file=open(r"awningstate.txt", mode= "w", encoding="utf-8")
    file.write(str(amount_total))
    file.close()

#Allow for temperature retrieval
def getTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return temp

#Convert the awning state to text
#468= Fully Extended, 168=Dog Shade
def getState(amount_total):
    if amount_total >468:
        return "Over Extended!"
    elif amount_total == 468:
        return "Fully Extended."
    elif amount_total < 468 and amount_total > 168:
        return "Between Dog Shade and Fully Extended."
    elif amount_total == 168:
        return "Dog Shade."
    elif amount_total < 168 and amount_total > 0:
        return "Between Dog Shade and Fully Retracted."
    elif amount_total == 0:
        return "Fully Retracted."
    else:
        return "Over Retracted!"

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

class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
            <html>
            <body
             style="width:960px; margin: 20px auto;">
            <h1>Welcome to my Raspberry Pi Awning Controller</h1>
            <p>Current PI temperature is {temp}</p>
            <p>Current awning state is {state}</p>
            <form action="/" method="POST">
                Move Awning to: 
                <input type="submit" name="submit" value="Fully-Extended">
                <input type="submit" name="submit" value="Fully-Retracted">
                <input type="submit" name="submit" value="Dog-Shade">
                <input type="submit" name="submit" value="Extend-a-Smidge">
                <input type="submit" name="submit" value="Retract-a-Smidge">
            </form>
            </body>
        '''
        temp = getTemperature()
        state = getState(amount_total)
        self.do_HEAD()
        self.wfile.write(html.format(temp=temp[5:], state=state).encode("utf-8"))

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]
        global amount_total

        if post_data == 'Fully-Extended':
            if amount_total > 468:
                amount = amount_total - 468
                retract(amount)
                amount_total = 468
                writefile(amount_total)
            elif amount_total < 468:
                amount = 468 - amount_total
                extend(amount)
                amount_total = 468
                writefile(amount_total)
            else:
                print("Awning is already Fully-Extended") 
        elif post_data == 'Fully-Retracted':
            if amount_total < 0:
                amount = amount_total * -1
                extend(amount)
                amount_total = 0
                writefile(amount_total)
            elif amount_total > 0:
                amount = amount_total
                retract(amount)
                amount_total = 0
                writefile(amount_total)
            else:
                print("Awning is already Fully-Retracted")
        elif post_data == 'Dog-Shade':
            if amount_total > 168:
                amount = amount_total - 168
                retract(amount)
                amount_total = 168
                writefile(amount_total)
            elif amount_total < 168:
                amount = 168 - amount_total
                extend(amount)
                amount_total = 168
                writefile(amount_total)
            else:
                print("Awning is already at Dog-Shade")
        elif post_data == 'Extend-a-Smidge':
            if amount_total < 469:
                amount = 6
                extend(amount)
                amount_total += amount
                writefile(amount_total)
            else:
                print("Awning too far to extend further.")
        elif post_data == 'Retract-a-Smidge':
            if amount_total > -1:
                amount = 6
                retract(amount)
                amount_total -= amount
                writefile(amount_total)
            else:
                print("Awning too close to retract further.")

        print("The current operation completed was {}".format(post_data))
        self._redirect('/') #Redirect back to the root url

# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name,host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()