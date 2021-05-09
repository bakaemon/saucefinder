import os, requests, urllib.parse, argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Search all the available doujin on nhentai.net based on keywords.")
parser.add_argument("-p", "--page", help="Get search result by page")
parser.add_argument("-q", "--query", help="Provide search query, keywords. Must be in quote.")
args = parser.parse_args()
page = 1
if not args.page:
    page = 1
else:
    page = int(args.page)


def yn(prompt: str):
    negative = True
    res = ""
    while negative:
        res = input(prompt).lower()
        if res not in ["y", "n"]:
            print("That's not an option.Try again\n")
            negative = True
        else:
            negative = False
    return res == "y"


def saucefind(text: str, page=1):
    os.system("cls")
    data = requests.get(f"https://nhentai.net/search/?q={text}&sort=popular&page={str(page)}").text
    soup = BeautifulSoup(data, 'html.parser')
    names_html = soup.findAll('div', class_='caption')
    links_html = soup.findAll('a', class_='cover')
    results_html = soup.find('h1')
    names = [x.text for x in names_html]
    results = results_html.text
    links = [f'https://nhentai.net{x.get("href")}' for x in links_html]
    print("Found" + results)
    for i in range(len(names)):
        print(f"{i + 1}. {names[i]}\nLink:{links[i]}\n")
    run = True
    while run:
        print("\n1. Change page.\n2. Enjoy one in incognito.\n")
        choice = int(input("Option: "))
        if choice == 0:
            run = False
        elif choice == 1:
            page_num = int(input(f"Current page: {str(page)}\nChoose page: "))
            if page_num <= 0:
                run = True
            else:
                saucefind(text, page=page_num)
        elif choice == 2:
            i = int(input("Which one you want to read (Enter number)?"))
            if 0 < i <= len(links):
                isPositive = yn("Would you like to read it on incognito mode? (y/n)\n")
                if isPositive:
                    os.system(
                        'start shell:AppsFolder\Microsoft.MicrosoftEdge_8wekyb3d8bbwe!MicrosoftEdge -private ' +
                        links[i - 1]
                    )
                    run = False
                else:
                    print("Can't find the number.")
                    run = True
    print("Process ended.")


if __name__ == '__main__':
    saucefind(urllib.parse.quote_plus(args.query), page=page)
