from datetime import datetime
from collections import OrderedDict


class Points:
    """
    This class represents the node in Double LinkedList
    """
    def __init__(self, payer, points, timestamp, format):
        self.payer = payer
        self.points = points
        self.timestamp = datetime.strptime(timestamp,format)
        self.next = None
        self.prev = None
        return


class PointsRecord:
    """
    class to create and persist data in LinkedList format
    self.head and self.tail stores the pointer to first and last node
    self.entire_info = DICTIONARY or HASHMAP | this will store data in key value pair, where key is payer and value is the total points corresponding to that payer so far
    self.total_points = INTEGER | total reward points of all payers so far.
    """
    def __init__(self):
        self.format = "%Y-%m-%dT%H:%M:%SZ"
        self.head = None
        self.tail = None
        self.entire_info = OrderedDict()
        self.total_points = 0
        return

    def insert(self, payer, points, timestamp):
        """
        This method contains logic of adding incoming data as per the increasing order of timestamp
        :param payer: string
        :param points: integer
        :param timestamp: timestamp
        """
        node = Points(payer, points, timestamp, self.format)
        #if the linkedlist is empty, first node is added without any date check
        if self.head == None:
            self.head = node
            self.tail = self.head
            return

        #logic to add nodes in order in which they arrive
        # self.tail.next = node
        # node.prev = self.tail
        # self.tail = node
        # return

        #logic to add new nodes as per timestamp
        temp = self.tail
        while temp and temp.timestamp > node.timestamp:
            temp = temp.prev

        #first position
        if temp == None:
            node.next = self.head
            self.head.prev = node
            self.head = node
            return

        #last position
        if temp == self.tail:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
            return

        #adding node in between
        node.next = temp.next
        node.prev = temp.next.prev
        temp.next = node
        node.next.prev = node
        return
        # temp.next.prev = node
        # node.prev = temp.next

    def insert_negative_points(self, payer, points):
        """
        This is basically removing nodes (if node.points <= points) or subtracting points from current node values (if node.points>points).
        :param payer: string
        :param points: int
        :return:
        """
        current = self.head
        sub = 0
        while points < 0:
            temp = current.next
            if current.payer == payer:
                if current.points + points > 0:  #subtracting value from current node
                    current.points += points
                    points = 0
                else:  #abs value of current node points are less than points. consuming the entire current node
                    left = current.prev
                    right = current.next
                    points += current.points

                    if left is None and right is None:  #only 1 node
                        self.head = self.tail = None
                    elif left is None:  #1st node
                        current.next = None
                        self.head = right
                        right.prev = None
                    elif right is None:  #last node
                        self.tail = left
                        current.prev = None
                        left.next = None
                    else:  #in between
                        current.prev = None
                        current.next = None
                        left.next = right
                        right.prev = left
            current = temp
        return

    def add(self, payer, points, timestamp, **kwargs):
        """
        This method get called to persist data. It uses 2 mechanism: 1. dictionary to persist data against each payer and their total points -> used to return total balance against each payer. 2. In form of LinkedList, as per ascending order of timestamp
        :param payer: string
        :param points: integer
        :param timestamp: timestamp
        :param kwargs: new/unknown parameters coming in from request
        :return: bool: if the entry was valid or not
        """
        if points == 0:
            return False
        if (payer in self.entire_info and points < 0 and abs(points) > self.entire_info[payer]) or (payer not in self.entire_info and points < 0):
            return False
        if payer not in self.entire_info:
            self.entire_info[payer] = 0
        # if points < 0 and abs(points) > self.entire_info[payer]:
        #     return False
        self.entire_info[payer] += points
        self.total_points += points
        if points < 0:
            self.insert_negative_points(payer, points)
        else:
            self.insert(payer, points, timestamp)
        return True

    def spend(self, redeem_point):
        """
        This method is called while redeeming the points. Before calling this method, make sure the user requested redeem amount is <= self.total_points
        :param redeem_point: int | points to be redeemed
        :return: the dictionary of payer and their corresponding points deducted.
        """
        self.total_points -= redeem_point
        payer_info = OrderedDict() #will store the points deducted from each payer and return the data to API call
        temp = self.head
        deduct = 0  #holds the amount from each node
        while redeem_point != 0:
            curr_payer = temp.payer
            #calculating the amount to be deducted from each node
            if redeem_point >= temp.points: #= condition when we reach the last node of LinkedList
                deduct = temp.points
                temp = temp.next
            else:
                temp.points -= redeem_point
                deduct = redeem_point

            self.entire_info[curr_payer] -= deduct
            redeem_point -= deduct
            # self.entire_info[temp.payer] -= deduct
            if curr_payer not in payer_info:
                payer_info[curr_payer] = 0
            payer_info[curr_payer] -= deduct

        #points deducted = total available points
        if temp == None:
            self.head = self.tail = None
        elif temp != self.head:  #not the first node
            #some partial points deducted
            self.head = temp
            # print(f"error here while value of redeem points is {redeem_point}")
            temp.prev.next = None
            temp.prev = None
        return payer_info

    def print(self, reverse=False):
        """
        This method was developed for testing purpose, to check if the LinkedList is working properly or not.
        :param reverse: bool | To print the LinkedList in ascending or descending order
        :return: None
        """
        if not reverse:
            node = self.head
            while node:
                print(node.payer, node.points, node.timestamp)
                node = node.next
        else:
            node = self.tail
            while node:
                print(node.payer, node.points, node.timestamp)
                node = node.prev
        return


    def clear(self):
        """
        Method created to reset the LinkedList. Useful when user don't want to restart the server, but clean the data.
        :return: None
        """
        self.head = self.tail = None
        self.entire_info.clear()
        self.total_points = 0
        return