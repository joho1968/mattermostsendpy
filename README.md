## mattermostsendpy
Simple CLI utility for posting text to a Mattermost Incoming Webhook, written in Python 3

## Usage

`mmsend.py [<section>|none] [test|send] [<url>|config] [<text>]`

## Background

Simply to start building (yet another) Python codebase for talking to Mattermost :)

## Installation

Put mmsend.py and mmsend.sample.ini somewhere, in the same place. Copy mmsend.sample.ini to mmsend.ini. Edit as needed. Set execute rights on mmsend.py (not required if you manually invoke with Python binary), and off you go. All output by mmsend.py is written to stderr, except for possible Python RTL output which goes wherever it's set to go :)

The intent has been to do this without third-party libraries/modules/etc.

Oh, you need to create an "Incoming Webhook" in your Mattermost as well.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
