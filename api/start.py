from fastapi import APIRouter
import json
import pygame  # Thư viện phát âm thanh
from typing import List

router = APIRouter()

# Khởi tạo pygame mixer
pygame.mixer.init()

# Đọc kịch bản từ file JSON
def load_script_data() -> dict:
    try:
        with open('data/scripts/action_script.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None  # Trả về None nếu file không tìm thấy

# Lọc kịch bản theo tên
def validate_script(script_name: str, all_scripts: dict) -> dict:
    selected_script = next((script for script in all_scripts['scripts'] if script['script_name'] == script_name), None)
    return selected_script

# Phát âm thanh theo tên file
def play_audio(file_name: str):
    try:
        pygame.mixer.music.load(f"data/assets/audio/{file_name}")  # Đường dẫn tới thư mục chứa âm thanh
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Đợi âm thanh phát xong
            pass
    except Exception as e:
        print(f"Error playing audio {file_name}: {e}")

# API để bắt đầu hành động
@router.get("/start")
async def start_action(script: str, person: str, repeat: int):
    all_scripts = load_script_data()
    
    if not all_scripts:
        return {"message": "Không thể đọc file action_script.json."}
    
    selected_script = validate_script(script, all_scripts)

    if not selected_script:
        return {"message": f"Kịch bản '{script}' không tồn tại."}
    
    # Thực hiện các hành động theo kịch bản
    for _ in range(repeat):
        for action in selected_script['actions']:
            if action['person_id'] == person:  # Kiểm tra xem người thực hiện có đúng không
                print(f"Đang thực hiện hành động: {action['action_name']}")
                play_audio(action['voice_file'])  # Phát âm thanh
                print(f"Đã phát âm thanh: {action['voice_file']} với thời gian: {action['duration_sec']} giây")
    
    return {"message": f"Kịch bản '{script}' đã được bắt đầu cho {person} với {repeat} lần lặp lại."}