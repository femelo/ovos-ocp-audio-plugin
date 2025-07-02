from typing import Optional, Dict
from pyhtmx import Div
from pyhtmx_gui.kit import Page


class SuggestionPage(Page):
    def __init__(self, session_data: Optional[Dict] = None):
        super().__init__(name="SuggestionsView", session_data=session_data)

        # Content element
        content = Div(
            "Test: Suggestion Page werkt!",
            _class="text-white text-3xl p-4 bg-blue-800",
        )

        # Voeg content toe aan de GUI componentenlijst
        self.add_component(content)

        # Complete pagina-opmaak
        self._page = Div(
            content,
            _id="suggestion-page",
            _class="w-[80vw] h-[80vh] bg-black text-white flex items-center justify-center",
        )
