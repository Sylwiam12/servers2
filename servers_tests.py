import unittest

from servers import Server, ListServer, Product, Client, TooManyProductsError


class ServerTest(unittest.TestCase):
    def test_get_entries_returns_sorted_results(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        server = ListServer(products)
        entries = server.get_entries(1)

        self.assertListEqual([products[0]], entries)

    def test_get_entries_raises_exceptions_if_too_many_results(self):
        products = [Product('PP234', 2)] * 5
        server = ListServer(products)

        with self.assertRaises(TooManyProductsError):
            server.get_entries(2)

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        server = ListServer(products)
        entries = server.get_entries(2)
        self.assertEqual([products[2], products[1]], entries)

class TestClient(unittest.TestCase):
    def test_total_price_is_zero_if_exception_raised(self):
        products = [Product('PP234', 2)] * 5
        server = ListServer(products)
        client = Client(server)
        with self.assertRaises(TooManyProductsError):
            server.get_entries(2)

    def test_total_price_for_normal_execution(self):
        products = [Product('P234', 2), Product('P235', 3)]
        server = ListServer(products)
        client = Client(server)
        self.assertEqual(5, client.get_total_price(1))


if __name__ == '__main__':
    unittest.main()