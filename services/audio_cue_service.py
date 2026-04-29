
# import json
# import time
# from pathlib import Path
# import pygame

# from app.core.config import AUDIO_DIR, SCRIPT_DIR
# from app.core.time_utils import utc_now_iso, perf_now

# class AudioCueService:
#     def __init__(self, session_dir: Path):
#         pygame.mixer.init()
#         self.session_dir = session_dir
#         self.log_file = session_dir / "logs" / "audio_events.csv"

#         if not self.log_file.exists():
#             self.log_file.write_text(
#                 "event_time_utc,planned_sec,actual_sec,event_type,action_name,voice_file\n",
#                 encoding="utf-8"
#             )

#     def _append_log(self, planned_sec, actual_sec, event_type, action_name, voice_file):
#         with open(self.log_file, "a", encoding="utf-8") as f:
#             f.write(
#                 f"{utc_now_iso()},{planned_sec:.3f},{actual_sec:.3f},{event_type},{action_name},{voice_file}\n"
#             )

#     def play_voice(self, voice_file: str):
#         path = AUDIO_DIR / voice_file
#         pygame.mixer.music.load(str(path))
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy():
#             time.sleep(0.05)

#     def beep(self):
#         beep_path = AUDIO_DIR / "beep.wav"
#         sound = pygame.mixer.Sound(str(beep_path))
#         sound.play()
#         time.sleep(0.25)

#     def run_script(self, script_name="action_script.json"):
#         script_path = SCRIPT_DIR / script_name
#         items = json.loads(script_path.read_text(encoding="utf-8"))

#         t0 = perf_now()
#         for item in items:
#             action_name = item["action_name"]
#             voice_file = item["voice_file"]

#             planned_sec = perf_now() - t0
#             self.play_voice(voice_file)
#             self.beep()

#             action_start = perf_now() - t0
#             self._append_log(planned_sec, action_start, "action_start", action_name, voice_file)

#             time.sleep(item["duration_sec"])

#             action_end = perf_now() - t0
#             self._append_log(planned_sec, action_end, "action_end", action_name, voice_file)

import csv
import time
from pathlib import Path

import pygame

from app.core.config import AUDIO_DIR
from app.core.time_utils import utc_now_iso, perf_now


class AudioCueService:
    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.action_file = session_dir / "action_events.csv"
        pygame.mixer.init()

        if not self.action_file.exists():
            with open(self.action_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "action_index",
                    "repeat_index",
                    "position_id",
                    "scenario",
                    "action_name",
                    "voice_file",
                    "start_sec",
                    "end_sec",
                    "start_time_utc",
                    "end_time_utc"
                ])

    # def run_action_plan(self, action_plan: list):
    #     session_t0 = perf_now()

    #     for item in action_plan:
    #         voice_file = item["voice_file"]
    #         action_name = item["action_name"]
    #         duration_sec = float(item["duration_sec"])

    #         self._play_voice(voice_file)
    #         self._beep()

    #         start_sec = perf_now() - session_t0
    #         start_time_utc = utc_now_iso()

    #         time.sleep(duration_sec)

    #         end_sec = perf_now() - session_t0
    #         end_time_utc = utc_now_iso()

    #         self._write_action_event(
    #             item=item,
    #             start_sec=start_sec,
    #             end_sec=end_sec,
    #             start_time_utc=start_time_utc,
    #             end_time_utc=end_time_utc
    #         )

    def run_action_plan(self, action_plan: list, session_t0: float | None = None):
        if session_t0 is None:
          session_t0 = perf_now()

        for item in action_plan:
            voice_file = item["voice_file"]
            duration_sec = float(item["duration_sec"])

            self._play_voice(voice_file)
            self._beep()

            start_sec = perf_now() - session_t0
            start_time_utc = utc_now_iso()

            time.sleep(duration_sec)

            end_sec = perf_now() - session_t0
            end_time_utc = utc_now_iso()

            self._write_action_event(
                item=item,
                start_sec=start_sec,
                end_sec=end_sec,
                start_time_utc=start_time_utc,
                end_time_utc=end_time_utc
            )

    def _play_voice(self, voice_file: str):
        path = AUDIO_DIR / voice_file

        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy file âm thanh: {path}")

        pygame.mixer.music.load(str(path))
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.05)

    def _beep(self):
        beep_path = AUDIO_DIR / "beep.wav"

        if not beep_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file beep: {beep_path}")

        sound = pygame.mixer.Sound(str(beep_path))
        sound.play()
        time.sleep(0.25)

    def _write_action_event(self, item, start_sec, end_sec, start_time_utc, end_time_utc):
        with open(self.action_file, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                item["action_index"],
                item["repeat_index"],
                item["position_id"],
                item["scenario"],
                item["action_name"],
                item["voice_file"],
                f"{start_sec:.6f}",
                f"{end_sec:.6f}",
                start_time_utc,
                end_time_utc
            ])