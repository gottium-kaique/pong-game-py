import pygame
from pygame.locals import *

width, height = 750, 500
window = pygame.display.set_mode([width, height])
pygame.display.set_caption('Pong Game')

black, white = (0, 0, 0), (255, 255, 255)
clock = pygame.time.Clock()
points_limit = 10

pygame.init()
font = pygame.font.SysFont('arial', 28)

def draw_winner_text(winner: int):
  gameover = True
  while gameover:
    window.fill(black)
    for e in pygame.event.get():
      if e.type == QUIT:
        exit()

      if e.type == KEYDOWN:
        if e.key == K_r:
          gameover = False

    winnerText = font.render(f'Player {winner} win! Enter R to Restart!', True, white)
    window.blit(
      winnerText, 
      (width //2 - winnerText.get_width() //2, height //2 - winnerText.get_height() //2)
    )

    pygame.display.update()

  paddle1.points, paddle2.points = 0, 0

def redraw():
  window.fill(black)
  text = font.render('Pong', True, white)
  textRect = text.get_rect()
  textRect.center = (width //2, 40)
  window.blit(text, textRect)

  # Player 1 Score
  p1_score = font.render(f'{paddle1.points}', True, white)
  p1_rect = p1_score.get_rect()
  p1_rect.center = (50, 50)
  window.blit(p1_score, p1_rect)

  # Player 2 Score
  p2_score = font.render(f'{paddle2.points}', True, white)
  p2_rect = p1_score.get_rect()
  p2_rect.center = (width - 50, 50)
  window.blit(p2_score, p2_rect)

  all_sprites.draw(window)
  pygame.display.update()

class Paddle(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([10, 75])
    self.image.fill(white)
    self.rect = self.image.get_rect()
    self.points = 0

class Ball(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([10, 10])
    self.image.fill(white)
    self.rect = self.image.get_rect()
    self.speed = 3
    self.dx = 1
    self.dy = 1

paddle1 = Paddle()

paddle1.rect.x = 25
paddle1.rect.y = 225

paddle2 = Paddle()
paddle2.rect.x = 715
paddle2.rect.y = 225

paddle_speed = 10

pong = Ball()
pong.rect.x = 375
pong.rect.y = 250

all_sprites = pygame.sprite.Group()
all_sprites.add(paddle1, paddle2, pong)

winner = None

while True:
  pygame.time.delay(10)
  window.fill(black)

  for e in pygame.event.get():
    if e.type == QUIT:
      exit()
  
  key = pygame.key.get_pressed()

  if key[pygame.K_w] and paddle1.rect.y > 0:
    paddle1.rect.y -= paddle_speed

  if key[pygame.K_s] and paddle1.rect.y < height - 75:
    paddle1.rect.y += paddle_speed

  if key[pygame.K_UP] and paddle2.rect.y > 0:
    paddle2.rect.y -= paddle_speed

  if key[pygame.K_DOWN] and paddle2.rect.y < height - 75:
    paddle2.rect.y += paddle_speed

  pong.rect.x += pong.speed * pong.dx
  pong.rect.y += pong.speed * pong.dy

  if pong.rect.y > height - 10:
    pong.dy = -1

  if pong.rect.y < 10:
    pong.dy = 1

  if pong.rect.x > width - 10:
    pong.rect.x, pong.rect.y = width //2, height //2
    pong.dx = -1
    paddle1.points += 1

  if pong.rect.x < 10:
    pong.rect.x, pong.rect.y = width //2, height //2
    pong.dx = 1
    paddle2.points += 1

  if paddle1.rect.colliderect(pong):
    pong.dx = 1

  if paddle2.rect.colliderect(pong):
    pong.dx = -1

  if paddle1.points == points_limit:
    draw_winner_text(1)

  if paddle2.points == points_limit:
    draw_winner_text(2)

  redraw()
  pygame.display.update()
