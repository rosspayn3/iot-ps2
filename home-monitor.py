import cherrypy, time, threading, json
from fakesensors import getFakeTemp, getFakeHumidity, getFakeDistance
#from realsensors import readHumidity, readTemp

humidity = 0
data = {}
alerts = {}
armed = True


def fakemonitor():
    while True:
        global armed
        if armed:
            print("🔵 Monitoring...")
            distance = getFakeDistance()
            print("📏 " + str( round(distance, 3)) )
            if distance < 10:
                fakealert()
        time.sleep(1)

def fakealert():
    global alerts
    print("🟡 ALERT ALERT")
    alerts[time.strftime("%a %b-%d-%Y %#I:%M:%S %p")] = "Movement detected"

class HomeMonitor(object):
    @cherrypy.expose
    def index(self):
        return open("dashboard.html").read()

    @cherrypy.expose
    def testing(self):
        return open("dashboard-test.html").read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def fakedata(self):
        global data
        global humidity
        global armed
        data["armed"] = armed
        tempc = getFakeTemp()
        data["tempC"] = str(round(tempc, 1))
        data["tempF"] = str(round((tempc * 9 / 5) + 32, 1))
        humidity = getFakeHumidity()
        data["humidity"] = str(round(humidity, 1))
        JSON = json.dumps(data)
        return JSON

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def data(self):
        global data
        global humidity
        data["armed"] = armed
        result = readHumidity()
        if result:
            humidity, temp = result
            data["humidity"] = str(round(humidity, 1))
        temp = readTemp()
        if temp != None:
            data["tempC"] = str(round(temp, 1))
            data["tempF"] = str(round( (temp * 9 / 5) + 32, 1))
        JSON = json.dumps(data)
        return JSON

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alerts(self):
        global alerts
        JSON = json.dumps(alerts)
        return JSON

    @cherrypy.expose
    def enable(self):
        if(cherrypy.request.remote.ip in ("127.0.0.1", "::1")):
            global armed
            armed = True
            cherrypy.response.cookie['armed'] = True
            print("🟢 alerts enabled")

    @cherrypy.expose
    def disable(self):
        if(cherrypy.request.remote.ip in ("127.0.0.1", "::1")):
            global armed
            armed = False
            cherrypy.response.cookie['armed'] = False
            print("🔴 alerts disabled")

    @cherrypy.expose
    def clearalerts(self):
        if(cherrypy.request.remote.ip in ("127.0.0.1", "::1")):
            global alerts
            alerts = {}
            print("🟡 alerts cleared")

    


if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=fakemonitor)
        t1.daemon = True
        t1.start()
        cherrypy.quickstart(HomeMonitor())
    except Exception:
        print("exception happened")
