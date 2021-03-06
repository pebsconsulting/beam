#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""End-to-end test for Bigquery tornadoes example."""

import logging
import time
import unittest

from hamcrest.core.core.allof import all_of
from nose.plugins.attrib import attr

from apache_beam.examples.cookbook import bigquery_tornadoes
from apache_beam.io.gcp.tests.bigquery_matcher import BigqueryMatcher
from apache_beam.test_pipeline import TestPipeline
from apache_beam.tests.pipeline_verifiers import PipelineStateMatcher


class BigqueryTornadoesIT(unittest.TestCase):

  # Enable nose tests running in parallel
  _multiprocess_can_split_ = True

  # The default checksum is a SHA-1 hash generated from sorted rows reading
  # from expected Bigquery table.
  DEFAULT_CHECKSUM = '83789a7c1bca7959dcf23d3bc37e9204e594330f'

  @attr('IT')
  def test_bigquery_tornadoes_it(self):
    test_pipeline = TestPipeline(is_integration_test=True)

    # Set extra options to the pipeline for test purpose
    output_table = ('BigQueryTornadoesIT'
                    '.monthly_tornadoes_%s' % int(round(time.time() * 1000)))
    query = 'SELECT month, tornado_count FROM [%s]' % output_table
    pipeline_verifiers = [PipelineStateMatcher(),
                          BigqueryMatcher(
                              project=test_pipeline.get_option('project'),
                              query=query,
                              checksum=self.DEFAULT_CHECKSUM)]
    extra_opts = {'output': output_table,
                  'on_success_matcher': all_of(*pipeline_verifiers)}

    # Get pipeline options from command argument: --test-pipeline-options,
    # and start pipeline job by calling pipeline main function.
    bigquery_tornadoes.run(
        test_pipeline.get_full_options_as_args(**extra_opts))

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  unittest.main()
