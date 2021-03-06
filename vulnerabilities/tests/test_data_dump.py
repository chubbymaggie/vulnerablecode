#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/vulnerablecode/
# The VulnerableCode software is licensed under the Apache License version 2.0.
# Data generated with VulnerableCode require an acknowledgment.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with VulnerableCode or any VulnerableCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with VulnerableCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  VulnerableCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  VulnerableCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/vulnerablecode/ for support and download.

import json
import os

from django.test import TestCase

from vulnerabilities.models import Vulnerability
from vulnerabilities.models import VulnerabilityReference
from vulnerabilities.models import Package
from vulnerabilities.data_dump import debian_dump
from vulnerabilities.data_dump import ubuntu_dump
from vulnerabilities.scraper import debian
from vulnerabilities.scraper import ubuntu


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA = os.path.join(BASE_DIR, 'test_data/')


class TestDataDump(TestCase):
    def test_debian_data_dump(self):
        """
        Scrape data from Debian' main tracker, save it
        in the database and verify entries.
        """
        with open(os.path.join(TEST_DATA, 'debian.json')) as f:
            test_data = json.loads(f.read())

        extract_data = debian.extract_vulnerabilities(test_data)
        debian_dump(extract_data)

        self.assertEqual(3, Vulnerability.objects.count())
        self.assertEqual(3, VulnerabilityReference.objects.count())
        self.assertEqual(3, Package.objects.count())

        self.assertTrue(Vulnerability.objects.get(
                        summary='Multiple stack-based buffer overflows in mimetex.cgi in mimeTeX'))

        self.assertTrue(Vulnerability.objects.get(
                        summary='Multiple unspecified vulnerabilities in mimeTeX.'))

        self.assertTrue(VulnerabilityReference.objects.get(reference_id='CVE-2009-2458'))

        self.assertTrue(VulnerabilityReference.objects.get(reference_id='CVE-2009-2459'))

        self.assertTrue(VulnerabilityReference.objects.get(reference_id='TEMP-0807341-84E914'))

        self.assertEqual(Package.objects.filter(name='mimetex')[0].name, 'mimetex')
        self.assertTrue(Package.objects.get(name='git-repair'))
        self.assertEqual(Package.objects.filter(version='1.50-1.1')[0].version, '1.50-1.1')

    def test_ubuntu_data_dump(self):
        """
        Scrape data from Ubuntu' main tracker, save it
        in the database and verify entries.
        """
        with open(os.path.join(TEST_DATA, 'ubuntu_main.html')) as f:
            test_data = f.read()

        data = ubuntu.extract_cves(test_data)
        ubuntu_dump(data)

        reference = VulnerabilityReference.objects.filter(reference_id='CVE-2002-2439')[0]
        self.assertEqual(reference.reference_id, 'CVE-2002-2439')
        self.assertTrue(Package.objects.filter(name='gcc-4.6')[0].name, 'gcc-4.6')
