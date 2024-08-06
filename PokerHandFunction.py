def findPokerHand(hand):
    ranks = []
    suits = []
    possibleRanks = []

    for card in hand: # goes through the poker hand
        if len(card) == 2:
            rank = card[0] #assigns the first value of each card to rank
            suit = card[1] #assigns the last value of each card to suit
        else:
            rank = card[0:2]
            suit = card[2]

        #assigns the face cards a number value so that it's easier to sort them
        if rank == "A":
            rank = 14
        elif rank == "K":
            rank = 13
        elif rank == "Q":
            rank = 12
        elif rank == "J":
            rank = 11

        ranks.append(int(rank))
        suits.append(suit)

    sortedRanks = sorted(ranks) #sorts the rank from low to high

    # Royal Flush, Straight Flush and Flush
    if suits.count(suits[0]) == 5: #goes through the suits list and compares the first element with the rest
        #Royal
        if 14 in sortedRanks and 13 in sortedRanks and 12 in sortedRanks and 11 in sortedRanks and 10 in sortedRanks:
            possibleRanks.append(10)
        elif all(sortedRanks[i] == sortedRanks[i-1] + 1 for i in range(1, len(sortedRanks))):
            possibleRanks.append(9)
        #Flush
        else:
            possibleRanks.append(6)

    #Straigth
    # 10 11 12 13 14
    # 11 == 10+1
    if all(sortedRanks[i] == sortedRanks[i-1] + 1 for i in range(1, len(sortedRanks))):
        possibleRanks.append(5)

    handUniqueVals = list(set(sortedRanks)) #gets the unique vals from each hand and puts it in list

    #Four of a Kind and Full House
    if len(handUniqueVals) == 2:
        for val in handUniqueVals:
            if sortedRanks.count(val) == 4: #Four of a Kind
                possibleRanks.append(8)
            elif sortedRanks.count(val) == 3: #Full House
                possibleRanks.append(7)

    #Three of a Kind and Two Pair
    if len(handUniqueVals) == 3:
        for val in handUniqueVals:
            if sortedRanks.count(val) == 3: #Three of a Kind
                possibleRanks.append(4)
            elif sortedRanks.count(val) == 2: #Two Pair
                possibleRanks.append(3)

    #Pair
    if len(handUniqueVals) == 4:
        possibleRanks.append(2)

    if not possibleRanks:
        possibleRanks.append(1)

    pokerHandRanks = {
        10: "Royal Flush",
        9: "Straight Flush",
        8: "Four of a Kind",
        7: "Full House",
        6: "Flush",
        5: "Straight",
        4: "Three of a Kind",
        3: "Two Pair",
        2: "Pair",
        1: "High Card"
    }

    output = pokerHandRanks[max(possibleRanks)]
    print(hand, output)

    return output

if __name__ == "__main__":
    findPokerHand(["AH", "KH", "QH", "JH", "10H"]) # Royal Flush
    findPokerHand(["QC", "JC", "10C", "9C", "8C"]) # Straight Flush
    findPokerHand(["5C", "5S", "5H", "5D", "QH"]) # Four of a Kind
    findPokerHand(["2H", "2D", "2S", "10H", "10C"]) # Full House
    findPokerHand(["2D", "KD", "7D", "6D", "5D"]) # Flush
    findPokerHand(["JC", "10H", "9C", "8C", "7D"]) # Straight
    findPokerHand(["10H", "10C", "10D", "2D", "5S"]) # Three of a Kind
    findPokerHand(["KD", "KH", "5C", "5S", "6D"]) # Two Pair
    findPokerHand(["2D", "2S", "9C", "KD", "10C"]) # Pair
    findPokerHand(["KD", "5H", "2D", "10C", "JH"]) # High Card



