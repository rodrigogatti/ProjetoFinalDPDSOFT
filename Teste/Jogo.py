# -*- coding: utf-8 -*-
"""
Created on Wed May 23 00:45:49 2018

@author: mathe
"""

import pygame,sys,random,time
import menu
from firebase import firebase #armezando os dados em nuvem , usando Firebase
#--------------------------------------------------------------------------------------------------------------------
#Definições
pygame.mixer.init()
pygame.font.init()

#Tela
altura=600
largura=800
metade_altura=altura/2
metade_largura=largura/2

clock=pygame.time.Clock()
fps=60
dt=clock.tick(fps) / 1000.0

vector=pygame.math.Vector2

imagem_fundo=pygame.image.load("fundo.jpg")
imagem_borda=pygame.image.load("borda.png")

#score
firebase=firebase.FirebaseApplication('https://guerradageometria.firebaseio.com/',None)
if firebase.get('Estoque',None) is None:
    highscore={"Highscore": 0} #estoque é representado por um dicionário
else:
    highscore=firebase.get('Estoque',None)
    
myfont = pygame.font.SysFont("monospace", 16)
fonte_titulo=pygame.font.Font("moonhouse.ttf", 100)
fonte_texto=pygame.font.Font("moonhouse.ttf", 30)

#inimigo
#imagem_inimigo1=pygame.image.load("hexagono.png")
imagem_inimigos_1=[pygame.image.load("hexagono.png"),pygame.image.load("circulo.png"),pygame.image.load("linhatriangulos.png"),pygame.image.load("losango.png"),pygame.image.load("quadrado.png"),pygame.image.load("retangulo.png"),pygame.image.load("triangulo.png"),]
imagem_inimigos_2=[pygame.image.load("inimigo_1.png"),pygame.image.load("inimigo_2.png"),pygame.image.load("inimigo_3.png")]
velocidade_inimigo=[200,300,250,100,400,150,125]
hitbox_inimigo=pygame.Rect(0,0,18,18)
vida_inimigo=3
dano_inimigo=1
raio_desvio=50
chance_inimigo=0.25

#tiro
imagem_tiro=pygame.image.load("bala_teste.png")
velocidade_tiro=700
tempos_spawn_tiro=2000
firerate_tiro=150
tiro_frente=vector(50,0)#para o tiro sair da frente da nave e nao do meio do sprite
dano_tiro=1

tamanho_tile=32
altura_grid=altura/tamanho_tile
largura_grid=largura/tamanho_tile

#Sons
jogo="tema.mp3"
GameOver="GameOver.mp3"
som_explosao=pygame.mixer.Sound("explosao.ogg")
som_tiro=pygame.mixer.Sound("tiro.ogg")
som_colisao=pygame.mixer.Sound("hit.ogg")
som_dano=pygame.mixer.Sound("dano.ogg")
som_morte=pygame.mixer.Sound("morri.ogg")

#Jogador
velocidade_jogador=550
rotacao_jogador=300
vidas_jogador=5
#imagem_jogador=pygame.image.load("3.png")
#imagem_jogador=[pygame.image.load("sprite_0.png"),pygame.image.load("sprite_1.png"),pygame.image.load("sprite_2.png"),pygame.image.load("sprite_3.png"),pygame.image.load("sprite_4.png"),pygame.image.load("sprite_5.png"),pygame.image.load("sprite_6.png")]
imagem_jogador=pygame.image.load("sprite_0.png")
imagem_imune=[pygame.image.load("sprite_0.png"),pygame.image.load("imune.png")]
hitbox_jogador=pygame.Rect(0,0,18,30)
knockback=40
imagem_vidacheia=pygame.image.load("vida_cheia.png")
imagem_vidavazia=pygame.image.load("vida_vazia.png")

imagem_explosao=[pygame.image.load("explosao1.png"),pygame.image.load("explosao2.png"),pygame.image.load("explosao3.png"),pygame.image.load("explosao4.png"),pygame.image.load("explosao5.png"),pygame.image.load("explosao6.png"),pygame.image.load("explosao7.png"),pygame.image.load("explosao8.png"),pygame.image.load("explosao9.png"),pygame.image.load("explosao10.png"),pygame.image.load("explosao11.png"),pygame.image.load("explosao12.png"),pygame.image.load("explosao13.png"),pygame.image.load("explosao14.png"),pygame.image.load("explosao15.png"),pygame.image.load("explosao16.png"),pygame.image.load("explosao17.png"),pygame.image.load("explosao18.png"),]

#--------------------------------------------------------------------------------------------------------------------
#Classes e funções(menos o jogo principal)

#Jogador
class jogador(pygame.sprite.Sprite):
    #define os parametros iniciais
    def __init__(self,loopPrincipal,x,y):
        self.groups=loopPrincipal.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game=loopPrincipal
        #self.image = random.choice(imagem_jogador)
        self.image=imagem_jogador
        self.rect = self.image.get_rect()
        self.hitbox_rect = hitbox_jogador
        self.hitbox_rect.center = self.rect.center        
        self.velocidade=vector(0,0)
        self.posicao=vector(x,y)*tamanho_tile
        self.rotacao=0
        self.ultimo=0#tiro
        self.vidas=vidas_jogador
        
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
        if key[pygame.K_SPACE]:
            momento=pygame.time.get_ticks()
            if momento - self.ultimo > firerate_tiro:
                som_tiro.play()
                self.ultimo=momento
                dir=vector(1,0).rotate(-self.rotacao)
                posicao_tiro=self.posicao+tiro_frente.rotate(-self.rotacao)
                Tiro(self.game,posicao_tiro,dir)
            
    #Colisao com os limites do mapa  
    def parede_colisao(self, dir):
        if dir == 'x':
            colidiu=pygame.sprite.spritecollide(self, self.game.limitadores, False,colidiu_func)
            if colidiu:
                som_colisao.play()
                if self.velocidade.x > 0:
                    self.posicao.x = colidiu[0].rect.left - self.hitbox_rect.width / 2.0
                if self.velocidade.x < 0:
                    self.posicao.x = colidiu[0].rect.right + self.hitbox_rect.width/ 2.0
                self.velocidade.x = 0
                self.hitbox_rect.centerx = self.posicao.x
        if dir == 'y':
            colidiu = pygame.sprite.spritecollide(self, self.game.limitadores, False, colidiu_func)
            if colidiu:
                som_colisao.play()
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
        #self.image=pygame.transform.rotate(random.choice(imagem_jogador),self.rotacao)
        if self.game.imunidade==False:
            self.image=pygame.transform.rotate(imagem_jogador,self.rotacao)
            self.rect=self.image.get_rect(center=self.rect.center)
        if self.game.imunidade==True:
            self.image=pygame.transform.rotate(random.choice(imagem_imune),self.rotacao)
            self.rect=self.image.get_rect(center=self.rect.center)
        
        self.rect.center=self.posicao
        self.posicao=self.posicao + self.velocidade *dt
        
        self.hitbox_rect.centerx = self.posicao.x
        parede_colisao(self,self.game.limitadores,'x')
        self.hitbox_rect.centery = self.posicao.y
        parede_colisao(self,self.game.limitadores,'y')
        
        self.rect.center = self.hitbox_rect.center 
        
            
        
        #surface.blit(self.image,(self.rect))  
        
#Colisao com os limites para qualquer objeto        
def parede_colisao(sprite, group ,dir):
    if dir == 'x':
        colidiu=pygame.sprite.spritecollide(sprite, group, False,colidiu_func)
        if colidiu:
            if sprite.velocidade.x > 0:
                sprite.posicao.x = colidiu[0].rect.left - sprite.hitbox_rect.width / 2.0
            if sprite.velocidade.x < 0:
                sprite.posicao.x = colidiu[0].rect.right + sprite.hitbox_rect.width/ 2.0
            sprite.velocidade.x = 0
            sprite.hitbox_rect.centerx = sprite.posicao.x
    if dir == 'y':
        colidiu = pygame.sprite.spritecollide(sprite, group, False, colidiu_func)
        if colidiu:
            if sprite.velocidade.y > 0:
                sprite.posicao.y = colidiu[0].rect.top - sprite.hitbox_rect.width/ 2.0
            if sprite.velocidade.y < 0:
                sprite.posicao.y = colidiu[0].rect.bottom + sprite.hitbox_rect.height / 2.0
            sprite.velocidade.y = 0
            sprite.hitbox_rect.centery = sprite.posicao.y   
            
#Colisao com rect         
def colidiu_func(objeto_1,objeto_2):
    return objeto_1.hitbox_rect.colliderect(objeto_2.rect)

#Limitador do jogo
class Limite_fisico(pygame.sprite.Sprite):
    def __init__(self, surface,loopPrincipal, x, y):
        self.groups =loopPrincipal.all_sprites, loopPrincipal.limitadores
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = loopPrincipal
        self.image = pygame.Surface((tamanho_tile, tamanho_tile))
        #self.image.fill((150,0,77))
        self.image=imagem_borda
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
        
#inimigos
class Inimigo_1(pygame.sprite.Sprite):
    def __init__(self, loopPrincipal, x, y):
        self.groups =loopPrincipal.all_sprites, loopPrincipal.inimigos
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game=loopPrincipal
        self.image=random.choice(imagem_inimigos_1)
        self.imagem=self.image
        self.rect=self.image.get_rect()
        self.hitbox_rect=hitbox_inimigo.copy()
        self.hitbox_rect.center = self.rect.center  
        self.posicao=vector(x,y)*tamanho_tile
        self.velocidade=vector(0,0)
        self.aceleracao=vector(0,0)
        self.rect.center=self.posicao
        self.rotacao=0
        self.vida=vida_inimigo
        
    def desviar_inimigos(self):
        for enemie in self.game.inimigos:
            if enemie != self:
                distancia=self.posicao - enemie.posicao
                if 0 < distancia.length() < raio_desvio:
                    self.aceleracao=self.aceleracao+distancia.normalize()
        
    def update(self,surface):
        self.rotacao=(self.game.jogador.posicao-self.posicao).angle_to(vector(1,0))
        self.image=pygame.transform.rotate(self.imagem,self.rotacao)
        self.rect=self.image.get_rect()
        self.rect.center=self.posicao
        
        #self.aceleracao=vector(velocidade_inimigo,0).rotate(-self.rotacao)
        self.aceleracao=vector(1,0).rotate(-self.rotacao)
        self.desviar_inimigos()
        self.aceleracao.scale_to_length(random.choice(velocidade_inimigo))
        self.aceleracao=self.aceleracao+self.velocidade*-1
        self.velocidade=self.velocidade+self.aceleracao*dt
        
        self.posicao=self.posicao+self.velocidade*dt+0.5*self.aceleracao*dt**2
        self.hitbox_rect.centerx=self.posicao.x
        parede_colisao(self,self.game.limitadores,'x')
        self.hitbox_rect.centery=self.posicao.y
        parede_colisao(self,self.game.limitadores,'y')
        
        self.rect.center=self.hitbox_rect.center
        if self.vida <= 0:
            som_explosao.play()
            inimugos_1.pop(1)
            self.game.score += 10
            if self.game.score > highscore['Highscore']:
                highscore['Highscore'] = self.game.score            
            self.kill()

class Inimigo_2(pygame.sprite.Sprite):
    def __init__(self, loopPrincipal, x, y):
        self.groups =loopPrincipal.all_sprites, loopPrincipal.inimigos
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game=loopPrincipal
        self.image=random.choice(imagem_inimigos_2)
        self.imagem=self.image
        self.rect=self.image.get_rect()
        self.hitbox_rect=hitbox_inimigo.copy()
        self.hitbox_rect.center = self.rect.center  
        self.posicao=vector(x,y)*tamanho_tile
        self.velocidade=vector(0,0)
        self.rect.center=self.posicao
        self.rotacao=0
        self.rotacao_velocidade=100
        self.vida=vida_inimigo

    def update(self,surface):
        self.rotacao=(self.rotacao+self.rotacao_velocidade*dt)%360
        self.image=pygame.transform.rotate(self.imagem,self.rotacao)
        self.rect=self.image.get_rect()
        self.rect.center=self.posicao
        
        self.velocidade=vector(velocidade_jogador,0).rotate(-self.rotacao)

        self.posicao=self.posicao+self.velocidade*dt
        
        self.hitbox_rect.centerx=self.posicao.x
        parede_colisao(self,self.game.limitadores,'x')
        self.hitbox_rect.centery=self.posicao.y
        parede_colisao(self,self.game.limitadores,'y')

        self.rect.center=self.hitbox_rect.center
        if self.vida <= 0:
            som_explosao.play()
            inimugos_2.pop(1)
            self.game.score += 10
            if self.game.score > highscore['Highscore']:
                highscore['Highscore'] = self.game.score            
            self.kill()
            
#Tiro
class Tiro(pygame.sprite.Sprite):
    
    def __init__(self, loopPrincipal, posicao, dir):
        self.groups =loopPrincipal.all_sprites, loopPrincipal.tiros
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = loopPrincipal
        self.image = imagem_tiro
        self.rect=self.image.get_rect()
        self.posicao=vector(posicao)
        self.rect.center=posicao
        self.velocidade=dir*velocidade_tiro
        self.spawn=pygame.time.get_ticks()
        self.rotacao=0
        
    def update(self,surface):
        #self.rotacao=(self.game.jogador.posicao+self.posicao).angle_to(vector(1,0))
        self.posicao=self.posicao+self.velocidade*dt
        self.rect.center=self.posicao
        #self.image=pygame.transform.rotate(self.image,self.rotacao)
        if pygame.sprite.spritecollideany(self,self.game.limitadores):
            self.kill()
        
        if pygame.time.get_ticks()-self.spawn > tempos_spawn_tiro:
            self.kill()
            
#Contador de vidas
def vida_jogador(surface,x,y,vidas,imagem1,imagem2):
    for i in range(vidas):
        imagem1_rect=imagem1.get_rect()
        imagem2_rect=imagem2.get_rect()
        
        imagem1_rect.x=x+30*i
        imagem1_rect.y=y
        
        surface.blit(imagem1,imagem1_rect)
#Game over
#--------------------------------------------------------------------------------------------------------------------
#Loop principal
class loopPrincipal:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela=pygame.display.set_mode((largura,altura))
        pygame.display.set_caption("Guerra da Geometria")
        self.clock=pygame.time.Clock()
        self.score=0
        self.map=Limite("limitacao.txt")
        pygame.mixer.music.load("jogo.mp3")
        pygame.mixer.music.play(-1) 
        self.imunidade=False
        self.ultimo_hit=0
        self.rodar=True
        self.gameover=False 
        self.placar=0
        
    def dar_load(self):
        self.all_sprites=pygame.sprite.Group()
        self.limitadores=pygame.sprite.Group()
        self.inimigos=pygame.sprite.Group()
        self.tiros=pygame.sprite.Group()
        
        global inimugos_1
        global inimugos_2
        global lista_linhas
        global lista_colunas
        
        inimugos_1=[]
        inimugos_2=[]
        lista_linhas=[]
        lista_colunas=[]
        
        for linhas,tile_1 in enumerate(self.map.local):
            for colunas ,tile_2 in enumerate(tile_1):
                if tile_2=="P":
                    Limite_fisico(self.tela,self,colunas,linhas)
                if tile_2=="J":
                    self.jogador=jogador(self,colunas,linhas)
                if 1<colunas<64:
                    lista_colunas.append(colunas)
                if 1<linhas<40:
                    lista_linhas.append(linhas)                            
                        
        self.camera=Cam(self.map.largura,self.map.altura)
        
    def roda(self):
        while self.rodar==True:
            self.dt = self.clock.tick(fps) / 1000.0
            self.eventos()
            if self.gameover==False:
                self.update()
            self.blitar()      
        
            
    def sair(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update(self.tela)
        self.camera.update(self.jogador) 


        if pygame.time.get_ticks() - self.ultimo_hit > 3000:
            self.imunidade=False
        
        if self.imunidade==False:
            hitou=pygame.sprite.spritecollide(self.jogador,self.inimigos,False,colidiu_func)
            for hit in hitou:
                som_dano.play()
                hit.velocidade=vector(0,0)
                self.jogador.vidas=self.jogador.vidas-1  
                self.ultimo_hit=pygame.time.get_ticks()
                self.imunidade=True
                
                if self.jogador.vidas<= 0:
                    som_morte.play()
                    firebase.patch('/Estoque',highscore)
                    self.score = 0 
                    self.gameover=True
                    pygame.mixer.music.load("GameOver.mp3")
                    pygame.mixer.music.play(-1) 
            
        hitou=pygame.sprite.groupcollide(self.inimigos,self.tiros,False,True)
        for hit in hitou:
            hit.vida=hit.vida-dano_tiro  
            hit.velocidade=vector(0,0)
            
    def blitar(self):
        if self.gameover==False:
            pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            self.tela.blit(imagem_fundo, (0,0))
            vida_jogador(self.tela,largura-150,5,self.jogador.vidas,imagem_vidacheia,imagem_vidavazia)
            for sprite in self.all_sprites:
                self.tela.blit(sprite.image,self.camera.apply(sprite))
            
            scoretext = myfont.render("Score: {0}, Highscore: {1}".format(self.score, highscore['Highscore']),1,(255,255,255))
            self.placar=self.score
            self.tela.blit(scoretext, (5,10))        
            vida_jogador(self.tela,largura-150,5,self.jogador.vidas,imagem_vidacheia,imagem_vidavazia)        
            
            while len(inimugos_1)<5:
                inimugos_1.append(Inimigo_1(self,random.choice(lista_colunas),random.choice(lista_linhas)))   
            while len(inimugos_2)<3:
                inimugos_2.append(Inimigo_2(self,random.choice(lista_colunas),random.choice(lista_linhas)))
        elif self.gameover==True:
            self.GameOver()
        
        pygame.display.flip()
        
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                self.sair()
            if evento.type==pygame.K_ESCAPE:
                self.sair()
                
    def GameOver(self):
        self.tela.fill((0,0,0)) 
        self.text=fonte_titulo.render("Game Over", 1, (250,0,0))
        self.tela.blit(self.text,(80,100))
        
        self.text_1=fonte_texto.render("O seu SCORE foi de {0}".format(self.placar), 1, (250,250,250))
        self.tela.blit(self.text_1,(150,250))        
        self.text_2=fonte_texto.render("Para voltar ao menu aperte M", 1, (250,250,250))
        self.tela.blit(self.text_2,(150,300))
        self.text_3=fonte_texto.render("Para jogar novamente aperte R", 1, (250,250,250))
        self.tela.blit(self.text_3,(150,330))         
                
        key = pygame.key.get_pressed()
        if key[pygame.K_m]:
            menu.menu()
        if key[pygame.K_r]: 
            jogo = loopPrincipal()
            jogo.dar_load()
            jogo.roda()            
        
#Função chamada pelo menu para iniciar o jogo
#def start():

#jogo = loopPrincipal()

#while True:
#    jogo.dar_load()
#    jogo.roda()
#--------------------------------------------------------------------------------------------------------------------
firebase.patch('/Estoque',highscore) #colocar quando morrer