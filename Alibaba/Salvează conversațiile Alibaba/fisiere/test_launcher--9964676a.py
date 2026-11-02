import unittest
from unittest.mock import Mock, patch
from launcher import create_launcher, Controller

class Tests(unittest.TestCase):
    def setUp(self):
        self.control=Mock();self.control.health.return_value=False
        self.client=create_launcher('fixture',self.control).test_client()
    def req(self,path,method='GET',**headers):
        return self.client.open(path,method=method,base_url='http://127.0.0.1:8766',headers={'X-Archive-Key':'fixture',**headers})
    def test_offline_dashboard_and_start(self):
        self.assertEqual(self.req('/').status_code,200)
        self.assertFalse(self.req('/control/status').json['running'])
        self.control.start.return_value={'running':True,'started':True}
        self.assertTrue(self.req('/control/start','POST').json['running'])
        self.control.start.assert_called_once_with()
    def test_security(self):
        self.assertEqual(self.client.post('/control/start',base_url='http://127.0.0.1:8766').status_code,401)
        self.assertEqual(self.req('/control/start','POST',Origin='https://evil.example').status_code,403)
        self.assertEqual(self.client.get('/',base_url='http://evil.example:8766').status_code,403)
        self.assertEqual(self.req('/control/start').status_code,405)
        self.control.start.assert_not_called()
    def test_errors_are_not_success(self):
        self.control.start.side_effect=RuntimeError('Nu a pornit')
        self.assertEqual(self.req('/control/start','POST').status_code,503)
    def test_running_worker_not_started_twice(self):
        c=Controller('fixture');c.health=Mock(return_value=True);c.spawn=Mock()
        self.assertEqual(c.start(),{'running':True,'started':False});c.spawn.assert_not_called()
    def test_start_waits_until_healthy(self):
        c=Controller('fixture');c.health=Mock(side_effect=[False,False,True]);c.spawn=Mock(return_value=Mock(poll=Mock(return_value=None)))
        with patch('launcher.socket.socket') as s,patch('launcher.time.sleep'):
            s.return_value.__enter__.return_value.connect_ex.return_value=1
            self.assertTrue(c.start()['running'])
        c.spawn.assert_called_once()

if __name__=='__main__':unittest.main()
