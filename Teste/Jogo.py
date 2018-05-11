# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 20:30:34 2018

@author: mathe
"""
#---------------------------------------------------------------------------------------------------------
#Imports
import pygame
import time
import random
import camera as c_mov 
import mapa 

vector=pygame.math.Vector2

pygame.init()
pygame.mixer.init()

#---------------------------------------------------------------------------------------------------------
#Funções e classes que formam o jogo
class jogador():
    def __init__(self,x,y):
        self.image = ship
        self.rect = self.image.get_rect()
        self.hitbox_rect = hitbox
        self.hitbox_rect.center = self.rect.center        
        self.velocidade=vector(0,0)
        self.posicao=vector(x,y)*16
        self.rotacao=0

    def teclas(self):
        self.rotacao_vel=0
        self.velocidade=vector(0,0)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]: 
            self.rotacao_vel= velocidade_rotacao  
            pygame.transform.rotate(self.image,self.rotacao)
        if key[pygame.K_RIGHT]:
            self.rotacao_vel= -velocidade_rotacao
            pygame.transform.rotate(self.image,self.rotacao)
        if key[pygame.K_UP]:
            self.velocidade=vector(velocidade_player,0).rotate(-self.rotacao)
        if key[pygame.K_DOWN]:
            self.velocidade=vector(-velocidade_player,0).rotate(-self.rotacao)

    def update(self, surface):
        self.teclas()
        self.rotacao=(self.rotacao+self.rotacao_vel*dt)%360
        
        self.image=pygame.transform.rotate(ship,self.rotacao)
        self.rect=self.image.get_rect()
        self.rect.center=self.posicao
        self.posicao+= self.velocidade 
        
        self.posicao= self.posicao+self.velocidade*dt
        
        self.rect.centerx=self.posicao.x
        self.rect.centery=self.posicao.y
        
        surface.blit(self.image,(self.posicao))
        
        
        
        
        
#---------------------------------------------------------------------------------------------------------
#Definiçoes gerais de imagens,sons e tamanhos
display_width = 800
display_height = 600

velocidade_player=250
velocidade_rotacao=250

hitbox=pygame.Rect(0, 0, 35,96 )

clock = pygame.time.Clock()
fps = 60
dt = clock.tick(fps) / 1000.0


metade_w=int(display_width  / 2)
metade_h=int(display_height/ 2)

gameDisplay = pygame.display.set_mode((display_width,display_height))
fundo=pygame.image.load('fundo.jpg')
pygame.display.set_caption("Guerra das formas")
ship=pygame.image.load("nave.png")

navezinha=jogador(0,0)



block_size = 10


font = pygame.font.SysFont("moonhouse.ttf", 25)

jogo="jogo.mp3"
GameOver="GameOver.mp3"
som="explosao.wav"

def fim_de_jogo(msg,color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [display_width/2, display_height/2])

#---------------------------------------------------------------------------------------------------------
#Funçao que inicia o jogo
def gameLoop():
    global cameraX, cameraY 
    pygame.mixer.music.load(jogo)
    pygame.mixer.music.play(-1)    
    
    jogador.cam=c_mov.camera(display_width,display_height)
    map=mapa.mapa_basico("mapa1.txt")
    
    gameExit = False
    gameOver = False
    
    while not gameExit:
    
        while gameOver == True:            
            gameDisplay.fill(black)
            fim_de_jogo("Game over" , red)   
            fim_de_jogo("Pressione C para jogar de novo" , red)  
            fim_de_jogo("Pressione Q para sair" , red)  
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:                        
                        gameLoop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                
        navezinha.teclas()
        gameDisplay.blit(fundo, (0,0))
        
        navezinha.update(gameDisplay)
        
        
        clock.tick(fps)
        pygame.display.update()

    
    pygame.quit()
    quit()

#---------------------------------------------------------------------------------------------------------
