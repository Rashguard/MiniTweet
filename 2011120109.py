def openWord():
    i = 0
    with open("word.txt", "r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            i = i + 1
            if (i+1) % 4 == 0:
                print(text)

def dataEmpty(userData, wordData):
    if userData == None or wordData == None:
        return True
    else:
        return False

def main():
    userData = None
    wordData = None
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
            #read
            print("Total users: ")
            print("Total friendship records: ")
            print("Total tweets: ")
        
        elif dataEmpty(userData, wordData):
            print("No data available. Reading data files first...")
            #read
            print("Total users: ")
            print("Total friendship records: ")
            print("Total tweets: ")
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
        
main()
