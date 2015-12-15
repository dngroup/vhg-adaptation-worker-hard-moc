import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from XMLparser import readXML
from settings import DELAY


def is_valideXML(srcPath):
    pass


def TestIfXML(srcPath):
    suffix = '.xml'
    if (srcPath.endswith(suffix)):
        return True
    else :
        return False




def movefile(srcPath):
    vtuxml = readXML(srcPath)
    if vtuxml == False:
        logging.info("%s doesn't validate", srcPath)
    else:
        logging.info("%s validates", srcPath)
        contentFile = vtuxml.find('in').find('local').find('stream').text
        logging.info("The content file is %s", contentFile)
        pathContentFile = "/vTU/vTU/input/" + contentFile

        # pathContentFile = os.path.dirname(os.path.abspath(srcPath)) +"/" +contentFile
        logging.info("The content file is here %s", pathContentFile)
        contentOuputFile = vtuxml.find('out').find('local').find('stream').text

        pathOuputContentFile = "/usr/share/nginx/html/output/" + contentOuputFile
        time.sleep(DELAY)
        try:
            os.rename(srcPath, pathOuputContentFile + '.xml')
            logging.info("move xml")
        except OSError as e:

            logging.info("The content file is not found may be already move %s", srcPath)
            pass
        try:
            os.rename(pathContentFile, pathOuputContentFile)
            logging.info("move content", srcPath)
        except OSError as e:
            logging.error("The content file is not found may be already move %s", pathContentFile)
            pass


def do(src_path):
    if TestIfXML(src_path):
        movefile(src_path)
    pass


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        do(event.src_path)

    def on_moved(self, event):
        do(event.dest_path)
        # what = 'directory' if event.is_directory else 'file'
        # logging.info("Moved %s: from %s to %s", what, event.src_path,
        #             event.dest_path)

    def on_created(self, event):
        do(event.src_path)
        # what = 'directory' if event.is_directory else 'file'
        # logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        # logging.info("Deleted file or directory: %s", event.src_path)
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Start python",)
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = '/vTU/vTU/spool/'
    # path = test
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
