import pytest
import sys
from unittest.mock import MagicMock

from lee2024.registry import registry

@pytest.fixture(autouse=True)
def clear_registry():
    """Resets the registry and clears sub-modules from sys.modules cache."""
    registry.objects.clear()
    registry._is_initialized = False
    
    to_forget = [m for m in sys.modules if m.startswith("lee2024.data") or 
                 m.startswith("lee2024.io") or m.startswith("lee2024.processing")]
    for mod in to_forget:
        del sys.modules[mod]
        
    yield