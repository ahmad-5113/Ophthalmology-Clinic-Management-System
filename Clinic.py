import sys
import pyodbc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, Qt, QTime
from PyQt6.QtGui import QFont

# ==================== DATABASE CONNECTION ====================
try:
    # conn = pyodbc.connect(
    #     'DRIVER={ODBC Driver 17 for SQL Server};'
    #     'SERVER=WAHEDNA;'
    #     'DATABASE=OpthalmologyClinicDatabase;'
    #     'Trusted_Connection=yes;'
    # )

    
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=DESKTOP-34G5GVS\SQLEXPRESS;'
        r'DATABASE=OpthalmologyClinicDatabase;'
        r'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    
except Exception as e:
    print(f"Database Error: Connection failed:\n{e}")
    sys.exit()

def execute_query(query, params=None, fetch=False):
    try:
                # Debug: Print the query and parameters
        print(f"DEBUG - Query: {query}")
        print(f"DEBUG - Params: {params}")
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return True
    except Exception as e:
        print(f"Query Error: {e}") 
        return None if fetch else False

# ==================== MAIN WINDOW ====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ophthalmology Clinic Management System")
        self.resize(720, 920)

        self.current_patient_id = None
        self.current_ophth_id = None

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create all widgets
        self.initial_screen = InitialScreen(self)
        self.patient_reg = PatientRegistration(self)
        self.ophth_reg = OphthalmologistRegistration(self)
        self.patient_login = PatientLogin(self)
        self.ophth_login = OphthalmologistLogin(self)
        self.book_appointment = BookAppointment(self)
        self.ophth_appointments = OphthalmologistAppointments(self)
        self.appointment_history = AppointmentHistory(self)
        self.add_record = AddUpdateRecord(self)
        self.patient_view_record = PatientViewRecord(self)
        self.patient_medical_history = PatientMedicalHistory(self)
        self.ophth_medical_history = OphthalmologistMedicalHistory(self)
        self.patient_billing = PatientBilling(self)
        self.ophth_billing = OphthalmologistBilling(self)
        self.patient_feedback = PatientFeedback(self)
        self.ophth_feedback = OphthalmologistFeedback(self)
        
        # Create home screens
        self.patient_home = PatientHome(self)
        self.ophth_home = OphthalmologistHome(self)

        for widget in [
            self.initial_screen, self.patient_reg, self.ophth_reg,
            self.patient_login, self.ophth_login, self.patient_home,
            self.ophth_home, self.book_appointment, self.ophth_appointments,
            self.appointment_history, self.add_record, self.patient_view_record,
            self.patient_medical_history, self.ophth_medical_history,
            self.patient_billing, self.ophth_billing,
            self.patient_feedback, self.ophth_feedback
        ]:
            self.stack.addWidget(widget)

        self.stack.setCurrentWidget(self.initial_screen)

    def go_to(self, widget):
        # Refresh data when navigating to certain screens
        if widget == self.book_appointment:
            widget.load_ophthalmologists()
        elif widget == self.appointment_history:
            widget.load_appointments()
        elif widget == self.ophth_appointments:
            widget.load_appointments()
        elif widget == self.patient_medical_history:
            widget.load_history()
        elif widget == self.ophth_medical_history:
            widget.load_patients()
        elif widget == self.patient_billing:
            widget.load_bills()
        elif widget == self.ophth_billing:
            widget.load_bills()
        elif widget == self.patient_view_record:
            widget.load_record()
        elif widget == self.ophth_feedback:
            widget.load_feedback()
        elif widget == self.patient_feedback:
            widget.load_ophthalmologists()
        elif widget == self.add_record:
            widget.load_patients()
        self.stack.setCurrentWidget(widget)

    def logout(self):
        self.current_patient_id = None
        self.current_ophth_id = None
        self.go_to(self.initial_screen)

# ==================== INITIAL SCREEN ====================
class InitialScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 100, 50, 100)
        layout.setSpacing(30)

        title = QLabel("Ophthalmology Clinic\nManagement System")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Thinner buttons (height reduced from 50 to 40)
        btn_signin = QPushButton("Sign In")
        btn_register = QPushButton("Register")
        for btn in [btn_signin, btn_register]:
            btn.setFixedSize(420, 40)  # Thinner buttons
            btn.setFont(QFont("Arial", 14))
        
        # Reduced spacing between buttons
        layout.addWidget(btn_signin, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(5)  # Closer together
        layout.addWidget(btn_register, alignment=Qt.AlignmentFlag.AlignCenter)

        role_layout = QHBoxLayout()
        role_layout.addStretch()
        self.rb_patient = QRadioButton("Patient")
        self.rb_ophth = QRadioButton("Ophthalmologist")
        self.rb_patient.setChecked(True)
        self.rb_patient.setFont(QFont("Arial", 14))
        self.rb_ophth.setFont(QFont("Arial", 14))
        role_layout.addWidget(self.rb_patient)
        role_layout.addWidget(self.rb_ophth)
        role_layout.addStretch()
        layout.addLayout(role_layout)

        btn_signin.clicked.connect(self.signin)
        btn_register.clicked.connect(self.register)
        self.setLayout(layout)

    def signin(self):
        if self.rb_patient.isChecked():
            self.parent.go_to(self.parent.patient_login)
        else:
            self.parent.go_to(self.parent.ophth_login)

    def register(self):
        if self.rb_patient.isChecked():
            self.parent.go_to(self.parent.patient_reg)
        else:
            self.parent.go_to(self.parent.ophth_reg)

# ==================== PATIENT REGISTRATION ====================
class PatientRegistration(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Patient Registration")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        form = QFormLayout()
        self.name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.dob = QDateEdit()
        self.dob.setDate(QDate(1995, 1, 1))
        self.dob.setCalendarPopup(True)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.EchoMode.Password)

        gender_layout = QHBoxLayout()
        self.gender_group = QButtonGroup()
        male = QRadioButton("Male")
        female = QRadioButton("Female")
        other = QRadioButton("Other")
        male.setChecked(True)
        self.gender_group.addButton(male, 0)
        self.gender_group.addButton(female, 1)
        self.gender_group.addButton(other, 2)
        gender_layout.addWidget(male)
        gender_layout.addWidget(female)
        gender_layout.addWidget(other)

        form.addRow("Name:", self.name)
        form.addRow("Email:", self.email)
        form.addRow("Phone:", self.phone)
        form.addRow("Date of Birth:", self.dob)
        form.addRow("Password:", self.password)
        form.addRow("Confirm Password:", self.confirm)
        form.addRow("Gender:", gender_layout)
        layout.addLayout(form)

        # Thinner buttons closer together
        btn_reg = QPushButton("Register")
        btn_reg.setFixedSize(400, 40)
        btn_reg.clicked.connect(self.register)
        layout.addWidget(btn_reg, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(3)

        btn_back = QPushButton("Back")
        btn_back.setFixedSize(400, 40)
        btn_back.clicked.connect(lambda: parent.go_to(parent.initial_screen))
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def register(self):
        if self.password.text() != self.confirm.text():
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return
        if not self.name.text() or not self.email.text() or not self.password.text():
            QMessageBox.warning(self, "Error", "Please fill all required fields!")
            return
        
        gender = ["Male", "Female", "Other"][self.gender_group.checkedId()]
        
        # Password stored as integer per your schema
        try:
            password_int = int(self.password.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Password must be numeric!")
            return
        
        try:
            phone_int = int(self.phone.text()) if self.phone.text() else 0
        except ValueError:
            QMessageBox.warning(self, "Error", "Phone must be numeric!")
            return
            
        result = execute_query(
            "INSERT INTO Patient(name, gender, date_of_birth, email, phonenumber, password) VALUES(?,?,?,?,?,?)",
            (self.name.text(), gender, self.dob.date().toString("yyyy-MM-dd"),
             self.email.text(), phone_int, password_int))
        
        if result:
            QMessageBox.information(self, "Success", "Registration successful!")
            self.parent.go_to(self.parent.initial_screen)

# ==================== OPHTHALMOLOGIST REGISTRATION ====================
class OphthalmologistRegistration(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Ophthalmologist Registration")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        form = QFormLayout()
        self.name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.clinic = QLineEdit()
        self.address = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Name:", self.name)
        form.addRow("Email:", self.email)
        form.addRow("Phone:", self.phone)
        form.addRow("Clinic Name:", self.clinic)
        form.addRow("Clinic Address:", self.address)
        form.addRow("Password:", self.password)
        layout.addLayout(form)

        btn_reg = QPushButton("Register")
        btn_reg.setFixedSize(400, 40)
        btn_reg.clicked.connect(self.register)
        layout.addWidget(btn_reg, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(3)

        btn_back = QPushButton("Back")
        btn_back.setFixedSize(400, 40)
        btn_back.clicked.connect(lambda: parent.go_to(parent.initial_screen))
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def register(self):
        if not self.name.text() or not self.email.text() or not self.password.text():
            QMessageBox.warning(self, "Error", "Please fill all required fields!")
            return
            
        try:
            password_int = int(self.password.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Password must be numeric!")
            return
        
        try:
            phone_int = int(self.phone.text()) if self.phone.text() else 0
        except ValueError:
            QMessageBox.warning(self, "Error", "Phone must be numeric!")
            return
            
        result = execute_query(
            "INSERT INTO Ophthalmologist(name, email, phonenumber, clinicname, clinicaddress, password) VALUES(?,?,?,?,?,?)",
            (self.name.text(), self.email.text(), phone_int,
             self.clinic.text(), self.address.text(), password_int))
        
        if result:
            QMessageBox.information(self, "Success", "Ophthalmologist registered!")
            self.parent.go_to(self.parent.initial_screen)

# ==================== PATIENT LOGIN ====================
class PatientLogin(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        title = QLabel("Patient Login")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.email = QLineEdit()
        self.email.setFixedWidth(400)
        self.email.setPlaceholderText("Enter your email")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedWidth(400)
        self.password.setPlaceholderText("Enter your password (numeric)")

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignCenter)

        # Thinner buttons closer together
        btn_login = QPushButton("Sign In")
        btn_login.setFixedSize(400, 40)
        btn_login.clicked.connect(self.login)
        layout.addWidget(btn_login, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(5)

        btn_back = QPushButton("Back")
        btn_back.setFixedSize(400, 40)
        btn_back.clicked.connect(lambda: parent.go_to(parent.initial_screen))
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def login(self):
        try:
            password_int = int(self.password.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Password must be numeric!")
            return
            
        rows = execute_query(
            "SELECT patient_id FROM Patient WHERE RTRIM(email)=? AND password=?", 
            (self.email.text(), password_int), fetch=True)
        if rows:
            self.parent.current_patient_id = rows[0][0]
            self.parent.go_to(self.parent.patient_home)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")

# ==================== OPHTHALMOLOGIST LOGIN ====================
class OphthalmologistLogin(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        title = QLabel("Ophthalmologist Login")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.email = QLineEdit()
        self.email.setFixedWidth(400)
        self.email.setPlaceholderText("Enter your email")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedWidth(400)
        self.password.setPlaceholderText("Enter your password (numeric)")

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_login = QPushButton("Sign In")
        btn_login.setFixedSize(400, 40)
        btn_login.clicked.connect(self.login)
        layout.addWidget(btn_login, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(5)

        btn_back = QPushButton("Back")
        btn_back.setFixedSize(400, 40)
        btn_back.clicked.connect(lambda: parent.go_to(parent.initial_screen))
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def login(self):
        try:
            password_int = int(self.password.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Password must be numeric!")
            return
            
        rows = execute_query(
            "SELECT ophthalmologist_id FROM Ophthalmologist WHERE RTRIM(email)=? AND password=?", 
            (self.email.text(), password_int), fetch=True)
        
        # Add this debug line too
        print(f"Query returned: {rows}")

        if rows:
            self.parent.current_ophth_id = rows[0][0]
            self.parent.go_to(self.parent.ophth_home)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")

# ==================== PATIENT HOME ====================
class PatientHome(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        title = QLabel("Welcome Patient")
        title.setFont(QFont("Arial", 20))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        buttons = [
            ("Book Appointment", parent.book_appointment),
            ("Appointment History", parent.appointment_history),
            ("View Medical Record", parent.patient_view_record),
            ("Medical History", parent.patient_medical_history),
            ("View Bills", parent.patient_billing),
            ("Give Feedback", parent.patient_feedback),
        ]

        for text, screen in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(500, 45)
            btn.setFont(QFont("Arial", 14))
            btn.clicked.connect(lambda checked, s=screen: parent.go_to(s))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        logout = QPushButton("Logout")
        logout.setFixedSize(500, 45)
        logout.clicked.connect(parent.logout)
        layout.addWidget(logout, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

# ==================== OPHTHALMOLOGIST HOME ====================
class OphthalmologistHome(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        title = QLabel("Welcome Ophthalmologist")
        title.setFont(QFont("Arial", 20))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        buttons = [
            ("Upcoming Appointments", parent.ophth_appointments),
            ("Add/Update Record", parent.add_record),
            ("View Medical History", parent.ophth_medical_history),
            ("Billing", parent.ophth_billing),
            ("View Feedback", parent.ophth_feedback),
        ]

        for text, screen in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(500, 45)
            btn.setFont(QFont("Arial", 14))
            btn.clicked.connect(lambda checked, s=screen: parent.go_to(s))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        logout = QPushButton("Logout")
        logout.setFixedSize(500, 45)
        logout.clicked.connect(parent.logout)
        layout.addWidget(logout, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

# ==================== BOOK APPOINTMENT ====================
class BookAppointment(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ophth_ids = []
        layout = QVBoxLayout()
        layout.addStretch()
        
        title = QLabel("Book Appointment")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Changed from "Doctor:" to "Ophthalmologist:"
        layout.addWidget(QLabel("Ophthalmologist:"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.ophth_combo = QComboBox()
        self.ophth_combo.setFixedWidth(400)
        layout.addWidget(self.ophth_combo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(QLabel("Date:"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate.currentDate())
        layout.addWidget(self.calendar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(QLabel("Time:"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.time = QComboBox()
        self.time.addItems(["10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"])
        self.time.setFixedWidth(400)
        layout.addWidget(self.time, alignment=Qt.AlignmentFlag.AlignCenter)
        
        book_btn = QPushButton("Book Now")
        book_btn.setFixedSize(400, 40)
        book_btn.clicked.connect(self.book_appointment)
        layout.addWidget(book_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(5)
        
        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.patient_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
    
    def load_ophthalmologists(self):
        self.ophth_combo.clear()
        self.ophth_ids = []
        rows = execute_query("SELECT ophthalmologist_id, RTRIM(name), RTRIM(clinicname) FROM Ophthalmologist", fetch=True)
        if rows:
            for row in rows:
                self.ophth_ids.append(row[0])
                self.ophth_combo.addItem(f"{row[1]} - {row[2]}")
    
    def book_appointment(self):
        if not self.ophth_ids:
            QMessageBox.warning(self, "Error", "No ophthalmologist selected!")
            return
            
        ophth_id = self.ophth_ids[self.ophth_combo.currentIndex()]
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        
        # Convert time to datetime format
        time_text = self.time.currentText()
        time_map = {
            "10:00 AM": "10:00:00", "11:00 AM": "11:00:00", "12:00 PM": "12:00:00",
            "01:00 PM": "13:00:00", "02:00 PM": "14:00:00", "03:00 PM": "15:00:00",
            "04:00 PM": "16:00:00", "05:00 PM": "17:00:00"
        }
        time_value = f"{date} {time_map.get(time_text, '10:00:00')}"
        
        result = execute_query(
            "INSERT INTO Appointment(patient_id, ophthalmologist_id, appointment_date, appointment_time, appointment_status) VALUES(?,?,?,?,?)",
            (self.parent.current_patient_id, ophth_id, date, time_value, 0))
        
        if result:
            QMessageBox.information(self, "Success", "Appointment booked successfully!")
            self.parent.go_to(self.parent.patient_home)

# ==================== APPOINTMENT HISTORY ====================
class AppointmentHistory(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.appointment_ids = []
        layout = QVBoxLayout()
        
        title = QLabel("Appointment History")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        # Changed "Doctor" to "Ophthalmologist"
        self.table.setHorizontalHeaderLabels(["Date", "Time", "Ophthalmologist", "Status", "Action"])
        self.table.setFixedSize(700, 400)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(5)
        
        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.patient_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
    
    def load_appointments(self):
        self.table.setRowCount(0)
        self.appointment_ids = []
        
        rows = execute_query("""
            SELECT a.appointment_id, a.appointment_date, a.appointment_time, 
                   RTRIM(o.name), a.appointment_status
            FROM Appointment a
            JOIN Ophthalmologist o ON a.ophthalmologist_id = o.ophthalmologist_id
            WHERE a.patient_id = ?
            ORDER BY a.appointment_date DESC
        """, (self.parent.current_patient_id,), fetch=True)
        
        if rows:
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                self.appointment_ids.append(row[0])
                self.table.setItem(i, 0, QTableWidgetItem(str(row[1])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row[2].strftime("%H:%M") if row[2] else "")))
                self.table.setItem(i, 2, QTableWidgetItem(str(row[3])))
               
                status_value = row[4]     # status = "Confirmed" if row[4] else "Pending"
                if status_value == 2:
                    status = "Rejected"
                elif status_value == 1:
                    status = "Approved"
                else:
                    status = "Pending"
                
                self.table.setItem(i, 3, QTableWidgetItem(status))
                
                # Cancel button
                cancel_btn = QPushButton("Cancel")
                cancel_btn.clicked.connect(lambda checked, aid=row[0]: self.cancel_appointment(aid))
                self.table.setCellWidget(i, 4, cancel_btn)
    
    def cancel_appointment(self, appointment_id):
        reply = QMessageBox.question(self, "Confirm", "Cancel this appointment?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            execute_query("DELETE FROM Appointment WHERE appointment_id = ?", (appointment_id,))
            self.load_appointments()

# ==================== PATIENT VIEW RECORD ====================
class PatientViewRecord(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("Your Latest Medical Record")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form = QFormLayout()
        
        self.date_label = QLineEdit()
        self.date_label.setReadOnly(True)
        
        # Changed from "Doctor:" to "Ophthalmologist:"
        self.ophth_label = QLineEdit()
        self.ophth_label.setReadOnly(True)
        
        self.diagnosis = QLineEdit()
        self.diagnosis.setReadOnly(True)
        
        self.treatment = QTextEdit()
        self.treatment.setFixedHeight(120)
        self.treatment.setReadOnly(True)
        
        self.prescription = QTextEdit()
        self.prescription.setFixedHeight(120)
        self.prescription.setReadOnly(True)
        
        form.addRow("Date:", self.date_label)
        form.addRow("Ophthalmologist:", self.ophth_label)
        form.addRow("Diagnosis:", self.diagnosis)
        form.addRow("Treatment:", self.treatment)
        form.addRow("Prescription:", self.prescription)
        layout.addLayout(form)
        
        layout.addSpacing(5)
        
        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.patient_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
    
    def load_record(self):
        rows = execute_query("""
            SELECT TOP 1 pr.record_date, RTRIM(o.name), RTRIM(pr.diagnosis), 
                   pr.treatment_details, RTRIM(pr.prescription)
            FROM Patient_Record pr
            JOIN Ophthalmologist o ON pr.ophthalmologist_id = o.ophthalmologist_id
            WHERE pr.patient_id = ?
            ORDER BY pr.record_date DESC
        """, (self.parent.current_patient_id,), fetch=True)
        
        if rows:
            row = rows[0]
            self.date_label.setText(str(row[0]))
            self.ophth_label.setText(str(row[1]))
            self.diagnosis.setText(str(row[2]) if row[2] else "")
            self.treatment.setText(str(row[3]) if row[3] else "")
            self.prescription.setText(str(row[4]) if row[4] else "")
        else:
            self.date_label.setText("")
            self.ophth_label.setText("")
            self.diagnosis.setText("No records found")
            self.treatment.setText("")
            self.prescription.setText("")

# ==================== PATIENT MEDICAL HISTORY ====================
class PatientMedicalHistory(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        
        title = QLabel("Medical History")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Ophthalmologist", "Diagnosis", "Treatment", "Prescription"])
        self.table.setFixedSize(750, 400)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(5)
        
        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.patient_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
    
    def load_history(self):
        self.table.setRowCount(0)
        
        rows = execute_query("""
            SELECT pr.record_date, RTRIM(o.name), RTRIM(pr.diagnosis), 
                   pr.treatment_details, RTRIM(pr.prescription)
            FROM Patient_Record pr
            JOIN Ophthalmologist o ON pr.ophthalmologist_id = o.ophthalmologist_id
            WHERE pr.patient_id = ?
            ORDER BY pr.record_date DESC
        """, (self.parent.current_patient_id,), fetch=True)
        
        if rows:
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
                self.table.setItem(i, 2, QTableWidgetItem(str(row[2]) if row[2] else ""))
                self.table.setItem(i, 3, QTableWidgetItem(str(row[3]) if row[3] else ""))
                self.table.setItem(i, 4, QTableWidgetItem(str(row[4]) if row[4] else ""))

# ==================== OPHTHALMOLOGIST APPOINTMENTS ====================
class OphthalmologistAppointments(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.appointment_ids = []
        layout = QVBoxLayout()
        
        title = QLabel("Upcoming Appointments")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Patient", "Date", "Time", "Status", "Action"])
        self.table.setFixedSize(700, 400)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(5)
        
        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.ophth_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        self.setLayout(layout)

    def load_appointments(self):
        self.table.setRowCount(0)
        self.appointment_ids = []
        
        rows = execute_query("""
            SELECT a.appointment_id, RTRIM(p.name), a.appointment_date, 
                   a.appointment_time, a.appointment_status
            FROM Appointment a
            JOIN Patient p ON a.patient_id = p.patient_id
            WHERE a.ophthalmologist_id = ?
            ORDER BY a.appointment_date ASC
        """, (self.parent.current_ophth_id,), fetch=True)
        
        if not rows:
            return
        
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            appointment_id = row[0]
            status_value = row[4]

            self.table.setItem(i, 0, QTableWidgetItem(str(row[1])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row[2])))
            self.table.setItem(i, 2, QTableWidgetItem(row[3].strftime("%H:%M") if row[3] else ""))

            if status_value == 2:
                status = "Rejected"
            elif status_value == 0:
                status = "Pending"
            else:
                status = "Approved"

            self.table.setItem(i, 3, QTableWidgetItem(status))

            if status_value == 0:
                action_widget = QWidget()
                layout_buttons = QHBoxLayout(action_widget)
                layout_buttons.setContentsMargins(0, 0, 0, 0)
                layout_buttons.setSpacing(5)

                approve_btn = QPushButton("Approve")
                reject_btn = QPushButton("Reject")
            
                approve_btn.clicked.connect(
                    lambda checked, aid=appointment_id: self.approve_appointment(aid)
                )
                reject_btn.clicked.connect(
                    lambda checked, aid=appointment_id: self.reject_appointment(aid)
                )

                layout_buttons.addWidget(approve_btn)
                layout_buttons.addWidget(reject_btn)
                self.table.setCellWidget(i, 4, action_widget)
            else:
                self.table.setItem(i, 4, QTableWidgetItem(status))

    
    def approve_appointment(self, appointment_id):
        execute_query(
            "UPDATE Appointment SET appointment_status = 1 WHERE appointment_id = ?",
            (appointment_id,)
        )
        self.load_appointments()

    def reject_appointment(self, appointment_id):
        execute_query(
            "UPDATE Appointment SET appointment_status = 2 WHERE appointment_id = ?",
            (appointment_id,)
        )
        self.load_appointments()


# ==================== ADD/UPDATE RECORD ====================
class AddUpdateRecord(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.patient_ids = []
        self.appointment_ids = []
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        
        title = QLabel("Add/Update Patient Record")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form = QFormLayout()
        
        self.patient_combo = QComboBox()
        self.patient_combo.setFixedWidth(400)
        self.patient_combo.currentIndexChanged.connect(self.load_appointments_for_patient)
        
        self.appointment_combo = QComboBox()
        self.appointment_combo.setFixedWidth(400)
        
        self.diagnosis = QLineEdit()
        self.diagnosis.setFixedWidth(400)
        
        self.treatment = QTextEdit()
        self.treatment.setFixedHeight(100)
        
        self.prescription = QTextEdit()
        self.prescription.setFixedHeight(100)
        
        form.addRow("Patient:", self.patient_combo)
        form.addRow("Appointment:", self.appointment_combo)
        form.addRow("Diagnosis:", self.diagnosis)
        form.addRow("Treatment Plan:", self.treatment)
        form.addRow("Prescription:", self.prescription)
        layout.addLayout(form)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save Record")
        save_btn.setFixedSize(180, 40)
        save_btn.clicked.connect(self.save_record)
        btn_layout.addWidget(save_btn)
        
        back = QPushButton("Back")
        back.setFixedSize(180, 40)
        back.clicked.connect(lambda: parent.go_to(parent.ophth_home))
        btn_layout.addWidget(back)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def load_patients(self):
        self.patient_combo.clear()
        self.patient_ids = []
        
        # Get patients who have appointments with this ophthalmologist
        rows = execute_query("""
            SELECT DISTINCT p.patient_id, RTRIM(p.name)
            FROM Patient p
            JOIN Appointment a ON p.patient_id = a.patient_id
            WHERE a.ophthalmologist_id = ?
        """, (self.parent.current_ophth_id,), fetch=True)
        
        if rows:
            for row in rows:
                self.patient_ids.append(row[0])
                self.patient_combo.addItem(str(row[1]))
    
    def load_appointments_for_patient(self):
        self.appointment_combo.clear()
        self.appointment_ids = []
        
        if not self.patient_ids or self.patient_combo.currentIndex() < 0:
            return
            
        patient_id = self.patient_ids[self.patient_combo.currentIndex()]
        
        rows = execute_query("""
            SELECT appointment_id, appointment_date
            FROM Appointment
            WHERE patient_id = ? AND ophthalmologist_id = ?
            ORDER BY appointment_date DESC
        """, (patient_id, self.parent.current_ophth_id), fetch=True)
        
        if rows:
            for row in rows:
                self.appointment_ids.append(row[0])
                self.appointment_combo.addItem(str(row[1]))
    
    def save_record(self):
        if not self.patient_ids or not self.appointment_ids:
            QMessageBox.warning(self, "Error", "Please select patient and appointment!")
            return
            
        patient_id = self.patient_ids[self.patient_combo.currentIndex()]
        appointment_id = self.appointment_ids[self.appointment_combo.currentIndex()]
        
        result = execute_query("""
            INSERT INTO Patient_Record(patient_id, ophthalmologist_id, appointment_id, 
                                       record_date, diagnosis, prescription, treatment_details)
            VALUES(?,?,?,GETDATE(),?,?,?)
        """, (patient_id, self.parent.current_ophth_id, appointment_id,
              self.diagnosis.text(), self.prescription.toPlainText(), self.treatment.toPlainText()))
        
        if result:
            QMessageBox.information(self, "Success", "Record saved successfully!")
            self.diagnosis.clear()
            self.treatment.clear()
            self.prescription.clear()

# ==================== OPHTHALMOLOGIST MEDICAL HISTORY ====================
class OphthalmologistMedicalHistory(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.patient_ids = []
        layout = QVBoxLayout()
        
        title = QLabel("Patient Medical History")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(QLabel("Select Patient:"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.patient_combo = QComboBox()
        self.patient_combo.setFixedWidth(400)
        self.patient_combo.currentIndexChanged.connect(self.load_history)
        layout.addWidget(self.patient_combo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Diagnosis", "Treatment", "Prescription"])
        self.table.setFixedSize(700, 400)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(5)
        
        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.ophth_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
    
    def load_patients(self):
        self.patient_combo.clear()
        self.patient_ids = []
        
        rows = execute_query("""
            SELECT DISTINCT p.patient_id, RTRIM(p.name)
            FROM Patient p
            JOIN Patient_Record pr ON p.patient_id = pr.patient_id
            WHERE pr.ophthalmologist_id = ?
        """, (self.parent.current_ophth_id,), fetch=True)
        
        if rows:
            for row in rows:
                self.patient_ids.append(row[0])
                self.patient_combo.addItem(str(row[1]))
    
    def load_history(self):
        self.table.setRowCount(0)
        
        if not self.patient_ids or self.patient_combo.currentIndex() < 0:
            return
            
        patient_id = self.patient_ids[self.patient_combo.currentIndex()]
        
        rows = execute_query("""
            SELECT record_date, RTRIM(diagnosis), treatment_details, RTRIM(prescription)
            FROM Patient_Record
            WHERE patient_id = ? AND ophthalmologist_id = ?
            ORDER BY record_date DESC
        """, (patient_id, self.parent.current_ophth_id), fetch=True)
        
        if rows:
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row[1]) if row[1] else ""))
                self.table.setItem(i, 2, QTableWidgetItem(str(row[2]) if row[2] else ""))
                self.table.setItem(i, 3, QTableWidgetItem(str(row[3]) if row[3] else ""))

# ==================== PATIENT BILLING ====================
class PatientBilling(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        
        title = QLabel("Your Bills")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        # Changed "Doctor" to "Ophthalmologist"
        self.table.setHorizontalHeaderLabels(["Date", "Ophthalmologist", "Amount", "Status", "Action"])
        self.table.setFixedSize(700, 400)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(5)
        
        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.patient_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
    
    def load_bills(self):
        self.table.setRowCount(0)
        
        rows = execute_query("""
            SELECT b.bill_id, b.payment_date, RTRIM(o.name), b.amount, b.payment_status
            FROM Bill b
            JOIN Appointment a ON b.appointment_id = a.appointment_id
            JOIN Ophthalmologist o ON a.ophthalmologist_id = o.ophthalmologist_id
            WHERE b.patient_id = ?
            ORDER BY b.payment_date DESC
        """, (self.parent.current_patient_id,), fetch=True)
        
        if rows:
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row[1])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row[2])))
                self.table.setItem(i, 2, QTableWidgetItem(f"${row[3]:.2f}"))
                status = "Paid" if row[4] else "Unpaid"
                self.table.setItem(i, 3, QTableWidgetItem(status))
                
                if not row[4]:
                    pay_btn = QPushButton("Pay Now")
                    pay_btn.clicked.connect(lambda checked, bid=row[0]: self.pay_bill(bid))
                    self.table.setCellWidget(i, 4, pay_btn)
                else:
                    self.table.setItem(i, 4, QTableWidgetItem("Completed"))
    
    def pay_bill(self, bill_id):
        execute_query("UPDATE Bill SET payment_status = 1 WHERE bill_id = ?", (bill_id,))
        QMessageBox.information(self, "Success", "Payment successful!")
        self.load_bills()

# ==================== OPHTHALMOLOGIST BILLING ====================
class OphthalmologistBilling(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        
        title = QLabel("Patient Billing")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add new bill section
        add_layout = QHBoxLayout()
        self.patient_combo = QComboBox()
        self.patient_combo.setFixedWidth(200)
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.amount_input.setFixedWidth(100)
        add_bill_btn = QPushButton("Create Bill")
        add_bill_btn.clicked.connect(self.create_bill)
        
        add_layout.addWidget(QLabel("Patient:"))
        add_layout.addWidget(self.patient_combo)
        add_layout.addWidget(self.amount_input)
        add_layout.addWidget(add_bill_btn)
        layout.addLayout(add_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Patient", "Date", "Amount", "Status"])
        self.table.setFixedSize(700, 350)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(5)
        
        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.ophth_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
        
        self.patient_ids = []
        self.appointment_map = {}
    
    def load_bills(self):
        # Load patients with appointments
        self.patient_combo.clear()
        self.patient_ids = []
        self.appointment_map = {}
        
        rows = execute_query("""
            SELECT DISTINCT p.patient_id, RTRIM(p.name), a.appointment_id
            FROM Patient p
            JOIN Appointment a ON p.patient_id = a.patient_id
            WHERE a.ophthalmologist_id = ?
        """, (self.parent.current_ophth_id,), fetch=True)
        
        if rows:
            for row in rows:
                if row[0] not in self.patient_ids:
                    self.patient_ids.append(row[0])
                    self.patient_combo.addItem(str(row[1]))
                    self.appointment_map[row[0]] = row[2]
        
        # Load existing bills
        self.table.setRowCount(0)
        
        bill_rows = execute_query("""
            SELECT RTRIM(p.name), b.payment_date, b.amount, b.payment_status
            FROM Bill b
            JOIN Patient p ON b.patient_id = p.patient_id
            JOIN Appointment a ON b.appointment_id = a.appointment_id
            WHERE a.ophthalmologist_id = ?
            ORDER BY b.payment_date DESC
        """, (self.parent.current_ophth_id,), fetch=True)
        
        if bill_rows:
            self.table.setRowCount(len(bill_rows))
            for i, row in enumerate(bill_rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
                self.table.setItem(i, 2, QTableWidgetItem(f"${row[2]:.2f}"))
                status = "Paid" if row[3] else "Unpaid"
                self.table.setItem(i, 3, QTableWidgetItem(status))
    
    def create_bill(self):
        if not self.patient_ids:
            QMessageBox.warning(self, "Error", "No patients available!")
            return
            
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount!")
            return
        
        patient_id = self.patient_ids[self.patient_combo.currentIndex()]
        appointment_id = self.appointment_map.get(patient_id)
        
        if not appointment_id:
            QMessageBox.warning(self, "Error", "No appointment found for this patient!")
            return
        
        result = execute_query("""
            INSERT INTO Bill(patient_id, appointment_id, amount, payment_status, payment_date)
            VALUES(?,?,?,0,GETDATE())
        """, (patient_id, appointment_id, amount))
        
        if result:
            QMessageBox.information(self, "Success", "Bill created successfully!")
            self.amount_input.clear()
            self.load_bills()

# ==================== PATIENT FEEDBACK ====================
class PatientFeedback(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ophth_ids = []
        layout = QVBoxLayout()
        layout.addStretch()
        
        title = QLabel("Give Feedback")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("Ophthalmologist:"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.ophth_combo = QComboBox()
        self.ophth_combo.setFixedWidth(400)
        layout.addWidget(self.ophth_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("Rating (1-5):"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.rating = QComboBox()
        self.rating.addItems(["5 - Excellent", "4 - Good", "3 - Average", "2 - Poor", "1 - Very Poor"])
        self.rating.setFixedWidth(400)
        layout.addWidget(self.rating, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("Your Feedback:"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.feedback_text = QTextEdit()
        self.feedback_text.setFixedSize(400, 150)
        layout.addWidget(self.feedback_text, alignment=Qt.AlignmentFlag.AlignCenter)

        submit_btn = QPushButton("Submit")
        submit_btn.setFixedSize(400, 40)
        submit_btn.clicked.connect(self.submit_feedback)
        layout.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.patient_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def load_ophthalmologists(self):
        self.ophth_combo.clear()
        self.ophth_ids = []

        rows = execute_query("""
            SELECT DISTINCT o.ophthalmologist_id, RTRIM(o.name)
            FROM Ophthalmologist o
            JOIN Appointment a ON o.ophthalmologist_id = a.ophthalmologist_id
            WHERE a.patient_id = ?
        """, (self.parent.current_patient_id,), fetch=True)

        if rows:
            for row in rows:
                self.ophth_ids.append(row[0])
                self.ophth_combo.addItem(str(row[1]))

    def submit_feedback(self):
        if not self.ophth_ids:
            QMessageBox.warning(self, "Error", "No ophthalmologist selected!")
            return

        ophth_id = self.ophth_ids[self.ophth_combo.currentIndex()]
        rating = 5 - self.rating.currentIndex()
        comments = self.feedback_text.toPlainText()

        result = execute_query("""
            INSERT INTO Feedback(patient_id, ophthalmologist_id, rating, comments, feedback_date)
            VALUES(?,?,?,?,GETDATE())
        """, (self.parent.current_patient_id, ophth_id, rating, comments))

        if result:
            QMessageBox.information(self, "Success", "Feedback submitted successfully!")
            self.feedback_text.clear()
            self.parent.go_to(self.parent.patient_home)

# ==================== OPHTHALMOLOGIST FEEDBACK ====================
class OphthalmologistFeedback(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        title = QLabel("Patient Feedback")
        title.setFont(QFont("Arial", 18))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Patient", "Rating", "Comments", "Date"])
        self.table.setFixedSize(700, 400)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)

        back = QPushButton("Back")
        back.setFixedSize(400, 40)
        back.clicked.connect(lambda: parent.go_to(parent.ophth_home))
        layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        self.setLayout(layout)

    def load_feedback(self):
        self.table.setRowCount(0)

        rows = execute_query("""
            SELECT RTRIM(p.name), f.rating, f.comments, f.feedback_date
            FROM Feedback f
            JOIN Patient p ON f.patient_id = p.patient_id
            WHERE f.ophthalmologist_id = ?
            ORDER BY f.feedback_date DESC
        """, (self.parent.current_ophth_id,), fetch=True)

        if rows:
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(i, 1, QTableWidgetItem(f"{row[1]}/5"))
                self.table.setItem(i, 2, QTableWidgetItem(str(row[2]) if row[2] else ""))
                self.table.setItem(i, 3, QTableWidgetItem(str(row[3])))


# ==================== RUN THE APPLICATION ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())