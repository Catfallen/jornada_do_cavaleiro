N = 8

# movimentos do cavalo
dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]


# verifica se posição é válida
def valido(x, y, tabuleiro):
    return (
        0 <= x < N and
        0 <= y < N and
        tabuleiro[x][y] == -1
    )


# calcula quantidade de movimentos futuros
def grau(x, y, tabuleiro):

    contador = 0

    for i in range(8):

        nx = x + dx[i]
        ny = y + dy[i]

        if valido(nx, ny, tabuleiro):
            contador += 1

    return contador


# gera movimentos ordenados pela heurística de Warnsdorff
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


# backtracking + warnsdorff
def resolver(x, y, passo, tabuleiro):

    if passo == N * N:
        return True

    movimentos = movimentos_ordenados(x, y, tabuleiro)

    for _, nx, ny in movimentos:

        tabuleiro[nx][ny] = passo

        if resolver(nx, ny, passo + 1, tabuleiro):
            return True

        # backtracking
        tabuleiro[nx][ny] = -1

    return False


# retorna a matriz do tour
def gerar_tour(inicio_x=7, inicio_y=1):

    tabuleiro = [[-1 for _ in range(N)] for _ in range(N)]

    tabuleiro[inicio_x][inicio_y] = 0

    if resolver(inicio_x, inicio_y, 1, tabuleiro):
        return tabuleiro

    return None
def resolver_simples(tabuleiro, x, y, passo):

    yield (
        [linha[:] for linha in tabuleiro],
        x,
        y,
        False
    )

    if passo == N * N:

        yield (
            [linha[:] for linha in tabuleiro],
            x,
            y,
            False
        )

        return True

    movimentos = movimentos_ordenados(x, y, tabuleiro)

    for _, nx, ny in movimentos:

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

            # backtracking visível
            tabuleiro[nx][ny] = -1

            yield (
                [linha[:] for linha in tabuleiro],
                nx,
                ny,
                True
            )

    return False
# uso
#tour = gerar_tour()

#print(tour)