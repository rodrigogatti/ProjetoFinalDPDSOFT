import pygame,sys,time
from pygame.locals import *


def tela():
    pygame.init()
    pygame.mixer.init()
    fonte=pygame.font.Font("moonhouse.ttf", 40)
    #Tela
    icon = pygame.image.load("icone.ico")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Guerra da Geometria")
    tela = pygame.display.set_mode((480,480))
    fundo=pygame.image.load('fundo.jpg')
    frames=30
    relogio=pygame.time.Clock()
    #Loop Principal
    mainloop = True
    while mainloop:
        tela.blit(fundo, (0,0))
        pygame.display.update()        
        tempo=relogio.tick(frames)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                mainloop=False
            elif event.type==pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    mainloop=False
                    
     
#Rodar o jogo automaticamente
if __name__=="__main__":
    tela()