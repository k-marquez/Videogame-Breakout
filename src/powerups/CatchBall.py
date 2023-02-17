"""
ISPPJ1 2023
Study Case: Breakout

Author: Kevin Márquez
marquezberriosk@gmail.com

This file contains the specialization of PowerUp to take the ball with de paddle.
"""
import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp


class CatchBall(PowerUp):
    """
    Power-up to take the ball with de paddle.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 7)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.paddle.sticky = True

        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

        self.in_play = False
