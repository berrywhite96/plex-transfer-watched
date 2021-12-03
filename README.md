# Plex Transfer Watched State

## Overview

As I wanted to switch to another Plex agent, I recognized that the already scanned files are not updated. For example if you switch to the Plex Movie agent the scanned items are not updated and doesn't get the trailer function or the IMDB rating. To rescan all items you need to recreate the library. So you loose all states including the watched states, this is the reason why this tool exist.

It exports all watched items from a movie or tv show library to a JSON file. This file can be imported to another library, it tries to match the item by the name and sets the watch state.

## Installation

Python 3 is needed, Python 3.8.3 was used during development.
Clone this repository and open console.

``pip install -r requirements.txt``

## Usage

### Export states

To export library states to a JSON file just replace the parameters.

``python plex_watched.py export PLEX_USERNAME PLEX_PASSWORD PLEX_SERVER_NAME OLD_PLEX_LIBRARY``

### Import states

To import library states to a JSON file just replace the parameters.

``python plex_watched.py import PLEX_USERNAME PLEX_PASSWORD PLEX_SERVER_NAME NEW_PLEX_LIBRARY``

## ToDo

Currently nothing.