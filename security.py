import cherrypy
from fakesensors import getFakeTempF, getFakeTempC, getFakeHumidity

# from realsensors import readHumidity, readTemp

times = 0
humidity = 0

class SecurityDashboard(object):
    @cherrypy.expose
    def index(self):
        return open("dashboard.html").read()

    @cherrypy.expose
    def testing(self):
        return open("dashboard-test.html").read()

    @cherrypy.expose
    def real(self):
        result = readHumidity()
        temp = readTemp()
        if result and temp != None:
            humidity, temperature = result
            print("%s" % (humidity))
            print("%s" % (temp))
            return "read the sensors\n%s %s" % (humidity, temp)

    @cherrypy.expose
    def faketempc(self):
        print("Fake temp C requested\n")
        return str(round(getFakeTempC(), 1))

    @cherrypy.expose
    def faketempf(self):
        print("Fake temp F requested\n")
        return str(round(getFakeTempF(), 1))

    @cherrypy.expose
    def fakehumidity(self):
        print("Fake humidity requested\n")
        return str(round(getFakeHumidity(), 1))

    @cherrypy.expose
    def tempc(self):
        temp = readTemp()
        if temp != None:
            return str(round(temp, 1))

    @cherrypy.expose
    def tempf(self):
        temp = readTemp()
        if temp != None:
            temp = (temp * 9 / 5) + 32
            return str(round(temp, 1))

    @cherrypy.expose
    def humidity(self):
        global humidity
        result = readHumidity()
        if result:
            humidity, temp = result
            return str(round(humidity, 1))
        else:
            return str(round(humidity, 1))


cherrypy.quickstart(SecurityDashboard())
