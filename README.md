# Rumo à Faixa Azul

Trilha de estudos gratuita para quem está na faixa branca de jiu-jitsu e quer chegar à azul.

**Site:** https://leonardofraga.github.io/rumo-a-faixa-azul/

- 8 etapas, dos fundamentos à finalização por cima e à defesa pessoal
- Técnicas escolhidas para iniciantes, com vídeos em português e inglês
- Glossário com busca e mapa das posições
- Progresso salvo no próprio navegador

## Usar como app no celular

O site pode ficar na tela de início do celular, com ícone próprio, e abrir em tela cheia, sem a barra do navegador.

### iPhone (Safari)

1. Abra o site no **Safari**. Pelo Chrome ou outro navegador do iPhone, a opção pode não aparecer.
2. Toque no botão **Compartilhar**, o quadrado com uma seta para cima. Nas versões mais novas do iOS, ele fica dentro do menu **•••**.
3. Role a lista e toque em **Adicionar à Tela de Início**.
4. Se aparecer a opção **Abrir como App Web**, deixe ligada.
5. Confirme o nome ("Faixa Azul") e toque em **Adicionar**.

O ícone da faixa azul aparece na tela de início. Abra sempre por ele.

### Android (Chrome)

1. Abra o site no **Chrome**.
2. Toque no menu **⋮** no canto superior direito.
3. Toque em **Instalar app** ou **Adicionar à tela inicial**.
4. Confirme em **Instalar**.

### Seu progresso no app

O progresso fica salvo no aparelho, dentro do app. No iPhone, o app da tela de início guarda os dados separado do Safari: o que você marcou no Safari não aparece no app, e vice-versa. Escolha um dos dois para usar sempre.

Apagar o app da tela de início ou limpar os dados do navegador apaga o progresso.

O app precisa de internet para abrir e para tocar os vídeos.

## Como funciona

O site é estático e não tem build: `index.html`, mais `manifest.webmanifest`, `favicon.svg`, `favicon.ico` e a pasta `icons/` para o modo app.

Os ícones saem todos de um único desenho (uma faixa azul amarrada). Para mudar o desenho, edite `icons/gerar_icones.py` e rode `python3 icons/gerar_icones.py` na raiz do repositório; o script precisa do Pillow (`pip install pillow`). A cada push na `main`, o workflow `.github/workflows/pages.yml` publica a versão nova no GitHub Pages.

## Vídeos fora do ar

O workflow `.github/workflows/verificar-videos.yml` confere todos os vídeos do guia toda segunda às 9h (horário de Brasília) e sempre que o `index.html` muda na `main`. Se algum vídeo for removido ou ficar privado, ele abre uma issue "Vídeos fora do ar" com a etapa, a técnica e o link para trocar. Quando todos voltam a funcionar, a issue é fechada sozinha.

Para conferir na hora: aba **Actions → Verificar vídeos → Run workflow**, ou localmente com `python3 scripts/verificar_videos.py`.

Os vídeos são links para o YouTube; nenhum vídeo é hospedado aqui. O conteúdo complementa a aula e não substitui o seu professor.
