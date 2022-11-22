
def pytest_addoption(parser):
    parser.addini("base_url", default=None, help="Base url")
    parser.addoption("--home_url_preset", action="store", type=str, default=None, help="Preset base url")
    parser.addoption("--country", action="store", type=str, default=None, help="Select Country")
    parser.addoption("--city", action="store", default=None, help="Select city")
