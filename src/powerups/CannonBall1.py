"""
ISPPJ1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

Author: Kevin Márquez
marquezberriosk@gmail.com

Author: Lewis Ochoa
lewis8a@gmail.com

This file contains the specialization of PowerUp to add a cannon and one shot until end to the game.
"""
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp

class CannonBall1(PowerUp):
    """
    Power-up to add a cannon to the game.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 6)
        self.activate = False
        self.ball_factory = Factory(Ball)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        paddle.cannon = True
        for _ in range(2):
            b = self.ball_factory.create(paddle.x, paddle.y - 8)
            b.vx = 0
            b.vy = -256
            play_state.projectiles.append(b)
        self.in_play = False

    def is_active(self) -> bool:
        return self.activate
    
    def deactivate(self, play_state: TypeVar("PlayState")) -> None:
        play_state.paddle.cannon = False
        self.activate = False
        self.in_play = True