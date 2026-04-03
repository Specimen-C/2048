import pygame

DIRECTIONS = ["left, right, up, down"]

def main():
    pygame.init()
    
    # Screen size in pixels
    size: tuple[int, int] = (1000, 1000)
    
    # RGB color values
    black: tuple[int, int, int] = (0, 0, 0)
    white: tuple[int, int, int] = (255, 255, 255)
    
    # Create the game window
    screen = pygame.display.set_mode(size)
    
    #Fill the screen with a white background initially
    screen.fill(color=white)        
    
    screenCenter: tuple[float, float] = (500, 500)
    running: bool = True
    
    ballLocation: tuple[float, float] = screenCenter
    #ballLocation = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    pygame.draw.circle(radius=10, color = black, surface=screen, center=screenCenter)
    
    clock = pygame.time.Clock()
    
    # Right now it seems to run a program that has a ball in the center of the screen. Moves upon input WASD (Up, Left, Down, Right)
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        
        keyAction: list = pygame.key.get_pressed()
        
        x: float = ballLocation[0]
        y: float = ballLocation[1]
        
        #added arrow key input functionality (it also allows movement diagonally if two keys held simulatenously, might be buggy for 2048?)
        if keyAction[pygame.K_d] or keyAction[pygame.K_RIGHT] == True:
            x += 300 * dt
        if keyAction[pygame.K_a] or keyAction[pygame.K_LEFT] == True:
            x -= 300 * dt
        if keyAction[pygame.K_s] or keyAction[pygame.K_DOWN] == True:
            y += 300 * dt
        if keyAction[pygame.K_w] or keyAction[pygame.K_UP] == True:
            y -= 300 * dt
            
        ballLocation =(x, y)
        
        screen.fill(color=white)
        
        pygame.draw.circle(radius=10, color = black, surface=screen, center=ballLocation)
        
        pygame.display.flip()
        
        pygame.event.clear()
        

main()