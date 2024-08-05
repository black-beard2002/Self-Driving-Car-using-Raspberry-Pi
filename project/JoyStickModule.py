import pygame
from time import sleep

pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

# Dictionary to store button states and analog stick values
buttons = {
    'x': 0, 'o': 0, 's': 0, 't': 0,
    'share': 0, 'useless':0,'options': 0,
    'axis1': 0.0, 'axis2': 0.0
}

# Function to update joystick state
def getJS(name=''):
    global buttons

    # Retrieve any events
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # Update left analog stick values only (axis 0 and 1)
            if event.axis == 0:
                buttons['axis1'] = round(event.value, 2)
            elif event.axis == 1:
                buttons['axis2'] = round(event.value, 2)

        elif event.type == pygame.JOYBUTTONDOWN:
            # Update button state to 1 when pressed
            if event.button < len(buttons):
                button_name = list(buttons.keys())[event.button]
                buttons[button_name] = 1

        elif event.type == pygame.JOYBUTTONUP:
            # Update button state to 0 when released
            if event.button < len(buttons):
                button_name = list(buttons.keys())[event.button]
                buttons[button_name] = 0

    # Return all buttons or specific button value
    if name == '':
        return buttons
    else:
        return buttons.get(name, None)

def main():
    print(getJS())  # Print all button states and analog values
    sleep(0.05)

if __name__ == '__main__':
    while True:
        main()