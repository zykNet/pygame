# -*- coding: utf-8 -*-
__author__ = 'zyk'

import pygame
import sys
from random import randint
from pygame.locals import *
from gameobjects import vector2 as vector2
from math import  *
SCREEN_SIZE = (640, 640)
ANT_COUNT = 10
NEST_SIZE = 10
NEST_POSITION =(100,300)
class GameEntity(object):
    def __init__(self, name, img):
        self.name = name
        self.img = img
        self.speed = 0
        self.id = 0
        self.location = vector2(50, 50)
        self.destination = vector2(0, 0)
        self.mind =State_machine()
    def render(self, surface):
        #world。process调用
        surface.blit(self.img, self.location)
        # print self.location,'1'
    def process(self, time_passed):
        #world。process调用
        self.mind.think()
        vecToDestination = self.destination - self.location
        heading = vecToDestination.get_normalized()

        distance = time_passed * self.speed
        # print self.destination,'2'
        self.location += distance*heading


class World(object):
    def __init__(self):
        self.entities = {} # id:obj
        self.entity_id = 0

        self.background = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        self.background.fill((255, 255, 255))
        pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, int(NEST_SIZE))
    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        #自动加id，，automatic id
        entity.id = self.entity_id
        self.entity_id += 1
    def remove_entity(self,entity):
        del self.entities[entity.id]

    def process(self, time_passed, surface):
        pass#需要时间和画面，
        self.background.fill((255, 255, 255))
        pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, int(NEST_SIZE))#nest is picture^_^
        surface.blit(self.background, (0, 0))#不太懂。。。
        for entity in self.entities.values():
            entity.process(time_passed)
            entity.render(surface)
def get_close_entity(name, entity, range=100.):
    '''name, entity, -> tg_entity'''
    try:
        location = entity.location
    except:
        location = entity#location两种都行
    for tg_entity in world.entities.values():
        if tg_entity.name == name:
            if tg_entity.location.get_distance_to(location) < range:
                return tg_entity
    return None
def get_entity(entity_id):
        """id -> class"""
        if entity_id in world.entities.keys():
            return world.entities[entity_id]
        else:
            return None

class State():
    def __init__(self, name):
        self.name = name
    def do_action(self):
        pass
    def check_station(self):
        pass
    def entry_action(self):
        pass
    def exit_action(self):
        pass
class State_machine():
    def __init__(self):
        self.states = {}#name:class
        self.active_state = None
    def add_state(self, State):
        self.states[State.name] = State
    def think(self):
        if self.active_state is None:
            return
        self.active_state.do_action()
        new_state = self.active_state.check_station()
        if new_state is not None:
            self.set_state(new_state)
    def set_state(self,new_state):
        if self.active_state is not None:
            self.active_state.exit_action()
        self.active_state = self.states[new_state]
        self.active_state.entry_action()
        # print self.active_state

class Leaf(GameEntity):
    def __init__(self, img):
        GameEntity.__init__(self, 'leaf', img)
class Spider(GameEntity):
    def __init__(self,img):
        GameEntity.__init__(self,'spider',img)
        self.health = 25
        self.left = False
    def render(self, surface):
        surface.blit(self.img, self.location)
        x, y = self.location
        w, h = self.img.get_size()
        surface.fill( (255, 0, 0), (x+10, y+h, 25, 4))
        surface.fill( (0, 255, 0), (x+10, y+h, self.health, 4))
    def process(self,time_passed):
        if  self.left == False:
            self.destination = NEST_POSITION
            self.speed = 30 + randint(-10, 30)
            if self.location.get_distance_to(NEST_POSITION) < 5:
                self.left = True
        else:
            if self.destination == NEST_POSITION:
                exit = [(0,0), (0,640), (640,0), (640, 640)]
                self.destination = exit[randint(0,3)]
            self.speed = 60 + randint(-10, 30)
            if self.location.get_distance_to((0, 0)) < 5:
                world.remove_entity(self)
        vecToDestination = self.destination - self.location
        heading = vecToDestination.get_normalized()

        distance = time_passed * self.speed
        # print self.destination,'2',self.location
        self.location += distance*heading


class Ant(GameEntity):
    def __init__(self, img):
        GameEntity.__init__(self, 'ant', img)#self?
        exploring_state = AntStateExploring(self)#?????????self
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)
        self.mind.add_state(exploring_state)
        self.mind.add_state(seeking_state)
        self.mind.add_state(delivering_state)
        self.mind.add_state(hunting_state)

        self.leaf_id = None
        self.spider = None
        self.carry_img = None
    def deliver(self, img):
        self.carry_img = img
    def drop(self):
        self.carry_img = None
        # self.leaf_id = None#????????????????????????????原来没有。。。。
    def render(self, surface):
        if self.carry_img == None:
            surface.blit(self.img, self.location)
        else:
            w, h = self.carry_img.get_size()
            x, y = self.location
            surface.blit(self.carry_img, (x+w/2, y-h/2))
            surface.blit(self.img, self.location)
class Antx(Ant):
    def __init__(self, img):
        Ant.__init__(self, img)
        self.x = True
        x_state = AntStatex(self)
        self.mind.add_state(x_state)
    def render(self, surface):
        x, y = self.location
        w, h = self.img.get_size()
        if self.carry_img == None:
            surface.blit(self.img, self.location)
        else:
            w, h = self.carry_img.get_size()
            x, y = self.location
            surface.blit(self.carry_img, (x+w/2, y-h/2))
            surface.blit(self.img, self.location)
        if self.x:
            surface.fill( (255, 0, 0), (x+w, y+h/4, 4, 4))
            # surface.fill( (0, 255, 0), (x+10, y+h, self.health, 4))

class AntStatex(State):
    def __init__(self, ant):
        State.__init__(self,"Antx")#self??
        self.ant = ant
    def do_action(self):
        pressed_keys = pygame.key.get_pressed()

        x, y = self.ant.location
        self.ant.speed = 1
        if pressed_keys[K_w]:
            y-=10
            self.ant.speed = 50
        if pressed_keys[K_s]:
            y+=10
            self.ant.speed = 50
        if pressed_keys[K_a]:
            x-=10
            self.ant.speed = 50
        if pressed_keys[K_d]:
            x+=10
            self.ant.speed = 50

        if pressed_keys[K_SPACE]:
            leaf =  get_close_entity('leaf', self.ant, 30)
            print leaf, self.ant.leaf_id

            try:
                if self.ant.leaf_id == None:
                    self.ant.leaf_id = leaf.id
                    self.ant.deliver(leaf.img)
                    world.remove_entity(leaf)
                else:
                    if vector2(*NEST_POSITION).get_distance_to(self.ant.location) < NEST_SIZE:
                        self.ant.drop()
                        self.ant.leaf_id = None
            except:
                pass
        # --------------------------------------------
        self.ant.destination = vector2(x+1, y)#???????????????????????



class AntStateExploring(State):

    def __init__(self, ant):
        State.__init__(self,"exploring")#self????????????????????
        self.ant = ant
    def do_action(self):
        god = randint(1, 40)
        if god == 1 or god == 2:
            self.random_destination()
        elif god == 3:
            self.ant.destination = (600, 600)
    def check_station(self):
        leaf = get_close_entity('leaf',self.ant)
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return "seeking"
        spider = get_close_entity('spider',NEST_POSITION,range= 10)
        if spider is not None:
            self.ant.spider_id = spider.id
            return "hunting"
        return None
    def entry_action(self):
        self.random_destination()
        self.ant.speed=100 + randint(-30, 50)
    def exit_action(self):
        pass
    def random_destination(self):
        w, h = SCREEN_SIZE
        self.ant.destination = vector2(randint(0, w), randint(0, h))

class AntStateSeeking(State):
    def __init__(self, ant):
        State.__init__(self,"seeking")#self??
        self.ant = ant #??
    def do_action(self):
        pass
    def check_station(self):
        '''return  -> new statiion'''
        leaf = get_entity  (self.ant.leaf_id)
        if leaf is  None:
            return 'exploring'
        if leaf.location.get_distance_to(self.ant.location) < 5:
            self.ant.deliver(leaf.img)
            world.remove_entity(leaf)
            return "delivering"
        return None
    def entry_action(self):
        leaf = get_entity(self.ant.leaf_id)
        if leaf is not None:
            self.ant.destination = leaf.location

    def exit_action(self):
        pass
class AntStateDelivering(State):
    def __init__(self, ant):
        State.__init__(self,"delivering")#self??
        self.ant = ant
    def do_action(self):
        pass
    def check_station(self):
        if vector2(*NEST_POSITION).get_distance_to(self.ant.location) < NEST_SIZE:
            if (randint(1, 1) == 1):
                self.ant.drop()
                return "exploring"
        return None
    def entry_action(self):
        self.ant.speed = 30+randint(5, 30)
        self.ant.destination = NEST_POSITION

    def exit_action(self):
        pass
class AntStateHunting(State):
    def __init__(self, ant):
        State.__init__(self,"hunting")#self??
        self.ant = ant #??
    def do_action(self):
        spider = get_close_entity('spider',self.ant.location,range= 30)
        if spider is not None:
            if spider.destination != NEST_POSITION:
                self.ant.spider_id = spider.id
    def check_station(self):
        spider = get_entity  (self.ant.spider_id)
        if spider is  None:
            return 'exploring'
        if spider.location.get_distance_to(self.ant.location) < 5:
            if spider.health <= 0:
                self.ant.deliver(spider.img)
                world.remove_entity(spider)
                return "delivering"
            else:
                spider.health -= randint(3, 6)
        return None
    def entry_action(self):
        spider = get_entity(self.ant.spider_id)
        if spider is  not None:
            self.ant.destination = spider.location
    def exit_action(self):
        pass
# **********run*************************************

pygame.init()



world = World()
w, h = SCREEN_SIZE
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
ant_image = pygame.image.load("ant.png").convert_alpha()
leaf_image = pygame.image.load("leaf.png").convert_alpha()
spider_image = pygame.image.load("spider.png").convert_alpha()

for ant_No in xrange(ANT_COUNT):
    ant = Ant(ant_image)
    ant.location = vector2(randint(0, w), randint(0, h))
    ant.mind.set_state("exploring")
    world.add_entity(ant)
me = Antx(ant_image)
me.location = vector2(randint(0, w), randint(0, h))
me.mind.set_state("Antx")
world.add_entity(me)
# spider = Spider(spider_image)
# spider.location = vector2(randint(0, w), randint(0, h))
# world.add_entity(spider)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    time_passed = clock.tick(30)

    if randint(1, 10) == 1:
        leaf = Leaf(leaf_image)
        leaf.location = vector2(randint(0, w), randint(0, h))
        world.add_entity(leaf)
    if randint(1, 50) == 1:
        spider = Spider(spider_image)
        spider.location = vector2(randint(0, w), randint(0, h))
        world.add_entity(spider)
    world.process(time_passed*1.0/1000, screen)


    pygame.display.update()