Chess2
======
A python implementation of David Sirlin's Chess 2: The Sequel.

Original source code written by [John Eriksson](www.arainyday.se).

Fork and additions written by Noah Bogart, 2013+.

Running
=======
To run: clone, cd into Chess2, "python ChessText.py".

Input
=====
* Input moves with: e4, e2e4, e2-e4, Ke2, etc.

* Whirlwind with: ww, whirlwind

* Skip Two Kings second turn with: decline, skip, s

* Initiate or decline duels with: yes, y, no, no

* Bluffing gain or loss with: gain, g, lose, l

* List moves so far with: an, san, lan

* Print out FEN with: fen

Issues
======
* Elephants can't check through units.

* ~~Pawns can't choose what they promote to, they just promote to a Queen of their army type (which sucks for Empowered and creates a third Warrior King.)~~

* Move tracking is out of whack with the addition of duels and stones.

* ~~Listing moves doesn't correctly note Two Kings second moves.~~
