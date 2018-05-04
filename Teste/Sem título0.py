# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 17:20:02 2018

@author: mathe
"""

import pygame,sys,time
from pygame.locals import *
import tela as tela
import teste as teste


def menu():
    pygame.init()
    pygame.mixer.init()
    fonte=pygame.font.Font("moonhouse.ttf", 40)
    
    #Tela
    cursor = ("cursor.png")
    icon = pygame.image.load("icone.ico")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Guerra da Geometria")
    tela = pygame.display.set_mode((1200,720))
    fundo=pygame.image.load('fundo.jpg')
    frames=30
    relogio=pygame.time.Clock()
    
    #Opçoes do menu
    
    jogar=fonte.render("Jogar",1,(254, 254, 254))
    tutorial=fonte.render("Tutorial",1,(254, 254, 254))
    sair=fonte.render("Sair",1,(254, 254, 254))    
    
    jogar_selecionado=fonte.render("Jogar",1,(76, 255, 254))
    tutorial_selecionado=fonte.render("Tutorial",1,(76, 255, 254))
    sair_selecionado=fonte.render("Sair",1,(76, 255, 254))    
    
    js=jogar_selecionado
    tut=tutorial
    exit=sair  
    
    #Musicas
    musica1="musica.mp3"
    pygame.mixer.music.load(musica1) #MÃºsica
    pygame.mixer.music.play(-1)    
    
    
    #variavel para o movimento do cursor
    mov=0
    start=[350,305]
    #Loop Principal
    mainloop = True
    while mainloop:
        tela.blit(fundo, (0,0))      
        tempo=relogio.tick(frames)
        tela.blit(js, [420,300])
        tela.blit(tut, [410,400])
        tela.blit(exit, [410,500])
        tela.blit(pygame.image.load(cursor), start)
    
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.mixer.music.fadeout(2)
                mainloop=False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.mixer.music.fadeout(2)
                    mainloop=False
                    
                elif js==jogar_selecionado and event.key==K_DOWN:
                    js=jogar
                    tut=tutorial_selecionado
                    exit=sair
                    markerp=2
                    start=[350,405]
            
                elif js==jogar_selecionado and event.key==K_UP:
                    js=jogar
                    tut=tutorial
                    exit=sair_selecionado
                    markerp=3
                    start=[350,505]
            
                elif tut==tutorial_selecionado and event.key==K_DOWN:
                    js=jogar
                    tut=tutorial
                    exit=sair_selecionado
                    markerp=3
                    start=[350,505]
            
                elif tut==tutorial_selecionado and event.key==K_UP:
                    js=jogar_selecionado
                    tut=tutorial
                    exit=sair
                    markerp=1
                    start=[350,305]
            
                elif exit==sair_selecionado and event.key==K_DOWN:
                    js=jogar_selecionado
                    tut=tutorial
                    exit=sair
                    markerp=1
                    start=[350,305]
            
                elif exit==sair_selecionado and event.key==K_UP:
                    js=jogar
                    tut=tutorial_selecionado
                    exit=sair
                    markerp=2
                    start=[350,405]
            
                elif markerp==1 and event.key==pygame.K_RETURN:
                    teste.principal()
            
                elif markerp==3 and event.key==pygame.K_RETURN:
                    pygame.mixer.music.fadeout(2)
                    sys.exit()
            
            
            mov=mov+1
            pygame.display.update()            
                    
     
#Rodar o jogo automaticamente
if __name__=="__main__":
    menu()