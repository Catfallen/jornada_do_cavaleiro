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

# =========================================================
# CONFIG
# =========================================================

N = 8

# movimentos do cavalo
dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]

TAMANHO = 700
DELAY = 120

# =========================================================
# ALGORITMO
# =========================================================

def valido(x, y, tabuleiro):

    return (
        0 <= x < N and
        0 <= y < N and
        tabuleiro[x][y] == -1
    )


def grau(x, y, tabuleiro):

    contador = 0

    for i in range(8):

        nx = x + dx[i]
        ny = y + dy[i]

        if valido(nx, ny, tabuleiro):
            contador += 1

    return contador


def movimentos_ordenados(x, y, tabuleiro):

    movimentos = []

    for i in range(8):

        nx = x + dx[i]
        ny = y + dy[i]

        if valido(nx, ny, tabuleiro):

            g = grau(nx, ny, tabuleiro)

            movimentos.append((g, nx, ny))

    movimentos.sort(key=lambda t: t[0])

    return movimentos


# =========================================================
# WARNDORFF
# =========================================================

def resolver_warnsdorff(tabuleiro, x, y, passo):

    yield (
        [linha[:] for linha in tabuleiro],
        x,
        y,
        False
    )

    if passo == N * N:
        return True

    movimentos = movimentos_ordenados(x, y, tabuleiro)

    for _, nx, ny in movimentos:

        tabuleiro[nx][ny] = passo

        resultado = yield from resolver_warnsdorff(
            tabuleiro,
            nx,
            ny,
            passo + 1
        )

        if resultado:
            return True

        # backtracking
        tabuleiro[nx][ny] = -1

        yield (
            [linha[:] for linha in tabuleiro],
            nx,
            ny,
            True
        )

    return False


# =========================================================
# DFS SIMPLES
# =========================================================

def resolver_simples(tabuleiro, x, y, passo):

    yield (
        [linha[:] for linha in tabuleiro],
        x,
        y,
        False
    )

    if passo == N * N:
        return True

    for i in range(8):

        nx = x + dx[i]
        ny = y + dy[i]

        if valido(nx, ny, tabuleiro):

            tabuleiro[nx][ny] = passo

            resultado = yield from resolver_simples(
                tabuleiro,
                nx,
                ny,
                passo + 1
            )

            if resultado:
                return True

            # backtracking
            tabuleiro[nx][ny] = -1

            yield (
                [linha[:] for linha in tabuleiro],
                nx,
                ny,
                True
            )

    return False


# =========================================================
# CONVERSÕES
# =========================================================

def matriz_para_path(tabuleiro):

    path = [None] * 64

    for linha in range(8):
        for coluna in range(8):

            passo = tabuleiro[linha][coluna]

            if passo != -1:

                square = chess.square(coluna, 7 - linha)

                path[passo] = square

    return path


# =========================================================
# NUMERAÇÃO SVG
# =========================================================

def criar_numeros_svg(tabuleiro):

    textos = []

    
    tamanho_casa = 45

    for linha in range(8):
        for coluna in range(8):

            valor = tabuleiro[linha][coluna]

            if valor == -1:
                continue

            x = coluna * tamanho_casa + tamanho_casa / 2

            y = linha * tamanho_casa + tamanho_casa / 2 + 8

            textos.append(f"""
            <text
                x="{x}"
                y="{y}"
                font-size="14"
                text-anchor="middle"
                fill="red"
                font-weight="bold"
            >
                {valor}
            </text>
            """)

    return "\n".join(textos)


# =========================================================
# RENDER SVG -> PNG BYTES
# =========================================================

def renderizar(tabuleiro, x, y, backtracking=False):

    board = chess.Board(None)

    square = chess.square(y, 7 - x)

    board.set_piece_at(
        square,
        chess.Piece(chess.KNIGHT, chess.WHITE)
    )

    fill = {}

    for linha in range(8):
        for coluna in range(8):

            if tabuleiro[linha][coluna] != -1:

                sq = chess.square(coluna, 7 - linha)

                if backtracking:
                    fill[sq] = "#ffaaaa"
                else:
                    fill[sq] = "#aaffaa"

    svg_data = chess.svg.board(
        board=board,
        fill=fill,
        size=TAMANHO
    )

    numeros_svg = criar_numeros_svg(tabuleiro)

    svg_data = svg_data.replace(
        "</svg>",
        numeros_svg + "</svg>"
    )

    png_bytes = cairosvg.svg2png(
        bytestring=svg_data.encode("utf-8")
    )

    return png_bytes


# =========================================================
# TKINTER
# =========================================================

root = tk.Tk()

root.title("Jornada do Cavalo")

label = tk.Label(root)
label.pack()

tk_image = None

# =========================================================
# ESCOLHA DO ALGORITMO
# =========================================================

#MODO = "warnsdorff"
MODO = "simples"

tabuleiro = [[-1 for _ in range(8)] for _ in range(8)]

inicio_x = 4
inicio_y = 4

tabuleiro[inicio_x][inicio_y] = 0

if MODO == "warnsdorff":

    generator = resolver_warnsdorff(
        tabuleiro,
        inicio_x,
        inicio_y,
        1
    )

else:

    generator = resolver_simples(
        tabuleiro,
        inicio_x,
        inicio_y,
        1
    )


# =========================================================
# LOOP DE ANIMAÇÃO
# =========================================================

def atualizar():

    global tk_image

    try:

        estado, x, y, backtracking = next(generator)

        png_bytes = renderizar(
            estado,
            x,
            y,
            backtracking
        )

        image = Image.open(
            io.BytesIO(png_bytes)
        )

        tk_image = ImageTk.PhotoImage(image)

        label.config(image=tk_image)

        root.after(DELAY, atualizar)

    except StopIteration:

        print("Finalizado")


# =========================================================
# START
# =========================================================

atualizar()

root.mainloop()