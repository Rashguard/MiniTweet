import sys
########################################################################
#Methods

def openFriend(rbtree):
    i = 0
    friendshipNum = 0
    currUser = ""
    with open("friend.txt", "r", encoding="utf-8") as f:
        for line in f:
            i = i + 1
            text = line.strip()
            if i % 3 == 1:
                currUser = text
            elif i % 3 == 2:
                userNode = rbtree.search(currUser)
                if userNode is not rbtree.nil:
                    userNode.userData.append(text)
                friendshipNum = friendshipNum + 1
    return friendshipNum
                    

def openUser(rbtree):
    i = 0
    userNum = 0
    with open("user.txt", "r", encoding="utf-8") as f:
        for line in f:
            i = i + 1
            if i % 4 == 1:
                text = line.strip()
                rbtree.insert_key(text)
                userNum = userNum + 1
    return userNum
                
def openWord(rbtree):
    i = 0
    wordNum = 0
    currUser = ""
    with open("word.txt", "r", encoding="utf-8") as f:
        for line in f:
            i = i + 1
            
            #user
            if i % 4 == 1:
                text = line.strip()
                currUser = text
                
            #word
            elif i % 4 == 3:
                text = line.strip()
                rbtree.insert_key(text)
                wordNum = wordNum + 1
                
                textNode = rbtree.search(text)
                if textNode is not rbtree.nil:
                    textNode.frequency = textNode.frequency + 1
                    textNode.userData.append(currUser)
    return wordNum

def dataEmpty(userTree, wordTree):
    if userTree.root == userTree.nil or wordTree.root == wordTree.nil:
        return True
    else:
        return False

########################################################################
#Data structure

#RBNode
class rbnode(object):
    def __init__(self, key):
        self._key = key
        self._red = False
        self._left = None
        self._right = None
        self._p = None
        self.frequency = 0
        self.userData = []

    key = property(fget=lambda self: self._key)
    red = property(fget=lambda self: self._red)
    left = property(fget=lambda self: self._left)
    right = property(fget=lambda self: self._right)
    p = property(fget=lambda self: self._p)
    userDataLen = property(fget=lambda self: len(self.userData))

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)

#RBTree   
class rbtree(object):
    def __init__(self, create_node=rbnode):
        self._nil = create_node(key=None)
        self._root = self.nil
        self._create_node = create_node

    root = property(fget=lambda self: self._root)
    nil = property(fget=lambda self: self._nil)

    def search(self, key, x=None):
        if None == x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x


    def minimum(self, x=None):
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x


    def maximum(self, x=None):
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def insert_key(self, key):
        self.insert_node(self._create_node(key=key))

    def insert_node(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self._insert_fixup(z)
        
    def _insert_fixup(self, z):
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False

    def _transplant(self, u, v):
        if u.p == self.nil:
            self._root = v
        elif u == u.p.left:
            u.p._left = v
        else:
            u.p._right = v
        v._p = u.p

    def delete_node(self, z):
        y = z
        if y.red:
            y_original_red = True
        else:
            y_original_red = False
            
        if z.left == self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            if y.red:
                y_original_red = True
            else:
                y_original_red = False
            x = y.right
            if y.p == z:
                x._p = y
            else:
                self._transplant(y, y.right)
                y._right = z.right
                y.right._p = y
            self._transplant(z, y)
            y._left = z.left
            y.left._p = y
            if y.red:
                z._red = True
            else:
                z._red = False

        if y_original_red == False:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.red == False:
            if x == x.p.left:
                w = x.p.right
                if w.red:
                    w._red = False
                    w.p._red = True
                    self._left_rotate(x.p)
                    w = x.p.right
                if w.left.red == False and w.right.red == False:
                    w._red = True
                    x = x.p
                else:
                    if w.right.red == False:
                        w.left._red = False
                        w._red = True
                        self._right_rotate(w)
                        w = x.p.right
                    if x.p.red:
                        w._red = True
                    else:
                        w._red = False
                    x.p._red = False
                    w.right._red = False
                    self._left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.red:
                    w._red = False
                    w.p._red = True
                    self._right_rotate(x.p)
                    w = x.p.left
                if w.right.red == False and w.left.red == False:
                    w._red = True
                    x = x.p
                else:
                    if w.left.red == False:
                        w.right._red = False
                        w._red = True
                        self._left_rotate(w)
                        w = x.p.left
                    if x.p.red:
                        w._red = True
                    else:
                        w._red = False
                    x.p._red = False
                    w.left._red = False
                    self._right_rotate(x.p)
                    x = self.root
        x._red = False
                    

    def _left_rotate(self, x):
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y


    def _right_rotate(self, y):
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x


    def check_invariants(self): #need?
        
        def is_red_black_node(node):
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            if not node.left and not node.right and node.red:
                return 0, False

            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
                    return 0, False

            if node.left and node.right:

                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
                if not right_ok:
                    return 0, False

                if left_counts != right_counts:
                    return 0, False
                return left_counts, True
            else:
                return 0, True

        num_black, is_ok = is_red_black_node(self.root)
        return is_ok and not self.root._red

########################################################################
#Main
    
def main():
    userTree = rbtree()
    wordTree = rbtree()
    friendshipNum = 0
    userNum = 0
    wordNum = 0
    fAverage = 0
    fMax = 0
    fMin = 0
    tAverage = 0
    tMax = 0
    tMin = 0
    userResult = []
    while True:
        print("")
        print("xXxX[ Mini Tweet Analyzer 9000 ]XxXx")
        print("0. Read data files")
        print("1. display statistics")
        print("2. Top 5 most tweeted words")
        print("3. Top 5 most tweeted users")
        print("4. Find users who tweeted a word")
        print("5. Find all people who are friends with the above users")
        print("6. Delete all mentions of a word")
        print("7. Delete all users who mentioned a word")
        print("8. Find strongly connected users")
        print("9. Find shortest path from a given user")
        print("99. Quit")
        sel = input("Select Menu: ")
        
        if sel =="99":
            print("")
            print("Exiting...")
            sys.exit()
            
        elif sel == "0":
            print("")
            print("Reading data files...")
            userNum = openUser(userTree)
            wordNum = openWord(wordTree)
            friendshipNum = openFriend(userTree)
            print("===== R E S U L T S =====")
            print("Total users: ", end = "")
            print(userNum)
            print("Total friendship records: ", end = "")
            print(friendshipNum)
            print("Total tweets: ", end = "")
            print(wordNum)
        
        elif dataEmpty(userTree, wordTree):
            print("")
            print("No data available. Reading data files first...")
            userNum = openUser(userTree)
            wordNum = openWord(wordTree)
            friendshipNum = openFriend(userTree)
            print("===== R E S U L T S =====")
            print("Total users: ", end = "")
            print(userNum)
            print("Total friendship records: ", end = "")
            print(friendshipNum)
            print("Total tweets: ", end = "")
            print(wordNum)
    
        elif sel == "1":
            fAverage = friendshipNum / userNum
            tAverage = wordNum / userNum
            #fMin =
            #tMin = 
            #fMax =
            #tMax =
            print("")
            print("===== S T A T S =====")
            print("Average number of friends : ", end = "")
            print(fAverage)
            print("Minimum number of friends : ", end = "")
            print(fMin)
            print("Maximum number of friends : ", end = "")
            print(fMax)
            print("")
            print("Average tweets per user : ", end = "")
            print(tAverage)
            print("Minimum tweets per user : ", end = "")
            print(tMin)
            print("Maximum tweets per user : ", end = "")
            print(tMax)
            
        
        elif sel == "2":
            #tweet frequency tree?
            print("")
            print("Top 5 most tweeted words")
        
        elif sel == "3":
            #tweet num tree?
            userResult = []
            print("")
            print("Top 5 most tweeted users")

        elif sel == "4":
            userResult = []
            print("")
            print("Users who tweeted a word")
            print("")
            whatWord = input("Search a word: ")
            wordNode = wordTree.search(whatWord)
            if wordNode == wordTree.nil:
                print("")
                print("Wow. Such empty.")
            else:
                for item in wordNode.userData:
                    print("User ", end = "") #fix duplicates!
                    print(item)
                    userResult.append(item)
        
        elif sel == "5":
            print("")
            print("Find all people who are friends with the above users")
            print("")
            if userResult == []:
                print("No users found or selected. Try Choosing 3 or 4.")
            else:
                for item in userResult:
                    userNode = userTree.search(item)
                    print("")
                    print("Friends of ", end = "")
                    print(item)
                    if userNode != userTree.nil:
                        for friend in userNode.userData:
                            print("User ", end = "")
                            print(friend)
                    
        elif sel == "6":
            print("")
            print("Delete all mentions of a word")
            print("Current words : ", end = "")
            print(wordNum)
            print("")
            whatWord = input("Search a word: ")
            wordNode = wordTree.search(whatWord)
            wordTree.delete_node(wordNode)
            wordNum = wordNum - 1
            print("")
            print("Delete complete")
            print("Current words : ", end = "")
            print(wordNum)
        
        elif sel == "7":
            print("")
            print("Delete all users who mentioned a word")
            print("Current users : ", end = "")
            print(userNum)
            print("")
            whatWord = input("Search a word: ")
            wordNode = wordTree.search(whatWord)
            if wordNode != wordTree.nil:
                for user in wordNode.userData:
                    userNode = userTree.search(user)
                    if userNode != userTree.nil:
                        userTree.delete_node(userNode)
                        userNum = userNum - 1
            print("")
            print("Delete complete")
            print("Current users : ", end = "")
            print(userNum)
            
        elif sel == "8":
            print("")
            print("Find strongly connected users")
            print("")
            #find
            
        elif sel == "9":
            print("")
            print("Find shortest path from a given user")
            print("")
            whatuser = input("Choose a user: ")
            #find
            
########################################################################
            
main()
