import pygame
import time

from models import Asteroid, Spaceship, Shield
from utils import get_random_position, load_sprite, print_text

class SpaceRocks :
    MIN_ASTEROID_DISTANCE = 250
    ASTEROID_VALUE = 100
    BONUS = 10
    BONUS_VALUE = 1000
    
    def __init__(self) :
        self._init_pygame()
        self.game_status = 1
        self.screen = pygame.display.set_mode((800,600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message_1 = ""
        self.message_2 = ""
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.shields = Shield(self.spaceship)
        self.player_score = 0
        self.bonus_count = 0
        for _ in range(6) :
            while True :
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ) :
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))
        
    def main_loop(self) :
        while True :
            self._handle_input()
            self._process_game_logic()
            self._draw()
                
    def _init_pygame(self) :
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        
    def _get_game_objects(self) :
        game_objects = [*self.asteroids, *self.bullets,]
        if self.spaceship :
            game_objects.append(self.spaceship)
            game_objects.append(self.shields)
        return game_objects

    def _handle_input(self) :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ) :
                quit()
            elif (
                self.game_status == 1
                and self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ) :
                self.spaceship.shoot()
            elif (
                self.spaceship
                and event.type == pygame.KEYUP
                and event.key == pygame.K_p
            ) :
                self.game_status = -1 if self.game_status == 1 else 1
        is_key_pressed = pygame.key.get_pressed()
        if self.spaceship and self.game_status == 1 :
            if is_key_pressed[pygame.K_RIGHT] :
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT] :
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP] :
                self.spaceship.accelerate()
            if is_key_pressed[pygame.K_DOWN] :
                self.spaceship.decelerate()  
    
    def _game_paused(self) :
        timer = 0
        print("Paused Game")
        while self.game_status == -1 :
            timer += 1
            self.message_1 = "GAME PAUSED"
            self.message_2 = f"{timer}"
            self._draw()
            time.sleep(1)
            self._handle_input()
        self.message_1 = ""
        self.message_2 = ""
        print("Resumed Game")
    
    def _process_game_logic(self) :
        for game_object in self._get_game_objects() :
            game_object.move(self.screen)
        if self.spaceship :
            self.shields.update(self.spaceship)  
            for asteroid in self.asteroids :
                if asteroid.collides_with(self.spaceship) :
                    print("Shields @ " + str(self.shields.strength))
                    self.bonus_count = 0
                    if self.shields.strength == 0 :
                        self.spaceship = None
                        self.game_status = 0
                        self.message_1 = "You lost!"
                        break
                    else :
                        for _ in range(asteroid.size * 2) :
                            self.spaceship.decelerate()
                        self.shields.decrease_shield(self.spaceship)
                        self.asteroids.remove(asteroid)
                        asteroid.reflect(
                            self.spaceship.direction,
                        )
        for bullet in self.bullets[:] :
            for asteroid in self.asteroids[:] :
                if asteroid.collides_with(bullet) :
                    self.player_score += self.ASTEROID_VALUE // asteroid.size
                    self.bonus_count += 1
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
        for bullet in self.bullets[:] :
            if not self.screen.get_rect().collidepoint(bullet.position) :
                self.bullets.remove(bullet)
        if self.bonus_count == self.BONUS :
            self.player_score += self.BONUS_VALUE
            self.shields.increase_shield(self.spaceship)
            self.bonus_count = 0
        if not self.asteroids and self.spaceship :
            self.game_status = 0
            self.message_1 = "You won!"
        if self.game_status == -1 :
            self._game_paused()
    
    def _draw(self) :
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects() :
            game_object.draw(self.screen)
        print_text(
            self.screen,
            str(self.player_score),
            self.font,
            elev="top",
            align="right",
            color="white"
        )
        if self.message_1 :
            print_text(self.screen, self.message_1, self.font)
        if self.message_2 :
            print_text(self.screen, self.message_2, self.font, line=2)
        pygame.display.flip()
        self.clock.tick(60)