from ovos_plugin_common_play.ocp.base import OCPAudioPlayerBackend
from ovos_bus_client import MessageBusClient


class OVOSTestAudioService(OCPAudioPlayerBackend):
    def __init__(
        self,
        config: dict,
        bus: MessageBusClient | None = None,
        name: str = 'ovos_test',
    ):
        super(OVOSTestAudioService, self).__init__(config, bus)
        self.name = name

    def supported_uris(self) -> list[str]:
        uris = ['file', 'http']
        return uris

    def play(self, repeat: bool = False) -> None:
        """ Play playlist using simple. """
        self.ocp_start()

    def stop(self) -> bool:
        """ Stop simple playback. """
        if self._now_playing:
            self.ocp_stop()
            return True
        return False

    def pause(self) -> None:
        """ Pause simple playback. """
        if self._now_playing:
            self.ocp_pause()

    def resume(self) -> None:
        """ Resume paused playback. """
        if self._now_playing:
            self.ocp_resume()

    def get_track_length(self) -> int:
        return 0
    
    def get_track_position(self) -> int:
        return 0
    
    def set_track_position(self, milliseconds: int) -> None:
        pass


def load_service(base_config, bus) -> list:
    backends = base_config.get('backends', [])
    services = [(b, backends[b]) for b in backends
                if backends[b]['type'] == 'ovos_test' and
                backends[b].get('active', False)]

    instances = [OVOSTestAudioService(s[1], bus, s[0]) for s in services]
    return instances
