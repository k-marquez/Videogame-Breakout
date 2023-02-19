"""
ISPPJ1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

Author: Kevin Márquez
marquezberriosk@gmail.com

Author: Lewis Ochoa
lewis8a@gmail.com

This file contains the specialization of PowerUp to add two more ball to the game.
"""
import random
from typing import TypeVar

import settings
from src.powerups.PowerUp import PowerUp


class LoseLife(PowerUp):
    """
    Power-up to lose one life to the game.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 3)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        settings.SOUNDS["hurt"].stop()
        settings.SOUNDS["hurt"].play()
        self.in_play = False
