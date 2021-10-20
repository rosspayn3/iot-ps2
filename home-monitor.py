import cherrypy, time, threading, json
from fakesensors import getFakeTemp, getFakeHumidity
#from realsensors import readHumidity, readTemp

humidity = 0
data = {}
alerts = {}
armed = True

def fakemonitor():
    while True:
        global armed
        print("🔵 Monitoring...")
        fakealert(armed)
        time.sleep(2)

def fakealert(armed):
    global alerts
    if armed:
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
        humidity = getFakeHumidity()
        tempc = getFakeTemp()
        data["tempC"] = str(round(tempc, 1))
        data["tempF"] = str(round((tempc * 9 / 5) + 32, 1))
        data["humidity"] = str(round(humidity, 1))
        JSON = json.dumps(data)
        return JSON

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def data(self):
        global data
        global humidity
        result = readHumidity()
        if result:
            humidity, temp = result
        temp = readTemp()
        if temp != None:
            return str(round(temp, 1))
        data["tempC"] = str(round(temp, 1))
        data["tempF"] = str(round( (temp * 9 / 5) + 32, 1))
        data["humidity"] = str(round(humidity, 1))
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
            print("🟢 alerts enabled")

    @cherrypy.expose
    def disable(self):
        if(cherrypy.request.remote.ip in ("127.0.0.1", "::1")):
            global armed
            armed = False
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
