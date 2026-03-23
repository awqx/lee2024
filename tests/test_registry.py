import pytest
import lee2024
from lee2024.registry import registry

def test_registry_is_initially_empty():
    """Ensure the conftest fixture is working and we start clean."""
    assert len(registry.objects) == 0

def test_discovery_fills_registry():
    """Verify that calling discover actually finds the methods."""
    # Trigger discovery manually
    tools = registry.discover("lee2024", ['data', 'io', 'processing'])
    
    assert len(tools) > 0
    assert any(callable(obj) for obj in tools.values())

def test_lazy_attribute_access():
    """Verify that accessing 'lee2024.tool' triggers the registry."""
    # 'load_recordings' is decorated with @registry.register
    # trigger __getattr__ in lee2024/__init__.py
    tool = getattr(lee2024, "RecordingSession", None)
    
    assert tool is not None
    assert registry._is_initialized is True
    assert "RecordingSession" in registry.objects

def test_import_from_lee2024():
    """Verify that 'from lee2024 import ...' works with our new setup."""
    # This is the 'acid test' for the __getattr__ logic
    try:
        from lee2024 import load_matlab_file
        assert callable(load_matlab_file)
    except ImportError:
        pytest.fail("Failed to import registered tool directly from package")