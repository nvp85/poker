import unittest
import unittest.mock
from collections import Counter
import the_best_hand as main_module
from the_best_hand import Hand, straight_flush, four_of_a_kind, full_house, \
    flush, straight, three_of_a_kind, two_pairs, pair, the_best_hand, OrderedRanks, app


class BestHandTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_validate_ok(self):
        h = Hand(
            (
                ('club', 'J'),
                ('diamond', 'J'),
                ('heart', 'J'),
                ('spade', 'J'),
                ('club', '5'),
            ),
        )
        self.assertEqual(h.validate_error(), [])

    def test_validate_duplicate(self):
        h = Hand(
            (
                ('club', 'J'),
                ('diamond', 'J'),
                ('heart', 'J'),
                ('spade', 'J'),
                ('club', 'J'),
            ),
        )
        self.assertEqual(h.validate_error(), ["Duplicate cards: ('club', 'J')"])

    def test_validate_not_five(self):
        h = Hand(
            (
                ('club', 'J'),
                ('diamond', 'J'),
                ('heart', 'J'),
                ('spade', 'J'),
                ('club', '3'),
                ('club', '1'),
            ),
        )
        self.assertEqual(h.validate_error(), ['The number of card is not five!'])

    def test_validate_err(self):
        h = Hand(
            (
                ('club', 'J'),
                ('diamond', 'J'),
                ('heart', 'J'),
                ('spade', 'J'),
                ('club', '1'),
            ),
        )
        self.assertEqual(h.validate_error(), ["Error: some suit or rank is not valid: ('club', '1')"])

    def test_ranks(self):
        h = Hand(
            (
                ('club', 'J'),
                ('diamond', 'J'),
                ('heart', 'J'),
                ('spade', 'J'),
                ('club', '5'),
            ),
        )
        self.assertEqual(h.ranks(), OrderedRanks('5JJJJ', ''))

    def test_suits(self):
        h = Hand(
            (
                ('club', 'J'),
                ('diamond', 'J'),
                ('heart', 'J'),
                ('spade', 'J'),
                ('club', '5'),
            ),
        )
        self.assertEqual(h.suits(), {'club', 'diamond', 'heart', 'spade'})

    def test_freqs(self):
        h = Hand(
            (
                ('club', 'J'),
                ('diamond', 'J'),
                ('heart', 'J'),
                ('spade', 'J'),
                ('club', '5'),
            ),
        )
        self.assertEqual(h.freqs(), Counter([4, 1,]))

    def test_order_by_rank(self):
        h = Hand()
        self.assertEqual(h.order_by_rank('739A4'), OrderedRanks('3479', 'A'))

    def test_straight_flush(self):
        self.assertTrue(straight_flush({'club',}, OrderedRanks('10JQK', "A")))
        self.assertTrue(straight_flush({'club',}, OrderedRanks('2345', "A")))
        self.assertTrue(straight_flush({'spade',},OrderedRanks('56789', "")))
        self.assertFalse(straight_flush({'club', 'diamond'}, OrderedRanks('2345', "A")))
        self.assertFalse(straight_flush({'diamond',}, OrderedRanks('34589', "")))

    def test_four_of_a_kind(self):
        self.assertTrue(four_of_a_kind(Counter([1,4])))
        self.assertFalse(four_of_a_kind(Counter([5,])))
        self.assertFalse(four_of_a_kind(Counter([2, 3])))

    def test_full_house(self):
        self.assertTrue(full_house(Counter([2, 3])))
        self.assertTrue(full_house(Counter([3, 2])))
        self.assertFalse(full_house(Counter([1, 2, 2])))
        self.assertFalse(full_house(Counter([1, 1, 1, 2])))

    def test_flush(self):
        self.assertTrue(flush({'diamond',}))
        self.assertFalse(flush({'club', 'diamond', 'spade'}))

    def test_straight(self):
        self.assertTrue(straight(OrderedRanks('10JQK', 'A')))

    def test_three_of_a_kind(self):
        self.assertTrue(three_of_a_kind(Counter([1, 1, 3])))
        self.assertTrue(three_of_a_kind(Counter([3, 1, 1])))

    def test_two_pairs(self):
        self.assertTrue(two_pairs(Counter([2, 2, 1])))
        self.assertFalse(two_pairs(Counter([1, 1, 3])))

    def test_pair(self):
        self.assertTrue(pair(Counter([1, 1, 1, 2])))
        self.assertFalse(pair(Counter([1, 1, 2])))

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
                Hand(
                    (
                        ('club', 'J'),
                        ('club','10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7')
                    ),
                ),
            ),
            "Straight Flush",
        )

        mock_straight_flush.return_value = False
        mock_four_of_a_kind.return_value = True
        self.assertEqual(
            the_best_hand(
                Hand(
                    (
                        ('club', 'J'),
                        ('club', '10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7'),
                    ),
                ),
            ),
            "Four of a kind",
        )

        mock_four_of_a_kind.return_value = False
        mock_full_house.return_value = True
        self.assertEqual(
            the_best_hand(
                Hand(
                    (
                        ('club', 'J'),
                        ('club', '10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7'),
                    ),
                ),
            ),
            "Full House",
        )

        mock_full_house.return_value = False
        mock_flush.return_value = True
        self.assertEqual(
            the_best_hand(
                Hand(
                    (
                        ('club', 'J'),
                        ('club', '10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7')
                    ),
                ),
            ),
            "Flush",
        )

        mock_flush.return_value = False
        mock_straight.return_value = True
        self.assertEqual(
            the_best_hand(
                Hand(
                    (
                        ('club', 'J'),
                        ('club', '10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7'),
                    ),
                ),
            ),
            "Straight",
        )

        mock_straight.return_value = False
        mock_three_of_a_kind.return_value = True
        self.assertEqual(
            the_best_hand(
                Hand(
                    (
                        ('club', 'J'),
                        ('club', '10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7'),
                    ),
                ),
            ),
            "Three of a Kind",
        )

        mock_three_of_a_kind.return_value = False
        mock_two_pairs.return_value = True
        self.assertEqual(
            the_best_hand(
                Hand(
                    (
                        ('club', 'J'),
                        ('club', '10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7'),
                    ),
                ),
            ),
            "Two Pairs",
        )

        mock_two_pairs.return_value = False
        mock_pair.return_value = True
        self.assertEqual(
            the_best_hand(
                Hand(
                    (
                        ('club', 'J'),
                        ('club', '10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7'),
                    ),
                ),
            ),
            "Pair",
        )

        mock_pair.return_value = False
        self.assertEqual(
            the_best_hand(
                Hand(
                    (
                        ('club', 'J'),
                        ('club', '10'),
                        ('club', '3'),
                        ('spade', '8'),
                        ('club', '7'),
                    ),
                ),
            ),
            "High Card",
        )

    def test_hello_get(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    @unittest.mock.patch.object(main_module.CardForm, 'validate_on_submit', autospec=True)
    @unittest.mock.patch.object(main_module.Hand, 'validate_error', autospec=True)
    @unittest.mock.patch('the_best_hand.the_best_hand')
    def test_hello_post_true(self, mock_best_hand, mock_validate_error, mock_validate_on_submit):
        mock_validate_on_submit.return_value = True
        mock_validate_error.return_value = []
        self.app.post('/', data={})
        self.assertTrue(mock_best_hand.called)

    @unittest.mock.patch.object(main_module.CardForm, 'validate_on_submit', autospec=True)
    @unittest.mock.patch.object(main_module.Hand, 'validate_error', autospec=True)
    @unittest.mock.patch('the_best_hand.the_best_hand')
    def test_hello_post_false(self, mock_best_hand, mock_validate_error, mock_validate_on_submit):
        mock_validate_on_submit.return_value = False
        mock_validate_error.return_value = ['some error']
        self.app.post('/', data={})
        self.assertFalse(mock_best_hand.called)


if __name__ == '__main__':
    unittest.main()
