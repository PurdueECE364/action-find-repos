from pytest import raises
import os
from main import main
from unittest import mock


@mock.patch.dict(os.environ, {
    "INPUT_ORG": "firebase",
    "INPUT_PATTERN": '^quickstart.*$'
})
def test_firebase():
    main()
    assert os.environ['OUTPUT_REPOS'] == '["firebase/quickstart-android", "firebase/quickstart-ios", "firebase/quickstart-js", "firebase/quickstart-cpp", "firebase/quickstart-nodejs", "firebase/quickstart-java", "firebase/quickstart-unity", "firebase/quickstart-python", "firebase/quickstart-testing", "firebase/quickstart-flutter"]'


@mock.patch.dict(os.environ, {
    "INPUT_ORG": "firebase",
    "INPUT_PATTERN": '^quickstart.*$',
    "INPUT_CREATED_AFTER": "2017-01-01T23:59:59-04:00",
})
def test_firebase_createdafter():
    main()
    assert os.environ['OUTPUT_REPOS'] == '["firebase/quickstart-python", "firebase/quickstart-testing", "firebase/quickstart-flutter"]'


@mock.patch.dict(os.environ, {
    "INPUT_ORG": "firebase",
    "INPUT_PATTERN": '^quickstart.*$',
    "INPUT_CREATED_BEFORE": "2017-01-01T23:59:59-04:00"
})
def test_firebase_createdbefore():
    main()
    assert os.environ['OUTPUT_REPOS'] == '["firebase/quickstart-android", "firebase/quickstart-ios", "firebase/quickstart-js", "firebase/quickstart-cpp", "firebase/quickstart-nodejs", "firebase/quickstart-java", "firebase/quickstart-unity"]'


@mock.patch.dict(os.environ, {
    "INPUT_ORG": "firebase",
    "INPUT_PATTERN": '^quickstart.*$',
    "INPUT_CREATED_AFTER": "2022-03-06T23:59:59-04:00",
    "INPUT_CREATED_BEFORE": "2022-03-07T23:59:59-04:00"
})
def test_firebase_timewindowed():
    main()
    assert os.environ['OUTPUT_REPOS'] == '["firebase/quickstart-flutter"]'


@mock.patch.dict(os.environ, {
    "INPUT_ORG": "firebase",
    "INPUT_PATTERN": '^quickstart.*$',
    "INPUT_CREATED_AFTER": "2022-03-07T23:59:59-04:00",
    "INPUT_CREATED_BEFORE": "2022-03-06T23:59:59-04:00"
})
def test_firebase_timewindowed_invalid():
    with raises(SystemExit) as e:
        main()


@mock.patch.dict(os.environ, {
    "INPUT_ORG": "firebase",
    "INPUT_PATTERN": '^quickstart.*$',
    "INPUT_CREATED_BEFORE": "2015-04-01T23:59:59-04:00"
})
def test_firebase_timewindowed_nonefound():
    with raises(SystemExit) as e:
        main()
