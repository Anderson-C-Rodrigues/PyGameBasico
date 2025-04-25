import pygame
import sys
import copy
import random
from random import randint
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
        self.parte_caminho = False

    def get_corPreenchimento(self):
        return self.corPreenchimento

    def get_arestasFechadas(self):
        return self.arestasFechadas

    def is_visited(self):
        return self.visited

    def desenhar(self, tela, x, y, aresta):
        arSuperiorIni = (x, y)
        arSuperiorFim = (x + aresta, y)
        arInferiorIni = (x, y + aresta)
        arInferiorFim = (x + aresta, y + aresta)
        arEsquerdaIni = (x, y)
        arEsquerdaFim = (x, y + aresta)
        arDireitaIni = (x + aresta, y)
        arDireitaFim = (x + aresta, y + aresta)

        if self.parte_caminho:
            pygame.draw.rect(tela, (255, 0, 0), (x, y, aresta, aresta))  # 
        elif self.aberta:
            pygame.draw.rect(tela, self.corAberta, (x, y, aresta, aresta))
        else:
            pygame.draw.rect(tela, self.corPreenchimento, (x, y, aresta, aresta))

        pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)


class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def resetaLabirinto(self):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna] = copy.deepcopy(self.celulaPadrao)

    def SorteiaCelulaVizinha(self, linhaCelulaAtual, colunaCelulaAtual):
        encontrou = False
        while not encontrou:
            linhaVizinha = linhaCelulaAtual + randint(-1, 1)
            colunaVizinha = colunaCelulaAtual + randint(-1, 1)
            if (linhaVizinha >= 0 and linhaVizinha < self.qtLinhas and
                    colunaVizinha >= 0 and colunaVizinha < self.qtColunas and
                    (linhaVizinha != linhaCelulaAtual or colunaVizinha != colunaCelulaAtual)):
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

        
        self.matriz[1][0].aberta = True  
        self.matriz[self.qtLinhas - 1][self.qtColunas - 1].aberta = True  # 

    def ResolverLabirinto(self):
        inicio = (1, 0)
        fim = (self.qtLinhas - 1, self.qtColunas - 1)
        visitados = set()
        fila = deque([(inicio, [inicio])])

        while fila:
            (linha, coluna), caminho = fila.popleft()

            if (linha, coluna) == fim:
                for l, c in caminho:
                    self.matriz[l][c].parte_caminho = True
                return True

            visitados.add((linha, coluna))

            for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nl, nc = linha + dl, coluna + dc
                if 0 <= nl < self.qtLinhas and 0 <= nc < self.qtColunas:
                    if self.matriz[nl][nc].aberta and (nl, nc) not in visitados:
                        fila.append(((nl, nc), caminho + [(nl, nc)]))

        return False


class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        self.matriz = self.GeraMatriz()

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def __getitem__(self, index):
        return self.matriz[index]

    def __setitem__(self, index, value):
        self.matriz[index] = value

    def __aslist__(self):
        return self.matriz

    def GeraMatriz(self):
        matriz = []
        for i in range(self.qtLinhas):
            linha = []
            for j in range(self.qtColunas):
                linha.append(copy.deepcopy(self.celulaPadrao))
            matriz.append(linha)
        return matriz

    def DesenhaLabirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)


def main():
    pygame.init()

    cinza_escuro = (30, 30, 30)
    azul_escuro = (0, 0, 139)
    branco = (255, 255, 255)
    azul_claro = (135, 206, 250)

    [largura, altura] = [600, 300]
    N = 20
    M = 20
    aresta = 10

    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), cinza_escuro, azul_escuro, branco, azul_claro, False, False)
    labirinto = AldousBroder(N, M, aresta, celulaPadrao)
    labirinto.GeraLabirinto()
    labirinto.ResolverLabirinto()

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mostra Labirinto 2.0 com Resolução')

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(cinza_escuro)

        [linha, coluna] = ((tela.get_width() - (M * aresta)) // 2,
                           (tela.get_height() - (N * aresta)) // 2)
        labirinto.matriz.DesenhaLabirinto(tela, linha, coluna)

        pygame.display.flip()


if __name__ == '__main__':
    main()
