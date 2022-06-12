import searchStock as ss
import sortData as sd

class Base:
    def __init__(self):
        pass  
                
    def searchStock(self):
        symbol = input("\nSearch a Stock: ")
        while True:
            print('\n1) Stock Details\n2) Previous History\n3) Plot a Stock\n4) Exit\n')
            ans = input('Enter an Option: ')
            if ans == "1":
                print('\nStock Details\n')
                ss.searchStock(symbol)
            elif ans == "2":
                print('\nPrevious History')
                ss.dateSearch(symbol)
            elif ans == "3":
                print('\nPlot a Stock')
                ss.plotStock(symbol)
            elif ans == "4":
                return
            else:
                print('\nUnknown Command\n')

    def platform(self):
        print("Welcome to Murrano Trading System")
        while True:
            print("\n\n1) Portfolio \n2) Search Stock \n3) Pairs Algorithm\n4) Exit")
            ans = input("Enter an Option: ")
            if ans == "1":
                print("\n\nPortfolio\n")
            elif ans == "2":
                print("\n\nSearch a Stock")
                self.searchStock()
            elif ans == "3":
                print("\n\nPairs Algorithm\n")
                sd.loaderFunction()
                
            elif ans == "4":
                break
            else:
                print("Unknown Command\n")
        

base = Base()
base.platform()