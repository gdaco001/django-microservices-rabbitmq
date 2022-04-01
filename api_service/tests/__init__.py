import sys
import os

from pathlib import Path
from os.path import join, dirname, abspath
from dotenv import load_dotenv

sys.path.append('.')
BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = join(BASE_DIR, '.dev.env')
load_dotenv(dotenv_path)
os.environ['DB_HOST'] = 'localhost'

