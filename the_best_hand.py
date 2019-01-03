suit = ('diamond', 'club', 'heart', 'spade')
rank = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
rank_aces_low = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
rank_aces_high = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
list_of_cards = [
(('club', 'J'), ('diamond','A'), ('heart', '2'), ('spade', 'A'), ('club', '5')),
(('club', 'J'), ('club','10'), ('club', '9'), ('club', '8'), ('club', '7')),
(('club', 'J'), ('diamond','J'), ('heart', 'J'), ('spade', 'J'), ('club', '5')),
(('club', '7'), ('diamond','7'), ('heart', '7'), ('spade', '10'), ('club', '10')),
(('spade', '7'), ('spade','2'), ('spade', '5'), ('spade', 'J'), ('spade', '10')),
(('club', '7'), ('diamond','8'), ('heart', '6'), ('spade', '10'), ('club', '9')),
(('club', '7'), ('diamond','7'), ('heart', '7'), ('spade', '10'), ('club', '9')),
(('club', '7'), ('diamond','7'), ('heart', 'J'), ('spade', 'J'), ('club', '9')),
(('club', 'A'), ('diamond','A'), ('heart', 'J'), ('spade', '10'), ('club', '9')),
(('club', 'A'), ('diamond','7'), ('heart', 'J'), ('spade', '6'), ('club', '9')),
(('club', 'A'), ('diamond','K'), ('heart', 'J'), ('spade', 'Q'), ('club', '10')),
]


def suits_ranks(cards):
    suits = []
    ranks = ''
    for card in cards:
        ranks = ranks + card[1]
        if card[0] not in suits:
            suits.append(card[0])
    ranks = order_by_rank(ranks)
    return suits, ranks


def order_by_rank(s):
    ace = ''
    ordered_s = ''
    for r in rank:
        ordered_s = ordered_s + r*s.count(r)
    ace = '' + 'A'*s.count('A')
    return (ordered_s, ace)


def freqs(ranks):
    ranks = "".join(ranks)
    f = []
    for r in rank_aces_low:
        if ranks.count(r) > 0:
            f.append(ranks.count(r))
    return f


def flush(suits):
    # Five cards of the same suit. For example spadeK-spadeJ-spade9-spade3-spade2.
    result = False
    if len(suits) == 1:
        result = True
    return result


def straight(s):
    """Five cards of mixed suits in sequence - for example spadeQ-diamondJ-heart10-spade9-club8.
    Optional: Ace can count high or low in a straight, but not both at once,
    so A-K-Q-J-10 and 5-4-3-2-A are valid straights, but 2-A-K-Q-J is not.
    """
    result = False
    if s[0] + s[1] in "".join(rank_aces_high):
        result = True
    elif s[1] + s[0] in "".join(rank_aces_low):
        result = True
    return result


def straight_flush(suits, ranks):
    """Five cards of the same suit in sequence - such as clubJ-club10-club9-club8-club7.
    Optional: An ace can be counted as low, so heart5-heart4-heart3-heart2-heartA is a straight flush,
    but its top card is the five, not the ace, so it is the lowest type of straight flush.
    The cards cannot "turn the corner": diamond4-diamond3-diamond2-diamondA-diamondK is not valid."""
    result = False
    if flush(suits) and straight(ranks):
        result = True
    return result


def four_of_a_kind(f):
    """Four cards of the same rank - such as four queens. The fifth card can be anything.
    This combination is sometimes known as "quads", and in some parts of Europe it is called a "poker",
    though this term for it is unknown in English."""
    result = False
    if 4 in f:
        result = True
    return result


def full_house(f):
    """This consists of three cards of one rank and two cards of another rank - for example three sevens and two tens
        (colloquially known as "sevens full" or more specifically "sevens on tens")."""
    result = False
    if 3 in f and 2 in f:
        result = True
    return result


def three_of_a_kind(f):
    """Three cards of the same rank plus two other cards. This combination is also known as Triplets or Trips.
    Example 5-5-5-3-2."""
    result = False
    if 3 in f and 2 not in f:
        result = True
    return result


def two_pairs(f):
    """A pair is two cards of equal rank. In a hand with two pairs, the two pairs are of different ranks
    (otherwise you would have four of a kind), and there is an odd card to make the hand up to five cards.
    Example J-J-2-2-4.
    """
    result = False
    if f.count(2) == 2:
        result = True
    return result


def pair(f):
    """A hand with two cards of equal rank and three other cards which do not match these or each other.
    Example 6-6-4-3-2 ."""
    result = False
    if f.count(2) == 1 and f.count(1) == 3:
        result = True
    return result


def the_best_hand(cards):
    print(cards)
    suits, ranks = suits_ranks(cards)
    f = freqs(ranks)
    result = "High Card"
    if straight_flush(suits, ranks):
        result = "Straight Flush"
    elif four_of_a_kind(f):
        result = "Four of a kind"
    elif full_house(f):
        result = "Full House"
    elif flush(suits):
        result = "Flush"
    elif straight(ranks):
        result = "Straight"
    elif three_of_a_kind(f):
        result = "Three of a Kind"
    elif two_pairs(f):
        result = "Two Pairs"
    elif pair(f):
        result = "Pair"
    return result



