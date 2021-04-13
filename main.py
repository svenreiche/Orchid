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
        # constuct the labels
        self.setComboBox(self.UIKultur, self.db.labels['Kultur'])
        self.setComboBox(self.UIKlima, self.db.labels['Klima'])
        self.setComboBox(self.UIWasser, self.db.labels['Wasser'])
        self.setComboBox(self.UIRuhe, self.db.labels['Ruhe'])
        self.setComboBox(self.UILicht, self.db.labels['Licht'])

        # events
        self.UISuche.textEdited.connect(self.search)
        self.UIResult.currentItemChanged.connect(self.infofromlist)
        self.UISave.clicked.connect(self.saveRecord)
        self.UINew.clicked.connect(self.newRecord)
        self.UIImageUpdate.clicked.connect(self.updateImage)
        self.UILaunchPflege.clicked.connect(self.launchWeb)
        self.UILaunchInternet.clicked.connect(self.launchWeb)
        self.actionSave.triggered.connect(self.saveDB)
        self.actionReport.triggered.connect(self.reportDB)
        self.recordID=-1

    def setComboBox(self,combo,labs):
        combo.clear()
        for lab in labs:
            combo.addItem(lab)
        combo.setCurrentIndex(0)

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
        self.recordID = maxID
        self.saveRecord()
        self.info(name)

    def saveRecord(self):
        if self.recordID < 0:
            return
        name = str(self.UIName.text())

        if not name in self.db.db.keys():   # key name has changed
            checkID = self.db.checkID(self.recordID)  # get former name for ID
            if checkID is None:
                return
            self.db.db[name] = self.db.db[checkID]
            del self.db.db[checkID]
        else:
            if not self.recordID == self.db.db[name]['ID']:   # name was changed to already existing key name
                QtWidgets.QMessageBox.about(self, 'Duplicate Entry', 'The record %s exists already' % name)
                return
        self.db.db[name]['Kultur'] = self.UIKultur.currentIndex()
        self.db.db[name]['Klima'] = self.UIKlima.currentIndex()
        self.db.db[name]['Wasser'] = self.UIWasser.currentIndex()
        self.db.db[name]['Licht'] = self.UILicht.currentIndex()
        self.db.db[name]['Ruhe'] = self.UIRuhe.currentIndex()
        self.db.db[name]['Anzahl'] = int(str(self.UIExemplare.text()))
        self.db.db[name]['Gattung'] = str(self.UIGattung.text())
        self.db.db[name]['Internet'] = str(self.UIInternetLink.text())
        self.db.db[name]['Pflege'] = str(self.UIPflege.text())

    def info(self, name):
        if name is None or not name in self.db.db.keys():
            self.UIName.clear()
            self.UIGattung.clear()
            self.UIExemplare.clear()
            self.UIKultur.setCurrentIndex(0)
            self.UIKlima.setCurrentIndex(0)
            self.UIWasser.setCurrentIndex(0)
            self.UILicht.setCurrentIndex(0)
            self.UIRuhe.setCurrentIndex(0)
            self.UIPflege.clear()
            self.UIInternetLink.clear()
            self.recordID = -1
            return
        item = self.db.db[name]
        self.recordID = item['ID']
        self.UIName.setText(name)
        self.UIGattung.setText(str(item['Gattung']))
        self.UIExemplare.setText('%d' % item['Anzahl'])
        self.UIKultur.setCurrentIndex(self.db.checkIntField(name, 'Kultur'))
        self.UIKlima.setCurrentIndex(self.db.checkIntField(name, 'Klima'))
        self.UIWasser.setCurrentIndex(self.db.checkIntField(name, 'Wasser'))
        self.UIRuhe.setCurrentIndex(self.db.checkIntField(name, 'Ruhe'))
        self.UILicht.setCurrentIndex(self.db.checkIntField(name, 'Licht'))
        self.UIInternetLink.setText(self.db.checkStrField(name, 'Internet'))
        self.UIPflege.setText(self.db.checkStrField(name, 'Pflege'))
        if 'Photo' in item.keys() and len(item['Photo'])>0:
            pixmap = QPixmap(item['Photo'])
            self.UIImage.setPixmap(pixmap.scaled(self.UIImage.width(),self.UIImage.height(),QtCore.Qt.KeepAspectRatio))
        else:
            self.UIImage.clear()

    def infofromlist(self):
        entry=self.UIResult.currentItem()
        if entry is None:
            self.info(None)
        else:
            self.info(str(entry.text()))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Orchid()
    main.show()
    sys.exit(app.exec_())
