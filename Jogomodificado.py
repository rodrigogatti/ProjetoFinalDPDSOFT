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

RED = (255, 0, 0)
BLACK = (0, 0, 0)

vector=pygame.math.Vector2

pygame.init()
pygame.mixer.init()
#---------------------------------------------------------------------------------------------------------
#Funções e classes que formam o jogo
class jogador(object):
    #define os parametros iniciais
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship
        self.rect = self.image.get_rect()
        self.rect=pygame.Rect(x, y, 32, 32)
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
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
    
        
#Criação de paredes para limitar o espaço que pode ser percorrido
class Wall():
    def __init__(self, x, y):
        self.image = surface
        self.image.convert()
        self.image.fill(pygame.Color("#000000"))
        self.rect = pygame.Rect(x, y, 32, 32)

    def update(self):
        pass
    
#Movimentçao da tela para acompanhar o jogador
class cam(object):
    def __init__(self, camera, width, height):
        self.camera = camera
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera(self.state, target.rect)
    
def cam_completa(camera, target_rect):
    x, y, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(metade_w-x,metade_h-y,w,h)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("meteorBrown_big1.png")
#        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(display_width - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(5, 20)
        self.speedx = random.randrange(-4, 4)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > display_height + 10 or self.rect.left < -25 or self.rect.right > display_width + 20:
            self.rect.x = random.randrange(display_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 20)
    
        
#        if self.rect.y > display_height + 10:
#            self.rect.y = 0
#        if self.rect.y < -10:
#            self.rect.y = display_height
#        if self.rect.x > display_width + 10:
#            self.rect.x = 0
#        if self.rect.x < -10:
#            self.rect.x = display_width
#        

                        
#---------------------------------------------------------------------------------------------------------
#Definiçoes gerais de imagens,sons e tamanhos
display_width = 1024
display_height = 768
flags=0
depth=0

velocidade_player=550
velocidade_rotacao=300

hitbox=pygame.Rect(0, 0, 32, 32)

clock = pygame.time.Clock()
fps = 20
dt = clock.tick(fps) / 1000.0


metade_w=int(display_width  / 2)
metade_h=int(display_height/ 2)

#Definiçoes de imagem e grupo do jogador
ship=pygame.image.load("12.png")
jogador_objeto=jogador(0,0)
navezinha=jogador(0,0)

#Definiçoes de imagem do mob
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for i in range(4):
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)


#Definindo melhor o fundo para a interação com a camera
gameDisplay = pygame.display.set_mode((display_width,display_height), flags, depth)
fundo=pygame.image.load('fundo.jpg').convert()
#gameDisplay.fill(RED)
surface=pygame.Surface((32,32))


x=0
y=0
parede=[]

limite=[
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "I                                          I",
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",]

for item in limite:
    for letra in item:
        if letra=="I":
            lim=Wall(x,y)
            parede.append(lim)
    y=y+32
    x=0
    
tela_largura  = len(limite[0])*32
tela_altura = len(limite)*32
camera = cam(cam_completa, tela_largura, tela_altura) 


pygame.display.set_caption("Guerra das formas")

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
    pygame.mixer.music.load(jogo)
    pygame.mixer.music.play(-1)    
    jogador(metade_h,metade_w)   
    
    
    gameExit = False
    gameOver = False
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                gameExit = True
#                raise SystemExit
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.mixer.music.fadeout(2)
                    raise SystemExit

        all_sprites.update()
        #camera.update(jogador_objeto)
        mobs.draw(gameDisplay)
        pygame.display.flip()
#        mobs.update()
        
#        
#        all_sprites.draw(gameDisplay)
        navezinha.teclas()
        gameDisplay.blit(fundo, (0,0))
        navezinha.update(gameDisplay)
        
        clock.tick(fps)
#        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    quit()
#---------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    gameLoop()