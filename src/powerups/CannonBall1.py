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
import pygame
import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp

class CannonBall1(PowerUp):
    """
    Power-up to add two barrels on each side of the racket.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 5)
        self.activate = False
        self.shoots = 1
        self.projectiles = []
        self.ball_factory = Factory(Ball)
        self.texture_cannons = settings.TEXTURES["cannons"]
        self.frames_cannons = settings.FRAMES["cannons"]

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        paddle.cannon = True
        self.activate = True
        self.projectiles = []
        self.in_play = False

    def is_active(self) -> bool:
        return self.activate
    
    def shoot(self, play_state: TypeVar("PlayState")) -> None:
        if self.shoots > 0:
            self.shoots -= 1
            for _ in range(2):
                b = self.ball_factory.create(play_state.paddle.x, play_state.paddle.y - 8)
                b.vx = 0
                b.vy = -256
                self.projectiles.append(b)
            
            self.projectiles[0].x = play_state.paddle.x + play_state.paddle.width + 3
            self.projectiles[1].x = play_state.paddle.x - 14
            play_state.balls.extend(self.projectiles)
            self.projectiles = []
        else:
            self.activate = False

    
    def deactivate(self, play_state: TypeVar("PlayState")) -> None:
        play_state.paddle.cannon = False
        self.activate = False
        self.in_play = True

    def update_lifetime(self) -> None:
        return self.shoots
    
    def render_powerup(self, surface: pygame.Surface, play_state: TypeVar("PlayState")) -> None:
        surface.blit(
            self.texture_cannons,
            (play_state.paddle.x - 25, play_state.paddle.y - 10),
            self.frames_cannons[11]
        )
        surface.blit(
            self.texture_cannons,
            (play_state.paddle.x + play_state.paddle.width - 8, play_state.paddle.y - 10),
            self.frames_cannons[11]
        )