from plexapi.myplex import MyPlexAccount
from plexapi.exceptions import NotFound as NotFoundException
import argparse
import logging
import json


class PlexWatched():
    def __init__(self, user, password, serverName, library, exportFilepath):
        logging.info("Logging into account...")
        self.account = MyPlexAccount(user, password)
        logging.info("Logged in!")
        logging.info("Connecting to server...")
        self.plexServer = self.account.resource(serverName).connect()
        logging.info("Connected!")
        self._library = library
        self._exportFilepath = exportFilepath
    
    def exportWatched(self):
        try:
            section = self.plexServer.library.section(self._library)
        except NotFoundException as e:
            logging.error("Unknown library: " + self._library)
            return
        
        exportedLibrary = []
        
        items = section.search(unwatched=False)
        for item in items:
            exportedLibrary.append({
                "title": item.title,
                "year": item.year,
            })
        
        with open(self._exportFilepath, 'w') as f:
            f.write(json.dumps(exportedLibrary))
        logging.info("Exported to " + self._exportFilepath)
        
    def importWatched(self):
        file = open(self._exportFilepath,mode='r')
        fileContent = file.read()

        try:
            section = self.plexServer.library.section(self._library)
        except NotFoundException as e:
            logging.error("Unknown library: " + self._library)
            return
            
        exportedData = json.loads(fileContent)
        for item in exportedData:
            try:
                libraryItem = section.get(item["title"])
            except NotFoundException as e:
                logging.warning("Unknown item: " + str(item))
                continue
            libraryItem.markWatched()
        
        logging.info("Imported from " + self._exportFilepath)

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, help="Mode can be 'export' or 'import'")
    parser.add_argument("plexUsername", type=str, help="Login Plex username")
    parser.add_argument("plexPassword", type=str, help="Login Plex password")
    parser.add_argument("plexServername", type=str, help="Plex server name which can be found in the webinterface")
    parser.add_argument("plexLibrary", type=str, help="Export library name name which can be found in the webinterface")
    parser.add_argument("--export-path", type=str, default="export.json", help="JSON filepath including all watched items from library")

    args = parser.parse_args()
    
    plexWatched = PlexWatched(args.plexUsername, args.plexPassword, args.plexServername, args.plexLibrary, args.export_path)
    if args.mode == "export":
        plexWatched.exportWatched()
    elif args.mode == "import":
        plexWatched.importWatched()
    else:
        logging.error("Unknown mode, exit")
