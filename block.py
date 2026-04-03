# module imports
import pygame

# item imports
from pygame import Clock, Surface


def main():
    # init pygame
    pygame.init()

    # constants
    DISPLAY_SIZE: tuple[int, int] = (500, 500)
    BLOCK_SIZE: tuple[int, int] = (100, 100)

    # setup
    screen: Surface = pygame.display.set_mode(DISPLAY_SIZE)
    screen.fill(color=(255, 255, 255))

    # state vars
    running: bool = True
    clock: Clock = pygame.time.Clock()
    block_location: str = "tr"

    while running:
        # time delta
        dt: float = clock.tick(60) / 1000

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("Move Up")
                elif event.key == pygame.K_s:
                    print("Move Down")
                elif event.key == pygame.K_a:
                    print("Move Left")
                elif event.key == pygame.K_d:
                    print("Move Right")

        # draw bg
        screen.fill(color=(255, 255, 255))

        # draw block
        match block_location:
            case "tl":
                pygame.draw.rect(
                    surface=screen, color=(0, 0, 0), rect=((0, 0), BLOCK_SIZE)
                )
            case "tr":
                pygame.draw.rect(
                    surface=screen,
                    color=(0, 0, 0),
                    rect=((DISPLAY_SIZE[0] - BLOCK_SIZE[0], 0), BLOCK_SIZE),
                )
            case _:
                raise ValueError("Invalid block location value")

        # draw to display
        pygame.display.flip()


# when run as script
if __name__ == "__main__":
    main()
