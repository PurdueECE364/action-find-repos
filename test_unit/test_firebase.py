import os
from main import main
from unittest import mock

@mock.patch.dict(os.environ, {
    "INPUT_ORG": "firebase",
    "INPUT_PATTERN": '^quickstart.*$'
    })
def test_firebase():
    main()