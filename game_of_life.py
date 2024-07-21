import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import convolve

from ca_player import play

KERNEL = np.array(
    [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
)


def init() -> NDArray:
    gosper_glider_gun = np.zeros((11, 38), dtype=bool)
    # fmt: off
    pattern = [
        (5, 1), (5, 2), (6, 1), (6, 2), (3, 13), (3, 14), (4, 12), (4, 16),
        (5, 11), (5, 17), (6, 11), (6, 15), (6, 17), (6, 18), (7, 11),
        (7, 17), (8, 12), (8, 16), (9, 13), (9, 14), (1, 25), (2, 23),
        (2, 25), (3, 21), (3, 22), (4, 21), (4, 22), (5, 21), (5, 22),
        (6, 23), (6, 25), (7, 25), (3, 35), (3, 36), (4, 35), (4, 36)
    ]
    # fmt: on
    for r, c in pattern:
        gosper_glider_gun[r, c] = True
    grid = np.zeros((200, 200), dtype=bool)
    grid[1:12, 1:39] = gosper_glider_gun
    return grid


def step(grid: NDArray) -> NDArray:
    neighbors = convolve(input=grid.astype(int), weights=KERNEL, mode="wrap")
    return (neighbors == 3) | ((neighbors == 2) & grid)


if __name__ == "__main__":
    play(init_fn=init, step_fn=step, cell_size=5, delay=10)
