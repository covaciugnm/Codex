"""Independent regression checks; no network or Docker is contacted."""
import json
import pathlib
import unittest
from unittest import mock

import monitor_domains as monitor


def response(status=200, ip='203.0.113.7', location=None, error=None):
    return {'status': status, 'ip': ip, 'location': location, 'cloudflare': False, 'error': error}


class MonitorTests(unittest.TestCase):
    def test_dns_subdomain_uses_parent_ns(self):
        def query(domain, kind):
            values = ['203.0.113.7'] if kind == 'A' else ['ns.example.com'] if domain == 'example.com' and kind == 'NS' else []
            return {'status': 'NOERROR', 'values': values}
        with mock.patch.object(monitor, 'dns_query', side_effect=query):
            result = monitor.dns_info('shop.example.com')
        self.assertEqual(result['ns_zone'], 'example.com')
        self.assertEqual(result['nameservers'], ['ns.example.com'])

    def test_missing_domain_does_not_attribute_tld_nameservers(self):
        with mock.patch.object(monitor, 'dns_query', return_value={'status': 'NXDOMAIN', 'values': []}) as query:
            result = monitor.dns_info('missing.example')
        self.assertEqual(result['status'], 'NXDOMAIN')
        self.assertEqual(result['nameservers'], [])
        self.assertNotIn(mock.call('example', 'NS'), query.call_args_list)

    def test_http_follows_relative_redirect_and_tracks_both_ips(self):
        with mock.patch.object(monitor, 'one_http', side_effect=[response(302, '203.0.113.7', '/new'), response(200, '203.0.113.8')]):
            result = monitor.http_info('https://example.com/')
        self.assertEqual(result['final_url'], 'https://example.com/new')
        self.assertEqual(result['status'], 200)
        self.assertTrue(result['responds'])
        self.assertEqual(result['initial_ip'], '203.0.113.7')
        self.assertEqual(result['remote_ip'], '203.0.113.8')

    def test_https_failure_retains_error_when_http_responds(self):
        with mock.patch.object(monitor, 'one_http', side_effect=[response(None, None, error='TLS failure'), response(200)]):
            result = monitor.http_info('https://example.com/')
        self.assertTrue(result['responds'])
        self.assertEqual(result['https_error'], 'TLS failure')
        self.assertEqual(result['final_url'], 'http://example.com/')

    def test_http_fallback_redirect_to_https_is_not_a_loop(self):
        replies = [response(None, None, error='Temporary timeout'), response(301, location='https://example.com/'), response(200)]
        with mock.patch.object(monitor, 'one_http', side_effect=replies) as request:
            result = monitor.http_info('https://example.com/')
        self.assertEqual(request.call_count, 3)
        self.assertEqual(result['status'], 200)
        self.assertIsNone(result['error'])

    def test_redirect_failure_is_preserved_despite_initial_response(self):
        with mock.patch.object(monitor, 'one_http', side_effect=[response(302, location='https://other.example/'), response(None, None, error='Timeout')]):
            result = monitor.http_info('https://example.com/')
        self.assertTrue(result['responds'])
        self.assertEqual(result['error'], 'Timeout')

    def test_redirect_loop_is_bounded(self):
        with mock.patch.object(monitor, 'one_http', return_value=response(302, location='/')) as request:
            result = monitor.http_info('https://example.com/')
        self.assertTrue(result['error'])
        self.assertEqual(request.call_count, 1)

    def test_unsupported_redirect_is_not_followed(self):
        with mock.patch.object(monitor, 'one_http', return_value=response(302, location='file:///etc/passwd')) as request:
            result = monitor.http_info('https://example.com/')
        self.assertTrue(result['error'])
        self.assertEqual(request.call_count, 1)

    def test_docker_missing_is_distinct_from_stopped(self):
        missing = monitor.docker_info({'container_names':['site']}, {}, None, {})
        stopped = monitor.docker_info({'container_names':['site']}, {'site':{'name':'site','state':'exited','health':None}}, None, {})
        self.assertFalse(missing['exists'])
        self.assertFalse(missing['active'])
        self.assertTrue(stopped['exists'])
        self.assertFalse(stopped['active'])

    def test_docker_inspection_failure_must_not_claim_absence(self):
        result = monitor.docker_info({'container_names':['site']}, {}, 'Docker unavailable', {})
        self.assertIsNone(result['exists'])
        self.assertIsNone(result['active'])
        self.assertNotEqual(result['containers'][0]['state'], 'absent')

    def test_user_account_inventory_is_exact(self):
        import build_registry
        names = sum(build_registry.ACCOUNTS.values(), [])
        self.assertEqual(len(names), 35)
        self.assertEqual(len(set(names)), 35)
        reference = json.loads((pathlib.Path(__file__).parent / 'reference.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(len(set(names) | set(reference['domains'])), 38)


if __name__ == '__main__':
    unittest.main(verbosity=2)
