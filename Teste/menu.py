# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 17:20:02 2018

@author: mathe
"""

import pygame,sys,time,random
from pygame.locals import *
from Jogo import *


def menu():
    pygame.init()
    pygame.mixer.init()
    fonte=pygame.font.Font("moonhouse.ttf", 40)
    
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
    
    js=jogar_selecionado
    tut=tutorial
    exit=sair  
    
    #Musicas
    musica1="musica.mp3"
    pygame.mixer.music.load(musica1) #MÃºsica
    pygame.mixer.music.play(-1)    
    
    global markerp
    #variavel para o movimento do cursor
    mov=0
    start=[250,250]
    #Loop Principal
    mainloop = True
    while mainloop:
        tela.blit(fundo, (0,0))      
        tempo=relogio.tick(frames)
        tela.blit(js, [330,250])
        tela.blit(tut, [330,350])
        tela.blit(exit, [330,450])
        tela.blit(pygame.image.load(cursor), start)
        
       
        
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.mixer.music.fadeout(2)
                mainloop=False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    som_select.play()
                    pygame.mixer.music.fadeout(2)
                    mainloop=False
                    
                  
                    
                elif js==jogar_selecionado and event.key==K_DOWN:
                    som_select.play()
                    js=jogar
                    tut=tutorial_selecionado
                    exit=sair
                    markerp=2
                    start=[250,350]
            
                elif js==jogar_selecionado and event.key==K_UP:
                    som_select.play()
                    js=jogar
                    tut=tutorial
                    exit=sair_selecionado
                    markerp=3
                    start=[250,450]
            
                elif tut==tutorial_selecionado and event.key==K_DOWN:
                    som_select.play()
                    js=jogar
                    tut=tutorial
                    exit=sair_selecionado
                    markerp=3
                    start=[250,450]
            
                elif tut==tutorial_selecionado and event.key==K_UP:
                    som_select.play()
                    js=jogar_selecionado
                    tut=tutorial
                    exit=sair
                    markerp=1
                    start=[250,250]
            
                elif exit==sair_selecionado and event.key==K_DOWN:
                    som_select.play()
                    js=jogar_selecionado
                    tut=tutorial
                    exit=sair
                    markerp=1
                    start=[250,250]
            
                elif exit==sair_selecionado and event.key==K_UP:
                    som_select.play()
                    js=jogar
                    tut=tutorial_selecionado
                    exit=sair
                    markerp=2
                    start=[250,350]
            
                elif markerp==1 and event.key==pygame.K_RETURN:
                    som_select.play()
                    jogo = loopPrincipal()
                    jogo.dar_load()
                    jogo.roda()                    
            
                elif markerp==3 and event.key==pygame.K_RETURN:
                    som_select.play()
                    pygame.mixer.music.fadeout(2)
                    sys.exit()
            
            
            mov=mov+1
            pygame.display.update()            
                    
     
#Rodar o jogo automaticamente
if __name__=="__main__":
    menu()