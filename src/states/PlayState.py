"""
ISPPJ1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

Author: Kevin Márquez
marquezberriosk@gmail.com

Author: Lewis Ochoa
lewis8a@gmail.com

This file contains the class to define the Play state.
"""
import random

import pygame

from gale.factory import AbstractFactory
from gale.state_machine import BaseState
from gale.input_handler import InputHandler, InputData, InputData
from gale.text import render_text

import settings
import src.powerups

class PlayState(BaseState):
    def enter(self, **params: dict):
        self.level = params["level"]
        self.score = params["score"]
        self.lives = params["lives"]
        self.paddle = params["paddle"]
        self.balls = params["balls"]
        self.brickset = params["brickset"]
        self.live_factor = params["live_factor"]
        self.points_to_next_live = params["points_to_next_live"]
        self.points_to_next_grow_up = (
            self.score
            + settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
        )
        self.powerups = params.get("powerups", [])
        self.catched_balls = params.get("catched_balls", [])
        self.projectiles = params.get("projectiles", [])
        self.activated_powerups = params.get("activated_powerups", {})
        self.time = 0
        self.paddle.sticky = False
        self.paddle.cannon = False
        if not params.get("resume", False):
            self.balls[0].vx = random.randint(-80, 80)
            self.balls[0].vy = random.randint(-170, -100)
            settings.SOUNDS["paddle_hit"].play()

        self.powerups_abstract_factory = AbstractFactory("src.powerups")

        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def update(self, dt: float) -> None:
        self.paddle.update(dt)
        for ball in self.catched_balls:
            if self.paddle.sticky:
                ball.update(dt)
                ball.solve_world_boundaries()
                ball.vx = self.paddle.vx
            else:
                ball.release()
                self.balls.append(ball)
                self.catched_balls.remove(ball)
        
        for ball in self.projectiles:
            if self.paddle.cannon:
                if(self.projectiles.index(ball) % 2 == 0):
                    ball.x = self.paddle.x + self.paddle.width + 3
                else:
                    ball.x = self.paddle.x - 14

        for ball in self.balls:
            ball.update(dt)
            ball.solve_world_boundaries()

            # Check collision with the paddle
            if ball.collides(self.paddle):
                if self.paddle.sticky:
                    ball.catched()
                    self.catched_balls.append(ball)
                else:
                    settings.SOUNDS["paddle_hit"].stop()
                    settings.SOUNDS["paddle_hit"].play()
                    ball.rebound(self.paddle)
                    ball.push(self.paddle)

            # Check collision with brickset
            if not ball.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(ball.get_collision_rect())

            if brick is None:
                continue
            else:
                if ball.vx == 0 and ball.vy == -250:
                    if ball.collides(brick):
                        ball.in_play = False
            brick.hit()
            self.score += brick.score()
            if ball.vx != 0 and ball.vy != -256:
                ball.rebound(brick)

            # Check earn life
            if self.score >= self.points_to_next_live:
                settings.SOUNDS["life"].play()
                self.lives = min(3, self.lives + 1)
                self.live_factor += 0.5
                self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

            # Check growing up of the paddle
            if self.score >= self.points_to_next_grow_up:
                settings.SOUNDS["grow_up"].play()
                self.points_to_next_grow_up += (
                    settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
                )
                self.paddle.inc_size()

            list_names = ["CannonBall1", "CannonBall2", "CannonBall3"]
            # Change to generate a powerup
            if random.random() < 0.75:
                r = brick.get_collision_rect()
                # Chance to generate two more balls
                if random.random() < 0.0:
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("TwoMoreBall").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )
                # Chance to generate a sticky paddle
                elif random.random() < 0.0 and not self.find_activated_powerups(["CatchBall"]):
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("CatchBall").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )
                # Chance to generate a pair of cannons
                elif random.random() < 0.0 and not self.find_activated_powerups(list_names) and not self.find_activated_powerups("CannonBall2"):
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("CannonBall1").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )
                # Chance to generate a pair of cannons
                elif random.random() < 0.0 and not self.find_activated_powerups(list_names) and not self.find_activated_powerups("CannonBall1"):
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("CannonBall2").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )
                # Chance to generate a confetti
                elif random.random() < 0.0 and not self.find_activated_powerups(["ConfettiBall"]):
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("ConfettiBall").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )
                
                # Chance to generate a lose live
                elif random.random() < 0.80 and not self.find_activated_powerups(["LoseLive"]):
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("LoseLife").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )

        # Removing all balls that are not in play
        self.balls = [ball for ball in self.balls if (ball.in_play and not ball.catch)]

        self.brickset.update(dt)

        if not (self.balls or self.catched_balls):
            self.lives -= 1
            if self.lives == 0:
                self.state_machine.change("game_over", score=self.score)
            else:
                self.paddle.dec_size()
                self.state_machine.change(
                    "serve",
                    level=self.level,
                    score=self.score,
                    lives=self.lives,
                    paddle=self.paddle,
                    brickset=self.brickset,
                    points_to_next_live=self.points_to_next_live,
                    live_factor=self.live_factor,
                )
        
        # Update powerups
        for powerup in self.powerups:
            powerup.update(dt)

            if powerup.collides(self.paddle):
                powerup.take(self)
                if type(powerup).__name__ == "CatchBall":
                    self.activated_powerups["CatchBall"] = powerup
                if type(powerup).__name__ == "CannonBall1":
                    self.activated_powerups["CannonBall1"] = powerup
                if type(powerup).__name__ == "CannonBall2":
                    self.activated_powerups["CannonBall2"] = powerup
                if type(powerup).__name__ == "LoseLife":
                    self.lives -= 1
                    if self.lives == 0:
                        self.state_machine.change("game_over", score=self.score)

        # Update persist powerups
        for powerup in self.activated_powerups.values():
            self.time = powerup.update_lifetime()
            if not powerup.is_active():
                powerup.deactivate(self)

        # Remove powerups that are not in play
        self.powerups = [p for p in self.powerups if p.in_play]

        # Remove persist powerups that are not actives
        self.activated_powerups = dict([p for p in self.activated_powerups.items() if p[1].is_active()])
        # Check victory
        if self.brickset.size == 1 and next(
            (True for _, b in self.brickset.bricks.items() if b.broken), False
        ):
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )

    def render(self, surface: pygame.Surface) -> None:
        heart_x = settings.VIRTUAL_WIDTH - 120

        i = 0
        # Draw filled hearts
        while i < self.lives:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][0]
            )
            heart_x += 11
            i += 1

        # Draw empty hearts
        while i < 3:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][1]
            )
            heart_x += 11
            i += 1

        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["tiny"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
        )
        if self.paddle.sticky:
            render_text(
                surface,
                f"Powerup: {self.time/100}",
                settings.FONTS["tiny"],
                settings.VIRTUAL_WIDTH - 200,
                5,
                (255, 255, 255),
            )
        if self.paddle.cannon and self.find_activated_powerups(["CannonBall1"]):
            render_text(
                surface,
                f"Shoots: {self.time}",
                settings.FONTS["tiny"],
                settings.VIRTUAL_WIDTH - 300,
                5,
                (255, 255, 255),
            )
        if self.paddle.cannon and self.find_activated_powerups(["CannonBall2", "CannonBall3"]):
            render_text(
                surface,
                f"Powerup: {self.time/100}",
                settings.FONTS["tiny"],
                settings.VIRTUAL_WIDTH - 200,
                5,
                (255, 255, 255),
            )

        self.brickset.render(surface)

        for powerup in self.activated_powerups.values():
            class_type = type(powerup).__name__
            if  class_type != "CatchBall" and class_type != "ConfettiBall":
                powerup.render_powerup(surface, self)

        self.paddle.render(surface)
        
        for ball in self.catched_balls:
            ball.render(surface)

        for ball in self.balls:
            ball.render(surface)

        for powerup in self.powerups:
            powerup.render(surface)

    def find_activated_powerups(self, list_names: list) -> bool:
        for name in list_names:
            if name in self.activated_powerups:
                return True

        return False
    
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            if input_data.pressed:
                self.paddle.vx = -settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx < 0:
                self.paddle.vx = 0
        elif input_id == "move_right":
            if input_data.pressed:
                self.paddle.vx = settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx > 0:
                self.paddle.vx = 0
        elif input_id == "enter":
            if input_data.released:
                for ball in self.catched_balls:
                    ball.release()
                    self.balls.append(ball)
                self.catched_balls = []
        elif input_id == "f":
            if self.activated_powerups.get("CannonBall1"):
                self.activated_powerups["CannonBall1"].shoot()
            elif self.activated_powerups.get("CannonBall2"):
                proyectiles = [b for b in self.balls if b.proyectile]
                if(len(proyectiles) == 0):
                    self.activated_powerups["CannonBall2"].recharge(self)    
            elif self.activated_powerups.get("CannonBall3"):
                self.activated_powerups["CannonBall3"].shoot()

            if input_data.pressed and self.paddle.cannon:
                for ball in self.projectiles:
                    self.balls.append(ball)
                self.projectiles = []
        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                level=self.level,
                score=self.score,
                lives=self.lives,
                paddle=self.paddle,
                balls=self.balls,
                catched_balls = self.catched_balls,
                brickset=self.brickset,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
                powerups=self.powerups,
                activated_powerups=self.activated_powerups,
                projectiles = self.projectiles,
            )
