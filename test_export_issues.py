#!/usr/bin/python

import unittest
from mock import patch
import export_issues
import requests
import redmine

class TestIssueImporter(unittest.TestCase):

    def setup(self):
        pass

    def test_get_config_value(self):
        pid = export_issues.get_config_value('REDMINE', 'id')
        self.assertIsNotNone(pid)

    def test_get_config_value_wrong_option(self):
        pid = export_issues.get_config_value('REDMINE', 'abc')
        self.assertIsNone(pid)

    def test_get_config_value_wrong_section(self):
        pid = export_issues.get_config_value('xyz', 'id')
        self.assertIsNone(pid)

    @patch.object(redmine.managers.ResourceManager, 'create')
    @patch.object(requests, 'get')
    @patch.object(requests.Response, 'json')
    def test_main(self, mock_json, mock_get, mock_create):
        assert requests.get is mock_get
        assert requests.Response.json is mock_json
        assert redmine.managers.ResourceManager.create is mock_create
        r = requests.Response()
        r.status_code = 200
        content = [{'state':'open', 'title':'my title', 'body':'test body'}]
        mock_get.return_value=r
        mock_json.return_value=content
        mock_create.return_value = None
        try:
            export_issues.main()
        except:
            self.fail("Exception thrown")
        

if __name__ == '__main__':
    unittest.main()
