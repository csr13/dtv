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

import os

from pygame import Rect


SCREENRECT = Rect(0, 0, 640, 480)
PUNTAJE = 0
VIDAS = 5
CHECK = {"limite": (480 - 40), "reset": (473 - 40)}


images_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes")
