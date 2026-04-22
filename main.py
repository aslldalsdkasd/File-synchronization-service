from pathlib import Path
from class_sync import Synchronization

if __name__ == "__main__":
    Path("logs").mkdir(exist_ok=True)
    sync = Synchronization()
    sync.load('test_text.txt')
    sync.reload('test_text.txt')
    sync.get_info()
    sync.delete('test_text.txt')
    sync.get_info()