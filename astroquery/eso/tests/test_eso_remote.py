# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os
from astropy.tests.helper import pytest, remote_data
from ...eso import Eso

CACHE_PATH = os.path.join(os.path.dirname(__file__), 'data')

try:
    import keyring
    HAS_KEYRING = True
except ImportError:
    HAS_KEYRING = False


@pytest.mark.skipif('not HAS_KEYRING')
@remote_data
class TestEso:
    def test_SgrAstar(self):
        eso = Eso()
        eso.cache_location = CACHE_PATH

        instruments = eso.list_instruments()
        result_i = eso.query_instrument('midi', target='Sgr A*')

        surveys = eso.list_surveys()
        result_s = eso.query_survey('VVV', target='Sgr A*')

        assert 'midi' in instruments
        assert result_i is not None
        assert 'VVV' in surveys
        assert result_s is not None

    def test_nologin():
        # WARNING: this test will fail if you haven't cleared your cache and
        # you have downloaded this file!
        eso = Eso()

        with pytest.raises(ValueError) as exc:
            eso.data_retrieval('AMBER.2006-03-14T07:40:19.830')

        assert exc.value.args[0] == "Not logged in.  You must be logged in to download data."

    def test_empty_return(self):
        # test for empty return with an object from the North
        eso = Eso()
        surveys = eso.list_surveys()
        result_s = eso.query_survey(surveys[0], target='M51')

        assert result_s is None
