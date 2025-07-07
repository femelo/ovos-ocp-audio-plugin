from typing import Optional, Dict
from pyhtmx import Div
from pyhtmx_gui.kit import Page, Control


class SuggestionPage(Page):
    def __init__(self, session_data: Optional[Dict] = None):
        super().__init__(name="playlist-page", session_data=session_data)

        # Add control to change to the previous page
        self.add_interaction(
            "prev-page-key-up",
            Control(
                context="global",
                event="keyup[event.code === 'ArrowLeft'] from:body",
                callback=(
                    lambda renderer, _: renderer.show_previous()
                ),
            ),
        )

        # Content element
        content = Div(
            "Test: Suggestion Page werkt!",
            _class="text-white text-3xl p-4 bg-blue-800",
        )

        # Complete pagina-opmaak
        self._page = Div(
            content,
            _id="suggestion-page",
            _class="w-[100vw] h-[100vh] bg-black text-white flex items-center justify-center",
        )
