import pygame
import random
import sys

pygame.init()

# Configuração da janela do jogo
largura_janela = 1000
altura_janela = 1000
janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Jogo do Dinossauro")

# Carregar imagens
imagem_dino = pygame.image.load("dino.png")
imagem_cacto = pygame.image.load("cacto.png")
imagem_chao = pygame.image.load("chao.png")
imagem_nuvem = pygame.image.load("nuvem.jpg")
imagem_game_over = pygame.image.load("game_over.png")

# Carregar sons
som_pulo = pygame.mixer.Sound("pulo.mp3")
som_game_over = pygame.mixer.Sound("game_over.mp3")


class Dinossauro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagem_dino
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = altura_janela - 150
        self.velocidade_y = 0
        self.gravidade = 1
        self.pulando = False

    def atualizar(self):
        self.velocidade_y += self.gravidade
        self.rect.y += self.velocidade_y

        if self.rect.y >= altura_janela - 150:
            self.rect.y = altura_janela - 150
            self.velocidade_y = 0
            self.pulando = False

    def pular(self):
        if not self.pulando:
            som_pulo.play()
            self.velocidade_y -= 15
            self.pulando = True


class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagem_cacto
        self.rect = self.image.get_rect()
        self.rect.x = largura_janela
        self.rect.y = altura_janela - 160

    def atualizar(self):
        self.rect.x -= 5

        if self.rect.x <= -100:
            self.rect.x = largura_janela
            self.rect.y = altura_janela - 160
            self.rect.x += random.randint(200, 400)


class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagem_nuvem
        self.rect = self.image.get_rect()


# Variáveis do jogo
pontuacao = 0
nome_recordista = "N/A"
recorde = 0

# Grupos de sprites
todos_sprites = pygame.sprite.Group()
cactos = pygame.sprite.Group()
nuvens = pygame.sprite.Group()

# Criação dos objetos do jogo
dinossauro = Dinossauro()
todos_sprites.add(dinossauro)

for i in range(3):
    cacto = Cacto()
    cactos.add(cacto)
    todos_sprites.add(cacto)

for i in range(2):
    nuvem = Nuvem()
    nuvem.rect.x = random.randint(0, largura_janela)
    nuvem.rect.y = random.randint(0, altura_janela // 2)
    nuvens.add(nuvem)
    todos_sprites.add(nuvem)

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dinossauro.pular()

    # Atualizar objetos do jogo
    todos_sprites.update()

    # Verificar colisão com os cactos
    colisoes = pygame.sprite.spritecollide(dinossauro, cactos, False)
    if colisoes:
        som_game_over.play()
        pygame.time.delay(1000)
        if pontuacao > recorde:
            nome_recordista = input(
                "Você fez um novo recorde! Digite seu nome: ")
            recorde = pontuacao
        pontuacao = 0
        dinossauro.rect.y = altura_janela - 150
        dinossauro.velocidade_y = 0
        cactos.empty()

    # Desenhar objetos na janela
    janela.fill((255, 255, 255))
    todos_sprites.draw(janela)
    pygame.display.flip()

    # Atualizar pontuação
    pontuacao += 1

    # Controlar velocidade do jogo
    pygame.time.delay(10)
