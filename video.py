from teste import resolver_simples
from teste import gerar_tour
#import os
#os.add_dll_directory(r"D:\cairos\ucrt64\bin")

#import ctypes
#ctypes.CDLL("libcairo-2.dll")

import cairosvg
import chess
import chess.svg
from PIL import Image
import io
import cv2
import numpy as np

# =========================
# TOUR DO CAVALEIRO
# =========================

tour = [
    [62, 9, 36, 53, 58, 11, 34, 31],
    [37, 50, 61, 10, 35, 32, 57, 12],
    [8, 63, 52, 49, 54, 59, 30, 33],
    [51, 38, 25, 60, 45, 48, 13, 56],
    [22, 7, 44, 39, 24, 55, 46, 29],
    [1, 4, 23, 26, 47, 40, 17, 14],
    [6, 21, 2, 43, 16, 19, 28, 41],
    [3, 0, 5, 20, 27, 42, 15, 18]
]


# =========================
# MATRIZ -> PATH
# =========================
path = [None] * 64

for row in range(8):
    for col in range(8):

        move_index = tour[row][col]

        square = chess.square(
            col,
            7 - row
        )

        path[move_index] = square

# =========================
# CONFIG VIDEO
# =========================
SIZE = 800
FPS = 30

video = cv2.VideoWriter(
    "tour_trilha.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (SIZE, SIZE)
)

# =========================
# CASA -> CENTRO PIXEL
# =========================
def square_center(square):

    # margem do SVG do python-chess
    margin = SIZE * 0.0375

    board_size = SIZE - (margin * 2)

    tile = board_size / 8

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    x = margin + (file * tile) + (tile / 2)
    y = margin + ((7 - rank) * tile) + (tile / 2)

    return (int(x), int(y))

# =========================
# BOARD
# =========================
board = chess.Board(None)

# =========================
# GERAR FRAMES
# =========================
for step in range(64):

    board.clear()

    current_square = path[step]

    # coloca cavalo
    board.set_piece_at(
        current_square,
        chess.Piece(chess.KNIGHT, chess.WHITE)
    )

    # destacar casas visitadas
    fill = {}

    #for i in range(step + 1):
    #    fill[path[i]] = "#aaffaa"

    # =========================
    # SVG TABULEIRO
    # =========================
    svg_data = chess.svg.board(
        board=board,
        fill=fill,
        size=SIZE
    )

    # SVG -> PNG
    png_bytes = cairosvg.svg2png(
        bytestring=svg_data.encode("utf-8")
    )

    image = Image.open(
        io.BytesIO(png_bytes)
    )

    # PIL -> OpenCV
    frame = np.array(image)

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2BGR
    )

     # =========================
    # DESENHAR TRILHA
    # =========================
    for i in range(step):

        start = path[i]
        end = path[i + 1]

        p1 = square_center(start)
        p2 = square_center(end)

        # glow
        cv2.line(
            frame,
            p1,
            p2,
            (0, 0, 180),
            12,
            cv2.LINE_AA
        )

        # linha principal
        cv2.line(
            frame,
            p1,
            p2,
            (0, 0, 255),
            5,
            cv2.LINE_AA
        )

    # =========================
    # NUMERAR CASAS
    # =========================
    for i in range(step + 1):

        square = path[i]

        x, y = square_center(square)

        text = str(i)

        # sombra
        cv2.putText(
            frame,
            text,
            (x - 14, y + 14),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 0),
            4,
            cv2.LINE_AA
        )

        # texto principal
        cv2.putText(
            frame,
            text,
            (x - 14, y + 14),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )
 # salvar último frame
    last_frame = frame.copy()

    # =========================
    # ESCREVER FRAME
    # =========================
    for _ in range(10):
        video.write(frame)

    print(f"Frame {step+1}/64")

# =========================
# FINALIZAR
# =========================
video.release()

# salvar imagem final
cv2.imwrite("tour_final.png", last_frame)

print("Vídeo salvo: tour_trilha.mp4")
print("Imagem final salva: tour_final.png")