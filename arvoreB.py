import sys
import os
import struct
#from dataclasses import dataclass, field

#variaveis globais
arqG = "games.dat"
arvoB = "btree.dat"
ORDEM = 4
arquivo = {} 

#@dataclass
class Pagina:
    def __init__(self) -> None:
        self.numChaves: int = 0
        self.chaves: list = [None] * (ORDEM-1)
        self.filhos: list = [None] * ORDEM

    def estaCheia(self):
        return self.numChaves >= ORDEM - 1

def leOperacoes(nomeArqOP : str):
    arqOP = open(nomeArqOP, "r")
    linha = arqOP.readline()
    while linha:
        char = linha.split(sep=" ")
        if char[0] == "c":
            #cria btree
        elif char[0] == "b":
            print("foda")

def buscaNaArvore(chave, rrn):
    if rrn == None:
        return False, None, None
    else:
        pag = rrn
        achou, pos = buscaNaPagina(chave,rrn)
        if achou:
            return True, rrn, pos
        else:
            return buscaNaArvore(chave, pag.filhos[pos])

def buscaNaPagina(chave, pag):
    pos = 0
    while pos < pag.numChaves and chave > pag.chaves[pos]:
        pos += 1
    if pos < pag.numChaves and chave == pag.chaves[pos]:
        return True, pos
    else:
        return False, pos
    
def insereNaArvore(chave, rrnAtual):
    if rrnAtual == None:
        chavePro = chave
        filhoDpro = None
        return chavePro, filhoDpro
    else:
        pag = rrnAtual
        achou, pos = buscaNaArvore(chave, pag)
    
    if achou:
        print("erro chave duplicada")#da pra gerar um erro tbm fe

    chavePro, filhoDpro, promo = insereNaArvore(chave, pag.filhos[pos])
    if not promo:
        return None, None, False
    else:
        if 

        else:
            chavePro, filhoDpro, pag, novapag = divide(chavePro, filhoDpro, pag)
        arq.seek(rrnAtual)
        arq.write(pag)
        arq.flush        

def divide():

try:
    arq = open(arqG, 'rb')
    arq.close()
except:
    print(f"arquivo {arqG} não existe!")
    exit(0)

if sys.argv[1] == "-c":
    leOperacoes(sys.argv[2])

elif sys.argv[1] == "-e":
    print("teste")
elif sys.argv[1] == "-p":
    print('teste')