from __future__ import annotations
from typing import Any, Optional, Dict
from pyhtmx import Div, Button, Img
from pyhtmx_gui.kit import Page, Widget, SessionItem, Control

CACHE_DIR = "/cache/ovos.common_play/py-htmx"


class MediaPlayerWidget(Widget):
    _parameters = ("title", "artist", "image", "position", "duration", "status")

    def __init__(self, session_data: Optional[Dict[str, Any]] = None):
        # Maak een kopie zodat we data kunnen transformeren zonder originele dict te wijzigen
        session_data = dict(session_data or {})

        data = session_data.get("data", session_data)  # soms zit data direct in session_data

        # Zet duration en position om van ms naar seconden als string
        if "duration" in data:
            seconds_duration = data["duration"] / 1000
            data["duration"] = str(seconds_duration)
        if "position" in data:
            seconds_position = data["position"] / 1000
            data["position"] = str(seconds_position)

        # update session_data met de aangepaste data
        session_data.update(data)

        super().__init__(name="media-player-widget", session_data=session_data)

        title = session_data.get("title", "Geen Titel")
        artist = session_data.get("artist", "Onbekende Artiest")
        original_image = session_data.get("image", "")
        image = original_image        
        # Try high-res thumbnail if it's a YouTube-thumbnail
        if "img.youtube.com" in original_image:
            for quality in ["default", "hqdefault", "mqdefault", "sddefault"]:
                if f"/{quality}.jpg" in original_image:
                    image = original_image.replace(f"/{quality}.jpg", "/maxresdefault.jpg")
                    break
        position = float(session_data.get("position", "0"))
        duration = float(session_data.get("duration", "1"))  # default 1s om delen door nul te voorkomen

        # Afbeelding
        self._image = Img(
            src=image,
            _id="track-image",
            _class="w-[20vw] h-[20vw] object-cover rounded-2xl shadow-md mb-6",
        )
        self.add_interaction(
            "image",
            SessionItem(
                parameter="image",
                attribute="src",
                component=self._image,
                target_level="outerHTML",
            ),
        )

        # Titel
        self._title = Div(
            inner_content=title,
            _id="track-title",
            _class="text-[3vw] font-bold text-[currentColor] mb-2",
        )
        self.add_interaction(
            "title",
            SessionItem(
                parameter="tr-title",
                attribute="inner_content",
                component=self._title,
            ),
        )

        # Artiest
        self._artist = Div(
            inner_content=artist,
            _id="track-artist",
            _class="text-[2vw] text-[currentColor] opacity-70 mb-4",
        )
        self.add_interaction(
            "artist",
            SessionItem(
                parameter="artist",
                attribute="inner_content",
                component=self._artist,
            ),
        )

        # Progress bar fill (width = progress in %)
        progress_pct = (position / duration * 100) if duration > 0 else 0
        self._progress_fill = Div(
            _id="progress-fill",
            _class="h-full bg-white rounded-full",
            style={"width": f"{progress_pct:.2f}%"},
        )

        # Progress bar container
        self._progress_bar = Div(
            [self._progress_fill],
            _id="progress-bar",
            _class="w-full h-[1vw] bg-gray-500 rounded-full mb-1",
            style={"maxWidth": "80vw"},
        )

        # Tijd labels: huidige positie en totale lengte
        self._current_time_label = Div(
            inner_content=MediaPlayerWidget._format_time(position),
            _id="current-time-label",
            _class="text-[1.5vw] text-white opacity-70",
        )

        self._total_time_label = Div(
            inner_content=MediaPlayerWidget._format_time(duration),
            _id="total-time-label",
            _class="text-[1.5vw] text-white opacity-70",
        )

        # Tijd labels container, flex row met space-between
        self._time_labels = Div(
            [self._current_time_label, self._total_time_label],
            _class="flex flex-row justify-between w-[80vw] mb-4",
        )

        # Interacties om progressbar en tijdlabels te updaten, nu met string seconds in session_data
        self.add_interaction(
            "position",
            SessionItem(
                parameter="position-fill",
                attribute="style",
                component=self._progress_fill,
                format_value=lambda p: f"width:{(float(p) / max(duration, 1)) * 100:.2f}%" if p else "width:0%",
            ),
        )
        self.add_interaction(
            "position",
            SessionItem(
                parameter="position-label",
                attribute="inner_content",
                component=self._current_time_label,
                format_value=lambda p: MediaPlayerWidget._format_time(float(p)) if p else "00:00",
            ),
        )
        self.add_interaction(
            "duration",
            SessionItem(
                parameter="duration-label",
                attribute="inner_content",
                component=self._total_time_label,
                format_value=lambda l: MediaPlayerWidget._format_time(float(l)) if l else "00:00",
            ),
        )

        # Knoppen
        common_classes = (
            "w-[5vw] h-[5vw] flex items-center justify-center "
            "text-[2vw] rounded-full transition-all duration-200 "
            "focus:outline-none focus:ring-2 focus:ring-white "
            "hover:scale-110 border-2"
        )

        status = session_data.get("status", "")
        toggle_icon = "⏸️" if status == "Playing" else "▶️"

        btn_toggle = Button(
            toggle_icon,
            _id="btn-toggle",
            _class=f"{common_classes} border border-gray-300 text-white hover:bg-white hover:text-black"
        )

        btn_next = Button(
            "⏭️",
            _id="btn-next",
            _class=f"{common_classes} border border-gray-300 text-white hover:bg-white hover:text-black"
        )

        btn_prev = Button(
            "⏮️",
            _id="btn-prev",
            _class=f"{common_classes} border border-gray-300 text-white hover:bg-white hover:text-black"
        )

        # Toggle-knop click
        self.add_interaction(
            "toggle-click",
            Control(
                context="global",
                event="click",
                source=btn_toggle,
                target=None,
                callback=lambda r, *args: print("toggle clicked"),
            ),
        )

        # Next / Prev click
        for btn, action in [
            (btn_next, "next"),
            (btn_prev, "prev")
        ]:
            self.add_interaction(
                f"{action}-click",
                Control(
                    context="global",
                    event="click",
                    source=btn,
                    target=None,
                    callback=lambda r, *args, a=action: print(f"{a} clicked"),
                ),
            )

        # Update toggle knop-icoon op basis van status
        self.add_interaction(
            "status",
            SessionItem(
                parameter="status",
                attribute="inner_content",
                component=btn_toggle,
                format_value=lambda s: "⏸️" if s == "Playing" else "▶️"
            ),
        )

        controls = Div(
            [btn_prev, btn_toggle, btn_next],
            _class="flex flex-row justify-center gap-[3vw] mt-6",
        )

        self._widget = Div(
            [
                self._image,
                self._title,
                self._artist,
                self._progress_bar,
                self._time_labels,
                controls,
            ],
            _id="media-player-widget",
            _class="flex flex-col items-center p-[2vw] bg-transparent text-white",
        )

    @staticmethod
    def _format_time(seconds: float) -> str:
        minutes = int(seconds // 60)
        sec = int(seconds % 60)
        return f"{minutes:02d}:{sec:02d}"


class PlayerLoader(Page):
    def __init__(self, session_data: Optional[Dict[str, Any]] = None):
        super().__init__(name="player-page", session_data=session_data)

        media_player_widget = MediaPlayerWidget(session_data=session_data)
        self.add_component(media_player_widget)

        # Add control to change to the next page
        self.add_interaction(
            "next-page-key-up",
            Control(
                context="global",
                event="keyup[event.code === 'ArrowRight'] from:body",
                callback=(
                    lambda renderer, _: renderer.show_next()
                ),
            ),
        )

        self._page = Div(
            [media_player_widget.widget],
            _id="media-player-page",
            _class="flex flex-col items-center justify-center bg-gray-900 fade-in",
            style={
                "width": "100vw",
                "height": "100vh",
            },
        )
