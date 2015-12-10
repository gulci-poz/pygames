import tkinter as tk

#frame to kontener, a na canvas będziemy rysowali wszystkie obiekty
#pierwszym argumentem konstruktorów są nadrzędne obiekty (widgety)
#metoda pack() umożliwia wyświetlenie widgetu na nadrzędnym obiekcie
#kolejność wywołania pack() dla frame i canvas oraz title nie ma znaczenia

lives = 3
root = tk.Tk()
frame = tk.Frame(root)
canvas = tk.Canvas(frame, width = 600, height=400, bg="#aaaaff")
frame.pack()
canvas.pack()
root.title("Hello, Pong!")
root.mainloop()
