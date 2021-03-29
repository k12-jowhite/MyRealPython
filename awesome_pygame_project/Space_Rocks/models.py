from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import (
    get_random_velocity,
    get_angle_modifier,
    load_sound,
    load_sprite,
    wrap_position
)

UP = Vector2(0, -1)

class GameObject :
    def __init__(self, position, sprite, velocity) :
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        
    def draw(self, surface) :
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)
        
    def move(self, surface) :
        self.position = wrap_position(self.position + self.velocity, surface)
        
    def collides_with(self, other_obj) :
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
        
class Spaceship(GameObject) :    
    MANEUVERABILITY = 3
    ACCELERATION = 0.1
    DECELERATION = 0.1
    MIN_SPEED = 0
    MAX_SPEED = 5
    BULLET_SPEED = 3
    SHIELD_MAX = 10
    def __init__(self, position, create_bullet_callback) :
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.shield = self.SHIELD_MAX
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("spaceship"), Vector2(0))
        
    def rotate(self, clockwise=True) :
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
        
    def draw(self, surface) :
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
    
    def accelerate(self) :
        self.velocity += self.direction * self.ACCELERATION
        if self.velocity.length() > self.MAX_SPEED :
            self.velocity.scale_to_length(self.MAX_SPEED)

    def decelerate(self) :
        if not self.velocity == (self.MIN_SPEED, self.MIN_SPEED) :
            dec_factor = self.velocity.x * self.DECELERATION
            self.velocity.x = self.MIN_SPEED if self.velocity.x == self.MIN_SPEED else (
                self.velocity.x - dec_factor
            )
            dec_factor = self.velocity.y * self.DECELERATION
            self.velocity.y = self.MIN_SPEED if self.velocity.y == self.MIN_SPEED else (
                self.velocity.y - dec_factor
            )
        print(self.velocity)
    
    def lose_shield(self) :
        self.shield -= 1
    
    def shoot(self) :
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()
        
class Asteroid(GameObject) :
    SPLITS_INTO = 2
    def __init__(self, position, create_asteroid_callback, size=3, vector=None) :
        self.create_asteroid_callback = create_asteroid_callback
        self.direction = vector if vector else get_random_velocity(1, 3)
        self.size = size
        size_to_scale = {
            3:1,
            2:0.5,
            1:0.25,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)
        trajectory = self.direction
        super().__init__(
            position, sprite, trajectory
        )
    
    def split(self) :
        if self.size > 1 :
            for _ in range(self.SPLITS_INTO) :
                asteroid = Asteroid(
                    self.position, 
                    self.create_asteroid_callback, 
                    self.size - 1
                )
                self.create_asteroid_callback(asteroid)
                
    def reflect(self, ship_vector) :
        ACC_FACTOR = 2
        curr_velocity = ship_vector.length()
        new_velocity = curr_velocity * ACC_FACTOR
        if self.size > 1 :
            for a in range(self.SPLITS_INTO) :
                angle_modifier = get_angle_modifier()
                if a % 2 :
                    new_angle = (
                        -ship_vector.x - angle_modifier,
                        -ship_vector.y + angle_modifier
                    )
                else :
                    new_angle = (
                        ship_vector.x - angle_modifier,
                        -ship_vector.y + angle_modifier
                    )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                print(new_angle)
                new_vector = ship_vector.reflect(new_angle)
                new_vector = new_vector.scale_to_length(new_velocity)
                asteroid = Asteroid(
                    self.position, 
                    self.create_asteroid_callback, 
                    self.size - 1,
                    new_vector
                )
                self.create_asteroid_callback(asteroid)
                print(asteroid.direction.angle_to(UP))

class Bullet(GameObject) :
    def __init__(self, position, velocity) :
        super().__init__(position, load_sprite("bullet"), velocity)
    
    def move(self, surface) :
        self.position = self.position + self.velocity