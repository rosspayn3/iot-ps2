import cherrypy, time, threading, datetime, json
from fakesensors import getFakeTempF, getFakeTempC, getFakeHumidity
#from realsensors import readHumidity, readTemp

humidity = 0
alerts = {}
armed = True

def monitor():
    while True:
        global armed
        print("🔵 watching...")
        alert(armed)
        time.sleep(2)

def alert(armed):
    global alerts
    if armed:
        print("🟡 ALERT ALERT 🟡")
        timestamp = datetime.datetime.now()
        alerts["{:%b-%d-%Y %H:%M:%S}".format(timestamp)] = "Movement detected"

class HomeMonitor(object):
    @cherrypy.expose
    def index(self):
        return open("dashboard.html").read()

    @cherrypy.expose
    def testing(self):
        return open("dashboard-test.html").read()

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

    @cherrypy.expose
    def enable(self):
        global armed
        armed = True
        print("🟢 alerts enabled")

    @cherrypy.expose
    def disable(self):
        global armed
        armed = False
        print("🔴 alerts disabled")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alerts(self):
        global alerts
        JSON = json.dumps(alerts)
        return JSON

    @cherrypy.expose
    def clearalerts(self):
        global alerts
        alerts = {}
        print("🟡 alerts cleared")


if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=monitor)
        t1.daemon = True
        t1.start()
        cherrypy.quickstart(HomeMonitor())
    except Exception:
        print("exception happened")
