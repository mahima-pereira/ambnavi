import random
import math
import time
import threading
import pygame
import sys
import os

defaultRed = 150
defaultYellow = 5
defaultGreen = 20
defaultMinimum = 10
defaultMaximum = 60

signals = []
noOfSignals = 4
simTime = 300
timeElapsed = 0

currentGreen = 0
nextGreen = (currentGreen + 1) % noOfSignals
currentYellow = 0

carTime = 2
bikeTime = 1
rickshawTime = 2.25
busTime = 2.5
truckTime = 2.5
ambulance = 3.0

noOfCars = 0
noOfBikes = 0
noOfBuses = 0
noOfTrucks = 0
noOfRickshaws = 0
noOfLanes = 2
noofambulance = 0


detectionTime = 5

speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'rickshaw': 2, 'bike': 2.5}

x = {'right': [0, 0, 0], 'down': [755, 727, 697], 'left': [1400, 1400, 1400], 'up': [602, 627, 657]}
y = {'right': [348, 370, 398], 'down': [0, 0, 0], 'left': [498, 466, 436], 'up': [800, 800, 800]}

vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
            'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}
vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'rickshaw', 4: 'bike',5:'ambulance'}
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]
signalTimerCoods = [(530, 210), (810, 210), (810, 550), (530, 550)]
vehicleCountCoods = [(480, 210), (880, 210), (880, 550), (480, 550)]
vehicleCountTexts = ["0", "0", "0", "0"]

stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stops = {'right': [580, 580, 580], 'down': [320, 320, 320], 'left': [810, 810, 810], 'up': [545, 545, 545]}

mid = {'right': {'x': 705, 'y': 445}, 'down': {'x': 695, 'y': 450}, 'left': {'x': 695, 'y': 425},
       'up': {'x': 695, 'y': 400}}
rotationAngle = 3

gap = 15
gap2 = 15

pygame.init()
simulation = pygame.sprite.Group()


class TrafficSignal:
    def __init__(self, red, yellow, green, minimum, maximum):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.minimum = minimum
        self.maximum = maximum
        self.signalText = "30"
        self.totalGreenTime = 0


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.willTurn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        vehicles[direction][lane].append(self)

        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.originalImage = pygame.image.load(path)
        self.currentImage = pygame.image.load(path)

        if direction == 'right':
            if len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0:
                self.stop = vehicles[direction][lane][self.index - 1].stop - \
                            vehicles[direction][lane][self.index - 1].currentImage.get_rect().width - gap
            else:
                self.stop = defaultStop[direction]

            temp = self.currentImage.get_rect().width + gap
            x[direction][lane] -= temp
            stops[direction][lane] -= temp

        elif direction == 'left':
            if len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0:
                self.stop = vehicles[direction][lane][self.index - 1].stop + \
                            vehicles[direction][lane][self.index - 1].currentImage.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]

            temp = self.currentImage.get_rect().width + gap
            x[direction][lane] += temp
            stops[direction][lane] += temp

        elif direction == 'down':
            if len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0:
                self.stop = vehicles[direction][lane][self.index - 1].stop - \
                            vehicles[direction][lane][self.index - 1].currentImage.get_rect().height - gap
            else:
                self.stop = defaultStop[direction]

            temp = self.currentImage.get_rect().height + gap
            y[direction][lane] -= temp
            stops[direction][lane] -= temp

        elif direction == 'up':
            if len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0:
                self.stop = vehicles[direction][lane][self.index - 1].stop + \
                            vehicles[direction][lane][self.index - 1].currentImage.get_rect().height + gap
            else:
                self.stop = defaultStop[direction]

            temp = self.currentImage.get

