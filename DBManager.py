import re
import json
from reportlab.pdfgen import canvas

class DBManager:
    def __init__(self):
        self.db = {}
        self.file = '/media/reiche/Storage/PyCharm Projects/Ochid/OrchidDB.json'
        self.readDB()

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