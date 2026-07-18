"""
Prepara uma foto de retrato para conversão limpa em ASCII:
  1. remove o fundo com rembg para isolar a pessoa
  2. aumenta o contraste local com CLAHE para destacar luzes e sombras
  3. compõe a pessoa sobre branco puro para o fundo virar espaço vazio

Saída: source-prepped.png em tons de cinza, consumida por make_ascii_svg.py.
Execute novamente sempre que a foto de origem mudar; o SVG ASCII é estático.

    python scripts/prep_photo.py <entrada.jpg> [saida.png]
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

# 1. recorta a pessoa
cut = remove(Image.open(INP).convert("RGBA"))
rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])                 # 0 = fundo

# 2. aplica contraste local na luminância com CLAHE
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
gray = clahe.apply(gray)

# leve ganho global para o rosto usar caracteres mais leves na escala
gray = cv2.convertScaleAbs(gray, alpha=1.05, beta=18)

# 3. cola sobre branco usando a máscara alpha, suavizada para evitar halo
mask = (alpha.astype(np.float32) / 255.0)
mask = cv2.GaussianBlur(mask, (0, 0), 1.0)
out = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)
out = np.clip(out, 0, 255).astype(np.uint8)

Image.fromarray(out, mode="L").save(OUT)
print("gerou", OUT, out.shape)
