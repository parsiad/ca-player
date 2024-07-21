from typing import Callable

import pygame
from numpy.typing import NDArray

_BLACK, _GRAY, _WHITE = (0, 0, 0), (100, 100, 100), (255, 255, 255)
_BUTTON_SIZE = (_BUTTON_WIDTH, _BUTTON_HEIGHT) = (200, 50)


def _draw_buttons(screen: pygame.Surface, width: int, height: int, playing: bool):
    play_rect = pygame.Rect((width - _BUTTON_WIDTH) // 2 - _BUTTON_WIDTH, height, *_BUTTON_SIZE)
    step_rect = pygame.Rect((width - _BUTTON_WIDTH) // 2, height, *_BUTTON_SIZE)
    clear_rect = pygame.Rect((width - _BUTTON_WIDTH) // 2 + _BUTTON_WIDTH, height, *_BUTTON_SIZE)

    for rect in [play_rect, step_rect, clear_rect]:
        pygame.draw.rect(screen, _WHITE, rect)

    font = pygame.font.Font(None, 36)
    texts = [
        (font.render("Pause" if playing else "Play", True, _BLACK), play_rect),
        (font.render("Step", True, _GRAY if playing else _BLACK), step_rect),
        (font.render("Clear", True, _GRAY if playing else _BLACK), clear_rect),
    ]

    for text, rect in texts:
        screen.blit(text, text.get_rect(center=rect.center))

    return play_rect, step_rect, clear_rect


def play(
    init_fn: Callable[[], NDArray],
    step_fn: Callable[[NDArray], NDArray],
    cell_size: int = 5,
    delay: int = 100,
) -> None:
    """Run a cellular automata.

    Parameters
    ----------
    init_fn
        Function which produces the initial grid (a 2d boolean array)
    step_fn
        Function which evolves the grid (a 2d boolean array) into its next state
    cell_size
        Size of a cell
    delay
        Delay in milliseconds between frames when playing
    """
    pygame.init()
    grid = init_fn()
    height, width = cell_size * grid.shape[0], cell_size * grid.shape[1]
    screen = pygame.display.set_mode((width, height + _BUTTON_HEIGHT))
    pygame.display.set_caption("Cellular Automata Player")

    playing, running, spawning, killing = False, True, False, False

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_y < height:
                    grid_x, grid_y = mouse_x // cell_size, mouse_y // cell_size
                    if grid[grid_y, grid_x]:
                        killing = True
                    else:
                        spawning = True
            if event.type == pygame.MOUSEBUTTONUP:
                spawning, killing = False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_rect, step_rect, clear_rect = _draw_buttons(screen, width, height, playing)
                if not playing:
                    if step_rect.collidepoint(event.pos):
                        grid = step_fn(grid)
                    if clear_rect.collidepoint(event.pos):
                        grid.fill(0)
                if play_rect.collidepoint(event.pos):
                    playing = not playing

        screen.fill(_BLACK)

        if not playing and (spawning or killing) and (mouse_y < height):
            grid[mouse_y // cell_size, mouse_x // cell_size] = True if spawning else False

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                color = _WHITE if grid[i, j] else _BLACK
                pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

        play_rect, step_rect, clear_rect = _draw_buttons(screen, width, height, playing)

        if playing:
            grid = step_fn(grid)

        pygame.display.flip()

        if playing:
            pygame.time.delay(delay)

    pygame.quit()
