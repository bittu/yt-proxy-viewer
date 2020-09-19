# yt-proxy-viewer
Increase youtube views with different proxies

This tool depends on python3 and uses some libraries. In order to install them, you can use pip:

```sh
$ sudo pip3 install -r requirements.txt
```

## Usage
```sh
$ python3 bot.py --help
usage: bot.py [--visits VISITS] [--file FILE] [--proxy PROXY] [-v] [-h] [--no-proxy]

Tool to increase YouTube views

Main Arguments:
  --visits VISITS  amount of times the video will be viewed. Default: 1
  --file FILE      Youtube URL file list (one url per line)
  --proxy PROXY    set the proxy server to be used. e.g: 127.0.0.1:8118

Optional Arguments:
  -v, --verbose    show more output
  -h, --help       show this help message and exit
  --no-proxy       play without proxy
$
```

## Example
```sh
$ python3 bot.py --visits 2 --file urls.txt --verbose
```

To run without proxy
```sh
$ python3 bot.py --visits 2 --file urls.txt --verbose --no-proxy
```
