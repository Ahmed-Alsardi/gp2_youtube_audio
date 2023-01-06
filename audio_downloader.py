from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from pytube import YouTube
import pandas as pd

AUDIO_META_CSV = Path("audio_meta.csv")


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


def insert_audio_meta_to_csv(audio_meta: AudioMeta, audio_df: pd.DataFrame) -> None:
    """This function inserts the metadata of the audio to a csv file.

    Args:
        audio_meta (AudioMeta): metadata of the audio
        csv_path (Path): path to the csv file
    """
    audio_df = audio_df.append(
        {
            "title": audio_meta.title,
            "video_id": audio_meta.video_id,
            "channel_id": audio_meta.channel_id,
        },
        ignore_index=True,
    )
    audio_df.to_csv(AUDIO_META_CSV, index=False)


def check_if_audio_exists(video_url: str, audio_df: pd.DataFrame) -> Optional[YouTube]:
    """This function checks if the audio exists in the csv file.

    Args:
        video_url (str): youtube video url
        audio_df (pd.DataFrame): dataframe of the audio metadata

    Returns:
        bool: youtube object if the audio not exists, otherwise None
    """
    yt = YouTube(video_url)
    if yt.video_id in audio_df["video_id"].values:
        return None
    return yt


def get_audio_dataframe(csv_path: Path) -> pd.DataFrame:
    """This function returns a dataframe of the audio metadata.

    Args:
        csv_path (Path): path to the csv file

    Returns:
        pd.DataFrame: dataframe of the audio metadata
    """
    if not csv_path.exists():
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("title,video_id,channel_id")
    df = pd.read_csv(csv_path, names=["title", "video_id", "channel_id"])
    return df


if __name__ == "__main__":
    pass
