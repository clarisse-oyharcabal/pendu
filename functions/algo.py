# On importe les librairie
import os
import pygame
import random

# On déclare les fonctions 

def display_menu() :
    print("\n📖 Main Menu 📖:")
    print("1. Easy mode")
    print("2. Medium mode")
    print("3. Hard mode")
    print("4. ⛷️ Exit\n") 


def input_validator() :
    while True:
        try: 
            choi