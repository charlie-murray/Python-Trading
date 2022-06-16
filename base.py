import searchStock as ss
import sortData as sd
import pairAlgorithm as pa

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
                symbols = [symbol]
                while True:
                    again = input('\nWould you Like to compare with another stock? y/n: ')
                    if again == 'y':
                        new_stock = input('Enter Another Stock: ')
                        symbols.append(new_stock)
                    else:
                        try:
                            all_question = input('\nDo you want 1Y? y/n: ')
                            if all_question == 'y':
                                pa.run_graph(symbols, 'y')
                            else:
                                pa.run_graph(symbols, 'n')
                        except Exception as e:
                            print(e)
                        break
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
                pa.calculate_pairs('p_value.csv')
                
            elif ans == "4":
                break
            else:
                print("Unknown Command\n")
        

base = Base()
base.platform()