Option _Explicit

Const NAUGHTY = 0
Const NICE = 1

Dim Shared testCounter%
testCounter% = 0

Call runTest1(NICE, "ugknbfddgicrmopn")
Call runTest1(NICE, "aaa")
Call runTest1(NAUGHTY, "jchzalrnumimnmhp")
Call runTest1(NAUGHTY, "haegwjzuvuyypxyu")
Call runTest1(NAUGHTY, "dvszwmarrgswjxmb")

Dim niceCount%, word$
niceCount% = 0
Open "input05.txt" For Input As #1
Do Until EOF(1)
    Input #1, word$
    If isWordNice(word$) = NICE Then
        niceCount% = niceCount% + 1
    End If
Loop
Close #1

Print "Day 5 Part 1: " + Str$(niceCount%)


End

Function isWordNice (word$)
    Dim le%, i%, vowelCount%, curr, prev, hasDouble
    prev = -1
    vowelCount% = 0
    hasDouble = 0
    le% = Len(word$)
    For i% = 1 To le%
        curr = Asc(word$, i%)
        If curr = prev Then
            hasDouble = 1
        End If
        If curr = 97 Or curr = 101 Or curr = 105 Or curr = 111 Or curr = 117 Then
            ' a vowel
            vowelCount% = vowelCount% + 1
        End If
        If (prev = 97 And curr = 98) Or (prev = 99 And curr = 100) Or (prev = 112 And curr = 113) Or (prev = 120 And curr = 121) Then
            ' one of the banned bi-graphs
            isWordNice = NAUGHTY
            Exit Function
        End If
        prev = curr
    Next i%
    If vowelCount% >= 3 And hasDouble = 1 Then
        isWordNice = NICE
    Else
        isWordNice = NAUGHTY
    End If
End Function

Function niceOrNaughty$ (which)
    If which = NAUGHTY Then
        niceOrNaughty$ = "naughty"
    Else
        niceOrNaughty$ = "nice"
    End If
End Function

Sub runTest1 (expected%, inp$)
    testCounter% = testCounter% + 1
    Dim result, p$
    result = isWordNice(inp$)
    p$ = "Test " + Str$(testCounter%) + ": '" + inp$ + "'"
    If result = expected% Then
        p$ = p$ + " passed as " + niceOrNaughty$(result)
    Else
        p$ = p$ + " FAILED. Expected " + niceOrNaughty$(expected%) + ", got " + niceOrNaughty$(result)
    End If
    Print p$
End Sub

