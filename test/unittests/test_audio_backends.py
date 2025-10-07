import json
import unittest
from unittest.mock import patch
from typing import Any

from ovos_audio.service import AudioService
from ovos_config.config import Configuration
from ovos_utils.messagebus import FakeBus

BASE_CONF = {"Audio":
    {
        "native_sources": ["debug_cli", "audio"],
        "default-backend": "OCP",  # only used by mycroft-core
        "preferred_audio_services": ["ovos_test", "mycroft_test"],
        "backends": {
            "OCP": {
                "type": "ovos_common_play",
                "active": True,
                "mode": "auto",
                "disable_mpris": True
            },
            "mycroft_test": {
                "type": "mycroft_test",
                "active": True
            },
            "ovos_test": {
                "type": "ovos_test",
                "active": True
            }
        }
    }
}


class WrappedFakeBus(FakeBus):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.emitted_msgs: list = []


class TestOCPLoad(unittest.TestCase):

    @classmethod
    @patch.object(Configuration, 'load_all_configs')
    def setUpClass(cls, mock_get) -> None:
        mock_get.return_value = BASE_CONF
        cls.bus = WrappedFakeBus()
        cls.bus.emitted_msgs = []

        def get_msg(msg):
            msg = json.loads(msg)
            msg.pop("context")
            cls.bus.emitted_msgs.append(msg)

        cls.bus.on("message", get_msg)

        cls.audio = AudioService(cls.bus)

    def tearDown(self) -> None:
        self.audio.shutdown()


if __name__ == '__main__':
    unittest.main()
