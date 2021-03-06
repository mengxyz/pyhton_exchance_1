import sys, sqlite3 
from sqlite3 import Error
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Ui_customer import * # นำเข้าฟรอม Result

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
        if self.ui.txtna.text() == "" or  self.ui.txttel.text() == "":
            QMessageBox.critical(self, 'Error','กรุณากรอกข้อมูลให้ครบถ้วน',QMessageBox.Ok,QMessageBox.Ok)
            self.Load()
            return
        if self.stat == 'add':
            sql = "INSERT INTO customer (c_name,c_tel)VALUES ('" + str(self.ui.txtna.text()) + "','" + str(self.ui.txttel.text()) + "')"
        elif self.stat == 'edit':
            sql = "update  customer set c_name='" + str(self.ui.txtna.text()) + "',c_tel = '" + str(self.ui.txttel.text()) + "' where c_id = '" + str(self.ui.txthid.text()) + "'"
        else:
            sql = "DELETE  from customer WHERE c_id = '" + str(self.ui.txthid.text()) + "'"
        self.exe_query(sql)
        self.Load()


    def cancel(self):
        self.Load()

    def edit(self):
        self.ui.btnEdit.setEnabled(False)
        self.ui.btnDel.setEnabled(False)
        self.ui.btnSave.setEnabled(True)
        self.ui.txthid.setEnabled(False)
        self.ui.txtna.setEnabled(True)
        self.ui.txttel.setEnabled(True)
        self.stat = "edit"
    
    def add(self):
        self.ui.btnAdd.setEnabled(False)
        self.ui.btnSave.setEnabled(True)
        self.ui.txthid.setEnabled(False)
        self.ui.txttel.setEnabled(True)
        self.ui.txtna.setEnabled(True)
        self.stat = "add"

    def twg_click(self):
        row = self.ui.tableWidget.currentRow()
        self.ui.txthid.setText(self.ui.tableWidget.item(row,0).text())
        self.ui.txtna.setText(self.ui.tableWidget.item(row,1).text())
        self.ui.txttel.setText(self.ui.tableWidget.item(row,2).text())
        self.ui.btnAdd.setEnabled(False)
        self.ui.btnEdit.setEnabled(True)
        self.ui.btnDel.setEnabled(True)
        self.stat = "del"

    def Load(self):
        self.ui.txtna.setText("")
        self.ui.txthid.setText("")
        self.ui.txttel.setText("")
        self.twgLoad_()
        self.ui.btnAdd.setEnabled(True)
        self.ui.txthid.setEnabled(False)
        self.ui.txttel.setEnabled(False)
        self.ui.txtna.setEnabled(False)
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
        sql = "Select c_id,c_name,c_tel from customer"
        data = self.exe_query(sql)
        self.ui.tableWidget.setRowCount(len(data)) 
        for i,row in enumerate(data):    
            for j,val in enumerate(row):       
                self.ui.tableWidget.setItem(i, j,QtWidgets.QTableWidgetItem(str(val)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Mainwindow()
    w.show()
    sys.exit(app.exec_())
