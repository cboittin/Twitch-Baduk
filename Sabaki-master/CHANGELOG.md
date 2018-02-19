# Changelog

All notable changes to this project will be documented in this file.

## [Sabaki v0.33.3][v0.33.3] (2018-02-10)

**Fixed**

* Fix game tree crashing when showing after branching the game tree
* Fix stones with labels not showing up in ASCII diagrams

## [Sabaki v0.33.2][v0.33.2] (2018-01-23)

**Fixed**

* Fix color of hoshi points not being themed
* Fix Markdown links not working properly

**Changed**

* Update to Electron v1.7.11

## [Sabaki v0.33.1][v0.33.1] (2018-01-09)

**Fixed**

* Fix board markups not being displayed on stones

## [Sabaki v0.33.0][v0.33.0] (2018-01-09)

**Added**

* Allow engines to send heatmaps and visualizes them
* Ability to specify commands that are sent to engines right after they start
* Add option whether Sabaki should start a game right after attaching engines

**Changed**

* The command history limit has been reinstated, but raised
* Update to Electron v1.7.10

**Fixed**

* Fix comment input area not being visible in edit mode sometimes
* Fix engine color indicator of GTP console being wrong when swapping engine color mid-game
* Up and down keys for traversing command history in the GTP console are working again
* Fix Sabaki trying to add engine variations while in scoring mode after a double pass
* Fix engine passes not getting passed on to opponent engine

## [Sabaki v0.32.2][v0.32.2] (2018-01-01)

**Added**

* Add engine integration protocol
* Add 'Synchronize' menu item in 'Engines' menu

**Changed**

* When updating engine boards, Sabaki will try to replay moves in game order first
* The command history limit of the GTP console has been lifted
* Focus find input when entering find mode
* Sabaki allows 2×2 boards

**Fixed**

* Fix Sabaki not continue generating moves in bot vs. bot games where only one of them passes
* Selecting 'Stone Tool' from the menu is now able to toggle stone color

## [Sabaki v0.31.5][v0.31.5] (2017-10-31)

**Changed**

* Pre-fill date field in new games with current date
* In the info drawer, show game result after user's affirmation
* Inactive nodes in the game tree get comment and hotspot coloring (Thanks to [@geovens](https://github.com/geovens))
* Update to Electron v1.7.9

**Fixed**

* Clicking 'Download Update' button opens the correct URL

## [Sabaki v0.31.4][v0.31.4] (2017-09-27)

**Changed**

* When selecting engines, player names are automatically filled unless changed by the user
* Downgrade to stable Electron v1.7.8 due to security reasons

**Fixed**

* Fix encoding problems in shape names

## [Sabaki v0.31.3][v0.31.3] (2017-09-19)

**Changed**

* Change 'Remove Node' shortcut to <kbd>Command+Backspace</kbd> on macOS
* Change 'Fullscreen' shortcut to <kbd>F11</kbd> on Linux and Windows
* Lift the arbitrary maximum limit of autoplay's 'sec per move' (Thanks to [@emauton](https://github.com/emauton))
* Per-window sidebars (see [#265](https://github.com/SabakiHQ/Sabaki/issues/265))
* Update to Electron v1.8.0 beta

**Fixed**

* Fix updated komi values not being sent to GTP engines during the game
* Fix pass moves not being sent to GTP engines

## [Sabaki v0.31.2][v0.31.2] (2017-07-15)

**Changed**

* Update to Electron v1.7.4 beta

**Fixed**

* Fix Sabaki crashing when pressing enter in autoplay mode
* Fix 'Clear Annotations' not working
* Fix Sabaki not sending pass command to attached engines
* Fix cursor jumping to the end of comment text when editing

## [Sabaki v0.31.1][v0.31.1] (2017-06-24)

**Added**

* Add support for outdated `L` property
* Add menu items for going to next/previous game

**Fixed**

* Fix 'Jump to end after loading file' not working
* Fix theme uninstallation failing on Windows with disabled recycle bin

## [Sabaki v0.31.0][v0.31.0] (2017-05-27)

**Added**

* Themes (Thanks to [@Seth-Rothschild](https://github.com/Seth-Rothschild))
* Ability to adjust UI zoom

**Changed**

* Update to Electron v1.7.2 beta
* Rename 'Pause' engines command to 'Suspend'

**Fixed**

* Fix player names not displaying in the game chooser drawer
* Fix Sabaki displaying 'Please wait...' forever after a two engines match ends in resignation
* Fix GTP console sending invalid commands
* Fix 'Go To Move Number' not working
* Fix move/position annotations being incorrectly applied

## [Sabaki v0.30.3][v0.30.3] (2017-05-10)

**Added**

* Ability to pause engines

**Fixed**

* Fix Sabaki not being able to undo a flatten node operation
* Fix Sabaki incorrectly setting `HA` and `AB` properties when there are no handicap stones
* Fix Sabaki sometimes not saving comments when comment box is focused
* Fix Sabaki crashing when checking for updates without internet connection

## [Sabaki v0.30.2][v0.30.2] (2017-05-03)

**Changed**

* Update to Electron v1.6.8 beta
* Reduce mouse wheel navigation sensitivity

**Fixed**

* Fix Sabaki being unresponsive for a short time during update checking
* Fix setting white player rank not working in info drawer

## [Sabaki v0.30.1][v0.30.1] (2017-04-25)

**Added**

* The game graph has been rewritten from scratch and is now more efficient with large game trees without the need to collapse subtrees. The graph is more accessible, the nodes have a bigger click surface and dragging the graph can go beyond the component.
* The game collection manager includes support for `ngf` and `gib` files. It also sports a slick board animation, which is very slick. Did I mention it's slick?
* You can assign custom label texts to a vertex on the board by selecting the label or number tool and clicking 'Edit Label' in the context menu.
* You can attach two engines to Sabaki and let them play each other while you can sip tea comfortably and watch them fight. The GTP console has been redesigned so you are able to address both engines separately. It also displays (usually) useful `stderr` information from the engines. Command autocompletion is more obvious now.
* Drawing with the line/arrow tool makes it clear that drawing over an existing line/arrow removes that line/arrow.
* Ability to hide menu bar on Windows and Linux.

**Changed**

* Update to Electron v1.6.7 beta

**Fixed**

* When encoding is not specified, Sabaki tries to infer the encoding from content instead of assuming ISO-8859-1 (Thanks to [@fohristiwhirl](https://github.com/fohristiwhirl)).
* When `CA` property is missing from an opened file, Sabaki previously saves it without correct UTF-8 `CA` property. This results in Sabaki opening these files in ISO-8859-1, not correctly displaying text. This is fixed now.
* When attaching engines, Sabaki previously sends the `boardsize` command after `clear_board` which technically can result in arbitrary board positions on the engine. This is fixed now.
* Other Go software may specify the same property multiple times on a tree node, which technically makes the SGF invalid. Sabaki can handle these files now.

## [Sabaki v0.21.0][v0.21.0] (2017-03-30)

**Added**

* Support for Tygem `gib` files and WBaduk `ngf` files (Thanks to [@fohristiwhirl](https://github.com/fohristiwhirl))
* Move spots on the board are getting colored according to its move annotation (Thanks to [@dfannius](https://github.com/dfannius))
* Move annotation context menu on the last played stone (Thanks to [@dfannius](https://github.com/dfannius))
* Sabaki Web can load and copy SGF files from/to the clipboard (Thanks to [@C0DEHERO](https://github.com/C0DEHERO))
* Use Monte Carlo algorithm for better dead stones estimation
* Ability to change the order of variations
* Ability to remove certain node information from the whole game or current position
* Ability to sort games in a game container
* Add compact and big style game tree

**Changed**

* Update to Electron v1.6.2
* Board grid lines are now vector images
* Sabaki Web saves settings in local storage
* Current variation is more distinguishable from other variations in the game tree

**Fixed**

* Windows installers create app folder if necessary
* Fix Sabaki being unresponsive when adding invalid files to a game collection
* Fix wrong initial `SZ` property value, thus resulting in an invalid SGF file
* Fix issue where Sabaki is inserting a ton of unnecessary empty lines in SGF files on Windows
* Fix GitHub and 'Report Issue' menu items not working
* Fix move interpretation stuck at '3-3 point' sometimes
* Fix reload file warning showing if the file has been removed
* Sabaki uses `\r\n` as linebreaks on Windows
* Fix 'Download' button when an update is available

## [Sabaki v0.19.3][v0.19.3] (2017-01-11)

**Added**

* Sabaki remembers board setup, i.e. komi, board size, and handicap stones
* Sabaki offers to reload an opened file if it has been changed externally
* Ability to remove all variations apart from the active one
* Ability to flatten nodes
* Add 'Play' menu
* Add 'Go To Move Number' menu item
* Ability to select points by keyboard input
* Ability to copy/cut/paste variations

**Changed**

* Change keyboard shortcuts for toggling sidebar elements
* Update to Electron v1.4.13
* Update to Octicons v5.0.1
* Remove gemini-scrollbar dependency

**Fixed**

* Fix copy to clipboard not working
* Fix board arrows not pointing in the right direction
* Fix incorrectly interpreting openings on boards other than 19&times;19
* Fix Sabaki closing even if user cancels
* Fix game graph not being updated when pasting variations sometimes
* Fix handicap stones being placed incorrectly
* Fix not being able to select executables for engines

## [Sabaki v0.18.3][v0.18.3] (2016-10-26)

**Added**

* Add support for non-UTF8 encodings (Thanks to [@apetresc](https://github.com/apetresc))
* Add basic text editing keyboard shortcuts when editing/writing comments on macOS

**Changed**

* Sidebar lag is reduced
* More intuitive 'Go To Next/Previous Variation'
* Update application icon
* Update to Electron v1.4.4

**Fixed**

* Fix 'Load From Clipboard' encoding issue
* Fix graph not displaying diamond shapes
* Fix arrow keys not working in open/save file dialog on macOS
* Fix guess mode when an engine is attached
* Fix removing nodes resulting in invalid game graphs sometimes
* Fix regression where guess mode stopped working

## [Sabaki v0.17.2][v0.17.2] (2016-09-10)

**Added**

* Autoplay mode
* `Ctrl`-click position to insert coordinates when in edit mode
* Add keyboard shortcut for 'Pass' (`Ctrl+P` or `Command+P`)

**Changed**

* Clicking on the current player indicator switches current player without passing
* Update to Electron v1.3.5
* Bump gemini-scrollbar@v1.4.3
* Bump octicons@v4.3.0

**Fixed**

* Fix `PL[B]` not working
* Fix scrollbar in engines list not updating correctly
* Fix system paths not being honored in macOS
* Fix autoplay stopping at non-move nodes
* Fix autoplay not working with non-alternating color moves
* Fix regression where swapping player names wouldn't work
* Fix performance issue where a huge amount of games inside a SGF collection can slow down Sabaki
* Fix games vanishing in 'Manage Games...' when dragging
* Fix unresponsiveness when cancelling adding files to games
* Fix adding files to games being impossible under Mac
* Fix GTP console being unusable under Mac when native overlay scrollbars are turned on

## [Sabaki v0.15.3][v0.15.3] (2016-06-16)

**Added**

* Create ASCII diagrams
* Ability to animate fuzzy placement of stones
* Ability to add existing files to SGF collection
* 'Resign' menu item under 'Pass'
* Ability to turn off automatic move titles in the preferences
* Add keyboard shortcut for 'Show Coordinates'
* Score estimator
* Ability to select multiple existing files to add to SGF collection

**Changed**

* Board adapts size, looking more natural
* Current stone markers resize with board
* Change 'Go To Beginning' and 'Go To End' keyboard shortcuts to `Home`/`End`
* Doesn't leave scoring mode when closing score table
* Change keyboard shortcut for 'Generate Move' to `F5`
* Remove keyboard shortcut for 'GTP console'
* Press `Esc` to exit full screen mode
* Update to Electron v1.2.2

**Fixed**

* Fix rounding errors regarding hoshi points
* Fix komi not updated for GTP engine
* Fix sending invalid GTP command when passing

## [Sabaki v0.14.0][v0.14.0] (2016-05-14)

**Added**

* Ability to add dates to games
* Ability to create games on small boards
* Ability to style Sabaki with userstyles (see [wiki](https://github.com/SabakiHQ/Sabaki/wiki/Userstyle-Tutorial))
* Support for non-square boards
* Ability to show sibling variations on the board
* Display result in scoring table

**Changed**

* Display non-moves as diamonds in the game graph
* Update to Electron v1.0.2

**Fixed**

* Fix coordinates in console not being styled correctly
* Fix weird grid lines behavior with small board sizes
* Fix deselecting vertex when finding moves
* Fix occasional crash when opening small files at startup
* Fix label markup cutting off content or truncating three digit numbers

## [Sabaki v0.12.4][v0.12.4] (2016-05-03)

**Added**

* Now board markup scales with board size
* Add edit button to comments section
* Allow a subset of Markdown in the comments section
* Ability to choose GTP engine directly inside the 'New Game' drawer
* Ability to link to move numbers in the comments (see [wiki](https://github.com/SabakiHQ/Sabaki/wiki/Markdown-in-Sabaki))
* Support for old SGF 'long property ids' (see [#68](https://github.com/SabakiHQ/Sabaki/issues/68))

**Changed**

* Doesn't clear GTP console when detaching engines
* Significant SGF parsing speed increase; parses Kogo's Joseki Dictionary in ~1 second
* Significant graph updating speed increase
* Update to Electon v0.37.7

**Fixed**

* Fix misplaced triangle markup under OS X
* Fix incorrect parsing of backslashes in comments
* Fix engines menu list not updating when adding/removing engines
* Fix comments textbox scrolling to top when editing
* Fix navigation shortcuts not working after closing drawers
* Fix conflicting auto-links in the comments section
* Slider doesn't stop halfway anymore when sliding over the end

## [Sabaki v0.11.5][v0.11.5] (2016-04-15)

**Changed**

* Add 'New Window' menu item
* Closing all windows doesn't quit the app in OS X
* Associate SGF files with Sabaki in OS X
* Faster startup
* Update to Electron v0.37.5

**Fixed**

* Fix missing WebGL libraries in Windows
* Fix crash while saving files
* Opening an unreadable file doesn't set represented filename anymore
* Fix repeated exceptions when opening an empty game tree
* Fix editing compressed point lists for AB/AW/AE properties not working

## [Sabaki v0.11.2][v0.11.2] (2016-04-01)

**Added**

* Guess mode
* Load SGF files from clipboard
* Copy SGF files to clipboard
* SGF-compatible line and arrow markup
* Filter in 'Manage Games'
* More game info fields
* Add opening data
* Add 'Go To Main Variation' menu item
* Supports SGF collections

**Changed**

* Show game result when at the end of main variation
* Smaller font size for larger board labels
* Update to Electron v0.37.3

**Fixed**

* Fix regression where saving SGF files does nothing
* Fix graph not updating when undoing
* Dragging slider outside window won't cause it to stop anymore

## [Sabaki v0.10.1][v0.10.1] (2016-02-27)

**Added**

* Show SGF node name (`N` property) if available
* Show node & move annotations
* Add 'Go To Next/Previous Comment' menu items

**Changed**

* Change 'Bookmark' to 'Hotspot'
* 'Show Variations' shows next move as well
* Don't make current variation to main variation when saving
* Update to Electron v0.36.9

**Fixed**

* Fix incorrectly escaped `>` character in comment
* Prevent user from sliding out of viewport by selecting text
* Fix regression where saving SGF files results in an exception

## [Sabaki v0.9.1][v0.9.1] (2016-02-24)

**Added**

* Add Mac OS X release
* Add bookmark indicator
* Ability to save into existing file
* Show basic move interpretation when no comment is provided

**Changed**

* Speed up SGF parsing
* Speed up scoring
* Show passes as squares in game graph
* Changed some menu shortcuts
* Bump electron@v0.36.8
* Bump gemini-scrollbar@v1.3.2
* Bump octicons@v3.5.0
* Bump sigma@v1.1.0

**Fixed**

* Fix regression when passing results in an uncatched exception sometimes
* Fix not being able to hide the indicator in find mode
* Clicking when busy does not have an effect now

## [Sabaki v0.8.1][v0.8.1] (2016-02-12)

**Added**

* Find menu
* Ability to find in comments
* Create bookmarks and jump to them

**Changed**

* Clicking on the player indicator results in a pass
* Enter scoring mode after two consecutive passes are created
* Change behavior of find buttons

**Fixed**

* Saving a game does not trigger 'File changed' flag
* Fix regression where a new variation is created when move already exists
* Fix regression where the slider doesn't jump when clicked

## [Sabaki v0.7.6][v0.7.6] (2016-01-30)

**Added**

* Autoscroll games

**Fixed**

* Fix weird `box-shadow` on stone overlays
* Fix not updating game graph sometimes when undoing
* Fix regression where a new variation is created when variation already exists
* Fix loading games with no player names not replacing old names
* Fix weird menu behavior

**Changed**

* Scale icons proportionally so they don't look weird
* Styled checkboxes
* Don't mark stones as dead in friendly territory
* Ability to directly enter engine path when adding an engine
* Detach engine before unloading
* More crisp SVG icons
* New slider design
* Update to Electron v0.36.7
* Update to Mootools v1.6.0

## [Sabaki v0.7.1][v0.7.1] (2015-12-31)

**Added**

* Find move
* Fullscreen mode
* Add GTP engines support
* Add preferences panel
* Undo 'Remove Node' and 'Clear All Overlays'
* Click current stone to remove node
* Ability to turn off 'Remove Node' warning

**Changed**

* More responsive game graph
* Touch-friendly slider
* Fix duplicate Taskbar icon in Windows
* Fix overlays being off-center
* Window has an icon in Linux

**Fixed**

* More crisp bar icons
* Fix engines not showing in preferences when removed but not saved
* Fix certain actions failing in scoring mode
* Update to Electron v0.36.2

## [Sabaki v0.5.0][v0.5.0] (2015-09-03)

**Added**

* Add 'Clear All Overlays' menu item
* Ask for saving file when closing a changed game
* Confirm remove node
* Add comment editing to edit mode
* Add Linux release

**Fixed**

* Always use system font
* Fix weird rendering artifacts
* Prevent new windows when Ctrl-clicking links

**Changed**

* Alpha and number tools use up lower, unused symbols before using higher symbols
* When opening Sabaki with a big file, the main window will show before loading file
* Update to Electron v0.31.2

## [Sabaki v0.4.2][v0.4.2] (2015-08-28)

**Added**

* Resizable comment view
* Comment view
* Add keyboard shortcut for 'Remove Node'
* Hovering over coordinates in a comment will show the corresponding position on the board

**Fixed**

* Avoid initial collision of fuzzily placed stones
* Mouse wheel navigation works when pointing at the game graph
* Fix slider arrow not being at the right place sometimes
* Fix a bug where saving games with comments could lead to unescaped characters

**Changed**

* Update to Electron v0.31.1
* Change name to Sabaki

## [Goban v0.3.7][v0.3.7] (2015-08-16)

**Added**

* Highlight current game track in graph

**Fixed**

* Fix wrong cross symbol on Windows 10
* Fix a bug where stone sounds are not played immediately
* Fix graph performance issues
* Fix uncaught exception when playing in pruned subgraphs again
* Faster click response when playing in large graphs

**Changed**

* Update to Electron v0.30.4

## [Goban v0.3.5][v0.3.5] (2015-08-04)

**Added**

* Check for updates at startup
* Add move count indicator next to slider
* Ability to load a game by dropping file onto the board
* Show error message when file is unreadable
* Warn user about suicide moves
* Play capture sounds when making suicide moves
* Show taskbar progress when loading large SGF files
* Color-code collapsed subgraphs
* Color-code commented nodes
* Automatically expand collapsed subgraphs

**Fixed**

* Fix uncaught exception when playing in pruned subgraphs
* Fix a bug where the slider won't update when playing in pruned subgraphs
* Fix a bug where label tooltips are not removed
* Fix a bug where the game graph is not updated when adding/removing stones manually
* Fix a bug where the graph camera is not positioned correctly when opening sidebar
* Fix weird graph camera behavior
* Fix uncaught exception when saving SGF file

**Changed**

* Faster slider response
* Collapse game graph for performance
* Update to Electron v0.30.2

## [Goban v0.3.0][v0.3.0] (2015-07-22)

**Added**

* Game graph
* Resizable sidebar
* Detect and notify user about ko
* Ability to remove SGF nodes
* Add slider
* Add navigation to sibling variations

**Fixed**

* Prevent accidentally clicking on the board when dragging graph
* Fix a bug where removed variations show up on the board
* Fix an error where updating the score of a drawed game, the SGF result will not be correct
* Fix sudden disappearances of the game graph when dragged
* Fix unresponsiveness when clicking on a vertex on the game graph

**Changed**

* Update to Electron v0.30.0

## Goban v0.1.0 (2015-06-20)

First release

[unreleased]: https://github.com/SabakiHQ/Sabaki/compare/v0.33.3...master
[v0.33.3]: https://github.com/SabakiHQ/Sabaki/compare/v0.33.2...v0.33.3
[v0.33.2]: https://github.com/SabakiHQ/Sabaki/compare/v0.33.1...v0.33.2
[v0.33.1]: https://github.com/SabakiHQ/Sabaki/compare/v0.33.0...v0.33.1
[v0.33.0]: https://github.com/SabakiHQ/Sabaki/compare/v0.32.2...v0.33.0
[v0.32.2]: https://github.com/SabakiHQ/Sabaki/compare/v0.31.5...v0.32.2
[v0.31.5]: https://github.com/SabakiHQ/Sabaki/compare/v0.31.4...v0.31.5
[v0.31.4]: https://github.com/SabakiHQ/Sabaki/compare/v0.31.3...v0.31.4
[v0.31.3]: https://github.com/SabakiHQ/Sabaki/compare/v0.31.2...v0.31.3
[v0.31.2]: https://github.com/SabakiHQ/Sabaki/compare/v0.31.1...v0.31.2
[v0.31.1]: https://github.com/SabakiHQ/Sabaki/compare/v0.31.0...v0.31.1
[v0.31.0]: https://github.com/SabakiHQ/Sabaki/compare/v0.30.3...v0.31.0
[v0.30.3]: https://github.com/SabakiHQ/Sabaki/compare/v0.30.2...v0.30.3
[v0.30.2]: https://github.com/SabakiHQ/Sabaki/compare/v0.30.1...v0.30.2
[v0.30.1]: https://github.com/SabakiHQ/Sabaki/compare/v0.21.0...v0.30.1
[v0.21.0]: https://github.com/SabakiHQ/Sabaki/compare/v0.19.3...v0.21.0
[v0.19.3]: https://github.com/SabakiHQ/Sabaki/compare/v0.18.3...v0.19.3
[v0.18.3]: https://github.com/SabakiHQ/Sabaki/compare/v0.17.2...v0.18.3
[v0.17.2]: https://github.com/SabakiHQ/Sabaki/compare/v0.15.3...v0.17.2
[v0.15.3]: https://github.com/SabakiHQ/Sabaki/compare/v0.14.0...v0.15.3
[v0.14.0]: https://github.com/SabakiHQ/Sabaki/compare/v0.12.4...v0.14.0
[v0.12.4]: https://github.com/SabakiHQ/Sabaki/compare/v0.11.5...v0.12.4
[v0.11.5]: https://github.com/SabakiHQ/Sabaki/compare/v0.11.2...v0.11.5
[v0.11.2]: https://github.com/SabakiHQ/Sabaki/compare/v0.10.1...v0.11.2
[v0.10.1]: https://github.com/SabakiHQ/Sabaki/compare/v0.9.1...v0.10.1
[v0.9.1]: https://github.com/SabakiHQ/Sabaki/compare/v0.8.1...v0.9.1
[v0.8.1]: https://github.com/SabakiHQ/Sabaki/compare/v0.7.6...v0.8.1
[v0.7.6]: https://github.com/SabakiHQ/Sabaki/compare/v0.7.1...v0.7.6
[v0.7.1]: https://github.com/SabakiHQ/Sabaki/compare/v0.5.0...v0.7.1
[v0.5.0]: https://github.com/SabakiHQ/Sabaki/compare/v0.4.2...v0.5.0
[v0.4.2]: https://github.com/SabakiHQ/Sabaki/compare/v0.3.7...v0.4.2
[v0.3.7]: https://github.com/SabakiHQ/Sabaki/compare/v0.3.6...v0.3.7
[v0.3.6]: https://github.com/SabakiHQ/Sabaki/compare/v0.3.5...v0.3.6
[v0.3.5]: https://github.com/SabakiHQ/Sabaki/compare/v0.3.0...v0.3.5
[v0.3.0]: https://github.com/SabakiHQ/Sabaki/compare/v0.1.0...v0.3.0
