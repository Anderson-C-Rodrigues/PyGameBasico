import pygame
import sys
import copy
import random
from random import randint

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
        self.caminho = False  # NOVO: marca se faz parte da solução

    def desenhar(self, tela, x, y, aresta):
        if self.caminho:
            pygame.draw.rect(tela, (255, 255, 0), (x, y, aresta, aresta))  # Amarelo = caminho
        elif self.aberta:
            pygame.draw.rect(tela, self.corAberta, (x, y, aresta, aresta))
        else:
            pygame.draw.rect(tela, self.corPreenchimento, (x, y, aresta, aresta))

        pygame.draw.line(tela, self.corLinha, (x, y), (x + aresta, y))
        pygame.draw.line(tela, self.corLinha, (x, y + aresta), (x + aresta, y + aresta))
        pygame.draw.line(tela, self.corLinha, (x, y), (x, y + aresta))
        pygame.draw.line(tela, self.corLinha, (x + aresta, y), (x + aresta, y + aresta))

class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao

    def resetaLabirinto(self):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna] = copy.deepcopy(self.celulaPadrao)

    def SorteiaCelulaVizinha(self, linhaCelulaAtual, colunaCelulaAtual):
        encontrou = False
        while not encontrou:
            direcao = random.choice([(0,1), (0,-1), (1,0), (-1,0)])  # apenas ortogonais
            linhaVizinha = linhaCelulaAtual + direcao[0]
            colunaVizinha = colunaCelulaAtual + direcao[1]
            if 0 <= linhaVizinha < self.qtLinhas and 0 <= colunaVizinha < self.qtColunas:
                encontrou = True
        return linhaVizinha, colunaVizinha

    def GeraLabirinto(self):
        self.resetaLabirinto()
        unvisitedCells = self.qtLinhas * self.qtColunas

        currentCellLine = randint(0, self.qtLinhas - 1)
        currentCellColumn = randint(0, self.qtColunas - 1)

        while unvisitedCells > 0:
            neighCellLine, neighCellColumn = self.SorteiaCelulaVizinha(currentCellLine, currentCellColumn)

            if not self.matriz[neighCellLine][neighCellColumn].visited:
                self.matriz[currentCellLine][currentCellColumn].aberta = True
                self.matriz[neighCellLine][neighCellColumn].visited = True
                unvisitedCells -= 1

            currentCellLine, currentCellColumn = neighCellLine, neighCellColumn

        # Garante entrada e saída
        self.matriz[1][0].aberta = True
        self.matriz[1][0].visited = True
        self.matriz[1][0].corAberta = (0, 255, 0)  # Verde

        self.matriz[self.qtLinhas - 1][self.qtColunas - 1].aberta = True
        self.matriz[self.qtLinhas - 1][self.qtColunas - 1].visited = True
        self.matriz[self.qtLinhas - 1][self.qtColunas - 1].corAberta = (255, 0, 0)  # Vermelho

    def ResolveLabirinto(self):
        destino = (self.qtLinhas - 1, self.qtColunas - 1)
        caminho = []

        def dfs(linha, coluna, visitados):
            if (linha, coluna) == destino:
                caminho.append((linha, coluna))
                return True

            visitados.add((linha, coluna))
            celula = self.matriz[linha][coluna]

            for dLinha, dCol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nLinha, nCol = linha + dLinha, coluna + dCol
                if 0 <= nLinha < self.qtLinhas and 0 <= nCol < self.qtColunas:
                    vizinha = self.matriz[nLinha][nCol]
                    if vizinha.aberta and (nLinha, nCol) not in visitados:
                        if dfs(nLinha, nCol, visitados):
                            caminho.append((linha, coluna))
                            return True
            return False

        if dfs(1, 0, set()):
            for l, c in caminho:
                self.matriz[l][c].caminho = True
        else:
            print("Não há caminho do início até a saída!")

class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        self.matriz = self.GeraMatriz()

    def __getitem__(self, index):
        return self.matriz[index]

    def GeraMatriz(self):
        return [[copy.deepcopy(self.celulaPadrao) for _ in range(self.qtColunas)] for _ in range(self.qtLinhas)]

    def DesenhaLabirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)

def main():
    pygame.init()

    azul = (50, 50, 255)
    preto = (10, 10, 10)
    branco = (255, 255, 255)
    verde = (0, 255, 0)
    cinza = (128, 128, 128)

    largura, altura = 600, 600
    N, M = 20, 20
    aresta = 20

    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), preto, cinza, preto, branco, False, False)
    labirinto = AldousBroder(N, M, aresta, celulaPadrao)
    labirinto.GeraLabirinto()
    labirinto.ResolveLabirinto()  # NOVO: resolve o labirinto

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mostra Malha - v2.0')

    while True:
        for
        labirinto.matriz.DesenhaLabirinto(tela, offset_linha, offset_coluna)
        pygame.display.flip()

if __name__ == '__main__':
    main()

