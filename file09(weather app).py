import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("enter city name: ", self)
        self.setWindowIcon(QIcon("folder02/weather app icon.png"))
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("get weather", self)
        self.temperature_label = QLabel("",self)#num lock on then alt + 0176 gives that degreee sign 
        self.emoji_label = QLabel("",self)
        self.description_label = QLabel("",self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("best wather app in the world mate (made by a master)(btw weather is mispronounced cuz its wabi sabi)")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temprature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QWidget{
                background-color: #6A0DAD;
            }
            QLabel,QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 45px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size:35px;
                font-weight: bold;
            }
            QLabel#temprature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size:100px;
                font-family; Segoe UI emoji;
            }
            QLabel#descryption_label{
                font-size: 70px;
            }
        
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        
    def get_weather(self):
        api_key = "2fd17f1979692b6744a34e9ed52fa2d5"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        #print("Thou dost receive the tidings of the heavens.")

        try:
            response = requests.get(url)
            response.raise_for_status()#raise exeption if http error
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("bad af request:\ncheck yo input BOY")
                case 401:
                    self.display_error("unauthorised:\ncheck api key")
                case 403:
                    self.display_error("hault mortal:\nyou are stepping out of your domain")
                case 404:
                    self.display_error("SERIOUSLY брат: \nthere ain't no city like that cracka")
                case 500:
                    self.display_error("internal server error\nnot ma fault gng chill out and try later")
                case 502:
                    self.display_error("bad gateway or smth:\ninvalid response from server dawg that shi be trippin")
                case 503:
                    self.display_error("service unavailable:\nserver is down ")
                case 504:
                    self.display_error("Gateway timeout:\nNO response from server")
                case _:
                    self.display_error(f"HttP error occured:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("connection error:\ncheck yo innernet nga")
        except requests.exceptions.Timeout:
            self.display_error("timeout error:\nts shi timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("too many redirects:\n check url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"request erro:r\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 40px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    def display_weather(self,data):
        temperature_k = data["main"]["temp"]
        temprature_c = temperature_k - 273.15
        self.temperature_label.setStyleSheet("font-size: 64px;")
        self.temperature_label.setText(f"{temprature_c:.2f}°C")
        weather_id =data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        self.description_label.setText(weather_description)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))

    @staticmethod
    def get_weather_emoji(weather_id):

        if weather_id >= 200 and weather_id <=232:
            return "⛈️"
        elif 300<= weather_id <= 321:
            return "🌥️"
        elif 500 <= weather_id <=531:
            return "🌧️"
        elif 600<= weather_id <= 622:
            return "🌨️❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️😶‍🌫️🌁"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return " "

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = weatherapp()
    weather_app.show()
    sys.exit(app.exec())
