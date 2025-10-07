from ovos_plugin_manager.templates.audio import AudioBackend
from ovos_bus_client import MessageBusClient


class TestMycroftAudioService(AudioBackend):
    def __init__(
        self,
        config: dict,
        bus: MessageBusClient,
        name: str = 'mycroft_test',
    ) -> None:
        super().__init__(config, bus)
        self.config = config
        self.bus = bus
        self.name = name
        self.index = 0
        self.tracks = []
        self.stopped = True
        self.paused = False
        self.playing = False
        self.ducked = False

    def supported_uris(self) -> list[str]:
        return ['file', 'http']

    def clear_list(self) -> None:
        self.tracks = []

    def add_list(self, tracks: list) -> None:
        self.tracks += tracks

    def play(self, repeat: bool = False) -> None:
        self.index = 0
        self.playing = True

    def stop(self) -> bool:
        self.stopped = True
        self.playing = False
        return self.stopped

    def pause(self) -> None:
        self.paused = True

    def resume(self):
        self.paused = False

    def next(self) -> None:
        # Terminate process to continue to next
        self.index += 1

    def previous(self) -> None:
        self.index -= 1

    def lower_volume(self) -> None:
        self.ducked = True

    def restore_volume(self) -> None:
        self.ducked = False

    def get_track_length(self) -> int:
        return 0
    
    def get_track_position(self) -> int:
        return 0

    def set_track_position(self, milliseconds: int) -> None:
        pass


def load_service(base_config: dict, bus: MessageBusClient) -> list:
    backends = base_config.get('backends', [])
    services = [(b, backends[b]) for b in backends
                if backends[b]['type'] == 'mycroft_test' and
                backends[b].get('active', False)]
    instances = [TestMycroftAudioService(s[1], bus, s[0]) for s in services]
    return instances
