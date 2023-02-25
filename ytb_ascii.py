import argparse
import multiprocessing
import os
from queue import Queue
import sys
import threading
import curses
from preprocessor import Preprocessor
from renderer import Renderer
from video import Video

SHOW_PROGRESS_BAR           = True
SHOW_PROGRESS_PERCENTAGE    = True
SHOW_FPS                    = False
SHOW_Q_SIZE                 = False
SHOW_POS                    = False
SHOW_TIME                   = False

PREPROCESSING_WORKERS       = 4

Q                           = Queue(maxsize=60)

def main(stdscr, video: Video, args):
    # Load the video
    video.load(args)

    # Enable colors
    curses.start_color()
    curses.use_default_colors()

    # Disable cursor
    curses.curs_set(0)

    # Disable echo
    curses.noecho()

    # Disable input buffering
    curses.cbreak()

    # Enable keypad
    stdscr.keypad(True)

    # Enable nodelay
    stdscr.nodelay(True)


    # Create the preprocessor
    preprocessor = Preprocessor(video, Q)
    # Create the renderer
    renderer     = Renderer(video, stdscr, preprocessor.Q)

    # Start the threads
    preprocessor.start()
    renderer.start()

# Download the video using yt-dlp
def download_video(url):
    # Get the video ID
    video_id = url.split("=")[-1]

    # Check if the video already exists
    if os.path.exists(f"{video_id}.webm"):
        return f"video/{video_id}.webm"

    # Create the directory for the video
    os.makedirs("video", exist_ok=True)

    # Change the working directory
    os.chdir("video")

    # Download the video
    os.system(f"yt-dlp -f bestvideo -o {video_id}.webm {url}")

    # Change the working directory
    os.chdir("..")

    return f"video/{video_id}.webm"


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(
        prog="yt-ascii",
        description="Convert a video to ASCII art."
    )

    # Add the arguments
    # -pw --preprocessing-workers -> Set the number of preprocessing workers
    # -u --url <url>              -> Download the video from the given URL
    # -f --file <file>            -> Load the video from the given file (webm)
    # -h --help                   -> Show the help message (DEFAULT)
    # -v --version                -> Show the version
    # --no-bar                    -> Disable the progress bar
    # --show-fps                  -> Show the FPS
    # --no-percentage             -> Disable the progress percentage
    # --show-q-size               -> Show the size of the queue
    # --show-frame-pos                  -> Show the position of the video
    # --show-time                 -> Show the time of the video
    # --no-color                  -> Disable color
    # --colorization {FG|BG}      -> How the ASCII art should be colorized
    parser.add_argument("-pw", "--preprocessing-workers", nargs="?", type=int, default=4, help="Set the number of preprocessing workers.")
    parser.add_argument("-u", "--url", nargs="?", type=str, help="Download the video from the given URL.")
    parser.add_argument("-f", "--file", nargs="?", type=str, help="Load the video from the given file (webm).")
    parser.add_argument("--colorization", type=str, default="FG", choices=["FG", "BG"], help="How the ASCII art should be colorized.")
    parser.add_argument("-v", "--version", action="version", version="yt-ascii 1.0.0", help="Show the version.")
    parser.add_argument("--no-bar", action="store_true", help="Disable the progress bar.")
    parser.add_argument("--show-fps", action="store_true", help="Show the FPS.")
    parser.add_argument("--no-percentage", action="store_true", help="Disable the progress percentage.")
    parser.add_argument("--show-q-size", action="store_true", help="Show the size of the queue.")
    parser.add_argument("--show-frame-pos", action="store_true", help="Show the position of the video.")
    parser.add_argument("--show-time", action="store_true", help="Show the time of the video.")
    parser.add_argument("--no-color", action="store_true", help="Disable color.")

    # Parse the arguments
    args = parser.parse_args()

    # Define the video path
    video_path = "video.webm"

    # Check if the video should be downloaded
    if args.url:
        # Download the video
        video_path = download_video(args.url)
    elif args.file:
        video_path = args.file
    else:
        print("Please specify a video to load.")
        sys.exit()

    # Get the terminal size
    rows, columns = os.popen('stty size', 'r').read().split()
    # Load the video
    video = Video(video_path, (int(columns), int(rows) - 1)) # -1 for the progress bar

    # Start the curses wrapper
    curses.wrapper(main, video, args)
    #main(None, video)