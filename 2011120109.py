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
                userNode = rbtree.search(currUser) #need to read user first
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


    def check_invariants(self):
        
        def is_red_black_node(node):
            # check has _left and _right or neither
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            # check leaves are black
            if not node.left and not node.right and node.red:
                return 0, False

            # if node is red, check children are black
            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
                    return 0, False

            # descend tree and check black counts are balanced
            if node.left and node.right:

                # check children's parents are correct
                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                # check children are ok
                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
                if not right_ok:
                    return 0, False

                # check children's counts are ok
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
    userResult = []
    while True:
        print("[[[ Hello World! ]]]")
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
            print("Exiting")
            
        elif sel == "0":
            print("Reading data files...")
            userNum = openUser(userTree)
            wordNum = openWord(wordTree)
            friendshipNum = openFriend(userTree)
            print("Total users: ", end = "")
            print(userNum)
            print("Total friendship records: ", end = "")
            print(friendshipNum)
            print("Total tweets: ", end = "")
            print(wordNum)
        
        elif dataEmpty(userTree, wordTree):
            print("No data available. Reading data files first...")
            userNum = openUser(userTree)
            wordNum = openWord(wordTree)
            friendshipNum = openFriend(userTree)
            print("Total users: ", end = "")
            print(userNum)
            print("Total friendship records: ", end = "")
            print(friendshipNum)
            print("Total tweets: ", end = "")
            print(wordNum)
            continue
    
        elif sel == "1":
            print("Statistics")
        
        elif sel == "2":
            print("Top 5 most tweeted words")
        
        elif sel == "3":
            print("Top 5 most tweeted users")

        elif sel == "4":
            print("Users who tweeted a word")
            whatword = input("Search a word: ")
        
        elif sel == "5":
            print("Find all people who are friends with the above users")
            if userResult == []:
                print("No users found or selected. Try Choosing 3 or 4.")
                continue
            else:
                print("")
            #find

        elif sel == "6":
            print("Delete all mentions of a word")
            whatword = input("Search a word: ")
            #delete
        
        elif sel == "7":
            print("Delete all users who mentioned a word")
            whatword = input("Search a word: ")
            #delete
            
        elif sel == "8":
            print("Find strongly connected users")
            #find
            
        elif sel == "9":
            print("Find shortest path from a given user")
            whatuser = input("Choose a user: ")
            #find
            
########################################################################
            
main()
