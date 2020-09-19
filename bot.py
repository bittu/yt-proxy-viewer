#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" Bot to increase YouTube views """

import sys
import time
from random import randrange, choice
from modules.youtube import YouTube
from modules import utils
import asyncio
from proxybroker import Broker
from tqdm import tqdm
import math


class Bot:
    """ A bot to increase YouTube views """
    # pylint: disable=R0903,R0912

    def __init__(self, options):
        """ init variables """

        self.opts = options

    @staticmethod
    def player_status(value):
        """ returns the status based one the input code """

        status = {
            -1: 'unstarted',
            0: 'ended',
            1: 'playing',
            2: 'paused',
            3: 'buffering',
            5: 'video cued',
        }
        return status[value] if value in status else 'unknown'

    def run(self):
        """ run """

        count = 1
        failed = False
        ipaddr = None
        while count <= self.opts.visits:
            if not ipaddr:
                ipaddr = utils.get_ipaddr(proxy=self.opts.proxy)
            print('ipaddr:', ipaddr)
            if not ipaddr:
                failed = True
                break
            youtube = YouTube(
                url=self.opts.url,
                proxy=self.opts.proxy,
                verbose=self.opts.verbose
            )
            title = youtube.get_title()
            if not title:
                if self.opts.verbose:
                    print('there was a problem loading this page. Retrying...')
                youtube.disconnect()
                failed = True
                break
            if self.opts.visits:
                length = (len(title) + 4 - len(str(count)))
                print('[{0}] {1}'.format(count, '-' * length))
            if ipaddr:
                print('external IP address:', ipaddr)
            channel_name = youtube.get_channel_name()
            if channel_name:
                print('channel name:', channel_name)
            subscribers = youtube.get_subscribers()
            if subscribers:
                print('subscribers:', subscribers)
            print('title:', title)
            views = youtube.get_views()
            if views:
                print('views:', views)
            # youtube.play_video()
            youtube.skip_ad()
            if self.opts.verbose:
                status = youtube.get_player_state()
                print('video status:', self.player_status(status))
            video_duration = youtube.time_duration()
            seconds = 30
            if video_duration:
                print('video duration time:', video_duration)
                seconds = utils.to_seconds(duration=video_duration.split(':'))
                if seconds:
                    if self.opts.verbose:
                        print('video duration time in seconds:', seconds)
            sleep_time = seconds
            print('stopping video in %s seconds' % sleep_time)
            youtube.get_screenshot()
            # time.sleep(sleep_time)
            playing = True
            # duration = math.floor(youtube.get_duration())
            # print('duration:', youtube.get_duration(),  duration)
            pbar = tqdm(total=seconds)
            while playing:
                status = youtube.get_player_state()
                current_time = math.floor(youtube.get_current_time())
                statusText = self.player_status(status)

                if status == -2:
                    playing = False
                    print('failure playing video')
                    break

                if statusText == 'ended':
                    playing = False
                    print('video playback ended')
                    break

                pbar.set_description(statusText)
                pbar.refresh()
                pbar.update()

                if statusText == 'unstarted':
                    youtube.skip_ad()
                    continue
                if statusText == 'paused' or statusText == 'video cued':
                    youtube.play_video()
                # print('video status: {0} current time: {1} duration: {2}'.format(statusText, current_time, duration))
                time.sleep(1)
            pbar.close()
            youtube.disconnect()
            count += 1

        if failed:
            return False
        return True

def call_bot(urls, cli_args):
    for i in range(3):
        cli_args.url = choice(urls)
        print(cli_args)
        bot = Bot(cli_args)
        status = bot.run()
        print('status with proxy: {0} is {1} for url: {2}'.format(cli_args.proxy, status, cli_args.url))
        if not status:
            break

def _main():
    """ main """

    proxy_idx = 0
    try:
        cli_args = utils.get_cli_args()

        urls = []
        url_file = open(cli_args.file,'r')
        for url in url_file.readlines():
            # print(url)
            urls.append(url)
        url_file.close()

        if cli_args.no_proxy:
            call_bot(urls, cli_args)
            return
        proxies = utils.get_broker_proxies()
        print('proxies:', proxies)


        while proxy_idx < len(proxies):
            print()
            print('[{0}] {1}'.format(proxy_idx, '*' * 20))
            cli_args.proxy = proxies[proxy_idx]
            call_bot(urls, cli_args)
            print('*' * 20)
            print()
            proxy_idx += 1
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    sys.exit(_main())

# vim: set et ts=4 sw=4 sts=4 tw=80
