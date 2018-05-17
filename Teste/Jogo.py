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
import camera 

vector=pygame.math.Vector2

pygame.init()
pygame.mixer.init()

#---------------------------------------------------------------------------------------------------------
#Funções e classes que formam o jogo
class jogador:
    #define os parametros iniciais
    def __init__(self,x,y):
        self.image = ship
        self.rect = self.image.get_rect()
        self.hitbox_rect = hitbox
        self.hitbox_rect.center = self.rect.center        
        self.velocidade=vector(0,0)
        self.posicao=vector(x,y)*32
        self.rotacao=0
        
    #Cria movimentação de acorodo com as teclas
    #Adiciona rotação
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
    
    #Update no sprite e na imagem dele para q a rotação seja visivel
    def update(self, surface):
        self.teclas()
        self.rotacao=(self.rotacao+self.rotacao_vel*dt)%360
        
        #Define a rotaçao da imagem sem distorcer
        #Centraliza o rect para ter uma rotação "Smooth"
        self.image=pygame.transform.rotate(ship,self.rotacao)

        self.rect=self.image.get_rect(center=self.rect.center)
        
        self.rect.center=self.posicao
        
        self.posicao=self.posicao + self.velocidade *dt
        
        
        surface.blit(self.image,(self.rect))

        
        
class Camera:
    #define os parametros iniciais
    def __init__(self, display_width, display_height):
        self.camera = pygame.Rect(0, 0, display_width , display_height)
        self.width = display_width
        self.height = display_height

    def aplicar(self, entity):
        return entity.rect.move(self.camera.topleft)

    #Limita a movimetação nas bordas
    def update(self, target):
        x = -target.rect.x + int(display_width / 2)
        y = -target.rect.y + int(display_height/ 2)
        x = min(0, x)  
        y = min(0, y)  
        x = max(-(self.width - display_width), x)  
        y = max(-(self.height - display_height), y)  
        self.camera = pygame.Rect(x, y, self.width, self.height)
        
        
#---------------------------------------------------------------------------------------------------------
#Definiçoes gerais de imagens,sons e tamanhos
display_width = 1024
display_height = 768

velocidade_player=350
velocidade_rotacao=250

hitbox=pygame.Rect(0, 0, 32, 32)

clock = pygame.time.Clock()
fps = 60
dt = clock.tick(fps) / 1000.0


metade_w=int(display_width  / 2)
metade_h=int(display_height/ 2)

gameDisplay = pygame.display.set_mode((display_width,display_height))
fundo=pygame.image.load('fundo.jpg')
pygame.display.set_caption("Guerra das formas")
ship=pygame.image.load("12.png")

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
    jogador(metade_h,metade_w)
    
    
    #camera = Camera(display_width, display_height)
    
    
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
            if event.type == pygame.QUIT :
                gameExit = True
                
        navezinha.teclas()
        #camera.update(jogador.update)
        gameDisplay.blit(fundo, (0,0))
        
        navezinha.update(gameDisplay)
        
        
        
        clock.tick(fps)
        pygame.display.update()
    
    
    pygame.quit()
    quit()

#---------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    gameLoop()