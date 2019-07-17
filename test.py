from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from lib.app import NSFWApp
import unittest


class NSFWAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        return NSFWApp(None)

    @unittest_run_loop
    async def test_get_root(self):
        resp = await self.client.request("GET", "/v1/")
        assert resp.status == 200
        text = await resp.text()
        assert text == 'OK'

    @unittest_run_loop
    async def test_get_spec(self):
        resp = await self.client.request("GET", "/v1/?spec")
        assert resp.status == 200
        spec = await resp.json()
        assert spec['info']['title'] == 'nsfwoid'

    @unittest_run_loop
    async def test_get_metrics(self):
        resp = await self.client.request("GET", "/v1/metrics")
        assert resp.status == 200
        metrics = await resp.text()
        assert 'python_info' in metrics

    @unittest_run_loop
    async def test_post_root(self):
        resp = await self.client.request("POST", "/v1/")
        assert resp.status == 405  # Method not allowed

    @unittest_run_loop
    async def test_post_metrics(self):
        resp = await self.client.request("POST", "/v1/metrics")
        assert resp.status == 405  # Method not allowed

    @unittest_run_loop
    async def test_get_score(self):
        resp = await self.client.request("GET", "/v1/score")
        assert resp.status == 405  # Method not allowed


if __name__ == '__main__':
    unittest.main()
