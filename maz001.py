import pygame
import sys
import copy
import random
import time
from collections import deque

class ArestasFechadas:
    def __init__(self, superior, inferior, esquerda, direita):
        self.superior = superior
        self.inferior = inferior
        self.esquerda = esquerda
        self.direita = direita

class Celula:
    def __init__(self, arestasFechadas, corPreenchimento, corVisitada, corLinha, corAberta, visitada, aberta):
        self.arestasFechadas = arestasFechadas
        self.corPreenchimento = corPreenchimento
        self.corVisitada = corVisitada
        self.corLinha = corLinha
        self.corAberta = corAberta
        self.visited = visitada
        self.aberta = aberta

    def desenhar(self, tela, x, y, aresta):
        if self.aberta:
            pygame.draw.rect(tela, self.corAberta, (x, y, aresta, aresta))
        else:
            pygame.draw.rect(tela, self.corPreenchimento, (x, y, aresta, aresta))

        if self.arestasFechadas.superior:
            pygame.draw.line(tela, self.corLinha, (x, y), (x + aresta, y))
        if self.arestasFechadas.inferior:
            pygame.draw.line(tela, self.corLinha, (x, y + aresta), (x + aresta, y + aresta))
        if self.arestasFechadas.esquerda:
            pygame.draw.line(tela, self.corLinha, (x, y), (x, y + aresta))
        if self.arestasFechadas.direita:
            pygame.draw.line(tela, self.corLinha, (x + aresta, y), (x + aresta, y + aresta))

class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)
        self.celulaPadrao = celulaPadrao

    def resetaLabirinto(self):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna] = copy.deepcopy(self.celulaPadrao)

    def sorteia_celula_vizinha(self, linha, coluna):
        direcoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(direcoes)
        for dl, dc in direcoes:
            nl, nc = linha + dl, coluna + dc
            if 0 <= nl < self.qtLinhas and 0 <= nc < self.qtColunas:
                return nl, nc
        return linha, coluna

    def gera_labirinto(self):
        self.resetaLabirinto()
        unvisitedCells = self.qtLinhas * self.qtColunas
        currentLine = random.randint(0, self.qtLinhas - 1)
        currentCol = random.randint(0, self.qtColunas - 1)
        self.matriz[currentLine][currentCol].visited = True
        unvisitedCells -= 1

        while unvisitedCells > 0:
            neighLine, neighCol = self.sorteia_celula_vizinha(currentLine, currentCol)
            if not self.matriz[neighLine][neighCol].visited:
                if neighLine < currentLine:
                    self.matriz[currentLine][currentCol].arestasFechadas.superior = False
                    self.matriz[neighLine][neighCol].arestasFechadas.inferior = False
                elif neighLine > currentLine:
                    self.matriz[currentLine][currentCol].arestasFechadas.inferior = False
                    self.matriz[neighLine][neighCol].arestasFechadas.superior = False
                elif neighCol < currentCol:
                    self.matriz[currentLine][currentCol].arestasFechadas.esquerda = False
                    self.matriz[neighLine][neighCol].arestasFechadas.direita = False
                elif neighCol > currentCol:
                    self.matriz[currentLine][currentCol].arestasFechadas.direita = False
                    self.matriz[neighLine][neighCol].arestasFechadas.esquerda = False

                self.matriz[neighLine][neighCol].visited = True
                unvisitedCells -= 1

            currentLine, currentCol = neighLine, neighCol

        self.matriz[1][0].arestasFechadas.esquerda = False
        self.matriz[self.qtLinhas - 1][self.qtColunas - 1].arestasFechadas.inferior = False

    def resolver_bfs(self, linha, coluna, destinoL, destinoC):
        inicio = time.time()

        fila = deque()
        fila.append((linha, coluna))
        visitados = set()
        pais = {}

        while fila:
            atualL, atualC = fila.popleft()
            if (atualL, atualC) == (destinoL, destinoC):
                break

            visitados.add((atualL, atualC))
            atual = self.matriz[atualL][atualC]

            direcoes = [(-1, 0, "superior"), (1, 0, "inferior"), (0, -1, "esquerda"), (0, 1, "direita")]

            for dl, dc, direcao in direcoes:
                nl, nc = atualL + dl, atualC + dc
                if 0 <= nl < self.qtLinhas and 0 <= nc < self.qtColunas:
                    if not getattr(atual.arestasFechadas, direcao) and (nl, nc) not in visitados:
                        fila.append((nl, nc))
                        visitados.add((nl, nc))
                        pais[(nl, nc)] = (atualL, atualC)

        caminho = []
        atual = (destinoL, destinoC)
        while atual in pais:
            caminho.append(atual)
            atual = pais[atual]
        caminho.append((linha, coluna))
        caminho.reverse()

        fim = time.time()
        print(f"BFS - Caminho encontrado com {len(caminho)} passos em {fim - inicio:.4f} segundos.")
        return caminho

class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.matriz = [[copy.deepcopy(celulaPadrao) for _ in range(qtColunas)] for _ in range(qtLinhas)]

    def __getitem__(self, index):
        return self.matriz[index]

    def desenha_labirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)

def main():
    pygame.init()

    vermelho = (255, 0, 0)
    azul_claro = (100, 150, 255)
    cinza_claro = (200, 200, 200)
    cinza_escuro = (80, 80, 80)

    largura, altura = 800, 800
    N, M = 30, 30
    aresta = 20

    celulaPadrao = Celula(
        ArestasFechadas(True, True, True, True),
        azul_claro, cinza_claro, cinza_escuro, vermelho,
        False, False
    )

    labirinto = AldousBroder(N, M, aresta, celulaPadrao)
    labirinto.gera_labirinto()

    caminho = labirinto.resolver_bfs(1, 0, N - 1, M - 1)
    for linha, coluna in caminho:
        labirinto.matriz[linha][coluna].aberta = True

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Labirinto Resolvido (BFS)')

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill((255, 255, 255))
        offsetX = (largura - (M * aresta)) // 2
        offsetY = (altura - (N * aresta)) // 2
        labirinto.matriz.desenha_labirinto(tela, offsetX, offsetY)
        pygame.display.flip()

if __name__ == '__main__':
    main()
