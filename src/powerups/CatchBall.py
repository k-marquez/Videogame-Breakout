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
        self.lifetime = 800
        self.activate = False

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.paddle.sticky = True

        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

        self.activate = True
        self.in_play = False

    def is_active(self) -> bool:
        return self.activate
    
    def deactivate(self, play_state: TypeVar("PlayState")) -> None:
        play_state.paddle.sticky = False
        settings.SOUNDS["selected"].play()
        self.in_play = True

    def update_lifetime(self) -> None:
        if self.lifetime < 0:
            self.activate = False
        else:
            self.lifetime -= 1
