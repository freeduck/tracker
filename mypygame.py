import sys, pygame
pygame.init()

size = width, height = ,
speed = [, ]
black = , ,

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.bmp")
ballrect = ball.get_rect()

while :
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < or ballrect.right > width:
        speed[] = -speed[]
    if ballrect.top < or ballrect.bottom > height:
        speed[] = -speed[]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
