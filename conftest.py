import sys
from unittest.mock import MagicMock

# Mock pyaudio for tests
class MockPyAudio:
    def __init__(self):
        self.stream = MagicMock()
        
    def open(self, *args, **kwargs):
        return self.stream
        
    def terminate(self):
        pass

sys.modules['pyaudio'] = MagicMock()
sys.modules['pyaudio'].PyAudio = MockPyAudio
sys.modules['pyaudio'].paFloat32 = 1
sys.modules['pyaudio'].paContinue = 0 