message:  como =        test_ficha_1a.ic
          o    = outpu\test_ficha_1a.o
          r    = runtp\test_ficha_1a.r
          mc   = mctal\test_ficha_1a.m
          me   = mesht\test_ficha_1a.me
          tasks 3

title: ficha_1 geometry
c Cell Cards
1  0 -2 3 -4         imp:n = 1 $ inner cylinder
2  1 -2.26 -5 1 -6 (2:4:-3) imp:n = 1 $ outer cylinder
3  0 -7 (5 : -1 : 6) imp:n = 1 $ Cylinder to first shield
4  2 -7.784 7 -8     imp:n = 1 $ 1st shield
5  2 -7.784 8 -9     imp:n = 1 $ 2nd shield
6  2 -7.784 9 -10    imp:n = 1 $ 3rd shield
7  2 -7.784 10 -11   imp:n = 1 $ 4th shield
8  2 -7.784 11 -12   imp:n = 1 $ 5th shield
20  3 -1 -13         imp:n = 1 $ water sphere
100 0 12 13 -14      imp:n = 1 $ outside sphere
c Graveyard
200 0 14             imp:n = 0

c Surface Cards
c Source cylinders
1 PZ -3.2
2 CZ 0.5
3 PZ -3
4 PZ 3
5 CZ 0.7
6 PZ 3.2
c Shielding spheres
7  SO 5
8  SO 6
9  SO 7
10 SO 8
12 SO 10
11 SO 9
c Water sphere
13 SZ 11 1
c outside sphere
14 SO 13

c Data Cards
M1   6000 1         $ Carbon / Graphite
M2   26000 1        $ Shielding
M3   1001 0.667
     8016 0.333  $ Water
sdef pos = 0 0 0 erg = 14.1 par= n rad = d1 axs = 0 0 1 ext = d2
si1 0 0.5
sp1 -21 1
si2 -3 3
sp2 -21 0
c sdef pos= 0 0 0 erg=14.1 $ point source
mode n
NPS 1e5
F1:n 7
F2:n 7
F4:n 4
c
F11:n 8
F12:n 8
F14:n 5
c
F21:n 9
F22:n 9
F24:n 6
c
F31:n 10
F32:n 10
F34:n 7
c
F41:n 11
F42:n 11
F44:n 8
c
F51:n 12
F52:n 12
c water sphere tallies
c F62:n 13
c F72:n -13
c F64:n 20
prdmp 2j 1
print