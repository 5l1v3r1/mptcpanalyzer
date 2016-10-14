from unittest import TestCase

from mptcpanalyzer.config import MpTcpAnalyzerConfig
import tempfile
import shutil
import os



config_file = "tests/test_config.ini"

class ConfigTest(TestCase):
# TODO check filename loaded correctly

    def test_xdg_config_home(self):
        """
        Override XDG_CONFIG_HOME and checks it's correctly loaded
        """
        #TODO use tempdir
        with tempfile.TemporaryDirectory() as dirname:
            # os.copy
            # TODO check it can work even if XDG_CONFIG_HOME is empty
            cfg = MpTcpAnalyzerConfig()
            shutil.copyfile(
                config_file,
                os.path.join(dirname, os.path.basename(config_file))
            )

            cfg = MpTcpAnalyzerConfig()

    def test_values_are_loaded(self):
        """
        Reads a config file and make sure some default values are ok
        """

        # config = MpTcpAnalyzerConfig()
        cfg = MpTcpAnalyzerConfig(config_file)
        # self.assert
        cfg = cfg["mptcpanalyzer"]
        self.assertEqual(cfg["tshark_binary"], "fake_tshark")
        self.assertEqual(cfg["delimiter"], "|")
