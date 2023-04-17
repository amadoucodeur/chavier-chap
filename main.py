from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivymd.uix.textfield import MDTextField

from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ObjectProperty

from pprint import pprint
from random import choice

class Game(MDWidget):
    words = ["good","bien","grand","beau","cool","mal","tech"]
    velocity = NumericProperty(0)
    playing = False
    text = ObjectProperty(None)
    input = ObjectProperty(None)
    input_hint = StringProperty('')
    scor = NumericProperty(0)
    bScor = NumericProperty(0)

    def start(self):
        self.playing = False
        self.velocity = 700
        self.text.center_x = self.center_x
        self.input.text = ''
        self.input_hint = 'Clickez ici pour commencer'
        self.text.text = 'Jouez'

    def move(self, *args):
        if self.playing:
            self.text.center_x = self.text.center_x-(self.width/self.velocity)
            self.lost()

    def play(self):
        self.text.x = self.width
        self.playing = True
        self.input_hint = 'Entrez le text qui défile'
        self.text.text = choice(self.words)
        self.saveData()
        if self.scor > self.bScor:
            self.bScor = self.scor
        self.scor = 0

    def on_text(self, *args):
        if self.ids['input'].focus and not self.playing:
            self.play()

    def win(self, *args):
        if self.text.text == self.input.text:
            self.text.x = self.width
            self.text.text = choice(self.words)
            self.input.text = ''
            self.velocity -= 10
            self.scor += 1

    def lost(self):
        if self.ids['text'].x + self.ids['text'].width < 0:
            self.start()
            self.ids['input'].focus = False

    def saveData(self):
        data = 0
        if self.bScor > self.scor:
            data = self.bScor
        else:
            data = self.scor
        with open('.data','w') as f:
            f.write(str(data))
    
    def lordData(self):
        self.dictLord()
        try:
            with open('.data','r') as f:
                self.bScor = int(f.read())
        except:
            with open('.data','w') as f:
                f.write('0')
            print('erreur lording data')

    def dictLord(self):
        self.words = []
        data = []
        with open('dict-data.txt','r') as f:
            data = f.read().split('\n')
        for i in data:
            if i != '' and i != ' ':
                self.words.append(i)

   
class ChapClavierApp(MDApp):
    game = ObjectProperty(None)
    def build(self):
        self.game = Game()
        self.game.lordData()
        self.game.start()
        Clock.schedule_interval(self.game.move, .01)
        return self.game
    
    def on_stop(self):
        print('stoped !')
        self.game.saveData()
        # return super().on_stop()


if __name__ == '__main__':
    ChapClavierApp().run()