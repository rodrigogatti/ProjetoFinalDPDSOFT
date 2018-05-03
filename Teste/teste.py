import pygame


class principal(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Guerra da Geometria")#Titulo
        self.width = 600#Altura
        self.height = 480#Largura
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        icon = pygame.image.load("icone.ico")#Carregar icone
        self.icon=pygame.display.set_icon(icon)#Fazer icone aparecer 
        self.clock = pygame.time.Clock()
        self.fps = 30#Frames por segundo

    #rodadndo o loop principal
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            milliseconds = self.clock.tick(self.fps)
            self.screen.blit(self.background, (0, 0))

        pygame.quit()


    

if __name__ == '__main__':
    principal()