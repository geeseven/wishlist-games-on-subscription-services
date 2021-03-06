#!/usr/bin/env python
import json
from argparse import ArgumentParser
from re import findall

from bs4 import BeautifulSoup
from requests import get

description = (
    "Check a public GOG, Humble Store, or Steam wishlist for games on "
    "Apple Arcade, "
    "EA Play, "
    "Stadia, "
    "Ubisoft+, and "
    "Xbox Game Pass."
)
epilog = (
    "This script has some limitations, see "
    "https://github.com/geeseven/wishlist-games-on-subscription-services/tree/main#limitations"  # noqa: E501
)
parser = ArgumentParser(description=description, epilog=epilog)
parser.add_argument("url", help="public GOG, Humble Store, or Steam wishlist url")
args = parser.parse_args()


def get_gog_wishlist(url):
    # GOG only provides json wishlist data by a gog-user ID
    # It is listed on a user's wishlist page, so we need to scrape it first.
    r = get(url, allow_redirects=False, timeout=(3.05, 27))
    goguser = findall(r'gog-user="([0-9]*)"', r.text)
    if r.ok is False:
        print("Could not load GOG wishlist.  Either bad URL or wishlist is not public.")
        exit(1)
    page = 1
    games = []
    while True:
        url_page = "https://embed.gog.com/public_wishlist/{}/search".format(goguser[0])
        params = {"page": page}
        r = get(url_page, params=params, allow_redirects=False, timeout=(3.05, 27))
        if r.json()["totalProducts"] == 0:
            print("GOG wishlist is empty.")
            exit()
        for item in r.json()["products"]:
            games.append((item["title"], str(item["id"])))
        if r.json()["totalPages"] == page:
            break
        else:
            page += page
    return games


def get_humble_wishlist(url):
    # no paganation, but a limit of 100 items
    r = get(url, allow_redirects=False, timeout=(3.05, 27))
    if r.ok is False:
        print(
            "Could not load Humble Store wishlist. Either bad URL or wishlist is not public."  # noqa: E501
        )
        exit(1)
    soup = BeautifulSoup(r.text, features="html.parser")
    script = soup.find("script", id="storefront-webpack-json-data")
    j = json.loads(script.contents[0])
    if len(j["products_json"]) == 0:
        print("Humble Store wishlist is empty.")
        exit()
    games = [item["human_name"] for item in j["products_json"]]
    return games


def get_steam_wishlist(url):
    # There are two different wish list URLs for steam
    # wishlist url
    # https://store.steampowered.com/wishlist/profiles/76561197974046543#sort=order
    # api call for wishlist
    # https://store.steampowered.com/wishlist/profiles/76561197974046543/wishlistdata/
    #
    # wishlist url
    # https://store.steampowered.com/wishlist/id/ezekiel_iii#sort=order
    # api call for wishlist
    # https://store.steampowered.com/wishlist/id/ezekiel_iii/wishlistdata/
    if "#sort=order" in url:
        url = url.replace("#sort=order", "/wishlistdata/")
    else:
        url = url + "/wishlistdata/"
    games = []
    page = 0
    while True:
        params = {"p": page}
        r = get(url, params=params, allow_redirects=False, timeout=(3.05, 27))
        # bad user/id will return {"success":2}
        # valid user with empty wishlist will return []
        # valid user with games in wishlist will return a dict of dict
        try:
            r.json()["success"]
        except (KeyError, TypeError):
            pass
        else:
            print(
                "Could not load Steam wishlist.  Either bad URL or wishlist is not public."  # noqa: E501
            )
            exit(1)

        if len(r.json()) == 0 and page == 0:
            print("Steam wishlist is empty.")
            exit()
        elif len(r.json()) == 0:
            return games
        else:
            for item in r.json():
                games.append((r.json()[item]["name"], item))

        page += 1


def get_pcgamingwiki(condition):
    games = []
    if "gog.com" in args.url:
        printouts = "GOGcom ID"
    else:
        printouts = "Steam_AppID"
    url = "https://www.pcgamingwiki.com/w/api.php"
    params = {
        "action": "askargs",
        "conditions": condition,
        "format": "json",
        "printouts": printouts,
    }
    r = get(url, params=params, allow_redirects=False, timeout=(3.05, 27))
    while True:
        for item in list(r.json()["query"]["results"].keys()):
            for id in r.json()["query"]["results"][item]["printouts"][printouts]:
                games.append((item, str(id)))
        try:
            r.json()["query-continue-offset"]
        except KeyError:
            break
        else:
            offset = str(r.json()["query-continue-offset"])
            params["parameters"] = "offset={}".format(offset)
            r = get(url, params=params, allow_redirects=False, timeout=(3.05, 27))
    return games


def get_stadia_list():
    # url = "https://stadiagamedb.com/data/gamedb.json"
    url = "https://raw.githubusercontent.com/nilicule/StadiaGameDB/master/data/gamedb.json"  # noqa: E501
    r = get(url, allow_redirects=False, timeout=(3.05, 27))
    games = [game[1] for game in r.json()["data"]]
    return games


def get_apple_arcade_list():
    games = []
    url = "https://en.wikipedia.org/wiki/List_of_Apple_Arcade_games"
    r = get(url, allow_redirects=False, timeout=(3.05, 27))
    soup = BeautifulSoup(r.text, features="html.parser")
    th = soup.find_all("th", scope="row")
    for item in th:
        try:
            item.find("i").text
        except AttributeError:
            pass
        else:
            games.append(item.find("i").text)
    return games


def output(wish_game_list, platform_game_list, platform_name):
    if "gog.com" in args.url:
        wish_list = "GOG"
    elif "humblebundle.com" in args.url:
        wish_list = "Humble Store"
    elif "store.steampowered.com" in args.url:
        wish_list = "Steam"

    # Steam, GOG and PCGamingWiki are lists of tuples like ('game name', game-id)
    # Humble, Apple and Stadia are just a list of game names
    # compare by game-id if available, fall back to matching game names

    # Humble and PCGamingWiki
    if type(wish_game_list[0]) is not tuple and type(platform_game_list[0]) is tuple:
        # platform_game_list = list_tuple_convertion(platform_game_list)
        platform_game_list = [item[0] for item in platform_game_list]
        g = list(set(wish_game_list) & set(platform_game_list))

    # Steam or GOG and Apple or Stadia
    elif type(platform_game_list[0]) is not tuple and type(wish_game_list[0]) is tuple:
        wish_game_list = [item[0] for item in wish_game_list]
        g = list(set(wish_game_list) & set(platform_game_list))

    # Humble and Apple or Stadia
    elif (
        type(wish_game_list[0]) is not tuple
        and type(platform_game_list[0]) is not tuple
    ):
        g = list(set(wish_game_list) & set(platform_game_list))

    # Steam or GOG and PCGamingWiki
    else:
        g = []
        for game in wish_game_list:
            if [tup for tup in platform_game_list if tup[1] == game[1]]:
                g.append(game[0])

    if len(g) == 0:
        print("\nNo games in {} wishlist are on {}.".format(wish_list, platform_name))
    else:
        print("\n{} wishlist games on {}:".format(wish_list, platform_name))
        g.sort()
        print(*g, sep="\n")


print("processing, this will take a few seconds")

if "gog.com" in args.url:
    game_list = get_gog_wishlist(args.url)
elif "humblebundle.com" in args.url:
    game_list = get_humble_wishlist(args.url)
elif "store.steampowered.com" in args.url:
    game_list = get_steam_wishlist(args.url)
else:
    print("bad url")
    exit()

apple_list = get_apple_arcade_list()
output(game_list, apple_list, "Apple Arcade")

ea_list = get_pcgamingwiki("EA Play (Steam)::true")
output(game_list, ea_list, "EA Play(Steam)")

ea_list = get_pcgamingwiki("EA Play::true")
output(game_list, ea_list, "EA Play")

ea_list = get_pcgamingwiki("EA Play Pro::true")
output(game_list, ea_list, "EA Play Pro")

stadia_list = get_stadia_list()
output(game_list, stadia_list, "Stadia")

ubisoft_list = get_pcgamingwiki("Ubisoft Plus::true")
output(game_list, ubisoft_list, "Ubisoft+")

game_pass_list = get_pcgamingwiki("Xbox Game Pass for PC::true")
output(game_list, game_pass_list, "Xbox Game Pass for PC(Windows 10)")

game_pass_list = get_pcgamingwiki(
    "Xbox Game Pass for PC::true|Xbox Play Anywhere::true"
)
output(
    game_list,
    game_pass_list,
    "Xbox Game Pass for PC(Windows 10) and are Xbox Play Anywhere games",
)
