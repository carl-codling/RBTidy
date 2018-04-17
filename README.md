** This project has not been followed or maintained for a few years now, I simply leave the code here for archival purposes **
-----------------------------------------------------------------------------------------------------------------------------

RBTidy - Rhythmbox Plugin
=========================

This plugin provides a toolbar which enables you to batch edit the title, artist, album and genre fields of your music files.

Once the plugin is installed and enabled you will find the toolbar at the bottom of the song list. You will find 4 rows of buttons, switches, etc.:

All the tools below work on the current selection (those songs you've selected and are highlighted orange)

__Row 1__

- [SELECT] Field selector: select whether you are currently editing title, artist, album or genre
- [INPUT] Test output: the result of the test buttons/switch on the other rows is output in this text field

__Row 2__

- [BTN] Strip track no.: attempts to strip any numbers and special chars that look like a track number (only generally relevant to the title field)
- [BTN] Strip special: Strip all special chars from the text. 
- [BTN] Special to space: Replace all special chars with a space
- [BTN] Special to -: Replace all special chars with -
- [BTN] Capitalise
- [SWITCH] Test: When set to on the output of the preceding buttons is sent to the test output field and does not modify the actual text

__Row 3__

Replace a segment of the text with something else

- [SELECT/INPUT] Replace: a string or regular expression (see in the dropdown options for examples) to replace in the selected songs/field
- [SELECT/INPUT] With: the replacement string - or select ::REGEX-MATCH from the drop down to replace the whole text with the first substring match from a regular expression string set in the Replace field above
- [BTN] Replace
- [BTN] Test

__Row 4__

Copy a segment of the current field to another field

- [SELECT/INPUT] Copy from: a string to search for in the current field that signifies the beggining of the copy text. Select [START] from the drop down to start the copied text from the start of the source text
- [SELECT/INPUT] to: a string to search for in the current field that signifies the end of the copy text. Select end to copy up to the end of the source text
- [SELECT] to: the field to paste the copied text to
- [SWITCH] Rem. from src: Remove the copied text from the source field
- [BTN] Move
- [BTN] Test
