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
rrnRaiz = -1

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
        pag.chaves[i] = pag.chaves[i-1]
        pag.offsetFilhos[i] = pag.offsetFilhos[i-1]
        pag.filhos[i] = pag.filhos[i-1]
        i = i-1
    pag.chaves[i] = chave
    pag.offsetFilhos[i] = calcOffset(chave)
    pag.filhos[i] = filhoD
    pag.numChaves += 1       
    
def calcOffset(chave):
    achou = False
    with open(arqB, "rb") as arq:    
        offset = 4
        arq.read(4)
        while arq and not achou:
            tam = struct.unpack("<h", arq.read(2))[0]
            reg = arq.read(tam).decode()
            if int(reg.split("|")[0]) == chave:
                achou = True
                offset += 2
            else:
                achou = False
                offset += 2
        return offset
    
def novoRRN():
    with open(arqB, "rb") as arq: #perguntar pro manu pq tava wb e nao rb
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        return (offset - 4) // tamRegbtree


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

def divide(chave, filhoD, pag):
    insereNaPagina(chave, filhoD)
    meio = ORDEM // 2
    chavePro = pag.chaves[meio]
    pAtual = paginaAvore()
    pNova = paginaAvore()
    filhoDpro = novoRRN()
    for i in range(meio):
        pAtual.chaves[i] = pag.chaves[i]
        pAtual.filhos[i] = pag.filhos[i]
        pAtual.offsetsFilhos[i] = pag.offsetsFilhos[i]
        pAtual.numChaves += 1
    for i in range(meio+1, ORDEM - 1):
        pNova.chaves[i] = pag.chaves[i]
        pNova.filhos[i] = pag.filhos[i]
        pNova.offsetsFilhos[i] = pag.offsetsFilhos[i]
        pNova.numChaves += 1
    return chavePro, filhoDpro, pAtual, pNova

def gerenciadorDeInsercao(rrnRaiz, chave):
    chavePro, filhoDpro, promo = insereNaArvore(chave, rrnRaiz)
    if promo: #vai vcirar uma nova pag raiz
        print("Resto")
        pNova = paginaAvore()
        pNova.chaves[0] = chavePro
        pNova.filhos[1] = filhoDpro
        pNova.offsetFilhos[0] = calcOffset(chavePro)
        pNova.numChaves += 1
        rrnRaiz = novoRRN()
        escrevePagina(rrnRaiz, pNova)
    return rrnRaiz

def principal():
    global rrnRaiz
    with open(arqG, "rb") as arq:
        qtdReg = struct.unpack(">i", arq.read(4))[0]
        for i in range(qtdReg - 1):
            cab = i
            cab = cab.to_bytes(4)
            arq = open(arqB, 'wb')
            arq.write(cab)
            arq.close()
            tam = struct.unpack('<h', arqG.read(2))[0]
            reg = arqG.read(tam)
            reg = reg.decode()
            rrnRaiz = gerenciadorDeInsercao(rrnRaiz, int(reg.split("|")[0]))

principal()

