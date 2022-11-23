from pathlib import Path
import sys

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.server import Wordle

def test_all_fail():
    myword = Wordle('world')
    assert myword.evaluate('theft') == 'xxxxx'

def test_green():
    myword = Wordle('media')
    assert myword.evaluate('mount') == 'Gxxxx'


def test_yellow():
    myword = Wordle('chief')
    assert myword.evaluate('lucky') == 'xxYxx'

def test_double_letters():
    myword = Wordle('cooks')
    assert myword.evaluate('coocs') == 'GGGxG'