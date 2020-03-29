# Copyright 2020 C. Sanchez Roman
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

import os

import pygame
from pygame.locals import *

from basemodel import BaseModel
from utils import load_image


class Unicorn(BaseModel):
    """
    Unicorn Class
    """

    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)

        self.alive = True
        self.life = 250
        self.dead = False
        self.dead_scene_time = 10
        self.speed = 20
        self.shield = False
        self.shield_energy = 250
        self.hit = False
        self.hit_time = 6

    def get_current_position(self):
        """
        Get the Unicorn current position.
        """

        # Return a tuple of (x, y) coordinates representing the current
        # location of the Unicorn within the screen.

        return (
            self.rect[0],
            self.rect[1],
        )

    def health_ok(self):
        """
        Checks the unicorn health.
        """

        # Return False if the instance has no life left.
        # Return True is the instance has life left

        if self.life <= 0:
            return False
        return True

    def regenerate_life(self):
        """
        Regenerates the energy of the unicorn.
        """

        # Increment the instance life by 0.025 if:
        #    1) Life is less than 250.

        if self.life < 250:
            self.life += 0.025

    def shield_ok(self):
        """
        Checks shield energy.
        """

        # Return False if the shield has no energy left.
        # Return True if the shield has energy left.

        if self.shield_energy <= 0:
            return False
        return True

    def regenerate_shield_energy(self):
        """
        Regenerates the energy of the shield.
        """

        # Increment the energy of the shield by 0.036 if:
        #    1) The energy of the shield is less than 250.
        #    2) The shield's usage signal is off.

        if self.shield_energy < 250 and self.shield == False:
            self.shield_energy += 0.036

    def activate_shield(self, screen, holder):
        """
        Activate the unicorn shield
        """

        # If the state sent a signal:
        #   1) Make a surface of the unicorn image size
        #   2) Fill it with some color.
        #   3) Blit it to the screen.
        #   4) Append that to be updated.
        #   5) Decrease the energy of the shield by a whole energy point.

        if self.shield_ok():
            shield = pygame.Surface(self.image.get_size()).convert_alpha()
            shield.fill((102, 255, 102, 0.666))
            shield_blit = screen.blit(shield, self.get_current_position())
            holder.dirtyrects.append(shield_blit)
            self.shield_energy -= 1

    def state(self, key, screen):
        """
        Capture actions for the unicorn
        """

        # These signal's declarations control the
        # behaviour of some of the unicorn's main actions,
        # they are set to false to re-enable their original state
        # everytime the state is called within the events loop of
        # the game loop.

        self.shield = False
        self.rotate = False

        # Handle a space key event.
        #
        #   1) If the shield has no energy
        #       1.a) Block the user from using the shield
        #
        #   2) If the shield has energy
        #       2.a) Allow the user to use the shield.
        #       2.b) Send a positive rotate signal to the update function.

        if key[K_SPACE]:
            if not self.shield_ok():
                self.shield = False
            elif self.shield_ok():
                self.shield = True
                self.rotate = True

        # Handle move keys place boundaries, code is self explanatory.

        if key[K_DOWN]:
            if not self.rect.y > 369:
                self.rect = self.rect.move(0, self.speed)

        if key[K_UP]:
            if not self.rect.y < 50:
                self.rect = self.rect.move(0, -self.speed)

        if key[K_RIGHT]:
            self.image = load_image("unicorn.png")
            copy_pos = self.get_current_position()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = copy_pos

            if not self.rect.x > 680:
                self.rect = self.rect.move(self.speed, 0)

        if key[K_LEFT]:
            self.image = load_image("left_unicorn.png")
            copy_pos = self.get_current_position()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = copy_pos

            if not self.rect.x < 20:
                self.rect = self.rect.move(-self.speed, 0)

    def death_scene(self):
        """
        Dramatic scene.
        """
        # All this function does is:
        #   1) Get the position of the current instance.
        #   2) Swap the intial image.
        #   3) Get a rect from the image
        #   4) Set the previous rect position to the new
        #      rect, so that it maintains the same position

        position = (self.rect[0], self.rect[1])
        self.image = load_image("x_x.gif")
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = position

    def update(self, screen, holder):
        """
        Update things.
        """

        # This checks to see if the instance is dead,
        # if so, this means the death scene has been
        # initiated. Therefore we need to decrement
        # it's duration so that the game can end.

        if self.dead:
            self.dead_scene_time -= 1

        # Deduct points from the instance life,
        # Set the hit flag to False, otherwise
        # it will keep decrementing life.

        if self.hit:
            self.life -= 5
            self.hit = False

        # If there was a shield signal from state,
        # call the activate_shield .

        if self.shield:
            self.activate_shield(screen, holder)

        # If there was a rotate signal from state
        # rotate the image by 90 degrees

        if self.rotate:
            self.image = pygame.transform.rotate(self.image, 90)

        # Regenerate

        self.regenerate_shield_energy()
        self.regenerate_life()
