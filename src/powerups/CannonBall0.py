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

import pygame

import settings
from src.powerups.PowerUp import PowerUp

class CannonBall(PowerUp):
    """
    Power-up to add two barrels on each side of the racket.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 2)
        self.activate = False
        self.lifetime = 800
        self.texture_cannons = settings.TEXTURES["cannons"]
        self.frames_cannons = settings.FRAMES["cannons"]

    def take(self, play_state: TypeVar("PlayState")) -> None:
        settings.SOUNDS["selected"].play()
        self.activate = True
        self.in_play = False
    
    def is_active(self) -> bool:
        return self.activate

    def deactivate(self, play_state: TypeVar("PlayState")) -> None:
        settings.SOUNDS["selected"].play()
        self.in_play = True

    def update_lifetime(self) -> None:
        if self.lifetime < 0:
            self.activate = False
        else:
            self.lifetime -= 1
            return self.lifetime

    def render_powerup(self, surface: pygame.Surface, play_state: TypeVar("PlayState")) -> None:
        surface.blit(
            self.texture_cannons,
            (play_state.paddle.x - 25, play_state.paddle.y - 10),
            self.frames_cannons[0]
        )
        surface.blit(
            self.texture_cannons,
            (play_state.paddle.x + play_state.paddle.width - 8, play_state.paddle.y - 10),
            self.frames_cannons[0]
        )