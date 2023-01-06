# Audio Downloader

Script that take a list of youtube url form file *youtube_urls.txt* and download the audio to `current_path/audios/`.

The information that we got from the vidoe:
1. title
2. video_id
3. channel_id

for `duration` attribute will be given when we transcribe the audio.

All audio information will be save in `current_path/audios_info.csv`.

The script should not download any audio that already exist in `current_path/audios/`. This can be done by checking the `video_id` after initiate `yt` object then compare it with `audios_info.csv`.