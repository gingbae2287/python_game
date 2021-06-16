import pygame
import os
import random
from setting import *
current_path=os.path.dirname(__file__)

object_gold=pygame.image.load(os.path.join(current_path,"images/gold.png"))  # 큰금
print(object_gold.get_rect().size)