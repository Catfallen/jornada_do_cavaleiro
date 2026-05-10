#import os
#os.add_dll_directory(r"D:\cairos\ucrt64\bin")

#import ctypes
#ctypes.CDLL("libcairo-2.dll")

import cairosvg
import chess
import chess.svg
from PIL import Image, ImageTk
import tkinter as tk
import io

# =========================
# TOUR DO CAVALEIRO (matriz 8x8)
# =========================
tour = [
    [0,59,38,33,30,17,8,63],
    [37,34,31,60,9,62,29,16],
    [58,1,36,39,32,27,18,7],
    [35,48,41,26,61,10,15,28],
    [42,57,2,49,40,23,6,19],
    [47,50,45,54,25,20,11,14],
    [56,43,52,3,22,13,24,5],
    [51,46,55,44,53,4,21,12]
]

# =========================
# CONVERTER MATRIZ -> SEQUÊNCIA DE CASAS
# =========================
path = [None] * 64

for row in range(8):
    for col in range(8):
        move_index = tour[row][col]
        square = chess.square(col, 7 - row)
        path[move_index] = square

# =========================
# TKINTER SETUP
# =========================
root = tk.Tk()
root.title("Jornada do Cavaleiro")

label = tk.Label(root)
label.pack()

board = chess.Board(None)

step = 0

# =========================
# FUNÇÃO PARA DESENHAR NÚMEROS
# =========================
def criar_numeros_svg():
    textos = []

    tamanho_casa = 45  # tamanho padrão do chess.svg

    for i in range(step + 1):
        sq = path[i]

        col = chess.square_file(sq)
        row = 7 - chess.square_rank(sq)

        x = col * tamanho_casa + tamanho_casa / 2
        y = row * tamanho_casa + tamanho_casa / 2 + 6

        textos.append(f'''
        <text x="{x}" y="{y}"
              font-size="14"
              text-anchor="middle"
              fill="black"
              font-weight="bold">
              {i}
        </text>
        ''')

    return "".join(textos)

# =========================
# ATUALIZAÇÃO DA ANIMAÇÃO
# =========================
def atualizar():
    global step, tk_image

    board.clear()

    # coloca cavalo na posição atual
    board.set_piece_at(path[step], chess.Piece(chess.KNIGHT, chess.WHITE))

    # desenha casas visitadas
    fill = {}
    for i in range(step + 1):
        fill[path[i]] = "#aaffaa"

    numeros_svg = criar_numeros_svg()

    svg_data = chess.svg.board(
        board=board,
        fill=fill
    )

    # inserir números antes do fechamento do SVG
    svg_data = svg_data.replace("</svg>", numeros_svg + "</svg>")

    png_bytes = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))
    image = Image.open(io.BytesIO(png_bytes))

    tk_image = ImageTk.PhotoImage(image)
    label.config(image=tk_image)

    step += 1

    if step < 64:
        root.after(300, atualizar)

# iniciar animação
atualizar()

root.mainloop()