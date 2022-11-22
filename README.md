# Pond Pad - A highly customizable Input Converter for Gamepads

#### Version 1.0.0

### [License Summary](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)#summary)

### Check out the [website](https://pond-pad.com/) :)

#

## Compatability
Windows 10
XBox One gamepad

Might also work with different harware, but it's not considered stable.

## Usage
Just launch the application and work, play, or browse on your computer leaning back, with an ergonomic grip.
The configurable layout allows for all people to use a PC in whichever way they choose.
If you want to quit Pond Pad, just hold the select button.

## Customization
In the [config](./config) you'll find the [config.json](./config/config.json) and [layout.json](./config/layout.json) file respectively. In them, you are able to configure the settings to your liking.

## Basic Configuration - [config.json](../config/config.json)
### "LAYOUT"
Customize the [layout.json](./config/layout.json) file notation.

### "DELIMITER"
Delimiter between an action type and the action itself.

#### "COMBINATION"
Delimiter to chain actions.

### "settings"
Basic settings.

#### "showMessages"
Determines whether messages are shown on screen. These include
- the current mode when switched and
- the shut-down message

#### "showNotifications"
Determines whether Windows toasts are displayed or not.

#### "shutDownMsg"
Lets you configure the message building up, when holding the select button to shut down the application.

## Layout Configuration - [layout.json](./config/layout.json)
Allows for the implementation of custom controller layouts.

### "settings"
#### "mouseLeft"
Determines whether the left or right joystick is used to control the mouse movement.

### "modes"
Modes hold separate layouts, which are switched by the press of a button. The switching of a mode displays (via message) the current mode.

### "plates"
Plates are sub-layouts within modes. They are switched to by holding down a button. Having a plate within a plate allows for the possibility of holding down multiple buttons for an alternative layout.

### Buttons
Most buttons within a plate are what they seem like. ```"A"``` means the "A" button and so forth. The select button is absent, because it is the button to quit the application. This should be the case in all plates and modes. You can thank me for that limitation, when you encounter a bug that would otherwise require you to restart your PC.

#### "mouseSpeed"
Lets you choose the mouse speed for every plate. When absent or set to ```0```, the respective ```JoySick[Left|Right]...``` "buttons" are used.

#### "scrollSpeed"
Controls the amount of lines scrolled every tick.

## Actions
There are 7 actions in total:
- mode
- plate
- scroll
- click
- press
- hold
- write

### mode
Switches to the specified mode.

#### Example
```json
"mode @@@ lower case"
```

### plate
Switches to the specified plate within the current mode, whilst the button is held down. Otherwise, the current plate is the first one defined within a mode.

It is recommended that a plate refers to itself. Meaning that if you would switch to the plate "```left```" with the "```TriggerLeft```" from the "```neutral```" (or in any case the first) plate, "```TriggerLeft```" should also be assigned to the "```left```" plate in *that* plate.

#### Example
```json
"plate @@@ dual"
```

### scroll
Scrolls in the specified direction.
The list of possible directions is:
- up
- down
- left
- right

#### Example
```json
"scroll @@@ down"
```

### click
Holds down the specified mouse button whilst pressed. Releases it at the same time as the mapped controller button.
The list of possible mouse buttons is:
- left
- right
- middle

#### Example
```json
"click @@@ left"
```

### press
Holds down a key until you release it. It is possible to write with this action, but it is not recommended. This action is intended for macros and actions in applications (e.g. pressing ```F``` to enter/exit full screen mode (or paying respect)).
The list of possible keys can be found [here](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key) and [here](https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys).

#### Example
```json
"press @@@ A"
```

#### Combinations
The press action allows for a combination of buttons to create macros. Simply separate the desired keys with the specified ```DELIMITER```. The keys are pressed in order of specification and released in reversed order. There is no (hard) limit to the amount of combinations possible.

#### Example
```json
"press @@@ alt +++ f4"
```

### hold
Intended to feel like holding down a key on an actual keyboard. When first pressing down, it instantly presses the specified key. After waiting for 0.4 seconds, it keeps pressing it until released.
The list of possible keys can be found [here](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key) and [here](https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys) as well.

#### Example
```json
"hold @@@ shift"
```

### write
Types the specified string after the delimiter. No ```"``` required, unless you explicitly want to print it. In that case, you'd need to escape it with a ```\```.

#### Example
```json
"write @@@ Hello, World!"
```

#