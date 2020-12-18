# wishlist-games-on-subscription-services

Check a public Steam or GOG wishlist for games on Apple Arcade, EA Play, Stadia, Ubisoft+, and Xbox Game Pass.

## Usage

```console
$ ./wishlist-games-on-subscription-services.py --help
usage: wishlist-games-on-subscription-services.py [-h] url

Check a public Steam or GOG wishlist for games on Apple Arcade, EA Play, Stadia, Ubisoft+, and Xbox Game Pass.

positional arguments:
  url         public Steam or GOG wishlist url

optional arguments:
  -h, --help  show this help message and exit

This script has some limitations, see https://github.com/geeseven/wishlist-games-on-subscription-services/tree/main#limitations

```

## Examples 

These are completely random wishlists.

```console
$ ./wishlist-games-on-subscription-services.py https://www.gog.com/u/J%20Lo/wishlist
processing, this will take a few seconds

No games in GOG wishlist are on Apple Arcade.

No games in GOG wishlist are on EA Play(Steam).

GOG wishlist games on EA Play:
Dead Cells
For The King
Mutant Year Zero: Road to Eden

GOG wishlist games on EA Play Pro:
Farmer's Dynasty
Sparklite
Sudden Strike 4
Sudden Strike 4: Complete Collection
Warhammer 40,000: Mechanicus

GOG wishlist games on Stadia:
Monster Boy and the Cursed Kingdom
SpongeBob SquarePants: Battle for Bikini Bottom - Rehydrated

No games in GOG wishlist are on Ubisoft+.

GOG wishlist games on Xbox Game Pass for PC(Windows 10):
Blair Witch
Children of Morta
Dead Cells
For The King
GreedFall
Hypnospace Outlaw
Ikenfell
Mutant Year Zero: Road to Eden
My Friend Pedro
Sea Salt
The Dark Crystal: Age of Resistance Tactics
The Messenger
Wasteland 3
Wasteland Remastered


$ ./wishlist-games-on-subscription-services.py https://store.steampowered.com/wishlist/profiles/76561197974046543#sort=order
processing, this will take a few seconds

Steam wishlist games on Apple Arcade:
Hot Lava
Manifold Garden
Pilgrims

Steam wishlist games on EA Play(Steam):
Need for Speed™
Need for Speed™ Heat
Need for Speed™ Rivals

Steam wishlist games on EA Play:
Need for Speed™
Need for Speed™ Heat
Need for Speed™ Rivals

Steam wishlist games on EA Play Pro:
A Plague Tale: Innocence

Steam wishlist games on Stadia:
Celeste
Cyberpunk 2077
Metro 2033 Redux
Metro Exodus
Red Dead Redemption 2
SteamWorld Dig 2

Steam wishlist games on Ubisoft+:
Beyond Good and Evil™
Far Cry 3
Far Cry® 4
Far Cry® 5
Far Cry® New Dawn
Far Cry® Primal
The Crew™
The Crew™ 2

Steam wishlist games on Xbox Game Pass for PC(Windows 10):
A Plague Tale: Innocence
Among Us
CARRION
Celeste
Deep Rock Galactic
Descenders
Eastshade
Gears 5
Halo: The Master Chief Collection
Levelhead
Lonely Mountains: Downhill
Night in the Woods
No Man's Sky
The Dark Pictures Anthology: Man of Medan
Xeno Crisis
```


## Limitations

All subscription service information are pulled from crowd sourced websites, so false positives/negatives are possible.  Apple Arcade data comes from [wikipedia]. Stadia data comes from [StadiaGameDB].  All others come from [PCGamingWiki].  If you notice errors, please updated these sites.  Also mismatched versions of games might get missed, i.e. 'Control' vs 'Control Ultimate Edition'.



[wikipedia]: https://en.wikipedia.org/wiki/List_of_Apple_Arcade_games
[stadiagamedb]: https://stadiagamedb.com
[PCGamingWiki]: https://www.pcgamingwiki.com
