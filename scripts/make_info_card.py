"""
Gera um cartão SVG no estilo neofetch para ficar à direita do retrato ASCII:
linhas coloridas de chave/valor com experiência, tecnologias e destaques, sem
estatísticas do GitHub, porque o gráfico de contribuições já cobre isso.

O conteúdo é estático e editado abaixo. As linhas aparecem com um pequeno
atraso entre elas para parecer que o painel está sendo impresso ao lado do
retrato. STATIC=1 emite o estado congelado para pré-visualizações.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 480, 480
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
LINE_H = 20.5

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # chaves em laranja
SECTION = "#58a6ff"  # títulos de seção em azul
GREEN = "#3fb950"
ACCENT = "#22d3ee"

# modelo de conteúdo: tuplas que descrevem cada linha
# ("host",)                    -> "janiele@github" + linha
# ("kv", chave, valor)         -> chave laranja + valor claro
# ("sec", título)              -> título azul + linha
# ("bul", texto)               -> ponto verde + texto claro
# ("gap",)                     -> espaço vertical
ROWS = [
    ("host",),

    ("kv", "Nome", "Janiele Cristina"),
    ("kv", "Cargo", "Desenvolvedora de aplicações completas Júnior"),
    ("kv", "Cidade", "Alfenas - MG"),
    ("kv", "Objetivo", "Desenvolvimento Back-end"),

    ("gap",),

    ("sec", "Tecnologias"),

    ("kv", "Front-end", "React, TypeScript, Tailwind"),
    ("kv", "Back-end", "Node.js, Express, NestJS"),
    ("kv", "Banco", "PostgreSQL, Prisma"),
    ("kv", "Ferramentas", "Git, GitHub, JWT, Zod"),
    ("kv", "Nuvem", "Supabase, Vercel"),

    ("gap",),

    ("sec", "Atualmente"),

    ("bul", "Estudando NestJS"),
    ("bul", "Criando aplicações completas"),
    ("bul", "Buscando oportunidade como desenvolvedora júnior"),

    ("gap",),

    ("sec", "Destaques"),

    ("bul", "Sistema de Mensalidades"),
    ("bul", "API de Pizzaria"),
    ("bul", "WebCarros"),
]

def esc(s):
    return html.escape(s)


def rise(inner, i):
    """Aplica fade e subida leve, com atraso por linha; congela visível."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">janiele@github: ~$ perfil</text>')

y = TITLEBAR_H + 30
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.5
        continue
    if kind == "host":
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                 f'<tspan fill="{GREEN}">janiele</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">github</tspan></text>'
                 f'<line x1="{KEY_X+132}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
                 f'&#8212; {title}</text>'
                 f'<line x1="{KEY_X + 12 + len(row[1])*8}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val}</text>')
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{txt}</text>')
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("gerou", OUT, len(svg), "bytes;", W, "x", H, "conteudo_ate", round(y))
