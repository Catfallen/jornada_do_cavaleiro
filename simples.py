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

        if valido(tabuleiro, nx, ny):

            tabuleiro[nx][ny] = passo

            resultado = yield from resolver_simples(
                tabuleiro,
                nx,
                ny,
                passo + 1
            )

            if resultado:
                return True

            # BACKTRACK VISÍVEL
            tabuleiro[nx][ny] = -1

            yield (
                [linha[:] for linha in tabuleiro],
                nx,
                ny,
                True
            )

    return False