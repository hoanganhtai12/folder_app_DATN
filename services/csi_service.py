from pathlib import Path
from app.core.time_utils import utc_now_iso

class CsiService:
    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.csi_file = session_dir / "csi" / "receiver_eth.csv"

        if not self.csi_file.exists():
            self.csi_file.write_text("timestamp_utc,source,payload\n", encoding="utf-8")

    def write_packet(self, source: str, payload: bytes):
        safe_payload = payload.hex()
        with open(self.csi_file, "a", encoding="utf-8") as f:
            f.write(f"{utc_now_iso()},{source},{safe_payload}\n")