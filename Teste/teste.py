import pygame

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

block_size = 10
FPS = 30


class principal(object):

    def __init__(self):
        pygame.init()
        tela = pygame.display.set_mode((1200,720))
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