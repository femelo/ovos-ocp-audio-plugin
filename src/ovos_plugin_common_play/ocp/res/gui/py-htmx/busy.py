from typing import Optional, Dict
from pyhtmx import Div, HTMLTag
from pyhtmx_gui.kit import Widget, SessionItem, Page


CACHE_DIR = "/cache/ovos.common_play/py-htmx"


class LoadingWidget(Widget):
    _parameters = ("title",)

    def __init__(self, session_data: Optional[Dict] = None):
        super().__init__(name="loading-widget", session_data=session_data)

        self._title = Div(
            inner_content=session_data.get("title", "Searching Media"),
            _id="loading-title",
            _class=[
                "text-[4vw]",
                "font-sans",
                "text-center",
                "text-white",
                "mb-4",
            ],
        )
        self.add_interaction(
            "title",
            SessionItem(
                parameter="ld-title",
                attribute="inner_content",
                component=self._title,
            ),
        )

        self._animation: HTMLTag = HTMLTag(
            "lottie-player",
            _id="loading-animation",
            _class="w-[60%] h-auto object-contain",
            autoplay="",
            loop="",
            src=f"{CACHE_DIR}/animations/installing.json",
            style={
                "width": "30vw",
                "height": "30vw",
            },
        )

        self._widget = Div(
            [
                self._title,
                self._animation,
            ],
            _id="loading-container",
            _class=[
                "flex",
                "flex-col",
                "items-center",
                "justify-center",
                "h-full",
                "w-full",
                "p-8",
                "bg-transparent",
            ],
        )


class LoadingPage(Page):
    def __init__(self, session_data: Optional[Dict] = None):
        super().__init__(name="loading-page", session_data=session_data)

        loading_widget = LoadingWidget(session_data=session_data)
        self.add_component(loading_widget)

        # Directly set the page content to the widget
        self._page = Div(
            Div(
                [loading_widget.widget],
                _id="loading-background",
                _class="bg-neutral-900",
                style={
                    "width": "80vw",
                    "height": "80vh",
                    "border-radius": "1rem",
                    "margin": "100px auto",
                    "box-shadow": "0 0 15px rgba(0,0,0,0.1)",
                },
            ),
            _id="loading-page",
            _class="fade-in bg-neutral-700",
            style={
                "width": "100vw",
                "height": "100vh",
            },
        )
