import os, requests, urllib.parse, argparse, webbrowser
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Search all the available doujin on nhentai.net based on keywords.")
parser.add_argument("-p", "--page", help="Get search result by page", default=1, type=int)
parser.add_argument("-q", "--query", help="Provide search query, keywords. Must be in quote.", required=True)
args = parser.parse_args()
page = args.page

def browser(url):
    os.system(
        'start shell:AppsFolder\Microsoft.MicrosoftEdge_8wekyb3d8bbwe!MicrosoftEdge -private ' +
        url
    )


def record(data: list):
    with open("saves.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(data))


def readCodes():
    with open("saves.txt", "r", encoding="utf-8") as f:
        return f.read().split("\n")


def isCodeEmpty():
    with open("saves.txt", "r", encoding="utf-8") as f:
        line = f.read(1)
        if not line:
            return True
        else:
            return False


def deleteCodes():
    with open("saves.txt", "w", encoding="utf-8") as f:
        f.truncate(0)
        f.close()

def yn(prompt: str):
    negative = True
    res = ""
    while negative:
        res = input(prompt).lower()
        if res not in ["y", "n"]:
            print("That's not an option. Try again\n")
            negative = True
        else:
            negative = False
    return res == "y"

""" clear the terminal on Windows or UNIX """
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def saucefind(text: str, page=1):
    clear() # clear terminal
    data = requests.get(f"https://nhentai.net/search/?q={text}&sort=popular&page={str(page)}").text
    soup = BeautifulSoup(data, 'html.parser')
    names_html = soup.findAll('div', class_='caption')
    links_html = soup.findAll('a', class_='cover')
    results_html = soup.find('h1')
    names = [x.text for x in names_html]
    results = results_html.text
    links = [x.get("href").split("/")[2] for x in links_html]
    run = True
    while run:
        clear() # clear terminal
        print("Found" + results+"|| Search results of \""+text+"\"")
        print("*=============================================*")
        for i in range(len(names)):
            print(f"{i + 1}. [{links[i]}]     {names[i]}\n")
        print("*=============================================*")
        print(f"Current page: {str(page)}\n")
        print("\n1. Change page.\n2. Enjoy one in incognito.\n3. Save one to bookmark\n4. Check bookmarks\n5. Clear "
              "bookmarks\n0. Exit")
        choice = int(input("Option: "))
        if choice == 0:
            run = False
        elif choice == 1:
            page_num = int(input(f"Choose page: "))
            if page_num <= 0:
                run = True
            else:
                saucefind(text, page=page_num)
        elif choice == 2:
            i = int(input("Which one you want to read (Enter number)?\n"))
            if 0 < i <= len(links):
                isPositive = yn("Are you sure to read it on incognito mode? (y/n)\n")
                if isPositive:
                    url = "https://nhentai.net/g/" + links[i - 1]
                    browser(url)
                    input("Press any keys to continue...")
                else:
                    print("Can't find the number.")
                    input("Press any keys to continue...")
                    run = True
        elif choice == 3:
            io = input("Enter a list of index number separated by whitespace: \n")
            indexes = io.split(" ")
            data = [f"{links[int(i)-1]}    {names[int(i)-1]}" for i in indexes]

            record(data)
        elif choice == 4:
            data = readCodes()
            code = []
            print("Saved in saves.txt:\n")
            if isCodeEmpty():
                print("There is no code in bookmark.\n")
                input("Press any keys to continue...")
            else:
                n = 1
                for x in data:
                    print(str(n)+". "+x, sep="\n")
                    code.append(x.split("    ")[0])
                    n += 1
                pr = yn("Would you like to read any?(y/n)\n")
                if pr:
                    i = int(input("Input the index to read: "))
                    if 0 < i-1 < len(code):
                        browser("https://nhentai.net/g/"+code[i-1])
                        input("Press any keys to continue...")
                    else:
                        print("Can't find index number.\n")
                        input("Press any keys to continue...")
        elif choice == 5:
            if yn("Are you sure to delete everything? (y/n)\n"):
                deleteCodes()
                print("Clear-up successfully.\n")
            input("Press any keys to continue...")
    print("Process ended.")


if __name__ == '__main__':
    if not page:
        page = 1
    saucefind(urllib.parse.quote_plus(args.query), page=page)
