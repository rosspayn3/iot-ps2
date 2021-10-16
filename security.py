import cherrypy
import random
import string
from sensors import getFakeTempF, getFakeTempC
from realsensors import readHumidity, readTemp

times = 0
humidity = 0
    
def clickFunction():
    global times
    times = times + 1
    print(f"Button clicked {times} times!")
    
def makeHeader():
    return """
        <!DOCTYPE html>
        <html>
            <head>
            <title>Best Python Web Page</title>
            <style>
                body { background-color: #333; color: white; width: 75%; margin: auto}
                .answer { color: #6FF; font-weight: 900 }
            </style>
            </head>
            <body>
        """

def makeFooter():
        return """
            </body>
            </html>
        """

def makeHTML(body):
    return makeHeader() + str(body) + makeFooter()
    
def returnHTML(values):
    return open("file.html").read().format(tempF=values[0],tempC=values[1])


class StringGenerator(object):
    
    @cherrypy.expose
    def index(self):
        temps = [round(getFakeTempF(),1), round(getFakeTempC(),1)]
        return returnHTML(temps)
    
    @cherrypy.expose
    def testing(self):
        return open("file2.html").read()

    @cherrypy.expose
    def real(self):
        result = readHumidity()
        temp = readTemp()
        if result and temp != None:
            humidity, temperature = result
            print ("%s" % (humidity))
            print ("%s" % (temp))
            return "read the sensors\n%s %s" % (humidity, temp) 
    
    @cherrypy.expose
    def faketempc(self):
        print("Fake temp C requested\n")
        return str( round(getFakeTempC(),1) )
    
    @cherrypy.expose
    def faketempf(self):
        print("Fake temp F requested\n")
        return str( round(getFakeTempF(),1) )

    @cherrypy.expose
    def tempc(self):
        temp = readTemp()
        if temp != None:
            return str( round(temp, 1) )

    @cherrypy.expose
    def tempf(self):
        temp = readTemp()
        if temp != None:
            temp = (temp * 9/5) + 32
            return str( round(temp, 1) )

    @cherrypy.expose
    def humidity(self):
        global humidity
        result = readHumidity()
        if result:
            humidity, temp = result
            return str( round(humidity, 1) )
        else:
            return str( round(humidity, 1) )

cherrypy.quickstart(StringGenerator())
