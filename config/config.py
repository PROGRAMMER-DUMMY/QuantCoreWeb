
import os
from dataclasses import dataclass

# 1. PATHS
@dataclass
class PathConfig:
    # Dynamically find the root (assuming config.py is in /config/)
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Match the folder structure of your private repo
    data_dir: str = os.path.join(base_dir, 'data', 'crypto')
    logs_dir: str = os.path.join(base_dir, 'logs')
    models_dir: str = os.path.join(base_dir, 'models')

# 2. EXECUTION SETTINGS
@dataclass
class ExecutionConfig:
    mode: str = "PUBLIC_VIEWER"  # Hardcoded for public safety
    leverage: int = 1

    # Empty credentials
    api_key_real: str = ""
    secret_real: str = ""
    api_key_paper: str = ""
    secret_paper: str = ""

# 3. CRYPTO SETTINGS (Placeholder)
@dataclass
class CryptoConfig:
    exchange_id: str = "binance"
    market_type: str = "future"

# --- GLOBAL INSTANCES ---
# This is what your app imports: "from config.config import PATHS, EXECUTION, CRYPTO"
PATHS = PathConfig()
EXECUTION = ExecutionConfig()
CRYPTO = CryptoConfig()
