# twitch-sabaki-bot

## Description

This program takes screenshots of the games you play on any application, in order to send them to the Sabaki application, and allows the twitch chat to interact with Sabaki by proposing variations.
You can then show the Sabaki window on your stream to make interactive reviews, or to let the chat review their own moves.

Currently only works on Windows, tested with python 2.7 in windows 7.

Sabaki github page : <https://github.com/SabakiHQ/Sabaki>

## Installation

In order to use the program, you'll need node.js (for Sabaki), python 2.7 and the listed modules (for this program), and the source files from this repo.
Then, you'll have to set up the window capture properties so that they fit your screen and resolution, for each application you want to use with this program. 

The default settings work with IGS/Pandanet, Foxwq, Tygem and CrazyStone, running in fullscreen for a resolution of 1680x1050 on Windows 7.

#### Install node.js
* from : <https://nodejs.org/en/>

#### Install python and its libraries
* Get python from : <https://www.python.org/downloads/release/python-2714/> (Usually comes pre-installed on linux)
* Install each of the following packages with `pip install <package name>`
    * keyboard
    * simplejson
    * win32gui
    * tornado
    * PIL
    * pyscreenshot

#### Install the program
* download as zip
* unzip anywhere on your computer
* open a command line
* go to Sabaki-master
* run command `npm install`
* run command `npm run build`
* run command `npm start` to check if everything works correctly
    * close sabaki

#### Set up your twitch bot
* Open `settings.json`.
* Fill in the 3 first properties.
    * `twitch_channel` : your channel's name in lowercase.
    * `twitch_bot_name` : the name of your bot in the twitch chat.
    * `twitch_bot_oauth` : a generated password to identify your bot, that you can get from <https://twitchapps.com/tmi>.

#### Set up the window capture and/or add new applications to capture
* Open `settings.json`
* The applications are listed under the "servers" property. A server is composed of the following properties.
    * `name` : an identifier for the program.
    * `pattern` : a string to look for in the application's window title. This is how the program will find the window to capture.
    * `crop_left`, `crop_right`, `crop_top`, `crop_bottom` : the relative portion (%) of the window to crop out in each direction, in order to get the image of the goban only.
    * `i_col` : true if the application's coordinate system uses an "i" column.
    * `reversed_rows` : true if the top row corresponds to the row n°19.

You can add any application you want by copy-pasting the properties for an existing application and replacing their values.

#### Setting up the window capture

The program uses a simplistic image recognition technique to turn the window capture into a go board position. The cropping therefore needs to be as accurate as possible.

To help you finding the proper settings, you can set the `setup_capture` property to true. Each screenshot taken by the program will then be shown to you. You still need to restart the program to update the settings every time.
    
## How to launch the program
Usually, simply double clicking `sabaki_twitch.py` should work.

If it doesn't, open a command prompt, navigate to the program's folder and run `python sabaki_twitch.py`. If this doesn't work either, check your `PATH` environment variable, and verify that it contains python's installation folder, and the Scripts subfolder inside it.

## Other useful settings

#### Coordinates
* `use_server_coordinates` : If set to false, will use the same coordinate system for all applications. Useful if your overlay integrates the coordinates.
* `coordinates_use_i_col` : Same as "i_col" if you do not use server coordinates, useless otherwise.
* `coordinates_reversed_rows` : Same as "reversed_rows" if you do not use server coordinates, useless otherwise.

#### Twitch chat moves
* `allowed_variations_per_user` : You can limit the number of variations (move sequences) a user is allowed to post. Resets every few minutes.
* `reset_variation_count_timer` : Time in minutes before resetting the variation count for everyone.
* `base_variation_displaying_time`: Base time a variation stays on screen.
* `variation_displaying_time_per_stone`: Additional time a variation stays on screen, depending on the number of moves in it.
* `time_between_captures`: Time in seconds between 2 window captures. Decrease for more responsiveness, increase if it slows your computer down.

## How to navigate to a folder using the command prompt
Use the command `cd`, which stands for "change directory".

    example :   `cd C:\Users\Me\Desktop\twitch-sabaki-bot`
                `cd Sabaki-master`

On windows, if the program's folder is on the D: drive, you can change the drive by entering `d:`.
