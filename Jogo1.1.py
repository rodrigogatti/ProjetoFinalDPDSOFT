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
        self.posicao=vector(metade_w,metade_h)
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
        
class inimigos(pygame.sprite.Sprite):
	def __init__(self,tela,circulo1,retangulo1,losango1,triangulo1,hexagono1,quadrdado1,tipo):
		pygame.sprite.Sprite.__init__(self)

		self.circulo1 = pygame.image.load(circulo1)
		self.retangulo1 = pygame.image.load(retangulo1)
		self.losango1 = pygame.image.load(losango1)
		self.triangulo1 = pygame.image.load(triangulo1)
		self.hexagono1 = pygame.image.load(hexagono1)
		self.quadrdado1 = pygame.image.load(quadrdado1)
		self.tela = tela
		self.passo  = 0
		self.passo1 = 0
		self.passo2 = 0
		self.passo3 = 0
		self.passo4 = 1
		self.direcao = 1
		self.direcaoy = 1
		self.type = 1
		self.tipo = tipo
		self.descida = 0

	def posicao(self,x,y):
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.yinicial = self.rect.y

	def desenha(self):
		self.tela.blit(self.image,(self.rect.x,
									self.rect.y))
        
	def update(self):
		if self.passo >= 715:
			self.direcao = -1
		elif self.passo <= 0:
			self.direcao = 1
	
		
		self.passo += self.direcao
		self.rect.x += self.direcao

		if self.image == self.retangulo1:
			self.passo3 += 1
			if self.passo3 >=10:
				self.kill()
		
		if self.image != self.retangulo1:
			if self.passo1 < 40:
				self.image = self.triangulo1
			elif self.passo1 >= 40:
				self.image = self.circulo1
			if self.passo1 == 80:
				self.passo1 = 0
			else:
				self.passo1 += 1
                
		self.teclas()
		self.rotacao=(self.rotacao+self.rotacao_vel*dt)%360
        
        #Define a rotaçao da imagem sem distorcer
        #Centraliza o rect para ter uma rotação "Smooth"
		self.image=pygame.transform.rotate(ship,self.rotacao)

		self.rect=self.image.get_rect(center=self.rect.center)
        
		self.rect.center=self.posicao
        
		self.posicao=self.posicao + self.velocidade *dt
        
        
		surface.blit(self.image,(self.rect))
    
class tiros(pygame.sprite.Sprite):
	def __init__(self,tela,tiro):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(tiro)
		self.tela = tela
		self.colisoes = 0

		
	def posicao(self,x,y):
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def desenha(self):
		self.tela.blit(self.image,(self.rect.x,self.rect.y))        
        
#---------------------------------------------------------------------------------------------------------
#Definiçoes gerais de imagens,sons e tamanhos
display_width = 1024
display_height = 768

velocidade_player=550
velocidade_rotacao=300

hitbox=pygame.Rect(0, 0, 32, 32)

clock = pygame.time.Clock()
fps = 60
dt = clock.tick(fps) / 1000.0


metade_w=int(display_width  / 2)
metade_h=int(display_height/ 2)

#Definindo melhor o fundo para a interação com a camera
gameDisplay = pygame.display.set_mode((display_width,display_height))
fundo=pygame.image.load('fundo.jpg').convert()
#fundoWidth,fundoHeight=fundo.get_rect()

#comprimento_tela=fundoWidth*2
#altura_tela=fundoHeight*2
#telaPosX=0

#comeca_scroll_x=metade_w #quando a tela começa a mexer em x
#comeca_scroll_y=metade_h #quando a tela começa a mexer em y

#raio_circulo=25


pygame.display.set_caption("Guerra das formas")
ship=pygame.image.load("12.png")

navezinha=jogador(0,0)
tiro = tiro(tela,"tiro.png",2,1)
grupo_tirosm = pygame.sprite.Group()


block_size = 10


font = pygame.font.SysFont("moonhouse.ttf", 25)

jogo="jogo.mp3"
GameOver="GameOver.mp3"
som="explosao.wav"

def \(msg,color):
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
	inimigos.update()
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