from main import AuthWindow, QTimer
from modules.ui_login_function import UILoginFunctions
import sqlite3
from email_validator import validate_email, EmailNotValidError

class Auth_system(AuthWindow):

    def check_email(self):
        username = self.ui.Forget_Username.text()
        email = self.ui.Forget_Email.text()
        if len(username) == 0 or len(email) == 0:
            self.ui.Forget_Status.setText(f"Please input all fields.")
            Auth_system.forget_fail(self)
        else:
            try:
                # E-mail
                valid = validate_email(email)
                email = valid.email
                # SQL
                conn = sqlite3.connect("bin/Data/Accounts.db")
                cur = conn.cursor()
                query = 'SELECT email FROM login_info WHERE username =\'' + username + "\'"
                cur.execute(query)
                try:
                    result_pass = cur.fetchone()[0]
                    if result_pass == email:
                        self.ui.Forget_Status.setText(f"Sending to email {email}")
                        self.ui.Forget_Status.setStyleSheet("#Forget_Status { color: #50fa7b }")
                        self.ui.Forget_Username.setStyleSheet("#Forget_Username:focus { border: 2px solid #50fa7b; }")
                        self.ui.Forget_Email.setStyleSheet("#Forget_Email:focus { border: 2px solid #50fa7b; }")
                    else:
                        self.ui.Forget_Status.setText(f"Invalid username or e-mail")
                        Auth_system.forget_fail(self)
                except Exception as e:
                    print(e)
                    self.ui.Forget_Status.setText(f"Invalid username or e-mail")
                    Auth_system.forget_fail(self)

            except EmailNotValidError as e:
                # email is not valid, exception message is human-readable
                Auth_system.forget_fail(self)
                self.ui.Forget_Status.setText(str(e))

    def check_login(self, guest):
        if guest:
            self.ui.Login_Status.setText(f"Welcome Guest !")
            self.ui.Login_Status.setStyleSheet("#Login_Status { color: #50fa7b }")
            QTimer.singleShot(1200, lambda: self.open_main())
        if not guest:
            username = self.ui.username.text()
            password = self.ui.password.text()

            if len(username) == 0 or len(password) == 0:
                self.ui.Login_Status.setText("Please input all fields.")
                Auth_system.login_fail(self)
            else:
                conn = sqlite3.connect("bin/Data/Accounts.db")
                cur = conn.cursor()
                query = 'SELECT password FROM login_info WHERE username =\'' + username + "\'"
                cur.execute(query)
                try:
                    result_pass = cur.fetchone()[0]
                    if result_pass == password:
                        self.ui.Login_Status.setText(f"Welcome {username} !")
                        self.ui.Login_Status.setStyleSheet("#Login_Status { color: #50fa7b }")
                        self.ui.username.setStyleSheet("#username:focus { border: 2px solid #50fa7b; }")
                        self.ui.password.setStyleSheet("#password:focus { border: 2px solid #50fa7b; }")
                        QTimer.singleShot(1200, lambda: self.open_main())
                    else:
                        self.ui.Login_Status.setText("Invalid username or password")
                        Auth_system.login_fail(self)
                except Exception as e:
                    print(e)
                    self.ui.Login_Status.setText("Invalid username or password")
                    Auth_system.login_fail(self)

    def check_register(self):
        username = self.ui.Reg_username.text()
        password = self.ui.Reg_password.text()
        con_Password = self.ui.Reg_password_2.text()
        email = self.ui.Reg_email.text()

        if len(username) == 0 or len(password) == 0 or len(con_Password) == 0 or len(email) == 0:
            self.ui.Reg_Status.setText("Please fill in all inputs.")
            Auth_system.regis_fail(self)
        elif password != con_Password:
            self.ui.Reg_Status.setText("Passwords do not match.")
            Auth_system.regis_fail(self)
        else:
            conn = sqlite3.connect("bin/Data/Accounts.db")
            cur = conn.cursor()
            user_info = [username, password, email]
            try:
                cur.execute('INSERT INTO login_info (username, password, email) VALUES (?,?,?)', user_info)
                conn.commit()
                conn.close()
                self.ui.Reg_username.clear()
                self.ui.Reg_password.clear()
                self.ui.Reg_password_2.clear()
                self.ui.Reg_email.clear()
                self.ui.Reg_Status.setStyleSheet("#Reg_Status { color: #50fa7b }")
                self.ui.Reg_username.setStyleSheet("#Reg_username:focus { border: 2px solid rgb(91, 101, 124); }")
                self.ui.Reg_password.setStyleSheet("#Reg_password:focus { border: 2px solid rgb(91, 101, 124); }")
                self.ui.Reg_password_2.setStyleSheet("#Reg_password_2:focus { border: 2px solid rgb(91, 101, 124); }")
                self.ui.Reg_email.setStyleSheet("#Reg_email:focus { border: 2px solid rgb(91, 101, 124); }")
                self.ui.Reg_Status.setText("Register Complete !")
            except Exception as e:
                print(e)
                self.ui.Reg_Status.setText("This username is already registered in the database.")
                Auth_system.regis_fail(self)

    def regis_fail(self):
        self.ui.Reg_Status.setStyleSheet("#Reg_Status { color: #ff5555 }")
        self.ui.Reg_username.setStyleSheet("#Reg_username:focus { border: 2px solid #ff5555; }")
        self.ui.Reg_password.setStyleSheet("#Reg_password:focus { border: 2px solid #ff5555; }")
        self.ui.Reg_password_2.setStyleSheet("#Reg_password_2:focus { border: 2px solid #ff5555; }")
        self.ui.Reg_email.setStyleSheet("#Reg_email:focus { border: 2px solid #ff5555; }")
        UILoginFunctions.shake_window(self)

    def login_fail(self):
        self.ui.Login_Status.setStyleSheet("#Login_Status { color: #ff5555 }")
        self.ui.username.setStyleSheet("#username:focus { border: 2px solid #ff5555; }")
        self.ui.password.setStyleSheet("#password:focus { border: 2px solid #ff5555; }")
        UILoginFunctions.shake_window(self)

    def forget_fail(self):
        self.ui.Forget_Status.setStyleSheet("#Forget_Status { color: #ff5555 }")
        self.ui.Forget_Username.setStyleSheet("#Forget_Username:focus { border: 2px solid #ff5555; }")
        self.ui.Forget_Email.setStyleSheet("#Forget_Email:focus { border: 2px solid #ff5555; }")
        UILoginFunctions.shake_window(self)