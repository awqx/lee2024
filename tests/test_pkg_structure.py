import pytest
import lee2024
from lee2024.registry import registry

def test_namespace_population():
    """
    Verify that the top-level 'lee2024' namespace contains the registered 
    classes and functions without needing deep imports.
    """
    # Check for Data Classes
    assert hasattr(lee2024, "RecordingSession"), "RecordingSession failed to register at top level"
    assert hasattr(lee2024, "load_matlab_file"), "load_matlab_file failed to register at top level"

def test_registry_contents():
    """
    Verify the ObjectRegistry instance actually collected the objects.
    """
    lee2024.get_tools()
    assert "RecordingSession" in registry.objects
    assert "load_matlab_file" in registry.objects

def test_module_locations():
    """
    Verify that the registered objects still know where they came from
    (Ensures the importlib logic didn't break their metadata).
    """
    from lee2024.data.recording import RecordingSession
    # The version at the top level should be the EXACT same object as the one in the sub-module
    assert lee2024.RecordingSession is RecordingSession