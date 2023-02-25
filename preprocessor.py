from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Lock, Thread
import numpy as np
from PIL import Image

from video import Video

class Preprocessor:
  def __init__(self, video: Video, Q: Queue):
    self.video              = video
    self.terminal_size      = video.terminal_size
    self.frame_count        = video.frame_count

    self.stopped            = False
    self.Q                  = Q
    self.frames             = []

    self.lock               = Lock()

    self.executor           = ThreadPoolExecutor(max_workers=video.PREPROCESSING_WORKERS)
    self.futures            = []

  def start(self):
    """
    for i in range(len(self.futures), self.frame_count):
      print(f"Preprocessing: Frame {i}/{self.frame_count} ({i*100/self.frame_count:.1f}%)", end="\r")
      time.sleep(0.01)
      self.futures.append(self.executor.submit(self.preprocess, i))
    """

    self.futures = [self.executor.submit(self.preprocess, i) for i in range(self.frame_count)]

    return self
  
  def stop(self):
    self.stopped = True

  def running(self):
    return self.more() or not self.stopped

  def more(self):
    return not all([future.done() for future in self.futures])

  def preprocess(self, index):
    self.lock.acquire()
    # Get the frame
    _, frame = self.video.reader.read(index)

    # Calculate the step size to use when converting the video to frames
    # Consider the terminal size and the frame size
    # note to remove height of progress bar
    x_step = self.video.frame_width / self.terminal_size[0]
    y_step = self.video.frame_height / (self.terminal_size[1] - 1)

    # Create an array of row and column indices for the image
    rows = np.arange(0, self.video.frame_height, y_step, dtype=int)
    cols = np.arange(0, self.video.frame_width, x_step, dtype=int)

    # Use meshgrid to create arrays of row and column indices for each pixel
    row_indices, col_indices = np.meshgrid(rows, cols, indexing='ij')

    # Index into the frame using the row and column indices to get the RGB values for each pixel
    pixels = frame[row_indices, col_indices]

    # Reshape the pixels array to be 1D and concatenate the RGB values for each pixel
    buffer = np.concatenate(pixels.reshape(-1, 3))

    # Convert the buffer to bytes
    buffer = buffer.astype(np.uint8).tobytes()


    # Create an image from the bytes and resize it
    image = Image.frombytes("RGB", (self.terminal_size[0], (self.terminal_size[1] - 1)), buffer)
    #image = image.resize(self.terminal_size, resample=Image.BILINEAR)

    ascii_parts = ""

    rgb_values = np.array(image)
    # Compute the luminance for each pixel using the formula Y = 0.299R + 0.587G + 0.114B
    luminance = np.dot(rgb_values, [0.299, 0.587, 0.114])

    # Compute the ASCII characters for the part using the luminance and color values
    ascii_chars = np.vectorize(self.get_char)(luminance, rgb_values[:, :, 2], rgb_values[:, :, 1], rgb_values[:, :, 0])

    # Join the ASCII characters for each row into a string and append it to ascii_parts
    ascii_part = "".join(ascii_chars.ravel())
    """
    for i in range(3):
      part = image.crop((0, i * part_length, width, (i + 1) * part_length))
      \"""
      # Convert the part to ASCII art
      r, g, b = np.array(part).T
      grayscale = int((r + g + b) / 3)
      ascii_chars = np.vectorize(self.get_char)(grayscale, r, g, b)
      ascii_part = "".join(ascii_chars)

      ascii_parts.append(ascii_part)


      ascii_part = ""
      for y in range(part.height):
        for x in range(part.width):
          b, g, r = part.getpixel((x, y))

          ascii_part += f"{self.get_char(int((r + g +b) / 3), r, g, b)}"
      ascii_parts.append(ascii_part)
      \"""

      # Get the RGB values for all pixels in the part
      rgb_values = np.array(part)

      # Compute the luminance for each pixel using the formula Y = 0.299R + 0.587G + 0.114B
      luminance = np.dot(rgb_values, [0.299, 0.587, 0.114])

      # Compute the color values for each pixel
      color_values = rgb_values.astype(float) / 255.0

      # Compute the ASCII characters for the part using the luminance and color values
      ascii_chars = np.vectorize(self.get_char)(luminance, rgb_values[:, :, 2], rgb_values[:, :, 1], rgb_values[:, :, 0])

      # Join the ASCII characters for each row into a string and append it to ascii_parts
      ascii_parts.append("".join(ascii_chars.ravel()))
    """

    self.Q.put((ascii_part, index))
    self.lock.release()

  def get_char(self, luminance: int, r, g, b) -> str:
    char = " "
    # 0 - 255
    if luminance < 25:
      char = " "
    elif luminance < 50:
      char = "."
    elif luminance < 75:
      char = ":"
    elif luminance < 100:
      char = "-"
    elif luminance < 125:
      char = "="
    elif luminance < 150:
      char = "+"
    elif luminance < 175:
      char = "*"
    elif luminance < 200:
      char = "#"
    elif luminance < 225:
      char = "%"
    else:
      char = "@"

    mode = f"\x1b[{38};2;{r};{g};{b}m" if self.video.COLORIZATION == "FG" else f"\x1b[{38};2;{r};{g};{b}m\x1b[{48};2;{r};{g};{b}m" 

    return f"{mode}{char}\x1b[0m" if not self.video.NO_COLOR else char

