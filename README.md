# Youtube ASCII

A script to display any Youtube video as ASCII art in the terminal.

## Installation

```bash
git clone
cd youtube-ascii
pip install -r requirements.txt
```

## Usage

### From a Youtube URL

```bash
python youtube-ascii.py -u <youtube-url>
```

### From a `webm` file

```bash
python youtube-ascii.py -f <webm-file>
```

## Dependencies

* [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading the video
* [ffmpeg](https://ffmpeg.org/) for converting the video to a `webm` file
* [Pillow](https://pillow.readthedocs.io/en/stable/) for resizing the video
* [pyvideoreader](https://github.com/postpop/videoreader) for reading the video

## Speed

The speed of the script depends on the number of threads you use. The default is 4 threads. You can change it by using the `-pw` option.

> Note: If you use too many threads, the script will be slower than if you use less threads.

> Note: More the the scaling factor is, more the script will be slower.

## Options

You hasn't to specify any width or height. The script will automatically calculate the width and the height of the terminal and adapt the video to it.

| Option | Params | Description |
| --- | --- | --- |
| `-pw`, `--preprocessing-workers` | WORKERS (default=4) | Number of threads to use for downloading the video |
| `-u`, `--url` | URL | Youtube URL |
| `-f`, `--file` | FILE | Webm file |
| `-h`, `--help` | | Show help |
| `-v`, `--version` | | Show version |
| `--no-color` | | Disable colorization |
| `--colorization` | {FG\|BG} (default=BG) | Colorization mode (foreground or background) |
| `--show-fps` | | Show the FPS of the video |
| `--no-bar` | | Disable the progress bar |
| `--no-percentage` | | Disable the percentage |
| `--show-time` | | Show the time elapsed |
| `--show-q-size` | | Show the size of the queue |
| `--show-frame-pos` | | Show the position of the frame |

### Colorization

The colorization is done by using the ANSI encoding. The color is chosen by using the average of the RGB values of the pixel.

If you want to disable the colorization, you can use the `--no-color` option. Only the
characters will be displayed.

#### Foreground

The foreground colorization is done by using the ANSI escape code `38;2;${r},${g},${b}` where `r`, `g` and `b` are the RGB values of the pixel.

#### Background

The background colorization is done by using the ANSI escape code `48;2;${r},${g},${b}` and the ANSI escape code `38;2;${r},${g},${b}` where `r`, `g` and `b` are the RGB values of the pixel.

## Examples

[![asciicast](https://asciinema.org/a/562819.svg)](https://asciinema.org/a/562819)

[![asciicast](https://asciinema.org/a/562822.svg)](https://asciinema.org/a/562822)

[![asciicast](https://asciinema.org/a/562825.svg)](https://asciinema.org/a/562825)

## Acknowledgments

* [sppmacd](https://gist.github.com/sppmacd/0a806c65ce634b2825c4016c88b73c73) for the idea

## Contributing

Feel free to open an issue or a pull request if you want to contribute to this project.

## Authors

* **Hokanosekai** - *Initial work* - [Hokanosekai](https://github.com/Hokanosekai)
* **Bash62** - *Initial work* - [Bash62](https://github.com/Bash62)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
