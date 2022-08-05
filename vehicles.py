import pygame
import random

class Particle:

    def __init__(self, b=1, x=None, y=None, color=(200, 200, 200), real_color=True):
        if x is None and y is None:
            self.position = pygame.Vector2(random.uniform(0, 900), random.uniform(0, 900))
        else: 
            self.position = pygame.Vector2(x, y)
        self.initial_position = pygame.Vector2(self.position)
        self.velocity = pygame.Vector2()
        self.real_color = real_color
        self.b = b
        self.color = color
        self.acceleration = pygame.Vector2()
        self.maxspeed = 4
        self.maxforce = 1.5
        self.flag_on_move = True
        # self.velocity = self.velocity.normalize() * self.maxspeed

    def apply_force(self, force):
        self.acceleration += force
        self.update_move(self.maxspeed)
    
    def limit(self, limit_value, vector):
        if vector.magnitude_squared() > limit_value * limit_value:
            try:
                return (vector.normalize()) * limit_value
            except:
                return pygame.Vector2()
        else:
            return vector

    def update_move(self, maxspeed=20):
        self.velocity += self.acceleration

        # Limit is maxspeed
        self.velocity = self.limit(maxspeed, self.velocity)

        # Update location with new velocity
        self.position += self.velocity

        # Boundary condition (depende da posição)
        #self.periodic_boundary()
        
        # Set zero acceleration
        self.acceleration = self.acceleration * 0

        if self.position != self.initial_position:
            self.flag_on_move = False
        else:
            self.flag_on_move = True

    def seek(self, target):
        # Calculate desired
        desired = target - self.position
        D = pygame.Vector2(desired)
        try:
            desired = desired.normalize() * self.maxspeed
        except:
            desired = pygame.Vector2()

        # Calculate steer (Craig Raynolds classic vehicle)
        # steering = desired - velocity
        steer = desired - self.velocity

        # Limit steer
        steer = self.limit(self.maxforce, steer)

        # if D.magnitude_squared() < 900:
        #     steer = pygame.Vector2()
        if D.magnitude_squared() < 30:
            self.position = pygame.Vector2(self.initial_position)
            self.velocity = pygame.Vector2()
            self.acceleration = pygame.Vector2()
            steer = pygame.Vector2()
    
        return self.apply_force(steer/2)
    
    def repulsion(self, position):
        neg_desired = position - self.position
        try:
            neg_desired = neg_desired.normalize() * self.maxspeed 
        except:
            neg_desired = pygame.Vector2()
        
        steer = neg_desired - self.velocity
        steer = self.limit(self.maxforce, steer)
        return self.apply_force((-steer / self.b))

