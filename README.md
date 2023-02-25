# Youtube ASCII

A script to display any Youtube video as ASCII art in the terminal.

## Installation

```bash
$ git clone
$ cd youtube-ascii
$ pip install -r requirements.txt
```

## Usage

### From a Youtube URL

```bash
$ python youtube-ascii.py -u <youtube-url>
```

### From a `webm` file

```bash
$ python youtube-ascii.py -f <webm-file>
```

## Options

| Option | Params | Description |
| --- | --- | --- |
| `-u` | \<youtube-url> | Youtube URL |
| `-f` | \<webm-file> | Webm file |
| `-h` | | Show help |
| `-v` | | Show version |
| `-pw` | \<threads> (default=4) | Number of threads to use for downloading the video |
| `--no-color` | | Disable colorization |
| `--colorization` | \<FG\|BG> | Colorization mode (foreground or background) |
| `--show-fps` | | Show the FPS of the video |
| `--no-bar` | | Disable the progress bar |
| `--no-percentage` | | Disable the percentage |
| `--show-time` | | Show the time elapsed |
| `--show-q-size` | | Show the size of the queue |
| `--show-frame-pos` | | Show the position of the frame |

## Examples

[![asciicast](https://asciinema.org/a/562819.svg)](https://asciinema.org/a/562819)

[![asciicast](https://asciinema.org/a/562822.svg)](https://asciinema.org/a/562822)

[![asciicast](https://asciinema.org/a/562825.svg)](https://asciinema.org/a/562825)

## Acknowledgments

* [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading the video
* [sppmacd](https://gist.github.com/sppmacd/0a806c65ce634b2825c4016c88b73c73) for the idea

## Contributing

Feel free to open an issue or a pull request if you want to contribute to this project.

## Authors

* **Hokanosekai** - *Initial work* - [Hokanosekai](https://github.com/Hokanosekai)
* **Bash62** - *Initial work* - [Bash62](https://github.com/Bash62)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
