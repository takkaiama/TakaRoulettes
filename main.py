# main.py
import requests
from datetime import datetime
from collections import deque
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class TakaRoulettesApp(App):

    def build(self):
        self.title = "TakaRoulettes"

        self.api_url = 'https://cgp.safe-iplay.com/cgpapi/liveFeed/GetLiveTables'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Android; Mobile)',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://br.888casino.com',
            'Referer': 'https://br.888casino.com/'
        }

        self.data = {
            'regulationID': '4',
            'lang': 'por',
            'clientRequestId': 'init',
            'clientProperties': '{"brandName":"888Casino","language":"por"}',
            'CGP_DomainOrigin': 'https://br.888casino.com',
            'CGP_Skin': '888casino',
            'CGP_SkinOverride': 'com',
        }

        self.ROLETAS = {
            "2010017": "Auto-Roulette",
            "2010016": "Immersive Roulette",
            "2010165": "Roulette",
            "2010098": "Auto-Roulette VIP",
            "2010012": "American Roulette",
            "2010565": "Gold Vault Roulette",
            "2010096": "Speed Auto Roulette",
            "2010033": "Lightning Roulette",
            "2010440": "XXXtreme Lightning Roulette",
            "2380064": "Roleta Azure",
            "2380038": "Roulette Macao",
            "2380148": "PowerUp Roulette",
            "2380390": "Immersive Roulette Deluxe",
        }

        self.game_id = None
        self.history = deque(maxlen=50)
        self.last_snapshot = []

        root = BoxLayout(orientation="vertical")

        self.spinner = Spinner(
            text="Escolha a roleta",
            values=list(self.ROLETAS.values()),
            size_hint=(1, 0.1)
        )
        self.spinner.bind(text=self.on_select)
        root.add_widget(self.spinner)

        self.status_label = Label(text="Aguardando seleção...", size_hint=(1, 0.1))
        root.add_widget(self.status_label)

        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.grid = GridLayout(cols=1, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        root.add_widget(self.scroll)

        Clock.schedule_interval(self.update_loop, 5)

        return root

    def on_select(self, spinner, text):
        for gid, nome in self.ROLETAS.items():
            if nome == text:
                self.game_id = gid
                self.status_label.text = f"Monitorando: {text}"
                self.history.clear()
                break

    def get_emoji(self, numero):
        if numero == 0:
            return "🟢"
        elif numero % 2 == 0:
            return "⚫"
        else:
            return "🔴"

    def coletar(self):
        try:
            r = requests.post(self.api_url, headers=self.headers, data=self.data, timeout=20)
            if r.status_code == 200:
                data = r.json()
                tables = data.get("LiveTables", {})
                if self.game_id in tables:
                    return list(map(int, tables[self.game_id]["RouletteLast5Numbers"]))
        except:
            pass
        return []

    def calcular_status(self, numero):
        if numero == 0:
            return "RESPECT {na_cara}"
        elif numero % 3 == 0:
            return "RESPECT {1vz}"
        elif numero % 5 == 0:
            return "NOT RESPECT"
        else:
            return "RESPECT {2vz}"

    def update_loop(self, dt):
        if not self.game_id:
            return

        resultados = self.coletar()
        if not resultados:
            return

        if resultados == self.last_snapshot:
            return

        self.last_snapshot = resultados

        numero = resultados[0]
        evento = {
            "numero": numero,
            "hora": datetime.now().strftime("%H:%M:%S")
        }

        self.history.appendleft(evento)
        self.refresh_display()

    def refresh_display(self):
        self.grid.clear_widgets()

        ultimos = list(self.history)[:7]

        for evento in reversed(ultimos):
            numero = evento["numero"]
            emoji = self.get_emoji(numero)
            status = self.calcular_status(numero)
            texto = f"{emoji} {str(numero).rjust(2)}  →  {status}"
            self.grid.add_widget(Label(text=texto, size_hint_y=None, height=40))

if __name__ == "__main__":
    TakaRoulettesApp().run()