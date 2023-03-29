"""
UMass ECE 241 - Advanced Programming
Project #1   Fall 2021
project1.py - Sorting and Searching

"""

import matplotlib.pyplot as plt
import time
import random
import csv


"""
Stock class for stock objects
"""
class Stock:

    """
    Constructor to initialize the stock object
    """
    def __init__(self, sname, symbol, val, prices): # constructor for Stock class

        self.sname = sname
        self.symbol = symbol
        self.val = val
        self.prices = prices



    """
    return the stock information as a string, including name, symbol, 
    market value, and the price on the last day (2021-02-01). 
    For example, the string of the first stock should be returned as: 
    “name: Exxon Mobil Corporation; symbol: XOM; val: 384845.80; price:44.84”. 
    """
    def __str__(self): # printing out Stock to a string

        info = 'name: ' + self.sname + '; symbol: ' + self.symbol + '; val: ' + self.val + '; price:' + str(self.prices[-1])
        return info


"""
StockLibrary class to mange stock objects
"""
class StockLibrary: # contains all the stocks

    """
    Constructor to initialize the StockLibrary
    """
    def __init__(self): # constructor for library

        self.stockList = []
        self.size = 0
        self.isSorted = False
        self.bst = None


    """
    The loadData method takes the file name of the input dataset,
    and stores the data of stocks into the library. 
    Make sure the order of the stocks is the same as the one in the input file. 
    """
    def loadData(self, filename: str): # takes data from csv file and converts it to a stock

        firstLn = True # helps with not reading the first line of the csv file

        file = list(open(filename, 'r')) # open file

        for line in file: # reads line in file
            if firstLn == True: # skips first line
                firstLn = False
            else:
                index = line.split('|') # what it splits info in line by

                index[-1] = index[-1].strip() # gets rid of \n at end of line

                findex2 = float(index[2])
                sindex2 = str("{:.1f}".format(findex2))

                self.stockList.append(Stock(index[0], index[1], sindex2, index[3:])) # creats a stock
        self.size = len(self.stockList) # size of library


    """
    The linearSearch method searches the stocks based on sname or symbol.
    It takes two arguments as the string for search and an attribute field 
    that we want to search (“name” or “symbol”). 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """
    def linearSearch(self, query: str, attribute: str): # search for stock given attribute and query

        for i in range(len(self.stockList)): # goes through stockList
            if attribute == "symbol": # if searching by symbol
                if query == self.stockList[i].symbol:
                    return self.stockList[i]

            if attribute == "name": # if searching by name
                if query == self.stockList[i].sname:
                    return self.stockList[i]

        return "Stock not found" # stock not in stockList

    def randLinearSearch(self, hlist): # searches random 100 stocks
        ts = time.time()

        for i in range(len(hlist)):
            stonk = self.linearSearch(hlist[i], 'symbol')

        te = time.time()

        tb = te - ts

        return tb


    """
    Sort the stockList using QuickSort algorithm based on the stock symbol.
    The sorted array should be stored in the same stockList.
    Remember to change the isSorted variable after sorted
    """
    def quickSort(self): # method for sorting

        self.quickSortHelper(0, len(self.stockList) - 1)
        self.isSorted = True

    def quickSortHelper(self, first, last): #defines splitpoint

        if first < last:
            splitpoint = self.partition(first, last)

            self.quickSortHelper(first, splitpoint - 1)
            self.quickSortHelper(splitpoint + 1, last)

    def partition(self, first, last):  # partition of the quicksort

        pivot = self.stockList[first].symbol

        leftmark = first + 1
        rightmark = last

        done = False
        while not done:
            while leftmark <= rightmark and self.stockList[leftmark].symbol <= pivot:
                leftmark = leftmark + 1

            while self.stockList[rightmark].symbol >= pivot and rightmark >= leftmark:
                rightmark = rightmark - 1

            if rightmark < leftmark:
                done = True
            else:
                self.stockList[leftmark], self.stockList[rightmark] = self.stockList[rightmark], self.stockList[
                    leftmark]  #sorts using symbol

        self.stockList[rightmark], self.stockList[first] = self.stockList[first], self.stockList[
            rightmark]

        return rightmark



    """
    build a balanced BST of the stocks based on the symbol. 
    Store the root of the BST as attribute bst, which is a TreeNode type.
    """
    def buildBST(self): # building BST using AvlTree

        ts = time.time()
        avl = AvlTree()

        for i in range(self.size):
            avl.put(self.stockList[i].symbol, self.stockList[i])

        self.bst = avl.root # storing root attribute bst
        self.avl = avl

        te = time.time()

        tb = te - ts

        return tb # returning time process took



    """
    Search a stock based on the symbol attribute. 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """
    def searchBST(self, query, current='dnode'):
        searchitem = self.avl.get(query) # using the get method to get the stock

        if searchitem == None: # if it returned None there is no stock
            return 'stock not found'
        else: # otherwise return the stock
            return searchitem

    def randSearchBST(self, hlist): # searching random 100 stocks
        ts = time.time()

        for i in range(len(hlist)):
            stonk = self.searchBST(hlist[i])

        te = time.time()

        tb = te - ts

        return tb # returning time process took



class TreeNode: # TreeNode class given by course

    def __init__(self,key,val,left=None,right=None,parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.balanceFactor = 0

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


class BinarySearchTree: # BinarySearchTree class given by course

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self,key,val):
        if self.root:
            self._put(key,val,self.root)
        else:
            self.root = TreeNode(key,val)
        self.size = self.size + 1

    def _put(self,key,val,currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                   self._put(key,val,currentNode.leftChild)
            else:
                   currentNode.leftChild = TreeNode(key,val,parent=currentNode)
        else:
            if currentNode.hasRightChild():
                   self._put(key,val,currentNode.rightChild)
            else:
                   currentNode.rightChild = TreeNode(key,val,parent=currentNode)

    def __setitem__(self,k,v):
       self.put(k,v)

    def get(self,key):
       if self.root:
           res = self._get(key,self.root)
           if res:
                  return res.payload
           else:
                  return None
       else:
           return None

    def _get(self,key,currentNode):
       if not currentNode:
           return None
       elif currentNode.key == key:
           return currentNode
       elif key < currentNode.key:
           return self._get(key,currentNode.leftChild)
       else:
           return self._get(key,currentNode.rightChild)

    def __getitem__(self,key):
       return self.get(key)

    def __contains__(self,key):
       if self._get(key,self.root):
           return True
       else:
           return False


class AvlTree(BinarySearchTree): # AvlTree given by course

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.leftChild)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.rightChild)

    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1

            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild

        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isRightChild():
                rotRoot.parent.rightChild = newRoot
            else:
               rotRoot.parent.leftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(rotRoot.balanceFactor, 0)

    def rebalance(self, node):
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                self.rotateLeft(node.leftChild)
                self.rotateRight(node)
            else:
                self.rotateRight(node)



# WRITE YOUR OWN TEST UNDER THIS IF YOU NEED
if __name__ == '__main__':

    stockLib = StockLibrary()
    testSymbol = 'GE'
    testName = 'General Electric Company'

    stockLib.loadData("stock_database.csv")

    HundoLib = []
    for i in range(100): # creates random 100 stock list
        HundoLib.append(stockLib.stockList[random.randint(0, stockLib.size - 1)].symbol)



    print("\n-------load dataset-------")
    # stockLib.loadData("stock_database.csv")
    print(stockLib.size)




    print("\n-------linear search-------")
    print(stockLib.linearSearch(testSymbol, "symbol"))
    print(stockLib.linearSearch(testName, "name"))


    print("\n-------quick sort-------")
    print(stockLib.isSorted)
    stockLib.quickSort()
    print(stockLib.isSorted)


    print("\n-------build BST-------")
    stockLib.buildBST()
    print("Time to build BST:", stockLib.buildBST())


    print("\n---------search BST---------")
    print(stockLib.searchBST(testSymbol))

    print("\n----- task 7 -----")
    print("Time to linear search 100 random stocks:", stockLib.randLinearSearch(HundoLib))

    print("\n----- task 8 -----")
    print("Time to BST search 100 random stocks:", stockLib.randSearchBST(HundoLib))

    print("\n----- task 9 -----")
    tbTree = stockLib.buildBST() # building BST

    tRandLinearSearch = stockLib.randLinearSearch(HundoLib) # time to do linear search
    tRandBSTSearch = stockLib.randSearchBST(HundoLib) # time to do BST search

    numSearch = (tbTree + (tRandBSTSearch/100))/ (tRandLinearSearch/100) # number of searches needed before runtime is more than BST method

    print("Number of linear searches necessary before overall runtime would be more than combined total of building and searching through BST:", numSearch)

    print("\n----- task 10 -----")
    longsname = stockLib.stockList[0] # create variable to store stock with longest name

    for stock in stockLib.stockList: # compares all the names within stockLibrary
        if len(stock.sname) > len(longsname.sname):
            longsname = stock

    listFloat = [] # create list to store floats

    for item in longsname.prices: # turns the prices of the stock from a string to a float
        listFloat.append(float(item))

    day = ['4', '5','6', '7', '8', '11', '12', '13', '14', '15', '19', '20', '21', '22', '25', '26', '27', '28',
         '29'] # create a list to store days of the prices
    x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

    plt.title("Prices of the Stock with Longest Name")
    plt.xticks(x, day)
    plt.xlabel("Month of January, 2021")
    plt.ylabel("Market Value (millions)")
    plt.plot(x, listFloat)

    plt.show()

    print("\n----- task 11 -----")

    largestInStock = stockLib.stockList[0] # variable to store stock with largest price increase
    largestDeStock = stockLib.stockList[0] # variable to store stock with largest price decrease

    largestIn = 0 # variable to store largest price increase
    largestDe = 0 # variable to store largest price decrease


    for stock in stockLib.stockList: # find largest price increase and decrease
        change = ((float(stock.prices[-1]) - float(stock.prices[0]))/float(stock.prices[0]))*100 # calculate price change in stock
        if change > largestIn: # compares current stock to previous stock with largest increase of price
            largestInStock = stock
            largestIn = change
        if change < largestDe: # compares current stock to previous stock with largest decrease of price
            largestDeStock = stock
            largestDe = change

    print("Largest Percent Increase and Stock\n" + str(largestIn) + "%\n" + str(largestInStock))

    print("\nLargest Percent Decrease and Stock\n" + str(largestDe) + "%\n" + str(largestDeStock))













