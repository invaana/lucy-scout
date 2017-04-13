from scout.scider import helpers
import time, os, pytest

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './github.json')


def test_read_json_file():
    config_data = helpers.read_json_file(file_path)
    assert config_data is not None
    assert type(config_data) is dict
    with pytest.raises(ValueError) as excinfo:
        helpers.read_json_file('../something.json')
    assert "Halting the program! Invalid file path provided" in str(excinfo.value)


def test_validate_config():
    config_data = helpers.read_json_file(file_path)
    # correct data
    assert helpers.validate_config(config_data) is None
    
    with pytest.raises(ValueError) as excinfo:
        helpers.validate_config(None)
    assert "Halting the program! No config data provided" in str(excinfo.value)
    
    with pytest.raises(ValueError) as excinfo:
        helpers.validate_config([])
    assert "Halting the program! Config file should be dictionary"  in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        helpers.validate_config({})
    assert "Halting the program! Invalid config format" in str(excinfo.value)


    
    
def test_getElapsedTime():
    assert helpers.getElapsedTime(time.time()) is not None
    
    
def test_scrape_error_message():
    assert helpers.ScrapeHTMLErrorMesg == "Unable to scrape the content"