# Minimax Game Fruit Rage
An AI agent designed to play a candy-crsuh-stlye game against an opponent.
The agent uses minimax algorithm with alpha beta pruning for lookahead and smart decision making leading to optimal game play.

The game board is represented as a series of numbers in an nxn grid.

0's represent empty spaces, all other digits are fruit.

If a number is selected, all the contiguous neighbors of the same number will be "popped" and replaced with 0's as empty spaces, then gravity will be applied so that all empty spaces are either occupied, or gave no fruit above them at any level.


Input: The	file	input.txt in	the	current	directory	of	your	program	will	be	formatted	as	follows:

First	line:	 integer	n,	the	width	and	height	of	the	square	board (0	<	n	£ 26)

Second	line:	 integer p,	the	number	of	fruit	types	(0	<	p	£ 9)

Third line:	 strictly	positive	floating	point	number,	your	remaining	time	in	seconds

Next	n	lines:	 the	n	x	n	board,	with	one	board	row	per	input	file	line,	and	n	characters	(plus	endof-line marker)	on	each	line.	

Each	character	can	be	either	a	digit	from	0	to	p-1,	or	 a	*	to	denote	an	empty	cell. Note:	for	ease	of	parsing,	the	extra	horizontal	and	 vertical	lines	shown	in	figures	1	– 5	will	not	be	present	in	the	actual	input.txt	(see	 below	for	examples).

Output:	The	file	output.txt which	your	program	creates	in	the	current	directory	should be	 formatted	as	follows:
First	line:	 your	selected	move,	represented	as	two	characters:	

A	letter from	A	 to	Z	 representing	 the	column	number	 (where	A	is	 the	leftmost	 column,	B	is	the	next	one	to	the	right,	etc),	and

A	number from	1	to	26	representing	the	row	number	(where	1	is	the	top	row,	2	is the	row	below	it,	etc).

Next	n	lines:	 the	n	x	n	board	just	after	your	move	and	after	gravity	has	been	applied	to	make any	 fruits	 fall	into	 holes	 created	 by	your	move	 taking	away	 some	 fruits (like	in	
figure	3).
