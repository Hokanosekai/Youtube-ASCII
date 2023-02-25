import curses
import math
from queue import Queue
from threading import Lock, Thread
import time
from video import Video

class Renderer:
  def __init__(self, video: Video, stdscr, Q: Queue):
    self.video              = video
    self.stdscr             = stdscr

    self.stopped            = False

    self.pos                = 0
    self.Q                  = Q

    self.lock               = Lock()
    self.thread             = Thread(target=self.update, args=(Q,))
    #self.thread.daemon = True

    self.buffer_1           = ""
    self.buffer_2           = None

    self.use_buffer_1       = True

  def start(self):
    self.thread.start()
    return self

  def stop(self):
    self.stopped = True

    self.thread.join()
  
  def running(self):
    return not self.stopped

  def update(self, Q: Queue):
    last_time, frames, current_second, previous_second, fps = 0, 0, 0, 0, 0
    start_time      = time.time()
    delay           = 1.0 / 50

    while self.running():
      # Clear the screen
      self.stdscr.clear()
      # Move the cursor to the top left
      print("\033[0;0H", end="")

      # Calculate the time it took to process the frame
      start_time  = time.time()
      delta_frame = start_time - last_time
      last_time   = start_time

      #print(f"Rendering: Frame {self.pos}/{self.video.frame_count} ({self.pos*100/self.video.frame_count:.1f}%) Qsize ({self.self.Q.qsize()})", end="")

      with self.lock:
        # Render the frame
        if self.use_buffer_1:
          self.render(self.buffer_1)
          self.buffer_2, _ = Q.get()
        else:
          self.render(self.buffer_2)
          self.buffer_1, _ = Q.get()

      self.pos += 1

      # Swap the buffers
      self.use_buffer_1 = not self.use_buffer_1

      # Show the progress bar
      if not self.video.NO_BAR:
        self.show_progress_bar(self.video, self.pos)

      # Show the stats
      if self.video.SHOW_Q_SIZE:
        with self.lock:
          # Show Qsize
          print(f"QS: {Q.qsize()} ", end="")

      if self.video.SHOW_FRAME_POS:
        # Show the frame number
        print(f"F: {self.pos}/{self.video.frame_count} ", end="")

      if self.video.SHOW_TIME:
        # Show the frame time
        print(f"FT: {delta_frame:.3f} ", end="")

        # Show the elapsed time in seconds
        print(f"ET: {current_second - previous_second:.3f}s ", end="")

        # Show the delay
        print(f"D: {delay:.3f} ", end="")

      if not self.video.SHOW_PROGRESS_PERCENTAGE:
        # Show the percentage
        print(f"P: {self.pos*100/self.video.frame_count:.1f}% ", end="")

      if self.video.SHOW_FPS:
        # Calculate the fps
        current_second += delta_frame
        elapsed_seconds = current_second - previous_second

        if elapsed_seconds >= 0.25:
          fps = frames / elapsed_seconds
          previous_second = current_second
          frames = 0

        frames += 1

        # Show the fps
        self.show_fps(fps)

      # Limit the framerate
      frame_time = time.time() - start_time
      if frame_time < delay:
        curses.napms(int((delay - frame_time) * 1000))

      with self.lock:
        Q.task_done()

  def show_progress_bar(self, video, pos):
    # Calculate the progress percentage
    progress = pos / video.frame_count * 100

    # Calculate the progress bar length = terminal width
    bar_length = video.terminal_size[0]

    # Calculate the progress bar position
    bar_pos = math.floor(progress / 100 * bar_length)

    # Create the progress bar
    bar = f"\x1b[37m{'█' * bar_pos}{' ' * (bar_length - bar_pos)}"

    print(f"\033[{self.video.terminal_size[1]};0H{bar}", end="")

  def show_fps(self, fps):
    print(f"{fps:.1f} FPS", end="")

  def render(self, ascii_frame):
    # Split the frame into 3 parts
    

    print(f"{ascii_frame}", end="")
    #try:
    #  self.stdscr.addnstr(0, 0, ascii_frame, self.video.terminal_size[0] * self.video.terminal_size[1])
    #except curses.error:
    #  pass

