#!/usr/bin/env python3

import argparse
import os
import re
import uuid

import requests


def extract_url(html, quality):
    if quality == "HD":
        try:
            file_url = re.findall('hd_src:"(.+?")', html)[0]
        except IndexError:
            print("Could not find HD source. Downloading SD...")
            file_url = re.findall('sd_src:"(.+?)"', html)[0]
    else:
        file_url = re.findall('sd_src:"(.+?")', html)[0]
    return file_url


def get_file_name(html):
    try:
        title = re.findall('title" content=(.+?)"', html)
    except IndexError:
        title = uuid.uuid4().hex
    return title + ".mp4"


def download_video(url, dir_path, quality="HD"):
    request = requests.get(url)
    file_url = extract_url(request.text, quality)
    request = requests.get(file_url)
    file_path = os.path.join(dir_path, get_file_name(request.text))
    with open(file_path, "wb") as file_:
        file_.write(request.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download videos from facebook from your terminal")
    parser.add_argument("url", type=str, help="URL of the video to be downloaded.")
    parser.add_argument(
        "-p",
        "--path",
        default=os.getcwd(),
        help="Directory where the video will be downloaded. Default is the current directory.",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default="HD",
        help="Quality of the download. HD or SD. If HD is not found, SD will be downloaded. "
        "Default is HD.",
    )
    args = parser.parse_args()

    download_video(args.url, args.path, args.quality)
