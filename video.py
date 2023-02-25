from videoreader import VideoReader

class Video:
  def __init__(self, path: str, terminal_size: tuple):
    self.path                = path
    self.terminal_size       = terminal_size
    self.frame_count         = 0
    self.frame_width         = 0
    self.frame_height        = 0
    self.fps                 = 0
    self.frames              = []
    self.preprocessed_frames = []

  def load(self, args):
    # Load the video
    self.reader         = VideoReader(self.path)
    self.frame_count    = self.reader.number_of_frames
    self.frame_width    = self.reader.frame_width
    self.frame_height   = self.reader.frame_height
    self.fps            = self.reader.frame_rate

    # Config options
    self.NO_BAR                     = args.no_bar
    self.SHOW_PROGRESS_PERCENTAGE   = args.no_percentage
    self.SHOW_FPS                   = args.show_fps
    self.SHOW_Q_SIZE                = args.show_q_size
    self.SHOW_FRAME_POS             = args.show_frame_pos
    self.SHOW_TIME                  = args.show_time

    self.NO_COLOR                   = args.no_color
    self.COLORIZATION               = args.colorization

    self.PREPROCESSING_WORKERS      = args.preprocessing_workers[0]

  def get_frame(self, pos):
    return self.reader[pos]

  def read(self, pos):
    with open(f"frames/{pos}", "rb") as f:
      return f.read()