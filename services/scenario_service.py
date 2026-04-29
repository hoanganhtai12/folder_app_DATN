# service đọc kịch bản từ file JSON và xây dựng kế hoạch hành động

# Đọc scenario được chọn
# Nhân số lần lặp repeat_count
# Sinh danh sách hành động hoàn chỉnh

import json
from pathlib import Path

from app.core.config import ACTION_SCENARIOS_PATH


class ScenarioService:
    def __init__(self, scenario_file: Path = ACTION_SCENARIOS_PATH):
        self.scenario_file = scenario_file

    def load_all(self):
        if not self.scenario_file.exists():
            raise FileNotFoundError(f"Không tìm thấy file kịch bản: {self.scenario_file}")

        with open(self.scenario_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_scenario(self, scenario_name: str):
        scenarios = self.load_all()

        for item in scenarios:
            if item.get("scenario") == scenario_name:
                return item

        raise ValueError(f"Không tìm thấy scenario: {scenario_name}")

    def build_action_plan(self, scenario_name: str, repeat_count: int, position_id: int):
        scenario = self.get_scenario(scenario_name)
        actions = scenario["actions"]

        action_plan = []
        action_index = 0

        for repeat_index in range(1, repeat_count + 1):
            for action in actions:
                action_index += 1

                action_plan.append({
                    "action_index": action_index,
                    "repeat_index": repeat_index,
                    "position_id": position_id,
                    "scenario": scenario_name,
                    "order": action["order"],
                    "voice_file": action["voice_file"],
                    "action_name": action["action_name"],
                    "duration_sec": float(action["duration_sec"])
                })

        return action_plan