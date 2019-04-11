import sys, sqlite3 
from sqlite3 import Error
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Ui_room_detail import * # นำเข้าฟรอม Result

class Mainwindow(QMainWindow):
    stat = ""
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.btnDel.clicked.connect(self.save)
        self.ui.btnSave.clicked.connect(self.save)
        self.ui.btnCancel.clicked.connect(self.cancel)
        self.ui.btnAdd.clicked.connect(self.add)
        self.ui.btnEdit.clicked.connect(self.edit)
        self.ui.tableWidget.cellDoubleClicked.connect(self.twg_click)
        self.ui.btnExit.clicked.connect(self.exit)
        self.Load()
        self.show

    def save(self):
        if self.ui.txtfoor.text() == "" or self.ui.txtnum.text() == "" or self.ui.comboBox.currentText() == "":
            QMessageBox.critical(self, 'Error','กรุณากรอกข้อมูลให้ครบถ้วน',QMessageBox.Ok,QMessageBox.Ok)
            self.Load()
            return
        if self.stat == 'add':
            sql = "INSERT INTO home (h_id,h_address,h_status)VALUES ('"+ str(self.ui.txtnum.text()) +"','"+ str(self.ui.txtfoor.text()) +"','"+ str(self.ui.comboBox.currentText()) +"')"
        elif self.stat == 'edit':
            sql = "update home set h_address = '"+ str(self.ui.txtfoor.text()) +"',h_status = '"+ str(self.ui.comboBox.currentText()) +"' where h_id = '"+ str(self.ui.txtnum.text()) +"'"
        else:
            sql = "DELETE from home WHERE h_id = '" + str(self.ui.txtnum.text()) + "'"
        self.exe_query(sql)
        self.Load()


    def cancel(self):
        self.Load()

    def edit(self):
        self.ui.btnEdit.setEnabled(False)
        self.ui.btnDel.setEnabled(False)
        self.ui.comboBox.setEnabled(True)
        self.ui.btnSave.setEnabled(True)
        self.ui.txtnum.setEnabled(False)
        self.ui.txtfoor.setEnabled(True)
        self.stat = "edit"
    
    def add(self):
        self.ui.btnAdd.setEnabled(False)
        self.ui.comboBox.setEnabled(True)
        self.ui.btnSave.setEnabled(True)
        self.ui.txtnum.setEnabled(True)
        self.ui.txtfoor.setEnabled(True)
        self.stat = "add"

    def twg_click(self):
        row = self.ui.tableWidget.currentRow()
        cb1 = self.ui.comboBox.findText(self.ui.tableWidget.item(row,2).text(),QtCore.Qt.MatchFixedString)
        self.ui.txtnum.setText(self.ui.tableWidget.item(row,0).text())
        self.ui.txtfoor.setText(self.ui.tableWidget.item(row,1).text())
        if cb1 >= 0:
            self.ui.comboBox.setCurrentIndex(cb1)
        self.ui.btnAdd.setEnabled(False)
        self.ui.btnEdit.setEnabled(True)
        self.ui.btnDel.setEnabled(True)
        self.stat = "del"

    def Load(self):
        self.ui.txtfoor.setText("")
        self.ui.txtnum.setText("")
        self.twgLoad_()
        self.cmbload()
        self.ui.btnAdd.setEnabled(True)
        self.ui.comboBox.setEnabled(False)
        self.ui.txtnum.setEnabled(False)
        self.ui.txtfoor.setEnabled(False)
        self.ui.btnSave.setEnabled(False)
        self.ui.btnDel.setEnabled(False)
        self.ui.btnEdit.setEnabled(False)
            

    def exe_query(self,sql):
        try:
            conn = sqlite3.connect("PROJECT3.db")
            with conn:
                cur = conn.cursor()
                cur.execute(sql)
            data = cur.fetchall()
        except Error as e:
            print(e)
            msg = QMessageBox()
            msg.critical(
                self, 'Error',  '%s' % e,
                QMessageBox.Ok, 
                QMessageBox.Ok
            )
        finally:
            conn.close()
            return data
    
    def exit(self):
        QApplication.exit()

    def twgLoad_(self):
        sql = "Select h_id,h_address,h_status FROM home"
        data = self.exe_query(sql)
        self.ui.tableWidget.setRowCount(len(data)) 
        for i,row in enumerate(data):    
            for j,val in enumerate(row):       
                self.ui.tableWidget.setItem(i, j,QtWidgets.QTableWidgetItem(str(val)))
    
    def cmbload (self):
        self.ui.comboBox.clear()
        value = self.exe_query("select * from catehome order by ch_name asc")
        if(len(value)>0):
            for i in range(len(value)):
                a = value[i]
                self.ui.comboBox.addItem(str(a[1]),str(a[0]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Mainwindow()
    w.show()
    sys.exit(app.exec_())
