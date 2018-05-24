# -*- coding: utf-8 -*-
"""
Created on Thu May 23 00:45:49 2018

@author: mathe
"""

import pygame,sys 
#--------------------------------------------------------------------------------------------------------------------
#Definições
#Tela
altura=768
largura=1024
metade_altura=altura/2
metade_largura=largura/2

clock=pygame.time.Clock()
fps=60
dt=clock.tick(fps) / 1000.0

vector=pygame.math.Vector2

imagem_fundo=pygame.image.load("fundo.jpg")

tamanho_tile=32
altura_grid=altura/tamanho_tile
largura_grid=largura/tamanho_tile

#Sons
jogo="tema.mp3"
GameOver="GameOver.mp3"
som="explosao.wav"

#Jogador
velocidade_jogador=550
rotacao_jogador=300
imagem_jogador=pygame.image.load("3.png")
hitbox_jogador=pygame.Rect(0,0,32,32)

#Tiro

#Inimigos
#--------------------------------------------------------------------------------------------------------------------
#Classes e funções(menos o jogo principal)

#Jogador
class jogador(pygame.sprite.Sprite):
    #define os parametros iniciais
    def __init__(self,loopPrincipal,x,y):
        self.groups=loopPrincipal.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game=loopPrincipal
        self.image = imagem_jogador
        self.rect = self.image.get_rect()
        #self.rect=pygame.Rect(x, y, 32, 32)
        self.hitbox_rect = hitbox_jogador
        self.hitbox_rect.center = self.rect.center        
        self.velocidade=vector(0,0)
        self.posicao=vector(metade_largura,metade_altura)
        self.rotacao=0
        self.ultimo=0#tiro
        
    #Cria movimentação de acordo com as teclas
    #Adiciona rotação
    def teclas(self):
        self.aceleracao=0
        self.rotacao_vel=0
        self.velocidade=vector(0,0)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]: 
            self.rotacao_vel= rotacao_jogador 
            pygame.transform.rotate(self.image,self.rotacao)
        if key[pygame.K_RIGHT]:
            self.rotacao_vel= -rotacao_jogador
            pygame.transform.rotate(self.image,self.rotacao)
        if key[pygame.K_UP]:
            self.velocidade=vector(velocidade_jogador,0).rotate(-self.rotacao)
        if key[pygame.K_DOWN]:
            self.velocidade=vector(-velocidade_jogador,0).rotate(-self.rotacao)
            
    #Colisao com os limites do mapa  
    def parede_colisao(self, dir):
        if dir == 'x':
            colidiu=pygame.sprite.spritecollide(self, self.game.limitadores, False,colidiu_func)
            if colidiu:
                if self.velocidade.x > 0:
                    self.posicao.x = colidiu[0].rect.left - self.hitbox_rect.width / 2.0
                if self.velocidade.x < 0:
                    self.posicao.x = colidiu[0].rect.right + self.hitbox_rect.width/ 2.0
                self.velocidade.x = 0
                self.hitbox_rect.centerx = self.posicao.x
        if dir == 'y':
            colidiu = pygame.sprite.spritecollide(self, self.game.limitadores, False, colidiu_func)
            if colidiu:
                if self.velocidade.y > 0:
                    self.posicao.y = colidiu[0].rect.top - self.hitbox_rect.width/ 2.0
                if self.velocidade.y < 0:
                    self.posicao.y = colidiu[0].rect.bottom + self.hitbox_rect.height / 2.0
                self.velocidade.y = 0
                self.hitbox_rect.centery = self.posicao.y    
            
    #Update no sprite e na imagem dele para q a rotação seja visivel
    def update(self, surface):
        self.teclas()
        self.rotacao=(self.rotacao+self.rotacao_vel*dt)%360
        
        #Define a rotaçao da imagem sem distorcer
        #Centraliza o rect para ter uma rotação "Smooth"
        self.image=pygame.transform.rotate(imagem_jogador,self.rotacao)
        self.rect=self.image.get_rect(center=self.rect.center)
        
        self.rect.center=self.posicao
        self.posicao=self.posicao + self.velocidade *dt
        
        self.hitbox_rect.centerx = self.posicao.x
        self.parede_colisao('x')
        self.hitbox_rect.centery = self.posicao.y
        self.parede_colisao('y')
        
        self.rect.center = self.hitbox_rect.center        

        surface.blit(self.image,(self.rect))  

#Colisao com rect         
def colidiu_func(objeto_1,objeto_2):
    return objeto_1.hitbox_rect.colliderect(objeto_2.rect)

#Limitador do jogo
class Limite_fisico(pygame.sprite.Sprite):
    def __init__(self, loopPrincipal, x, y):
        self.groups =loopPrincipal.all_sprites, loopPrincipal.limitadores
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = loopPrincipal
        self.image = pygame.Surface((tamanho_tile, tamanho_tile))
        self.image.fill((150,0,77))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x=x*tamanho_tile
        self.rect.y=y*tamanho_tile

#Limite do jogo
class Limite:
    def __init__(self, arquivo):
        self.local = []
        with open(arquivo, 'rt') as f:
            for line in f:
                self.local.append(line.strip())

        self.tamanho_x = len(self.local[0])
        self.tamanho_y = len(self.local)
        self.largura = self.tamanho_x * tamanho_tile
        self.altura = self.tamanho_y * tamanho_tile

#Movimentação da camera
class Cam:
    def __init__(self, largura, altura):
        self.camera = pygame.Rect(0, 0, largura, altura)
        self.largura = largura
        self.altura = altura

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.centerx + int(largura/ 2)
        y = -player.rect.centery + int(altura/ 2)

        x = min(0, x)  
        y = min(0, y)  
        x = max(-(self.largura - largura), x) 
        y = max(-(self.altura - altura), y)  
        self.camera = pygame.Rect(x, y, self.largura, self.altura)
        
#--------------------------------------------------------------------------------------------------------------------
#Loop principal
class loopPrincipal:
    def __init__(self):
        pygame.init()
        self.tela=pygame.display.set_mode((largura,altura))
        pygame.display.set_caption("Guerra da Geometria")
        self.clock=pygame.time.Clock()
        self.map=Limite("limitacao.txt")
        pygame.mixer.music.load(jogo)
        pygame.mixer.music.play(-1)          
        
    def dar_load(self):
        self.all_sprites=pygame.sprite.Group()
        self.limitadores=pygame.sprite.Group()
        
        for linhas,tile_1 in enumerate(self.map.local):
            for colunas ,tile_2 in enumerate(tile_1):
                if tile_2=="P":
                    Limite_fisico(self,colunas,linhas)
                if tile_2=="J":
                    self.jogador=jogador(self,colunas,linhas)
        self.camera=Cam(self.map.largura,self.map.altura)
        
    def roda(self):
        self.rodar=True
        while self.rodar:
            self.dt = self.clock.tick(fps) / 1000.0
            self.eventos()
            self.update()
            self.blitar()
            
    def sair(self):
        pygame.quit()
        sys.exit()
    
    def update(self):
        self.all_sprites.update(self.tela)
        self.camera.update(self.jogador)
        
    def blitar(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.tela.fill((0,0,0))
        self.tela.blit(imagem_fundo, (0,0))
        for sprite in self.all_sprites:
            self.tela.blit(sprite.image,self.camera.apply(sprite))
        pygame.display.flip()
        
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                self.sair()
            if evento.type==pygame.K_ESCAPE:
                self.sair()
                

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

def start():
    jogo = loopPrincipal()
    jogo.show_start_screen()
    while True:
        jogo.dar_load()
        jogo.roda()
        jogo.show_go_screen()
    
                
                
    
#--------------------------------------------------------------------------------------------------------------------