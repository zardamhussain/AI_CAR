
import math
import random
import os
import sys
import pygame
import copy
import numpy as np

from brain import NeuralNetwork

WIDTH = 1920 / 1.25
HEIGHT = 1080 / 1.25

CAR_SIZE_X = 60 / 1.25
CAR_SIZE_Y = 60 / 1.25
CAR_POS_X = 820 / 1.25
CAR_POS_Y = 920 / 1.25

BORDER_COLOR = (255, 255, 255, 255)

POPULATION_SIZE = 3
MUTATION_RATE = 0.05
ELITE_COUNT = 2

# --- Genetic Algorithm Functions ---
def crossover(parent1, parent2):
    child_weights = []
    for w1, w2 in zip(parent1, parent2):
        mask = np.random.rand(*w1.shape) > 0.5
        child = np.where(mask, w1, w2)
        child_weights.append(child)
    return child_weights

def mutate(weights, rate=MUTATION_RATE):
    new_weights = []
    for w in weights:
        mutation_mask = np.random.rand(*w.shape) < rate
        mutation = np.random.randn(*w.shape) * mutation_mask
        new_weights.append(w + mutation)
    return new_weights

# --- Car Class (add weights getter/setter) ---
class Car:
    MIN_SPEED = 2.0
    MAX_SPEED = 4.0
    FINISH_LINE_RECT = pygame.Rect(WIDTH // 2 - 20, 100, 40, 40)
    LAP_COOLDOWN_FRAMES = 30  # Must leave finish area for at least 30 frames
    
    def __init__(self):
        self.img = pygame.image.load('car.png').convert()
        self.img = pygame.transform.scale(self.img, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_img = self.img
        self.pos = [CAR_POS_X, CAR_POS_Y]
        self.center = [ self.pos[0] + 0.5 * CAR_SIZE_X, self.pos[1] + 0.5 * CAR_SIZE_Y ]
        self.angle = 0
        self.speed = 4.0
        self.radar = []
        self.drawing_radars = []
        self.alive = True
        self.distance = 0
        self.time = 0
        self.speed_set = False
        self.lap_complete = False
        self.lap_cooldown = 0
        self.brain = NeuralNetwork(5, 8, 4)
        self.fitness = 0

    def get_weights(self):
        return self.brain.get_weights()

    def set_weights(self, weights):
        self.brain.set_weights(weights)

    def draw(self, screen):
        pixel_rect = self.rotated_img.get_bounding_rect()
        screen.blit(self.rotated_img, self.pos, pixel_rect)
        self.draw_radar(screen)



    def collison(self, game_map):
        self.alive = True

        for point in self.corners :
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                return True

        return False

    def update(self, game_map):

        if not self.speed_set:
            self.speed = 4.0  # Lower default speed, use float
            self.speed_set = True

        if self.time % 60 == 0:
            self.distance += 1

        self.rotated_img = self.rotate_center(self.img, self.angle)
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed

        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.center = [ self.pos[0] + 0.5 * CAR_SIZE_X, self.pos[1] + 0.5 * CAR_SIZE_Y ]

        # Clamp speed to min and max
        self.speed = max(self.MIN_SPEED, min(self.speed, self.MAX_SPEED))

        # Lap completion check with cooldown
        if self.FINISH_LINE_RECT.collidepoint(self.center[0], self.center[1]):
            if not self.lap_complete and self.lap_cooldown == 0:
                self.lap_complete = True
                print("Lap completed!")
        else:
            if self.lap_complete:
                self.lap_cooldown = self.LAP_COOLDOWN_FRAMES
                self.lap_complete = False
        if self.lap_cooldown > 0:
            self.lap_cooldown -= 1

        length = 0.75 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        if self.collison(game_map):
            self.alive = False

        self.radar.clear()

        for d in range(-90, 120, 45):
            self.check_rader(d, game_map)
        self.time += 1
        # Fitness: distance + lap bonus
        self.fitness = self.distance + (1000 if self.lap_complete else 0)

    def draw_radar(self, screen):
        for radar in self.radar:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_rader(self, angle, game_map):
        length  = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + angle))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + angle))) * length)

        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + angle))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + angle))) * length)

        dist = math.sqrt(math.pow(x-self.center[0], 2) + math.pow(y-self.center[1], 2))
        self.radar.append([(x, y), dist])

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def get_data(self):
        radars = self.radar
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def predict(self):
        return self.brain.predict(self.get_data())


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

clock = pygame.time.Clock()
game_map = pygame.image.load('map.png').convert()
game_map = pygame.transform.scale(game_map, (WIDTH, HEIGHT))
alive_font = pygame.font.SysFont("Arial", 20)

# --- Main Genetic Algorithm Loop ---
def next_generation(old_cars):
    # Sort by fitness
    sorted_cars = sorted(old_cars, key=lambda c: c.fitness, reverse=True)
    print(f"Best fitness: {sorted_cars[0].fitness}")
    new_cars = []
    # Elitism: keep best
    for i in range(ELITE_COUNT):
        elite = Car()
        elite.set_weights(sorted_cars[i].get_weights())
        new_cars.append(elite)
    # Generate rest by crossover/mutation
    while len(new_cars) < POPULATION_SIZE:
        parent_pool = sorted_cars[:max(2, POPULATION_SIZE//2)]
        parent1, parent2 = np.random.choice(parent_pool, 2, replace=False)
        child = Car()
        child_weights = crossover(parent1.get_weights(), parent2.get_weights())
        child_weights = mutate(child_weights)
        child.set_weights(child_weights)
        new_cars.append(child)
    return new_cars

# --- Main Loop ---
cars = [Car() for _ in range(POPULATION_SIZE)]
generation = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    screen.blit(game_map, (0, 0))
    # pygame.draw.rect(screen, (255, 0, 0), Car.FINISH_LINE_RECT, 2)  # Removed red box
    alive_count = 0
    for car_idx, car in enumerate(cars):
        if car.alive and not car.lap_complete:
            output = list(car.predict()[0])
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10
            elif choice == 1:
                car.angle -= 10
            elif choice == 2:
                if(car.speed - 2 >= 4.0):
                    car.speed -= 2
                    car.speed = max(car.MIN_SPEED, min(car.speed, car.MAX_SPEED))
            else:
                car.speed += 2
                car.speed = max(car.MIN_SPEED, min(car.speed, car.MAX_SPEED))
            car.update(game_map)
            car.draw(screen)
            # Draw car specs in a different color (e.g., blue)
            specs_text = alive_font.render(f"Car {car_idx+1} | Speed: {car.speed:.2f} | Dist: {car.distance} | Fit: {car.fitness}", True, (255, 0, 0))
            specs_rect = specs_text.get_rect()
            specs_rect.center = (int(car.center[0]), int(car.center[1]) - 50)
            screen.blit(specs_text, specs_rect)
            alive_count += 1
            
    text = alive_font.render(f"Generation: {generation}  Alive: {alive_count}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (900, 30)
    screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(60)
    # If all cars are dead or finished, evolve
    if alive_count == 0:
        cars = next_generation(cars)
        generation += 1
        # Reset map for new generation
        screen.blit(game_map, (0, 0))
        pygame.display.flip()
