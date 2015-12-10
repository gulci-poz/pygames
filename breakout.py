import tkinter as tk

#nasza klasa Game pochodzi od Frame
#koncept z breakout_early.py opakowujemy w klasę
class Game(tk.Frame):
    def __init__(self, master):
        #do py 2.1
        #Game.__init__(self, master)
        #w py3 może być
        #super().__init__(master)
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = 610
        self.height = 400
        #(0, 0) - top-left, 2d, kierunek down-right
        self.canvas = tk.Canvas(
            self,
            width = self.width,
            height=self.height,
            bg="#aaaaff"
        )
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas, self.width / 2, 326)
        #kluczami w słowniku obiektów będą referencje do nich
        #zawiera wszystkie obiekty, z którymi może zderzać się piłka: paddle i cegły
        #słownik items będzie przydatny przy sprawdzaniu kolizji
        self.items[self.paddle.item] = self.paddle

        #generujemy cegły, zostawiamy po 5 pikseli po lewej i prawej, 75 to szerokość cegły
        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)

        self.hud = None
        self.setup_game()
        #focus na canvas, input events są bezpośrednio powiązane do canvas
        self.canvas.focus_set()
        #dzięki lambda mamy anonimowe funkcje, które są event handlerami
        #te funkcje dostają jako argument Tkinter event, lambda_ ignoruje pierwszy argument
        self.canvas.bind("<Left>", lambda _: self.paddle.move(-10))
        self.canvas.bind("<Right>", lambda _: self.paddle.move(10))

    def setup_game(self):
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200, "Press Space to start")
        self.canvas.bind("<space>", lambda _: self.start_game())

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()

        paddle_coords = self.paddle.get_position()
        #środek x paddle
        x = (paddle.coords[0] + paddle.coords[2]) * 0.5
        #dajemy 5 od środka paddle, które ma wysokość 10, do tego 10 na promień piłki i jeden na odstęp - i mamy środek y piłki
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    #skrótowiec na dodanie cegły i dodanie jej do słownika obiektów
    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    #domyślny argument size
    #stworzony obiekt będzie zwrócony, będzie można go modyfikować, żeby zmienić komunikat
    def draw_text(self, x, y, text, size="40"):
        font = ("Helvetica", size)
        return self.canvas.create_text(x, y, text=text, font=font)

    def update_lives_text(self):
        pass


class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y);

    def delete(self):
        self.canvas.delete(self.item)


#direction - kierunek, dla ułatwienia tylko ruchy po skosie
#top-left [-1, -1]
#top-right [1, -1]
#bottom-left [-1, 1]
#bottom-right [1, 1]
#zmiana znaku jednego komponentu wektora - zmiana kierunku o 90, zmiana znaku dwóch komponentów - zmiana kierunku o 180
#zmiana o 90 - przy odbiciu od krawędzi canvas, cegły lub platformy (paddle)
#(x, y) to współrzędne środka
class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, -1]
        self.speed = 10
        #atrybut klasy Ball
        #przy pomocy współrzędnych środka obliczamy bounding box
        item = canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill = "white"
        )
        super(Ball, self).__init__(canvas, item)


#(x, y) to współrzędne środka paddle (prostokąta)
class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill = "blue"
        )
        super(Padle, self).__init__(canvas, item)

    #pozycja początkowa piłki nie pokrywa się z pozycją początkową paddle
    #w obiekcie Game mamy metodę add_ball(), tam piłka będzie dodana na paddle
    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        #nie wyjdziemy z paddle poza canvas
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            #jeśli mamy przypisaną piłeczkę, to również ją przesuwamy
            #jeśli mamy referencję do ball, oznacza to, że gra jeszcze się nie rozpoczęła
            if self.ball is not None:
                self.ball.move(offset, 0)


class Brick(GameObject):
    COLORS = {1: "#999999", 2: "#555555", 3: "#222222"}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        #wartość hits oznacza pozostałe jeszcze trafienia
        self.hits = hits
        #atrybut klasy, potrzebujemy go tylko na chwilę do przypisania do fill
        color = Brick.COLORS[hits]
        #to może być atrybut klasy, też potrzebujemy go tylko na chwilę
        #jeszcze w konstruktorze przekazujemy go do konstruktora nadrzędnej klasy, tam atrybut klasy jest naspisywany przez atrybut obiektu, no i mamy zapamiętaną figurę w danym obiekcie
        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill = color,
            tags = "brick"
        )
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            #tutaj odwołujemy się to atrybutu danego obiektu obiektu
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hello, Pong!")
    game = Game(root)

    #musimy mieć jakiś obiekt canvas do wykonywania metod
    #posłużymy się obiektem canvas naszej gry
    #item = game.canvas.create_rectangle(10, 10, 100, 80, fill="green")
    #game_object = GameObject(game.canvas, item)
    #print(game_object.get_position())
    #game_object.move(20, -10)
    #print(game_object.get_position())
    #game_object.delete()

    #test piłeczki
    #ball_example = Ball(game.canvas, 200, 200)
    #print(ball_example.get_position())
    #ball_example.move(100, 100)
    #print(ball_example.get_position())
    #ball_example.delete()

    root.mainloop()

#obie metody zwracają integer, który identyfikuje handle do naszych obiektów
#współrzędne top-left i bottom-right, opcje key-value
#paddle = canvas.create_rectangle(x0, y0, x1, y1, **options)
#paddle = canvas.create_rectangle(250, 300, 330, 320, fill="blue", tags="paddle")
#ball = canvas.create_oval(x0, y0, x1, y1, **options)

#mała referencja
#canvas.coords(item) - współrzędne bounding box
#canvas.move(item, x, y)
#canvas.delete(item) - usuwa obiekt z canvas
#canvas.winfo_width()
#canvas.itemconfig(item, **options) - zmiana konfiguracji wybranego parametru, np. fill lub tag
#canvas.bind(event, callback) - handler callbaka przyjmuje parametr typu Tkinter event
#canvas.unbind(event)
#canvas.create_text(*position, **opts) - argumenty podobnie jak w rectangle i oval
#canvas.find_withtag(tag)
#canvas.find_overlapping(*position) - obiekty, które przecinają się lub pokrywają z prostokątem zadanym we współrzędnych
