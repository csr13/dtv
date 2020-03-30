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


from utils import load_image


class BaseModel:
    def __init__(self, img, spawn_location=None):
        self.image = load_image(img)
        if spawn_location:
            self.rect = self.image.get_rect(**spawn_location)
        else:
            self.rect = self.image.get_rect()

    def get_current_position(self):
        return (
            self.rect[0],
            self.rect[1],
        )

    def draw(self, screen, holder):
        blt = screen.blit(self.image, self.rect)
        holder.dirtyrects.append(blt)

    def erase(self, screen, background, holder):
        blt = screen.blit(background, self.rect, self.rect)
        holder.dirtyrects.append(blt)

    def update(self):
        """Override this in each of the classes"""
        pass
