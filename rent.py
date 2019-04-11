import sys, sqlite3 
from sqlite3 import Error
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Ui_rent import * # นำเข้าฟรอม Result

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
        if  self.ui.cmbemp.currentText() == "" or self.ui.cmbcus.currentText() == "":
            QMessageBox.critical(self, 'Error','กรุณากรอกข้อมูลให้ครบถ้วน',QMessageBox.Ok,QMessageBox.Ok)
            self.Load()
            return
        if self.stat == 'add':
            sql = "INSERT INTO rental (c_id,em_id)VALUES ('" + str(self.ui.cmbcus.currentData()) + "','" + str(self.ui.cmbemp.currentData()) + "')"
        elif self.stat == 'edit':
            sql = "update  rental set c_id ='" + str(self.ui.cmbcus.currentData()) + "',em_id = '" + str(self.ui.cmbemp.currentData()) + "' where r_id = '" + self.ui.txtid.text() + "'"
        else:
            sql = "DELETE from rental WHERE r_id = '" + str(self.ui.txtid.text()) + "'"
        self.exe_query(sql)
        self.Load()


    def cancel(self):
        self.Load()

    def edit(self):
        self.ui.btnEdit.setEnabled(False)
        self.ui.btnDel.setEnabled(False)
        self.ui.cmbcus.setEnabled(True)
        self.ui.cmbemp.setEnabled(True)
        self.ui.btnSave.setEnabled(True)
        self.ui.txtid.setEnabled(False)
        self.stat = "edit"
    
    def add(self):
        self.ui.btnAdd.setEnabled(False)
        self.ui.cmbcus.setEnabled(True)
        self.ui.cmbemp.setEnabled(True)
        self.ui.btnSave.setEnabled(True)
        self.ui.txtid.setEnabled(False)
        self.stat = "add"

    def twg_click(self):
        row = self.ui.tableWidget.currentRow()
        cb1 = self.ui.cmbcus.findText(self.ui.tableWidget.item(row,1).text(),QtCore.Qt.MatchFixedString)
        cb2 = self.ui.cmbemp.findText(self.ui.tableWidget.item(row,2).text(),QtCore.Qt.MatchFixedString)
        self.ui.txtid.setText(self.ui.tableWidget.item(row,0).text())
        if cb1 >= 0:
            self.ui.cmbcus.setCurrentIndex(cb1)
        if cb2 >= 0:
            self.ui.cmbemp.setCurrentIndex(cb2)
        self.stat = "del"
        self.ui.btnAdd.setEnabled(False)
        self.ui.btnEdit.setEnabled(True)
        self.ui.btnDel.setEnabled(True)

    def Load(self):
        self.ui.txtid.setText("")
        self.twgLoad_()
        self.cmbload()
        self.ui.btnAdd.setEnabled(True)
        self.ui.cmbcus.setEnabled(False)
        self.ui.cmbemp.setEnabled(False)
        self.ui.txtid.setEnabled(False)
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
        sql = "select rental.r_id,customer.c_name,employee.em_name from rental,customer,employee where rental.c_id = customer.c_id and rental.em_id = employee.em_id"
        data = self.exe_query(sql)
        self.ui.tableWidget.setRowCount(len(data)) 
        for i,row in enumerate(data):    
            for j,val in enumerate(row):       
                self.ui.tableWidget.setItem(i, j,QtWidgets.QTableWidgetItem(str(val)))
    
    def cmbload (self):
        self.ui.cmbcus.clear()
        self.ui.cmbemp.clear()

        value = self.exe_query("select * from customer order by c_name asc")
        if(len(value)>0):
            for i in range(len(value)):
                a = value[i]
                self.ui.cmbcus.addItem(str(a[1]),str(a[0]))

        value = self.exe_query("select * from employee order by em_name asc")
        if(len(value)>0):
            for i in range(len(value)):
                a = value[i]
                self.ui.cmbemp.addItem(str(a[1]),str(a[0]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Mainwindow()
    w.show()
    sys.exit(app.exec_())
