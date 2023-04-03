from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')

#classes with the same names as rules in the design.kv - always the same template for mobile App
class LoginScreen(Screen):
    def sign_up(self):
        print("Sign up button pressed!")
        self.manager.current = "sign_up_screen" #calling SignUpScreen
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
            if uname in users and users[uname]['password'] == pword:
                self.manager.transition.direction = "left"
                self.manager.current = "app_screen"
                self.ids.wrong_login.text = ""
            else:
                self.ids.wrong_login.text = "Incorrect username or password!"  #printing wrong login info
            #cleaning text input windows
            self.ids.username.text = ""
            self.ids.password.text = ""
    #cleaning "wring password" message while proceeding to different pages
    def clear_label(self):
        self.ids.wrong_login.text = ""

        
class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file) #loading json file data   
            users[uname] = { "username": uname, "password": pword, "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")} #adding new user
            print(users)
        with open("users.json", 'w') as file:  #overwriting the file with existing + new users
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"  #calling SignUpScreenSuccess
        
class SignUpScreenSuccess(Screen):
    def go_to_login_screen(self):
        self.manager.transition.direction = "right"  #transition direction of the screen
        self.manager.current = "login_screen"

class AppScreen(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"  #transition direction of the screen
        self.manager.current = "login_screen"
        #cleaning textinput and label when logging out
        self.ids.requested_quote.text = ""
        self.ids.feeling.text = ""

    #method to compare user input with available quotes
    def get_quote(self, feel):
        feel = feel.lower() #turning all the letters to lower case 
        available_feelings = glob.glob("quotes/*txt")  #returning all the txt files names from quotes folder
        available_feelings = [Path(filename).stem for filename in available_feelings]  #Path object plus .stem returns only names from the full files names: happy.txt -> happy
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
               quotes = file.readlines()
            self.ids.requested_quote.text = random.choice(quotes)
        else:
            self.ids.requested_quote.text = "Try another feeling :(" 

class MainApp(App):
    def build(self):
        return RootWidget()

#When you nest the code that’s specific to the script usage of your file under the if __name__ == "__main__" idiom, 
#then you avoid running code that’s irrelevant for imported modules.

if __name__ == "__main__":
    MainApp().run()
