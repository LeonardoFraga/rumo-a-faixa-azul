"""Confere se os vídeos do YouTube citados no guia ainda estão no ar.

Lê os dados embutidos no index.html, consulta o oEmbed do YouTube para cada
vídeo e gera um relatório em Markdown. Usa só a biblioteca padrão do Python.

Uso:  python3 scripts/verificar_videos.py [relatorio.md]

No GitHub Actions, escreve `quebrados=<n>` em $GITHUB_OUTPUT.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

OEMBED = "https://www.youtube.com/oembed?format=json&url="


def carregar_dados(caminho="index.html"):
    html = open(caminho, encoding="utf-8").read()
    marca = "const DATA = "
    inicio = html.index(marca) + len(marca)
    dados, _ = json.JSONDecoder().raw_decode(html[inicio:])
    return dados


def videos_do_guia(dados):
    """Lista (onde aparece, título do vídeo, url) para cada vídeo citado."""
    out = []
    for etapa in dados:
        local = f"Etapa {etapa['modulo']} · {etapa['titulo']}"
        for v in etapa.get("videos_gerais") or []:
            out.append((f"{local} › Comece por aqui", v["titulo"], v["url"]))
        for p in etapa.get("posicoes") or []:
            if p.get("video"):
                out.append((f"{local} › Mapa: {p['nome']}", p["video"]["titulo"], p["video"]["url"]))
        for grupo in etapa["grupos"]:
            for t in grupo["tecnicas"]:
                for v in t.get("videos") or []:
                    out.append((f"{local} › {t['nome']}", v["titulo"], v["url"]))
    return out


def checar(url, tentativas=3):
    """Devolve 'ok', 'sem_incorporacao', 'quebrado' ou 'nao_verificado'."""
    req = urllib.request.Request(OEMBED + urllib.parse.quote(url, safe=""),
                                 headers={"User-Agent": "rumo-a-faixa-azul-link-check"})
    for n in range(tentativas):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return "ok" if r.status == 200 else "nao_verificado"
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):      # existe, mas o dono desativou a incorporação
                return "sem_incorporacao"
            if e.code in (400, 404):      # removido, privado ou id inválido
                return "quebrado"
            if e.code == 429:
                time.sleep(5 * (n + 1))
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 * (n + 1))
    return "nao_verificado"


def main():
    destino = sys.argv[1] if len(sys.argv) > 1 else None
    itens = videos_do_guia(carregar_dados())
    status = {}
    for url in sorted({u for _, _, u in itens}):
        status[url] = checar(url)
        time.sleep(0.3)               # educado com o YouTube

    quebrados = [i for i in itens if status[i[2]] == "quebrado"]
    sem_verificar = [i for i in itens if status[i[2]] == "nao_verificado"]
    sem_incorp = [i for i in itens if status[i[2]] == "sem_incorporacao"]
    agora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    linhas = [f"Verificação de {agora}: {len(status)} vídeos diferentes, citados {len(itens)} vezes no guia.", ""]
    if quebrados:
        linhas += ["## Fora do ar", "", "Esses vídeos foram removidos ou ficaram privados. Troque por outro no `index.html`.", ""]
        linhas += [f"- [ ] **{onde}**: [{titulo}]({url})" for onde, titulo, url in quebrados]
        linhas.append("")
    else:
        linhas += ["Nenhum vídeo fora do ar.", ""]
    if sem_verificar:
        linhas += ["## Não foi possível verificar", "", "Falha de rede ou limite do YouTube. Serão conferidos de novo na próxima execução.", ""]
        linhas += [f"- {onde}: [{titulo}]({url})" for onde, titulo, url in sem_verificar]
        linhas.append("")
    if sem_incorp:
        linhas += [f"_{len(sem_incorp)} vídeo(s) existem, mas não permitem incorporação. Continuam assistíveis pelo link._", ""]

    relatorio = "\n".join(linhas)
    print(relatorio)
    if destino:
        open(destino, "w", encoding="utf-8").write(relatorio)
    saida = os.environ.get("GITHUB_OUTPUT")
    if saida:
        with open(saida, "a") as f:
            f.write(f"quebrados={len(quebrados)}\n")


if __name__ == "__main__":
    main()
