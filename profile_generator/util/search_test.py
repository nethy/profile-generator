from unittest import TestCase

from .search import get_table, table_search


class SearchTest(TestCase):
    def test_get_table(self) -> None:
        self.assertEqual(get_table(0, 0, 2, SearchTest._identity), {0: 0})
        self.assertEqual(
            get_table(0, 9, 10, SearchTest._identity), {i: i for i in range(10)}
        )

    def test_table_search(self) -> None:
        table = get_table(0, 0, 2, SearchTest._identity)
        self.assertEqual(table_search(table, SearchTest._identity, 0), 0)

        table = get_table(0, 1, 2, SearchTest._identity)
        self.assertEqual(table_search(table, SearchTest._identity, 0), 0)
        self.assertEqual(table_search(table, SearchTest._identity, 1), 1)
        self.assertEqual(table_search(table, SearchTest._identity, 0.5), 0.5)

        table = get_table(0, 2, 3, SearchTest._identity)
        self.assertEqual(table_search(table, SearchTest._identity, 0.5), 0.5)
        self.assertEqual(table_search(table, SearchTest._identity, 1.5), 1.5)

    @staticmethod
    def _identity(x: float) -> float:
        return x
