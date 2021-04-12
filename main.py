import sys
import DBManager

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.uic import loadUiType

Ui_OrchidGUI, QMainWindow = loadUiType('Orchid.ui')


class Orchid(QMainWindow, Ui_OrchidGUI):
    def __init__(self):
        super(Orchid, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Orchideen Datenbank")

        self.db = DBManager.DBManager()
        self.search()
        # events
        self.UISuche.textEdited.connect(self.search)
        self.UIResult.currentItemChanged.connect(self.info)
        self.UISave.clicked.connect(self.saveRecord)
        self.UINew.clicked.connect(self.newRecord)
        self.UIImageUpdate.clicked.connect(self.updateImage)
        self.UILaunchPflege.clicked.connect(self.launchWeb)
        self.UILaunchInternet.clicked.connect(self.launchWeb)
        self.actionSave.triggered.connect(self.saveDB)
        self.actionReport.triggered.connect(self.reportDB)
        self.recordID=-1


    def reportDB(self):
        self.db.report()

    def launchWeb(self):
        if self.recordID < 0:
            return
        name = str(self.UIName.text())
        tag = 'Internet'
        if self.sender() is self.UILaunchPflege:
            tag = 'Pflege'
        if tag in self.db.db[name].keys() and len(self.db.db[name][tag]) > 0:
            QDesktopServices.openUrl(QtCore.QUrl(self.db.db[name][tag]))


    def updateImage(self):
        if self.recordID < 0:
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Orchideen Photo", "",
                                                  "PNG Files (*.png);JPEG Files (*.jpg)", options=options)
        if fileName:
            name = str(self.UIName.text())
            self.db.db[name]['Photo']=fileName
            self.info(self.UIResult.currentItem())


    def saveDB(self):
        self.db.saveDB()

    def search(self):
        regexp = str(self.UISuche.text())
        res = self.db.search(regexp)
        self.UIResult.clear()
        nlen = len(res)
        self.UIResult.setRowCount(nlen)
        self.UIResult.setColumnCount(1)
        for i in range(nlen):
            self.UIResult.setItem(i,0,QtWidgets.QTableWidgetItem(res[i]))
        self.UIResult.verticalHeader().hide()
        self.UIResult.horizontalHeader().hide()
        self.UIResult.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.UIAnzahl.setText('%d' % nlen)


    def newRecord(self):
        maxID = -1
        for key in self.db.db.keys():
            if self.db.db[key]['ID']> maxID:
                maxID = self.db.db[key]['ID']
        maxID += 1
        name = str(self.UIName.text())
        if not name:
            name = 'New Entry'
        if name in self.db.db.keys():
            QtWidgets.QMessageBox.about(self, 'Duplicate Entry', 'The record %s exists already' % name)
            return
        self.db.db[name] = {}
        self.db.db[name]['ID'] = maxID
        self.db.db[name]['Kultur'] = self.UIKultur.currentIndex()
        self.db.db[name]['Klima'] = self.UIKlima.currentIndex()
        self.db.db[name]['Wasser'] = self.UIWasser.currentIndex()
        self.db.db[name]['Ruhe'] = self.UIRuhe.currentIndex()
        self.db.db[name]['Licht'] = self.UILicht.currentIndex()
        self.db.db[name]['Anzahl'] = 1
        self.db.db[name]['Gattung'] = str(self.UIGattung.text())
        self.db.db[name]['Internet'] = str(self.UIInternetLink.text())
        self.db.db[name]['Pflege'] = str(self.UIPflege.text())
        self.db.db[name]['Photo'] = str('')
        # make sure that the new record is also displayed
        self.UISuche.setText('')
        self.search()

    def saveRecord(self):
        if self.recordID < 0:
                return
        name = str(self.UIName.text())
        if name in self.db.db.keys():
            if self.db.db[name]['ID'] == self.recordID:   # simplest case - name has not changed
                self.db.db[name]['Kultur'] = self.UIKultur.currentIndex()
                self.db.db[name]['Klima'] = self.UIKlima.currentIndex()
                self.db.db[name]['Wasser'] = self.UIWasser.currentIndex()
                self.db.db[name]['Licht'] = self.UILicht.currentIndex()
                self.db.db[name]['Ruhe'] = self.UIRuhe.currentIndex()
                self.db.db[name]['Anzahl'] = int(str(self.UIExemplare.text()))
                self.db.db[name]['Gattung'] = str(self.UIGattung.text())
                self.db.db[name]['Internet'] = str(self.UIInternetLink.text())
                self.db.db[name]['Pflege'] = str(self.UIPflege.text())
            else:
                QtWidgets.QMessageBox.about(self,'Duplicate Entry','The record %s exists already' % name)
        else:    # check if the ID is the same
            for key in self.db.db.keys():
                if self.recordID == self.db.db[key]['ID']:
                    self.db.db[name]=self.db.db[key]
                    del self.db.db[key]
                    self.search()
                    return


    def info(self, item):
        if item is None:
            self.UIName.clear()
            self.UIGattung.clear()
            self.UIExemplare.clear()
            self.recordID = -1
            return
        name = str(item.text())
        item = self.db.db[name]
        self.UIName.setText(name)
        self.UIGattung.setText(str(item['Gattung']))
        self.UIExemplare.setText('%d' % item['Anzahl'])
        if 'Kultur' in item.keys():
            self.UIKultur.setCurrentIndex(item['Kultur'])
        else:
            self.UIKultur.setCurrentIndex(0)
        if 'Klima' in item.keys():
            self.UIKlima.setCurrentIndex(item['Klima'])
        else:
            self.UIKlima.setCurrentIndex(0)
        if 'Licht' in item.keys():
            self.UILicht.setCurrentIndex(item['Licht'])
        else:
            self.UILicht.setCurrentIndex(0)
        if 'Wasser' in item.keys():
            self.UIWasser.setCurrentIndex(item['Wasser'])
        else:
            self.UIWasser.setCurrentIndex(0)
        if 'Ruhe' in item.keys():
            self.UIRuhe.setCurrentIndex(item['Ruhe'])
        else:
            self.UIRuhe.setCurrentIndex(0)
        if 'Pflege' in item.keys():
            self.UIPflege.setText(item['Pflege'])
        else:
            self.UIPflege.setText('')
        if 'Internet' in item.keys():
            self.UIInternetLink.setText(item['Internet'])
        else:
            self.UIInternetLink.setText('')
        if 'Photo' in item.keys() and len(item['Photo'])>0:
            pixmap = QPixmap(item['Photo'])
            self.UIImage.setPixmap(pixmap.scaled(self.UIImage.width(),self.UIImage.height(),QtCore.Qt.KeepAspectRatio))
        else:
            self.UIImage.clear()

        self.recordID = item['ID']
        print(self.recordID)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Orchid()
    main.show()
    sys.exit(app.exec_())
