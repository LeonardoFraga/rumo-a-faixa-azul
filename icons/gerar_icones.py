"""Gera o favicon e os ícones do app a partir de um único desenho.

Desenho: uma faixa azul amarrada (nó no centro, duas pontas caindo),
com a ponteira preta e dois graus numa das pontas, sobre fundo azul-noite.
Rode na raiz do repositório:  python3 icons/gerar_icones.py
"""
import math
from PIL import Image, ImageDraw

FUNDO = "#0C1120"
AZUL = "#2F63E8"
AZUL_ESCURO = "#1F47B8"
AZUL_CLARO = "#4A7BF5"
PONTEIRA = "#06070B"
GRAU = "#FAFAF7"


def ponta(inicio, fim, meia_largura):
    """Retângulo inclinado ao longo da linha inicio→fim, com corte reto nas pontas."""
    (x1, y1), (x2, y2) = inicio, fim
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    px, py = -dy / n * meia_largura, dx / n * meia_largura
    return [(x1 + px, y1 + py), (x2 + px, y2 + py), (x2 - px, y2 - py), (x1 - px, y1 - py)]


def trecho(inicio, fim, t0, t1, meia_largura):
    """Pedaço da ponta entre as frações t0 e t1 do comprimento."""
    (x1, y1), (x2, y2) = inicio, fim
    a = (x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0)
    b = (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)
    return ponta(a, b, meia_largura)


def formas(escala=1.0):
    """Lista de (tipo, cor, pontos) num grid 100x100. escala<1 encolhe para a área segura."""
    c = 50

    def s(pts):
        return [(c + (x - c) * escala, c + (y - c) * escala) for x, y in pts]

    out = []
    # a faixa passando por trás, em volta da cintura
    out.append(("rect", AZUL_ESCURO, s([(8, 31), (92, 45)])))
    # pontas caindo do nó
    esq = ((43, 45), (25, 80))
    dir_ = ((57, 45), (75, 80))
    out.append(("poly", AZUL, s(ponta(*esq, 7))))
    out.append(("poly", AZUL, s(ponta(*dir_, 7))))
    # ponteira preta com dois graus na ponta da direita
    out.append(("poly", PONTEIRA, s(trecho(*dir_, 0.50, 0.88, 7))))
    out.append(("poly", GRAU, s(trecho(*dir_, 0.59, 0.655, 7))))
    out.append(("poly", GRAU, s(trecho(*dir_, 0.71, 0.775, 7))))
    # o nó: base e a volta diagonal por cima
    out.append(("rect", AZUL, s([(37, 24), (63, 50)])))
    out.append(("poly", AZUL_CLARO, s([(37, 41), (63, 25), (63, 33), (37, 49)])))
    return out


def png(tamanho, caminho, escala=1.0, cantos=0):
    S = tamanho * 4
    u = S / 100
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if cantos:
        d.rounded_rectangle([0, 0, S, S], radius=cantos * u, fill=FUNDO)
    else:
        d.rectangle([0, 0, S, S], fill=FUNDO)
    for tipo, cor, pts in formas(escala):
        pts = [(x * u, y * u) for x, y in pts]
        if tipo == "rect":
            d.rectangle([pts[0], pts[1]], fill=cor)
        else:
            d.polygon(pts, fill=cor)
    im = im.resize((tamanho, tamanho), Image.LANCZOS)
    if not cantos:
        im = im.convert("RGB")      # iOS e Android não querem transparência no ícone do app
    im.save(caminho, optimize=True)
    return im


def svg(caminho):
    partes = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">',
        f'<rect width="100" height="100" rx="22" fill="{FUNDO}"/>',
    ]
    for tipo, cor, pts in formas(1.0):
        if tipo == "rect":
            (x1, y1), (x2, y2) = pts
            partes.append(f'<rect x="{x1:g}" y="{y1:g}" width="{x2 - x1:g}" height="{y2 - y1:g}" fill="{cor}"/>')
        else:
            p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
            partes.append(f'<polygon points="{p}" fill="{cor}"/>')
    partes.append("</svg>")
    open(caminho, "w").write("".join(partes) + "\n")


if __name__ == "__main__":
    svg("favicon.svg")
    # favicon clássico: fundo com cantos arredondados, como o SVG
    base = png(256, "/tmp/favicon-256.png", cantos=22)
    base.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    # app: quadrado cheio (o sistema arredonda os cantos)
    png(180, "icons/apple-touch-icon.png")
    png(192, "icons/icon-192.png")
    png(512, "icons/icon-512.png")
    # Android "maskable": desenho menor, dentro da área segura de 80%
    png(512, "icons/icon-maskable-512.png", escala=0.78)
    print("ícones gerados")
