# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 17:20:02 2018

@author: mathe
"""

import pygame,sys,time,random
from pygame.locals import *
from Jogo import *
from firebase import firebase



firebase = firebase.FirebaseApplication('https://guerradageometria.firebaseio.com/',None)
hs = firebase.get('Estoque',None)

#dic = {'Ter':300, 'Est':400, 'Tee':250, 'Teh':275, 'TER': 325, 'EST': 350, 'ESQ':410, 'ESK': 330, 'The':290, 'Tet': 310, 'TTT': 340, 'TeT':100}
#print(dic)

####################################### recebe um dicionario, organiza e devolve uma lista com eles no formato correto
def orgpontos(dicionario):
    fonte2 = pygame.font.Font("moonhouse.ttf", 30)
    high = sorted(dicionario.items(), key = lambda x: x[1], reverse=True)
    pontosorg = []
    for k, v in high:
        pontos = fonte2.render('{0} : {1}'.format(k,v) , False, (255,255,255))
        pontosorg.append(pontos)
    return pontosorg


#######################################
def Funcaohighscore():
    pygame.init()
    pygame.mixer.init()
    
    fonte = pygame.font.Font("moonhouse.ttf", 40)
    fonte2 = pygame.font.Font("moonhouse.ttf", 30)
    som_select=pygame.mixer.Sound("select.ogg")
    
    
    fundo_highscore = pygame.image.load('imagem_highscore.png')
    
    musica1="tema.mp3"
    pygame.mixer.music.load(musica1) #MÃºsica
    pygame.mixer.music.play(-1) 
    
    pos_x = 210
    pos_x2 = 515
    
    loophigh = True
    while loophigh:
        relogio = pygame.time.Clock()
        pontosorg = orgpontos(hs)
        
        pygame.display.set_caption("Guerra da Geometria")
        tela = pygame.display.set_mode((800,600))
        
        tela.blit(fundo_highscore, (-70,20))
        tela.blit(pontosorg[0],(pos_x,268))
        tela.blit(pontosorg[1],(pos_x,328))
        tela.blit(pontosorg[2],(pos_x,391))
        tela.blit(pontosorg[3],(pos_x,448))
        tela.blit(pontosorg[4],(pos_x,511))
        tela.blit(pontosorg[5],(pos_x2,268))
        tela.blit(pontosorg[6],(pos_x2,328))
        tela.blit(pontosorg[7],(pos_x2,391))
        tela.blit(pontosorg[8],(pos_x2,448))
        tela.blit(pontosorg[9],(pos_x2,511))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                 pygame.quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==K_RETURN:
                    som_select.play()
                    loophigh = False
                    
        
    
        pygame.display.update()
    
    
    
    
    
    
    
    
    


def menu():
    pygame.init()
    pygame.mixer.init()
    fonte = pygame.font.Font("moonhouse.ttf", 40)
    fonte2 = pygame.font.Font("moonhouse.ttf", 25)
    
    #Tela
    cursor = ("cursor.png")
    icon = pygame.image.load("icone.ico")
    pygame.display.set_icon(icon)
    som_select=pygame.mixer.Sound("select.ogg")
    
    pygame.display.set_caption("Guerra da Geometria")
    tela = pygame.display.set_mode((800,600))
    fundo=pygame.image.load('fundo.jpg')
    
    frames=30
    relogio=pygame.time.Clock()
    
    #Opçoes do menu
    
    jogar=fonte.render("Jogar",1,(254, 254, 254))
    tutorial=fonte.render("Highscore",1,(254, 254, 254))
    sair=fonte.render("Sair",1,(254, 254, 254))    
    
    jogar_selecionado=fonte.render("Jogar",1,(76, 255, 254))
    tutorial_selecionado=fonte.render("Highscore",1,(76, 255, 254))
    sair_selecionado=fonte.render("Sair",1,(76, 255, 254))  
    
    digite_nome = fonte2.render("Digite seu nome", 1, (255,255,255))
    
    A = fonte.render("A",1,(255,255,255))
    B = fonte.render("B",1,(255,255,255))
    C = fonte.render("C",1,(255,255,255))
    D = fonte.render("D",1,(255,255,255))
    E = fonte.render("E",1,(255,255,255))
    F = fonte.render("F",1,(255,255,255))
    G = fonte.render("G",1,(255,255,255))
    H = fonte.render("H",1,(255,255,255))
    I = fonte.render("I",1,(255,255,255))
    J = fonte.render("J",1,(255,255,255))
    K = fonte.render("K",1,(255,255,255))
    L = fonte.render("L",1,(255,255,255))
    M = fonte.render("M",1,(255,255,255))
    N = fonte.render("N",1,(255,255,255))
    O = fonte.render("O",1,(255,255,255))
    P = fonte.render("P",1,(255,255,255))
    Q = fonte.render("Q",1,(255,255,255))
    R = fonte.render("R",1,(255,255,255))
    S = fonte.render("S",1,(255,255,255))
    T = fonte.render("T",1,(255,255,255))
    U = fonte.render("U",1,(255,255,255))
    V = fonte.render("V",1,(255,255,255))
    W = fonte.render("W",1,(255,255,255))
    X = fonte.render("X",1,(255,255,255))
    Y = fonte.render("Y",1,(255,255,255))
    Z = fonte.render("Z",1,(255,255,255))
    
    js=jogar_selecionado
    tut=tutorial
    exi=sair  
    
    #Musicas
    musica1="tema.mp3"
    pygame.mixer.music.load(musica1) #MÃºsica
    pygame.mixer.music.play(-1)    
    
    global markerp
    markerp = 1
    #variavel para o movimento do cursor
    mov=0
    start=[250,250]
    cont=0
    lista_nome = []
    #Loop Principal
    mainloop = True
    while mainloop:
        tela.blit(fundo, (0,0))      
        tempo=relogio.tick(frames)
        tela.blit(js, [330,250])
        tela.blit(tut, [330,350])
        tela.blit(exi, [330,450])
        tela.blit(pygame.image.load(cursor), start)
        tela.blit(digite_nome, (300,130))
        while cont < 3:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==K_a:
                        som_select.play()
                        if cont == 0:
                            tela.blit(A,(310,150))
                            lista_nome.append('A')
                        if cont == 1:
                            tela.blit(A,(350,150))
                            lista_nome.append('A')
                        if cont == 2:
                            tela.blit(A,(390,150))
                            lista_nome.append('A')
                        cont += 1
                        
                    if event.key==K_b:
                        som_select.play()
                        if cont == 0:
                            tela.blit(B,(310,150))
                            lista_nome.append('B')
                        if cont == 1:
                            tela.blit(B,(350,150))
                            lista_nome.append('B')
                        if cont == 2:
                            tela.blit(B,(390,150))
                            lista_nome.append('B')
                        cont += 1
                        
                    if event.key==K_c:
                        som_select.play()
                        if cont == 0:
                            tela.blit(C,(310,150))
                            lista_nome.append('C')
                        if cont == 1:
                            tela.blit(C,(350,150))
                            lista_nome.append('C')
                        if cont == 2:
                            tela.blit(C,(390,150))
                            lista_nome.append('C')
                        cont += 1
                    if event.key==K_d:
                        som_select.play()
                        if cont == 0:
                            tela.blit(D,(310,150))
                        if cont == 1:
                            tela.blit(D,(350,150))
                        if cont == 2:
                            tela.blit(D,(390,150))
                        cont += 1
                    if event.key==K_e:
                        som_select.play()
                        if cont == 0:
                            tela.blit(E,(310,150))
                        if cont == 1:
                            tela.blit(E,(350,150))
                        if cont == 2:
                            tela.blit(E,(390,150))
                        cont += 1
        
        
        NOME = ''.join(lista_nome)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.mixer.music.fadeout(2)
                sys.exit()
                
            elif event.type==pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    som_select.play()
                    pygame.mixer.music.fadeout(2)
                    sys.exit()
                    
                elif js==jogar_selecionado and event.key==K_DOWN:
                    som_select.play()
                    js=jogar
                    tut=tutorial_selecionado
                    exi=sair
                    markerp=2
                    start=[250,350]
            
                elif js==jogar_selecionado and event.key==K_UP:
                    som_select.play()
                    js=jogar
                    tut=tutorial
                    exi=sair_selecionado
                    markerp=3
                    start=[250,450]
            
                elif tut==tutorial_selecionado and event.key==K_DOWN:
                    som_select.play()
                    js=jogar
                    tut=tutorial
                    exi=sair_selecionado
                    markerp=3
                    start=[250,450]
            
                elif tut==tutorial_selecionado and event.key==K_UP:
                    som_select.play()
                    js=jogar_selecionado
                    tut=tutorial
                    exi=sair
                    markerp=1
                    start=[250,250]
            
                elif exi==sair_selecionado and event.key==K_DOWN:
                    som_select.play()
                    js=jogar_selecionado
                    tut=tutorial
                    exi=sair
                    markerp=1
                    start=[250,250]
            
                elif exi==sair_selecionado and event.key==K_UP:
                    som_select.play()
                    js=jogar
                    tut=tutorial_selecionado
                    exi=sair
                    markerp=2
                    start=[250,350]
            
                elif markerp==1 and event.key==pygame.K_RETURN:
                    som_select.play()
                    jogo = loopPrincipal()
                    jogo.dar_load()
                    jogo.roda()  
                    #jogo.GameOver()
            
                elif markerp==3 and event.key==pygame.K_RETURN:
                    som_select.play()
                    pygame.mixer.music.fadeout(2)
                    sys.exit()
                
                elif markerp == 2 and event.key==pygame.K_RETURN:
                    som_select.play()
                    Funcaohighscore()
                    
            
            mov=mov+1
            pygame.display.update()            
                    
     
#Rodar o jogo automaticamente
if __name__=="__main__":
    menu()