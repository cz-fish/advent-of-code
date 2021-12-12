DECLARE FUNCTION getSum (days AS INTEGER, ageCounters() AS INTEGER)

LET inputStr$ = "3,4,3,1,2"
LET days% = 80

DIM ageCounters(0 TO 8) AS INTEGER

PRINT "AoC 2021 day 6"

FOR i = 1 TO LEN(inputStr$) STEP 2
  LET c$ = MID$(inputStr$, i, 1)
  LET v = ASC(c$) - ASC("0")
  LET ageCounters(v) = ageCounters(v) + 1
NEXT i

FOR i = 1 TO days%
  LET day0 = (i + 8) MOD 9
  LET day6 = (i + 6) MOD 9
  ageCounters(day6) = ageCounters(day6) + ageCounters(day0)
  ' getSum(i, ageCounters())
NEXT i

LET sum = getSum(days%, ageCounters())









FUNCTION getSum (day AS INTEGER, ageCounters() AS INTEGER)
  LET p$ = "Day " + STR$(day) + ":"
  LET sum = 0
  FOR b = 0 TO 8
    p$ = p$ + " " + STR$(ageCounters(b))
    LET sum = sum + ageCounters(b)
  NEXT b
  p$ = p$ + " .. total " + STR$(sum)
  PRINT p$
  getSum = sum
END FUNCTION

