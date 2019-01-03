import unittest
import unittest.mock
from the_best_hand import freqs, suits_ranks, order_by_rank, straight_flush, four_of_a_kind, full_house, \
    flush, straight, three_of_a_kind, two_pairs, pair, the_best_hand


class BestHandTestCase(unittest.TestCase):

    def test_suits_ranks(self):
        self.assertEqual(suits_ranks(
            (
                ('club', 'J'),
                ('diamond','J'),
                ('heart', 'J'),
                ('spade', 'J'),
                ('club', '5'),
            ),
        ),
        (
            ['club', 'diamond', 'heart', 'spade'],
            ('5JJJJ', ''),
        ),
    )

    def test_freqs(self):
        self.assertEqual(freqs(('10JQK', "A")), [1, 1, 1, 1, 1])

    def test_order_by_rank(self):
        self.assertEqual(order_by_rank('739A4'), ('3479', 'A'))

    def test_straight_flush(self):
        self.assertTrue(straight_flush(['club',], ('10JQK', "A")))
        self.assertTrue(straight_flush(['club', ], ('2345', "A")))
        self.assertTrue(straight_flush(['spade', ], ('56789', "")))
        self.assertFalse(straight_flush(['club', 'diamond'], ('2345', "A")))
        self.assertFalse(straight_flush(['diamond',], ('34589', "")))

    def test_four_of_a_kind(self):
        self.assertTrue(four_of_a_kind([1,4]))
        self.assertFalse(four_of_a_kind([5,]))
        self.assertFalse(four_of_a_kind([2, 3]))

    def test_full_house(self):
        self.assertTrue(full_house([2, 3]))
        self.assertTrue(full_house([3, 2]))
        self.assertFalse(full_house([1, 2, 2]))
        self.assertFalse(full_house([1, 1, 1, 2]))

    def test_flush(self):
        self.assertTrue(flush(['diamond',]))
        self.assertFalse(flush(['club', 'diamond', 'spade']))

    def test_straight(self):
        self.assertTrue(straight(('10JQK', 'A')))

    def test_three_of_a_kind(self):
        self.assertTrue(three_of_a_kind([1, 1, 3]))
        self.assertTrue(three_of_a_kind([3, 1, 1]))

    def test_two_pairs(self):
        self.assertTrue(two_pairs([2, 2, 1]))
        self.assertFalse(two_pairs([1, 1, 3]))

    def test_pair(self):
        self.assertTrue(pair([1, 1, 1, 2]))
        self.assertFalse(pair([1, 1, 2]))

    @unittest.mock.patch('the_best_hand.pair')
    @unittest.mock.patch('the_best_hand.two_pairs')
    @unittest.mock.patch('the_best_hand.three_of_a_kind')
    @unittest.mock.patch('the_best_hand.straight')
    @unittest.mock.patch('the_best_hand.flush')
    @unittest.mock.patch('the_best_hand.full_house')
    @unittest.mock.patch('the_best_hand.four_of_a_kind')
    @unittest.mock.patch('the_best_hand.straight_flush')
    def test_the_best_hand(
            self,
            mock_straight_flush,
            mock_four_of_a_kind,
            mock_full_house,
            mock_flush,
            mock_straight,
            mock_three_of_a_kind,
            mock_two_pairs,
            mock_pair,
    ):
        mock_straight_flush.return_value = True
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club','10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7')
                ),
            ),
            "Straight Flush",
        )

        mock_straight_flush.return_value = False
        mock_four_of_a_kind.return_value = True
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club', '10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7'),
                ),
            ),
            "Four of a kind",
        )

        mock_four_of_a_kind.return_value = False
        mock_full_house.return_value = True
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club', '10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7'),
                ),
            ),
            "Full House",
        )

        mock_full_house.return_value = False
        mock_flush.return_value = True
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club', '10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7')
                ),
            ),
            "Flush",
        )

        mock_flush.return_value = False
        mock_straight.return_value = True
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club', '10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7'),
                ),
            ),
            "Straight",
        )

        mock_straight.return_value = False
        mock_three_of_a_kind.return_value = True
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club', '10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7'),
                ),
            ),
            "Three of a Kind",
        )

        mock_three_of_a_kind.return_value = False
        mock_two_pairs.return_value = True
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club', '10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7'),
                ),
            ),
            "Two Pairs",
        )

        mock_two_pairs.return_value = False
        mock_pair.return_value = True
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club', '10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7'),
                ),
            ),
            "Pair",
        )

        mock_pair.return_value = False
        self.assertEqual(
            the_best_hand(
                (
                    ('club', 'J'),
                    ('club', '10'),
                    ('club', '3'),
                    ('spade', '8'),
                    ('club', '7'),
                ),
            ),
            "High Card",
        )


if __name__ == '__main__':
    unittest.main()
