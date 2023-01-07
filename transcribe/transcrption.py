from pathlib import Path
import logging
import whisper
import time

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


ROOT_PATH = Path("../data/version_0")
AUIDO_PATH = ROOT_PATH / "audios"
SUBTITLE_PATH = ROOT_PATH / "subtitles"


def initialize_subtitle(subtitle_path: Path) -> None:
    if not subtitle_path.exists():
        logger.info("Subtitle path not exists. Creating a new one.")
        subtitle_path.mkdir()


def check_root_path(root_path: Path) -> None:
    if not root_path.exists():
        raise FileNotFoundError(
            "ROOT_PATH not exists. either the path are wrong, or there are no file yet."
        )


def get_audios_path(audio_path: Path) -> list[Path]:
    audio_list = [path for path in audio_path.glob("*")]
    if len(audio_list) == 0:
        raise FileNotFoundError("There are no audio file in the path.")
    return audio_list


def get_audio_id(audio_path: Path) -> str:
    return audio_path.stem


def check_if_subtitle_exist(subtitle_path: Path, audio_id: str) -> bool:
    subtitle_path = subtitle_path / f"{audio_id}.vtt"
    if subtitle_path.exists():
        return True
    return False


def load_model() -> whisper.Whisper:
    return whisper.load_model("large-v2")


def transcribe(model: whisper.Whisper, audio_path: Path, subtitle_path: Path) -> None:
    audio_id = get_audio_id(audio_path)
    if check_if_subtitle_exist(subtitle_path, audio_id):
        logger.info("%s already exists. skip transcribing.", audio_id)
        return
    logger.info("Transcribing %s", audio_id)
    subtitle = whisper.transcribe(model, str(audio_path))
    logger.info("Finished transcribing %s, saving vtt file", audio_id)
    subtitle_path = subtitle_path / f"{audio_id}.vtt"
    with open(subtitle_path, "w", encoding="utf-8") as f:
        whisper.utils.write_vtt(subtitle["segments"], f)
    logger.info("Finished saving vtt file")


if __name__ == "__main__":
    start_time = time.time()
    logger.info("========== Start transcribing ==========")
    check_root_path(ROOT_PATH)
    initialize_subtitle(SUBTITLE_PATH)
    audios_path = get_audios_path(AUIDO_PATH)
    logger.info("Loading model")
    model = load_model()
    for audio_path in audios_path:
        transcribe(model, audio_path, SUBTITLE_PATH)
    end_time = time.time()
    logger.info(
        "========== Finished transcribing at %s ==========",
        round(end_time - start_time, 3),
    )
