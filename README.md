# 🧩 Maze Generator com Pygame

Projeto desenvolvido em Python para geração e visualização gráfica de labirintos utilizando **Pygame** e o algoritmo **Aldous–Broder**.

Além da interface gráfica, o projeto trabalha conceitos de Programação Orientada a Objetos, matrizes, geração aleatória e representação de caminhos em uma malha.

## ✨ Principais conceitos

- Geração procedural de labirintos
- Algoritmo Aldous–Broder
- Representação do labirinto através de uma matriz de células
- Programação Orientada a Objetos
- Manipulação gráfica com Pygame
- Estruturas de dados
- Controle de células visitadas e caminhos

## 🛠️ Tecnologias

- Python
- Pygame

## 🧱 Estrutura do código

O projeto utiliza classes para representar diferentes partes do labirinto, incluindo:

- `ArestasFechadas` — representa as paredes de cada célula
- `Celula` — armazena estado e informações visuais da célula
- `AldousBroder` — implementa a lógica de geração do labirinto

O algoritmo percorre células aleatoriamente e constrói progressivamente o labirinto até completar a malha.

## 🚀 Como executar

Certifique-se de ter Python instalado e instale o Pygame:

```bash
pip install pygame
```

Depois execute:

```bash
python maz001.py
```

## 🎯 Objetivo

O projeto foi desenvolvido como exercício prático de algoritmos e programação gráfica, combinando estruturas de dados, orientação a objetos e visualização com Pygame.
