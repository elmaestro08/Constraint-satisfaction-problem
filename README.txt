# Constraint-satisfaction-problem
Suppose you have a wedding to plan, and want to arrange the wedding seating for a certain
number of guests in a hall. The hall has a certain number of tables for seating. Some pairs of
guests are couples or close Friends (F) and want to sit together at the same table. Some other
pairs of guests are Enemies(E) and must be separated into different tables. The rest of the pairs
are Indifferent (I) to each other and do not mind sitting together or not. However, each pair of
guests can have only one relationship, (F), (E) or (I). This program finds a seating arrangement that
satisfies all the above constraints.

This programming assignment, generates CNF sentences for an input instance of wedding seating arrangements. 

The inputs include the number of guests <M>, the number of tables <N>, and a sparse representation of the
relationship matrix R with elements Rij = 1, -1 or 0 to represent whether guests i and j are
Friends (F), Enemies (E) or Indifferent (I). 

The code implements a SAT solver to find a satisfying assignment for any given CNF sentences. 

This code implements two methods to find the satisfiability and truth assignments:

I) Satisfiability is check by the PL-Resolution algorithm.
If satisfiable, then the assignment of the truth values is determined by the WalkSAT algorithm.

II) The code also implements DPLL algorithm which checks the satisfiability and generates the truth assignments.

Sample Input
4 2
1 2 F
2 3 E
The first line contains two integers denoting the number of guests <M> and the number of
tables <N> respectively. Each line following contains two integers representing the indices of a
pair of guests and one character indicating whether they are Friends(F) or Enemies(E). The rest
of the pairs are indifferent by default. For example, in the above sample input, there are 4
guests and 2 tables in total, and guest 1 and guest 2 are Friends, and guest 2 and guest 3 are
Enemies.
Sample Output
yes
1 2
2 2
3 1
4 1
