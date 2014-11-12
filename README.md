Chess2
======
A python implementation of David Sirlin's Chess 2: The Sequel.

Original source code written by [John Eriksson](www.arainyday.se).

Fork and additions written by Noah Bogart, 2013+.

Running
=======
To run: clone, cd into Chess2, "python ChessText.py".

To run sunfish, cd into Chess2, "python sunfish.py".

Input for Chess2
=====
* Input moves with: e4, e2e4, e2-e4, Ke2, etc.

* Whirlwind with: ww, whirlwind

* Skip Two Kings second turn with: decline, skip, s

* Initiate or decline duels with: yes, y, no, no

* Bluffing gain or loss with: gain, g, lose, l

* List moves so far with: an, san, lan

* Print out FEN with: fen

Input for sunfish
=================
* Input moves in longform: e2e4

* Whirlwind by moving to the same location: e2e2

* Exit with: exit

Issues
======
* Sunfish: can move into check.