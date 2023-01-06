from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from pytube import YouTube


@dataclass
class AudioMeta:
    title: str
    video_id: str
    channel_id: str


def download_video(yt: YouTube, download_path: Path) -> AudioMeta:
    """This function downloads a video from youtube and returns the metadata of the video.

    Args:
        yt (YouTube): YouTube object
        download_path (Path): path to download the video

    Returns:
        AudioMeta: metadata of the video
    """
    filename = f"{yt.video_id}.mp4"
    yt.streams.filter(only_audio=True).first().download(
        download_path, filename=filename
    )
    audio_meta = AudioMeta(
        title=yt.title, video_id=yt.video_id, channel_id=yt.channel_id
    )
    return audio_meta


def insert_audio_meta_to_csv(audio_meta: AudioMeta, csv_path: Path) -> None:
    """This function inserts the metadata of the audio to a csv file.

    Args:
        audio_meta (AudioMeta): metadata of the audio
        csv_path (Path): path to the csv file
    """
    with open(csv_path, "a", encoding="utf-8") as f:
        f.write(f"{audio_meta.title},{audio_meta.video_id},{audio_meta.channel_id}\n")


def check_if_audio_exists(video_url: str, csv_path: Path) -> Optional[YouTube]:
    """This function checks if the audio exists in the csv file.

    Args:
        video_url (str): youtube video url
        csv_path (Path): path to the csv file

    Returns:
        bool: youtube object if the audio not exists, otherwise None
    """
    yt = YouTube(video_url)
    video_id = yt.video_id
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            if video_id in line:
                return None
    return yt


if __name__ == "__main__":
    pass
