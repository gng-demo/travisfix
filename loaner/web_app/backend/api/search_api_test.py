# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for backend.api.search_api."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized
import mock

from protorpc import message_types

from google.appengine.ext import deferred

from loaner.web_app.backend.api import search_api
from loaner.web_app.backend.api.messages import search_messages
from loaner.web_app.backend.models import device_model
from loaner.web_app.backend.models import shelf_model
from loaner.web_app.backend.testing import loanertest


class SearchApiTest(parameterized.TestCase, loanertest.EndpointsTestCase):

  def setUp(self):
    super(SearchApiTest, self).setUp()
    self.service = search_api.SearchApi()
    self.login_admin_endpoints_user()

  def tearDown(self):
    super(SearchApiTest, self).tearDown()
    self.service = None

  @parameterized.parameters(
      (device_model.Device.clear_index,
       search_messages.SearchIndexEnum.DEVICE),
      (shelf_model.Shelf.clear_index,
       search_messages.SearchIndexEnum.SHELF),
  )
  def test_clear_index(self, expected_call, test_enum):
    """Test clearing the index of the shelves and devices."""
    with mock.patch.object(deferred, 'defer') as mock_deferred:
      request = search_messages.SearchMessage(model=test_enum)
      response = self.service.clear(request)
      self.assertIsInstance(response, message_types.VoidMessage)
      mock_deferred.assert_called_once_with(expected_call)

  @parameterized.parameters(
      (device_model.Device.index_entities_for_search,
       search_messages.SearchIndexEnum.DEVICE),
      (shelf_model.Shelf.index_entities_for_search,
       search_messages.SearchIndexEnum.SHELF),
  )
  def test_reindex(self, expected_call, test_enum):
    """Test reindexing the shelves and devices."""
    with mock.patch.object(deferred, 'defer') as mock_deferred:
      request = search_messages.SearchMessage(model=test_enum)
      response = self.service.reindex(request)
      self.assertIsInstance(response, message_types.VoidMessage)
      mock_deferred.assert_called_once_with(expected_call)


if __name__ == '__main__':
  loanertest.main()
