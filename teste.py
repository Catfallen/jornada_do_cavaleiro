N = 8

# movimentos do cavalo
dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]

# tabuleiro
tabuleiro = [[-1 for _ in range(N)] for _ in range(N)]


# verifica se posição é válida
def valido(x, y):
    return (
        0 <= x < N and
        0 <= y < N and
        tabuleiro[x][y] == -1
    )


# calcula quantidade de movimentos futuros
# (grau do vértice)
def grau(x, y):

    contador = 0

    for i in range(8):

        nx = x + dx[i]
        ny = y + dy[i]

        if valido(nx, ny):
            contador += 1

    return contador


# gera movimentos ordenados pela heurística de Warnsdorff
def movimentos_ordenados(x, y):

    movimentos = []

    for i in range(8):

        nx = x + dx[i]
        ny = y + dy[i]

        if valido(nx, ny):

            g = grau(nx, ny)

            movimentos.append((g, nx, ny))

    # menor grau primeiro
    movimentos.sort(key=lambda t: t[0])

    return movimentos


# backtracking + warnsdorff
def resolver(x, y, passo):

    # visitou todas as casas
    if passo == N * N:
        return True

    movimentos = movimentos_ordenados(x, y)

    for _, nx, ny in movimentos:

        tabuleiro[nx][ny] = passo

        if resolver(nx, ny, passo + 1):
            return True

        # backtracking
        tabuleiro[nx][ny] = -1

    return False


# posição inicial
inicio_x = 7
inicio_y = 1

tabuleiro[inicio_x][inicio_y] = 0

if resolver(inicio_x, inicio_y, 1):

    for linha in tabuleiro:

        for valor in linha:
            print(f"{valor:2}", end=" ")

        print()

else:
    print("Sem solução")