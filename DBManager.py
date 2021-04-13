import re
import json
from reportlab.pdfgen import canvas

class DBManager:
    def __init__(self):
        self.db = {}
        kultur =['Unbekannt', 'Topf', 'Korb', 'Aufgebunden', 'P.E.T.', 'Glas']
        klima = ['Unbekannt', 'Kalt', 'Kalt/Temperiert', 'Temperiert', 'Temperiert/Warm', 'Warm']
        wasser = ['Unbekannt', 'Taeglich Bespruehen', 'Viel Wasser', 'Feucht Halten', 'Austrocknen Lassen']
        ruhe = ['Unbekannt', 'Keine Pause', 'Wenig Wasser', 'Kein Wasser']
        licht = ['Unbekannt', 'etwa 40.000 Lux', 'etwa 30.000 Lux', 'etwa 20.000 Lux', 'etwa 10.000 Liux']
        self.labels = {'Kultur': kultur, 'Klima': klima, 'Wasser': wasser, 'Ruhe': ruhe, 'Licht': licht}
        self.file = '/media/reiche/Storage/PyCharm Projects/Ochid/OrchidDB.json'
        self.readDB()

    def checkIntField(self,name,key):
        if not name in self.db.keys():
            return 0
        if not key in self.db[name].keys():
            return 0
        return int(self.db[name][key])

    def checkStrField(self, name, key):
        if not name in self.db.keys():
            return ''
        if not key in self.db[name].keys():
            return ''
        return str(self.db[name][key])
    
    def checkID(self,id):
        for key in self.db.keys():
            if self.db[key]['ID'] == id:
                return key
        return None

    def readDB(self):
        self.db.clear()
        with open(self.file,'r') as f:
            self.db = json.load(f)

    def saveDB(self,file=None):
        if not file is None:
            self.file = file
        with open(self.file, 'w') as out:
            json.dump(self.db, out, indent=4, sort_keys=True)

    def search(self, regexp):
        regexp='.*'+regexp.upper()+'.*'
        RE=re.compile(regexp)

        res=[]
        for key in sorted(self.db.keys()):
            if not RE.match(key.upper()) is None:
                res.append(key)
        return res

    def report(self):
        Kultur = ['Unbekannt', 'Topf', 'Korb', 'Aufgebunden', 'P.E.T.', 'Glas']
        c = canvas.Canvas("Orchideen-Report.pdf")
        c.setFont("Helvetica", 10)
        x0 =50
        y0 =800
        for key in sorted(self.db.keys()):
            c.drawString(x0, y0, key)
            c.drawString(x0-10, y0, '%d' % self.db[key]['Anzahl'])
            cul=0
            if 'Kultur' in self.db[key].keys():
                cul=self.db[key]['Kultur']
            c.drawString(300, y0, '%s' % Kultur[cul])
            y0 -= 15
            if y0 < 50:
               c.showPage()
               c.setFont("Helvetica", 10)
               y0 = 800
        c.showPage()
        c.save()