from typing import Callable, Dict


class Router:
    """
    A simple router that maps paths to handlers. The router is used by the RequestHandler
    to find the appropriate handler for a given path.
    """

    def __init__(self):
        self.routes: Dict[str, Callable] = {}

    def add_route(self, path: str, handler: Callable) -> None:
        self.routes[path] = handler

    def get_handler(self, path: str) -> Callable:
        return self.routes.get(path, None)
