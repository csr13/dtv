# Copyright 2020 C. Sanchez Roman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import os
import random
import time
import pdb

import pygame
from pygame.locals import *

from characters import *
from config import SCREENRECT
from utils import load_image, Img, writer

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#
# Initial setup
#
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(10, 100)
screen = pygame.display.set_mode(SCREENRECT.size)
pygame.display.set_caption(" Slip the Virus ")

Img.background = load_image("background.gif")
background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, Img.background.get_width()):
    background.blit(Img.background, (x, 0))
background_rect = background.get_rect()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#
# The key master, holder.
#
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

holder = Holder(
    unicorn=Unicorn("unicorn.png", spawn_location={"midleft": (50, 640 // 2)}),
    virus_holder=[],
    stats=StatsBar(),
)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#
# Main Loop
#
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


while holder.unicorn.alive == bool(1):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Check to see if the rest of the loop will execute, this happens because
    # we are checking to see if the death scene has a;ready happend.
    # here we cset the final pointage, we can that to be the first otherwise we
    # can leak points, the we send the kill signal to the main loop.
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    if holder.unicorn.dead_scene_time <= 0:
        holder.stats.final_points = holder.stats.get_current_game_time()
        holder.unicorn.alive = False

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Handle the background first
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    holder.dirtyrects.append(screen.blit(background, (0, 0)))

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Evaluate vents & keys pressed
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    for event in pygame.event.get():
        pygame.event.pump()
        key = pygame.key.get_pressed()
        holder.unicorn.state(key, screen)

        if key[K_ESCAPE]:
            exit(1)

        if event.type == pygame.QUIT:
            exit(1)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Here, within this if block we index the virus that collided with
    # the user object, the Unicorn.
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    x_x = holder.unicorn.rect.collidelist(holder.virus_holder)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # If a collision was found, then execute the following
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    if x_x != -1:

        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #
        # If the virus holder is dead then pass, because the virus was already dead
        # nothing more to do here.
        #
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        
        if holder.virus_holder[x_x].dead:
            pass

        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #
        # If the unicorn had its shield activated when it collided with the virus
        #
        #   1) Signal the virus that it needs to be removed
        #   2) Increment the viruses eliminated count by one.
        #
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

        elif holder.unicorn.shield == True:
            holder.virus_holder[x_x].dead = True
            holder.stats.viruses_eliminated += 1

        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #
        # If the unicorn did not have its shield on when the collision happened
        # a couple of things will happen.
        #
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #
        #   1) If the unicorn has no health.
        #
        #       1.1) Set the dead status of the unicorn to True,
        #            This does a couple of things, first it sends a signal to the
        #            unicorn.update() (called later) method which indicates that
        #            the unicorn death scene count needs to decrement by one.
        #
        #       1.2) Initiate te unicorn death scene, which relays on a a count
        #            to orchestrate it's duration.
        #
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #
        #   2) If the unicorn has health, then a couple of things will happen.
        #       
        #       2.1) Send a signal to the unicorn instance that a hit occured.
        #            This signal decrements the instance health by 5 points.
        #
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

        elif holder.unicorn.shield == False:

            if not holder.unicorn.health_ok():
                holder.unicorn.dead = True
                holder.unicorn.death_scene()

            else:
                holder.unicorn.hit = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Update Viruses
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    # 
    # First we roll some odds for if a new virus will appear.
    #
    #   1) append a new virus instance to the virus holder list.
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # First loop is important, we update all the viruses, this does a couple of 
    # things.
    #
    #   1) It checks the boundaries of the virus y axis with respect to the screen
    #   2) It checks for a signal to see if the virus is dead and we need to
    #      initiate a decremental count for the death scene duriation.
    #   3) It increments the virus instance x coordinate, for movement.
    #   4) It checks to see if there are any viruses off the screen, and pops them
    #      it also directs the virus.
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Second loop draws all the updated batch of viruses, using it draw method
    # 
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Third loop checks does a couple of things
    #   1) It checks to see if the virus is dead, and if its time scene count
    #      has finished, and if True then;
    #       1.1) It calls its own method to erase the instance from the screen.
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    if not int(random.random() * 12):
        holder.virus_holder.append(Virus("virus.gif"))

    for host in holder.virus_holder:
        host.update(holder)

    for host in holder.virus_holder:
        host.draw(screen, holder)

    for host in holder.virus_holder:
        if host.dead and host.death_scene_time < 0:
            host.erase(screen, background, holder)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Update Unicorn & draw Unicorn
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    holder.unicorn.update(screen, holder)
    holder.unicorn.draw(screen, holder)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Update the stats
    #
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    holder.stats.update(screen, holder)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #
    # Update display by passing the list of dirty rects collecred by each of the
    # draw and earase methods of the instances that where manipulated.
    # Set frames pre second with clock.tick, by default, nice.
    # 
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    pygame.display.update(holder.dirtyrects)
    holder.reset_dirtyrects()
    clock.tick(69)

print(
f"""
+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 

Game stats (*_*)

+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 

Total time lasted        => {holder.stats.final_points}
Total viruses eliminated => {holder.stats.viruses_eliminated}

+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 
"""
)