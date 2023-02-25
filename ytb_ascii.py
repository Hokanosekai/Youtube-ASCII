import argparse
import os
from queue import Queue
import sys
import curses
from preprocessor import Preprocessor
from renderer import Renderer
from video import Video

__version__ = "0.1.0"
__authors__ = ["Hokanosekai", "Bash62"]
__description__ = "Watch a video in ASCII art in your terminal."
__license__ = "MIT"

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
        prog="ytb_ascii",
        description=__description__,
        epilog=f"Authors: {', '.join(__authors__)}",
        allow_abbrev=False,
        add_help=False,
    )

    # Add the arguments
    # DEFAULT: (REQUIRED)
    # -pw --preprocessing-workers -> Set the number of preprocessing workers
    # SOURCE: (MUTUALLY EXCLUSIVE) (REQUIRED)
    # -u --url <url>              -> Download the video from the given URL
    # -f --file <file>            -> Load the video from the given file (webm)
    # HELP:
    # -h --help                   -> Show the help message (DEFAULT)
    # -v --version                -> Show the version
    # OPTIONS: (NOT REQUIRED)
    # --no-bar                    -> Disable the progress bar
    # --show-fps                  -> Show the FPS
    # --no-percentage             -> Disable the progress percentage
    # --show-q-size               -> Show the size of the queue
    # --show-frame-pos            -> Show the position of the video
    # --show-time                 -> Show the time of the video
    # --no-color                  -> Disable color
    # --colorization {FG|BG}      -> How the ASCII art should be colorized

    default_group = parser.add_argument_group("Default arguments", "These arguments are used by default.")
    default_group.add_argument("-pw", "--preprocessing-workers", nargs=1, type=int, default=4, help="Set the number of preprocessing workers.")

    source_group = default_group.add_mutually_exclusive_group(required=True)
    source_group.add_argument("-u", "--url", nargs=1, type=str, help="Download the video from the given URL.")
    source_group.add_argument("-f", "--file", nargs=1, type=str, help="Load the video from the given file (webm).")

    help_group = parser.add_argument_group("Help arguments", "These arguments are used to show help messages.")
    help_group.add_argument("-v", "--version", action="version", version=__version__, help="Show the version.")
    help_group.add_argument("-h", "--help", action="help", help="Show the help message.")

    options_group = parser.add_argument_group("Options", "These arguments are used to change the options.")
    options_group.add_argument("--no-bar", action="store_true", help="Disable the progress bar.", default=False)
    options_group.add_argument("--show-fps", action="store_true", help="Show the FPS.", default=True)
    options_group.add_argument("--no-percentage", action="store_true", help="Disable the progress percentage.", default=True)
    options_group.add_argument("--show-q-size", action="store_true", help="Show the size of the queue.", default=False)
    options_group.add_argument("--show-frame-pos", action="store_true", help="Show the position of the video.", default=False)
    options_group.add_argument("--show-time", action="store_true", help="Show the time of the video.", default=False)
    options_group.add_argument("--no-color", action="store_true", help="Disable color.", default=False)
    options_group.add_argument("--colorization", type=str, default="BG", choices=["FG", "BG"], help="How the ASCII art should be colorized. (FG: Foreground, BG: Background) (Default: BG)")

    # Parse the arguments
    args = parser.parse_args()

    # Define the video path
    video_path = "video.webm"

    # Check if the video should be downloaded
    if args.url:
        # Download the video
        video_path = download_video(args.url[0])
    elif args.file:
        video_path = args.file[0]
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