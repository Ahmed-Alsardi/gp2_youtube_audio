from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import logging
from pytube import YouTube
from pytube.exceptions import PytubeError, VideoUnavailable


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_PATH = Path("version_0")

AUDIO_META_CSV = ROOT_PATH / "audio_meta.csv"
URLS_FILE = ROOT_PATH / "urls.txt"
AUDIO_PATH = ROOT_PATH / "audios"


@dataclass
class AudioMeta:
    """This class represents the metadata of the audio."""

    title: str
    video_id: str
    channel_id: str

    @property
    def get_csv_row(self):
        """This function returns the csv row of the metadata."""
        return f"{self.title},{self.video_id},{self.channel_id}\n"


def download_video(yt: YouTube, download_path: Path) -> AudioMeta:
    """This function downloads a video from youtube and returns the metadata of the video.

    Args:
        yt (YouTube): YouTube object
        download_path (Path): path to download the video

    Returns:
        AudioMeta: metadata of the video
    """
    filename = f"{yt.video_id}.mp4"
    try:
        yt.streams.filter(only_audio=True).first().download(
            download_path, filename=filename
        )
        audio_meta = AudioMeta(
            title=yt.title, video_id=yt.video_id, channel_id=yt.channel_id
        )
        logger.info("Downloaded `%s`", yt.title)
        return audio_meta
    except PytubeError:
        logger.error("Failed to download `%s`", yt.title)
        return None


def insert_audio_meta_to_csv(audio_meta: AudioMeta, csv_file: Path) -> None:
    """This function inserts the metadata of the audio to a csv file.

    Args:
        audio_meta (AudioMeta): metadata of the audio
        csv_path (Path): path to the csv file
    """
    with open(csv_file, "a", encoding="utf-8") as f:
        f.write(audio_meta.get_csv_row)
    logger.info("Inserted `%s` to csv file", audio_meta.title)


def check_if_audio_exists(video_url: str, csv_path: Path) -> Optional[YouTube]:
    """This function checks if the audio exists in the csv file.

    Args:
        video_url (str): youtube video url
        csv_path (Path): path to the csv file

    Returns:
        bool: youtube object if the audio not exists, otherwise None
    """
    try:
        yt = YouTube(video_url)
        youtube_id = yt.video_id
        # this will raise an error if the video is unavailable, video_id will not raise an error
        youtube_title = yt.title 
        with open(csv_path, "r", encoding="utf-8") as f:
            for line in f:
                if youtube_id in line:
                    logger.info("`%s` audio already exists", youtube_title)
                    return None
        return yt
    except VideoUnavailable:
        logger.error("Failed to retreieve yt object `%s`", video_url)
        return None


def initialize_csv(csv_path: Path) -> None:
    """This function initializes the csv file.

    Args:
        csv_path (Path): path to the csv file
    """
    if csv_path.exists():
        return
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("title,video_id,channel_id\n")


def read_urls_file(urls_file: Path) -> list:
    """This function reads a file and returns the urls.

    Args:
        urls_file (Path): path to the urls file

    Returns:
        list: list of urls
    """
    if not urls_file.exists():
        raise FileNotFoundError(f"{urls_file} does not exists")
    with open(urls_file, "r", encoding="utf-8") as f:
        urls = f.read().splitlines()
    return urls


def initialize_project_structures() -> None:
    """This function checks the path structures."""
    if not ROOT_PATH.exists():
        logger.info("Creating project structure")
        ROOT_PATH.mkdir()
    if not AUDIO_PATH.exists():
        logger.info("Creating audio path")
        AUDIO_PATH.mkdir()

if __name__ == "__main__":
    initialize_project_structures()
    youtube_urls = read_urls_file(URLS_FILE)
    initialize_csv(AUDIO_META_CSV)
    for url in youtube_urls:
        yt = check_if_audio_exists(url, AUDIO_META_CSV)
        if yt:
            audio_meta = download_video(yt, AUDIO_PATH)
            if audio_meta: # in case of download failure
                insert_audio_meta_to_csv(audio_meta, AUDIO_META_CSV)
    logger.info("======== Done")
