# twitch-Sabaki-bot

## Description

This program takes screenshots of the games you play on any application, and either sends them to the Sabaki application, and allows the twitch chat to interact with Sabaki by proposing variations, or generates an overlay image to put over the board on your streaming application, or both.

Currently only works on Windows, tested with python 2.7 in windows 7.

Sabaki github page : <https://github.com/SabakiHQ/Sabaki>

## Usage ##

Simply run twitch_baduk.py to launch the program. Press escape from anywhere to end it (you have to close Sabaki manually as well). You can interrupt sending moves to Sabaki by pressing ctrl+K, and resume it by pressing ctrl+P again.

Twitch chat can send variations by writing their coordinates, for example : `k10 d16 c4 q16 r4`. It is possible to force the first move being a specific color by beginning the sequence with `b` or `w` : `b q16 r14 p17 s16 r17 r11`. Variations show in Sabaki for a few seconds, depending on the number of moves in the variation, then the game reverts to its current state. You can press ctrl+K to keep the variation on Sabaki.

If double clicking the launcher doesn't work, open a command prompt, navigate to the program's folder and run `python twitch_baduk.py`. If this doesn't work either, check your `PATH` environment variable, and verify that it contains python's installation folder, and the Scripts subfolder inside it.

The variations overlay image is located in `overlay/overlay.png`.

## Installation

In order to use the program, you'll need node.js (for Sabaki), python 2.7 and the listed modules (for this program), and the source files from this repo.
Then, you'll have to set up the window capture properties so that they fit your screen and resolution, for each application you want to use with this program.
If you're not going to use Sabaki but only the goban overlay, then you only python and its libraries, and you only need follow step 1 to 3 of the installation process.

The default settings work with IGS/Pandanet, Foxwq, Tygem and CrazyStone, running in fullscreen for a resolution of 1680x1050 on Windows 7.

#### Install node.js
* from : <https://nodejs.org/en/>

#### 1. Install python and its libraries
* Get python from : <https://www.python.org/downloads/release/python-2714/> (Usually comes pre-installed on linux)
* Install each of the following packages with `pip install <package name>`
    * keyboard
    * simplejson
    * win32gui
    * tornado
    * PIL
    * pyscreenshot

#### 2. Install the program
* download as zip
* unzip anywhere on your computer
* Rename `settings.json.example` into `settings.json`
* Open settings.json in a notepad 
    * find `generate_overlay_image` and set it to `false` if you don't want to use the overlay image
    * find `use_sabaki` and set it to `false` if you don't want to use Sabaki

#### 3. Set up your twitch bot
* Open `settings.json`.
* Fill in the 3 first properties.
    * `twitch_channel` : your channel's name in lowercase.
    * `twitch_bot_name` : the name of your bot in the twitch chat.
    * `twitch_bot_oauth` : a generated password to identify your bot, that you can get from <https://twitchapps.com/tmi>.

#### 4. Install Sabaki
* open a command line (See )
* go to Sabaki-master
* run command `npm install`
* run command `npm run build`
* run command `npm start` to check if everything works correctly
    * close Sabaki

#### 5. Set up the window capture and/or add new applications to capture -- Optional --
* Open `settings.json`
* The applications are listed under the `servers` property. A server is composed of the following properties.
    * `name` : an identifier for the program.
    * `pattern` : a string to look for in the application's window title. This is how the program will find the window to capture.
    * `crop_left`, `crop_right`, `crop_top`, `crop_bottom` : the relative portion (%) of the window to crop out in each direction, in order to get the image of the goban only.
    * `i_col` : true if the application's coordinate system uses an "i" column.
    * `reversed_rows` : true if the top row corresponds to the row n°19.

You can add any application you want by copy-pasting the properties for an existing application and replacing their values.

#### Setting up the window capture

The program uses a simplistic image recognition technique to turn the window capture into a go board position. The cropping therefore needs to be as accurate as possible.

To help you finding the proper settings, you can set the `setup_capture` property to true. Each screenshot taken by the program will then be shown to you. You still need to restart the program to update the settings every time.

## Other useful settings

#### Hotkeys
* The hotkeys are located under the `keys` property. Be aware that the hotkeys are active globally, pressing a hotkey in another application might trigger them.
    * `endProgram` : hotkey to end the program, defaults to escape.
    * `toggleCommunication` : Interrupts/Resume sending updates to Sabaki
    
#### Coordinates
* `use_server_coordinates` : If set to false, will use the same coordinate system for all applications. Useful if your overlay integrates the coordinates.
* `coordinates_use_i_col` : Same as "i_col" if you do not use server coordinates, useless otherwise.
* `coordinates_reversed_rows` : Same as "reversed_rows" if you do not use server coordinates, useless otherwise.

#### Twitch chat moves
* `allowed_variations_per_user` : You can limit the number of variations (move sequences) a user is allowed to post. Resets every few minutes.
* `reset_variation_count_timer` : Time in minutes before resetting the variation count for everyone.
* `base_variation_displaying_time`: Base time a variation stays on screen.
* `variation_displaying_time_per_stone`: Additional time a variation stays on screen, depending on the number of moves in it.

#### Overlay & Sabaki
* `generate_overlay_image` : generate the overlay image when tiwtch proposes a variation
* `overlay_image_path`: `./overlay/overlay.png`,
* `overlay_padding_left`, `overlay_padding_right`, `overlay_padding_top`, `overlay_padding_bottom` : reduces the area of the overlay in which to display the moves
* `use_sabaki` : Launch sabaki with the program, and the window capture to generate go games
* `time_between_captures`: Time in seconds between 2 window captures. Decrease for more responsiveness, increase if it slows your computer down.

## TODO

* Add hotkey to recreate sgf with all proposed variations
* Add hotkey to save sgf
* OBS plugin to switch scenes when a variation is proposed
* Find a way to detect snapbacks when 2 moves have been played before last update
* Code cleaning
* Probably some bug fixing

## How to navigate to a directory with the command prompt
To open a command prompt on windows, open the start menu and type `cmd`. On most linux installations, press `ctrl+alt+T`.
Use the command `cd`, which stands for "change directory".

    examples :   cd C:\Users\Me\Desktop\twitch-baduk
                cd Sabaki-master

On windows, if the program's folder is on the D: drive, you can change the drive by entering `d:`.
