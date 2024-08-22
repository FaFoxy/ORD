import sys
import os
import struct

#ordem da arvore
ORDEM = 5

#tamanho do registro baseado na ordem
tamRegbtree = (12*ORDEM)-4

#nome dos arquivos
arqG = "games.dat"
arqB = "btree.dat" 

#RRN da raiz
rrnRais = -1

#@dataclass
class paginaAvore:
    def __init__(self) -> None:
        self.numChaves: int = 0
        self.chaves: int = [-1] * (ORDEM-1)
        self.offsetFilhos: int = [-1]*(ORDEM-1)
        self.filhos: int = [-1] * ORDEM
def lePagina(RRN:int) -> None:
    offset = 4 + (RRN * tamRegbtree)
    pag = paginaAvore()
    with open(arqB, "rb") as arq:
        arq.seek(offset)
        pag.numChaves = struct.unpack("<i", arq.read(4))[0]
        for i in range(ORDEM-1):
            pag.chaves[i] = struct.unpack(">i",arq.read(4))[0]
        for i in range(ORDEM-1):
            pag.offsetFilhos[i] = struct.unpack(">i",arq.read(4))[0]
        for i in range(ORDEM-1):
            pag.filhos[i] = struct.unpack(">i", arq.read(4)[0])
    return pag  

def escrevePagina(RRN:int, pag:paginaAvore): #escreve a pagina no arquivo da arvoreB
    if RRN == -1:
        offset = 4
    else:
        offset = 4 + (RRN * tamRegbtree)
        with open(arqB, "rb") as arq:
            arq.seek(offset)
            arq.write(struct.pack(">i", pag.numChaves))
            for i in range(ORDEM-1):
                print(pag.chave[i])
                arq.write(struct.pack(">i", pag.chaves[i]))
            for i in range(ORDEM-1):
                arq.write(struct.pack(">i", pag.offsetFilhos[i]))
            for i in range(ORDEM-1):
                arq.write(struct.pack(">i", pag.filhos))

def insereNaPagina(chave, filhoD, pag:paginaAvore):
    if pag.numChaves == (ORDEM-1):
        pag.filhos.append(None)
        pag.chaves.append(None)
    i = pag.numChaves
    while i > 0 and chave < pag.chaves [i-1]:
        
def buscaNaArvore(chave: int, rrn: int):
    if rrn == -1:
        return False, None, None
    
    else:
        pag = lePagina(rrn)
        achou, pos = buscaNaPagina(chave,rrn)

        if achou:
            return True, rrn, pos
        
        else:
            return buscaNaArvore(chave, pag.filhos[pos])

def buscaNaPagina(chave, pag):
    pos:int = 0
    while pos < pag.numChaves and chave > pag.chaves[pos]:
        pos += 1
    if pos < pag.numChaves and chave == pag.chaves[pos]:
        return True, pos
    else:
        return False, pos
    
def insereNaArvore(chave, rrnAtual):
    if rrnAtual == -1:
        chavePro = chave
        filhoDpro = -1
        return chavePro, filhoDpro, True
    else:
        pag = lePagina(rrnAtual)
        achou, pos = buscaNaArvore(chave, pag)
    
    if achou:
        print("erro! chave duplicada")#da pra gerar um erro tbm fe
        raise(ValueError)
    
    chavePro, filhoDpro, promo = insereNaArvore(chave, pag.filhos[pos])
    if not promo:
        return -1, -1, False
    else:
        if pag.numChves != (ORDEM-1):
            insereNaPagina(chavePro, filhoDpro, pag)
            escrevePagina(rrnAtual, pag)
            return -1, -1, False

        else:
            chavePro, filhoDpro, pag, novapag = divide(chavePro, filhoDpro, pag)
            escrevePagina(rrnAtual, pag)
            escrevePagina(novapag, filhoDpro)
            return chavePro, filhoDpro, True

def divide():
