import argparse
import logging
import subprocess
import threading
import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

logging.basicConfig()
logger = logging.getLogger(__name__)


class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, exec_string, *args, **kwargs):
        super(FileChangeHandler, self).__init__(*args, **kwargs)
        self.exec_string = exec_string
        self.updated = threading.Event()

        def worker():
            while True:
                self.updated.wait()
                # Allow multiple inst. saves to not cause multiple execs
                time.sleep(0.5)
                subprocess.call(self.exec_string, shell=True)
                self.updated.clear()

        self.thread = threading.Thread(target=worker)
        self.thread.daemon = True
        self.thread.start()

    def on_modified(self, event):
        super(FileChangeHandler, self).on_modified(event)
        print "Modified {}".format(event.src_path)
        self.updated.set()

def main():
    parser = argparse.ArgumentParser()
    # First argument
    parser.add_argument(
        'exec_string', type=str, help='Command to run when files change')
    # Optional arguments
    parser.add_argument(
        '--pattern', type=str, help='What types of files to match')
    args = parser.parse_args()
    subprocess.call(args.exec_string, shell=True)
    event_handler = FileChangeHandler(
        exec_string=args.exec_string,
        patterns=['*.py',],
        ignore_directories=True)
    observer = Observer()
    observer.schedule(event_handler, './', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.error("Keyboard Interrupt: Stopping")
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
