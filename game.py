import pygame

DIRECTIONS = ["left, right, up, down"]

def main():
    pygame.init()

    size: tuple[int, int] = (1000, 1000)
    black: tuple[int, int, int] = (0, 0, 0)
    white: tuple[int, int, int] = (255, 255, 255)
    
    screen = pygame.display.set_mode(size)
    
    screen.fill(color=white)
    
    screenCenter: tuple[float, float] = (500, 500)
    running: bool = True
    
    ballLocation: tuple[float, float] = screenCenter
    #ballLocation = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    pygame.draw.circle(radius=10, color = black, surface=screen, center=screenCenter)
    
    clock = pygame.time.Clock()
    
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        
        keyAction: list = pygame.key.get_pressed()
        
        x: float = ballLocation[0]
        y: float = ballLocation[1]
        
        if keyAction[pygame.K_d] == True:
            x += 300 * dt
        if keyAction[pygame.K_a] == True:
            x -= 300 * dt
        if keyAction[pygame.K_s] == True:
            y += 300 * dt
        if keyAction[pygame.K_w] == True:
            y -= 300 * dt
            
        ballLocation =(x, y)
        
        screen.fill(color=white)
        
        pygame.draw.circle(radius=10, color = black, surface=screen, center=ballLocation)
        
        pygame.display.flip()
        
        pygame.event.clear()
        

main()