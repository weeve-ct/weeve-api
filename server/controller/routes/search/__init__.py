from server.controller.security import SecureBlueprint

bp = SecureBlueprint('search', __name__)

# put below blueprint to stop circular import failure
from . import post
