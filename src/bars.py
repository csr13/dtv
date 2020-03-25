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

from basemodel import BaseModel

from utils import writer, Img


class TopBar(BaseModel):
    def update(self, screen):
        pass


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Load player lives, this needs to be converted to a class and inherited to
# the Uniconrn
"""
Img.heart = load_image("heart.png")
courage_meter = []
padding = [2, 195]
padding_copy = padding[:]

for each in range(VIDAS):

    courage_load = Img.heart
    courage_meter.append(courage_load.get_rect())
    courage_meter[each].x = padding[1]
    courage_meter[each].y = padding[0]
    background.blit(courage_load, courage_meter[each])
    padding[1] += 35


score, score_position = writer(
    phrase=f"Puntos: {PUNTAJE}",
    font="ubuntumono",
    size=20,
    color=(102, 255, 102),
    where={"top": 10, "right": 110},
)

vidas, vidas_position = writer(
    phrase=f"Vidas: ",
    font="ubuntumono",
    size=20,
    color=(102, 255, 102),
    where={"top": 10, "right": 200},
)
"""
