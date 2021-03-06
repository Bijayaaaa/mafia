import random
# from cards import Card


class CardDistribution:
    '''
        # problem:
        - you have three set of cards
        - you want to distribute cards among three players
        - players would have to get:<required_distribution> no. of cards
        - e.g. required_distribution = [2,5,3]

        - problem with distributing cards randomly is : it might distributel sth. like all cards from intersection to one player so there are not enough cards left for another player sharing the intersection


        # solution:
        - First distribute roughly half of only intersect of two sub-sets among both players
        - Then distribute a_intersect_b_intersect_c so as not to exceed the required no. of cards
        - note: donot give the player more cards than required
        - and distribution should balance themselves out

        '''

    def __init__(self, a, b, c, required_distribution):
        self.a = a
        self.b = b
        self.c = c
        # no. of cards required to be distributed e.g.[2,3,4]
        self.required = required_distribution
        # print('\n\n----------distributor--------------', '\n\a:', (a), '\n\b:',
        #       (b), '\n\c:', (c), '\n:', required_distribution, '\n\n')

        # print('\n\n----------distributor--------------', '\n\nhere:', Card.convert_back(a), '\n\nhere:',
        #       Card.convert_back(b), '\n\nhere:', Card.convert_back(c), '\n:', required_distribution, '\n\n')

    def generate_decks(self, how_many):
        decks = []
        for i in range(how_many):
            decks.append(self.distribute())
        return decks

    def distribute(self):
        def set_members(a, b, c):
            # returns aintbintc, aintb, aintc, bintc, a0, b0, c0
            # # aintb -> a intersection b, ao -> a only

            def distribute(a, b, c):
                a0 = []
                aintbintc = []
                aintb = []
                aintc = []
                for val in a:
                    if (val in b and val in c):
                        aintbintc.append(val)
                    elif (val in b):
                        aintb.append(val)
                    elif (val in c):
                        aintc.append(val)
                    else:
                        a0.append(val)
                return a0, aintbintc, aintb, aintc

            ao, aintbintc, aintb, aintc = distribute(a, b, c)
            bo, bintcinta, bintc, binta = distribute(b, c, a)
            co, cintaintb, cinta, cintb = distribute(c, a, b)
            return aintbintc, aintb, aintc, bintc, ao, bo, co

        aintbintc, aintb, aintc, bintc, ao, bo, co = set_members(
            self.a, self.b, self.c)
        # print('\n-----------distributor:\n--------', aintbintc, '\n',
        #       aintb, '\n', aintc, '\n', bintc, '\n', ao, '\n', bo, '\n', co)
        p1 = ao.copy()  # player:p1 cards
        p2 = bo.copy()  # player:p2 cards
        p3 = co.copy()  # player:p3 cards

        def proper_ratio(aintb, required_no_a, existing_no_a):
            if int(len(aintb)/2) <= required_no_a - existing_no_a:
                # card to give is less than requirement
                return int(len(aintb)/2)
            else:
                return required_no_a - existing_no_a
                # giving player cards equal to requirement
                # <preventing from giving more cards than required>

        # distributing (aintb) to p1 and p2
        r1 = proper_ratio(aintb, self.required[0], len(ao))

        p1.extend(random.sample(aintb, r1))
        p2.extend(random.sample([i for i in aintb if i not in p1], r1))

        # distributing (aintb) to p2 and p3
        r1 = proper_ratio(bintc, self.required[1], len(bo))

        p2.extend(random.sample(bintc, r1))
        p3.extend(random.sample([i for i in bintc if i not in p2], r1))

        # distributing (aintb) to p1 and p2
        r1 = proper_ratio(aintc, self.required[2], len(co))

        p3.extend(random.sample(aintc, r1))
        p1.extend(random.sample([i for i in aintc if i not in p3], r1))

        # distributing aintbintc cards to all players
        no_req = []
        no_req_p1 = self.required[0] - len(p1)
        no_pre_p2 = self.required[1] - len(p2)
        no_req_p3 = self.required[2] - len(p3)
        for n, player_cards in enumerate([p1, p2, p3]):
            no_cards_req = self.required[n] - len(player_cards)
            player_cards.extend(random.sample(aintbintc, no_cards_req))

        return {0: p1, 1: p2, 2: p3}

        # return p1_cards, p2_cards, p3_cards


if __name__ == "__main__":
    # a = [1,2,3,4,5,6,9]
    # b = [1,2,3,4,7,8,10]
    # c = [1,2,5,6,7,8,11]
    # n_cards = [3, 4, 4]

    # p1_cards, p2_cards, p3_cards = CardDistribution(a, b, c, [3,4,4]).distribute()
    # print(p1_cards, p2_cards, p3_cards)
    a = ['5S', '4S', 'TH', '5H', 'JC', 'TC',
         '9C', '8C', 'KD', '5D', '4D', '3D']

    b = ['2C', '3C', '4C', '5C', '6C', '7C', 'QC', 'KC', '1C', '2D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', '1D', '2H',
         '3H', '4H', '6H', '7H', '8H', '9H', 'JH', 'QH', 'KH', '1H', '2S', '3S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', '1S']

    c = ['2C', '3C', '4C', '5C', '6C', '7C', 'QC', 'KC', '1C', '2D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', '1D', '2H',
         '3H', '4H', '6H', '7H', '8H', '9H', 'JH', 'QH', 'KH', '1H', '2S', '3S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', '1S']
    n_cards = [13, 13, 13, 12]
    n_cards.reverse()
    print(CardDistribution(a, b, c, n_cards).generate_decks(3))
