import pygame
import random
import math

# Global settings
window_size = 800 
speed_multiplier = 1.0 
pygame.init()
window = pygame.display.set_mode((window_size, window_size))

# Particle class
class Particle:
    def __init__(self, x, y, color, properties):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.properties = properties
        self.energy = 0 
        self.creation_time = pygame.time.get_ticks()
        self.is_green = False  

    def apply_force(self, fx, fy):
        self.vx = (self.vx + fx) * 0.5
        self.vy = (self.vy + fy) * 0.5

    def move(self):
        global speed_multiplier
        self.x += self.vx * speed_multiplier
        self.y += self.vy * speed_multiplier
        if self.x <= 0 or self.x >= window_size:
            self.vx *= -1
        if self.y <= 0 or self.y >= window_size:
            self.vy *= -1

    def interact(self, other):
        if 'acid' in self.properties and 'base' in other.properties:
            if distance(self, other) < 10:
                self.color = (0, 255, 0)  # Change color to green
                other.color = (0, 255, 0)
                self.is_green = True
                other.is_green = True
                self.creation_time = pygame.time.get_ticks()
                other.creation_time = pygame.time.get_ticks()
                self.energy += 1
                other.energy += 1

    def check_half_life(self):
        half_life = 15000  # 15 seconds in milliseconds
        current_time = pygame.time.get_ticks()
        if self.is_green and (current_time - self.creation_time) > half_life:
            # Splitting logic
            return True
        return False
    
    def check_life_cycle(self):
        if self.energy > 10: 
            # Implement particle creation or destruction logic
            pass

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)

# Utility functions
def randomxy():
    return round(random.random() * window_size + 1)

def create_particles(number, color, properties):
    return [Particle(randomxy(), randomxy(), color, properties) for _ in range(number)]

def distance(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return math.sqrt(dx*dx + dy*dy)

def interaction_force(a, b, g):
    d = distance(a, b)
    if 0 < d < 80:
        force_magnitude = g / d
        dx = (a.x - b.x) / d
        dy = (a.y - b.y) / d
        return force_magnitude * dx, force_magnitude * dy
    return 0, 0

# Main simulation function
def simulate(particles, g):
    new_particles = []
    for a in particles:
        fx, fy = 0, 0
        for b in particles:
            if a != b:
                dfx, dfy = interaction_force(a, b, g)
                fx += dfx
                fy += dfy
                a.interact(b)
        a.apply_force(fx, fy)
        a.move()
        a.check_life_cycle()
        if a.check_half_life():
            # Create new red and yellow particles at the same location
            new_particles.append(Particle(a.x, a.y, (255, 0, 0), ['base']))
            new_particles.append(Particle(a.x, a.y, (255, 255, 0), ['acid']))
            particles.remove(a)  # Remove the original green particle
    particles.extend(new_particles)  # Add new particles to the list

# Create particles
yellow_particles = create_particles(100, (255, 255, 0), ['acid'])
red_particles = create_particles(100, (255, 0, 0), ['base'])

# Main loop
run = True
while run:
    window.fill(0)
    all_particles = yellow_particles + red_particles
    simulate(all_particles, -0.1)
    for particle in all_particles:
        particle.draw(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                speed_multiplier = 1.0  # Normal speed
            elif event.key == pygame.K_2:
                speed_multiplier = 1.5  # 1.5x speed
            elif event.key == pygame.K_3:
                speed_multiplier = 2.0  # 2x speed

    pygame.display.flip()

pygame.quit()