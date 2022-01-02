Option _Explicit

Const NAUGHTY = 0
Const NICE = 1

Dim Shared testCounter%
testCounter% = 0

' tests part 1
Call runTest(NICE, "ugknbfddgicrmopn", 1)
Call runTest(NICE, "aaa", 1)
Call runTest(NAUGHTY, "jchzalrnumimnmhp", 1)
Call runTest(NAUGHTY, "haegwjzuvuyypxyu", 1)
Call runTest(NAUGHTY, "dvszwmarrgswjxmb", 1)
' tests part 2
Call runTest(NICE, "qjhvhtzxzqqjkmpb", 2)
Call runTest(NICE, "xxyxx", 2)
Call runTest(NAUGHTY, "uurcxstgmygtbstg", 2)
Call runTest(NAUGHTY, "ieodomkazucvgmuy", 2)
Call runTest(NAUGHTY, "aaa", 2)
Call runTest(NICE, "aaaa", 2)

Dim niceCountPt1%, niceCountPt2%, word$
niceCountPt1% = 0
niceCountPt2% = 0
Open "input05.txt" For Input As #1
Do Until EOF(1)
    Input #1, word$
    If isWordNicePt1(word$) = NICE Then
        niceCountPt1% = niceCountPt1% + 1
    End If
    If isWordNicePt2(word$) = NICE Then
        niceCountPt2% = niceCountPt2% + 1
    End If
Loop
Close #1

Print "Day 5 Part 1: " + Str$(niceCountPt1%)
Print "Day 5 Part 2: " + Str$(niceCountPt2%)

End

Function isWordNicePt1 (word$)
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
            isWordNicePt1 = NAUGHTY
            Exit Function
        End If
        prev = curr
    Next i%
    If vowelCount% >= 3 And hasDouble = 1 Then
        isWordNicePt1 = NICE
    Else
        isWordNicePt1 = NAUGHTY
    End If
End Function

Function isWordNicePt2 (word$)
    Dim pair%(0 To 25, 0 To 25)
    Dim le%, i%, hasPair, hasPali, curr, prev, c
    le% = Len(word$)
    For i% = 2 To le%
        prev = Asc(word$, i% - 1) - 97
        curr = Asc(word$, i%) - 97
        c = pair%(prev, curr)
        If c = 0 Then
            pair%(prev, curr) = i%
        ElseIf c <> i% - 1 Then
            hasPair = 1
        End If
        If i% > 2 Then
            prev = Asc(word$, i% - 2) - 97
            If curr = prev Then
                hasPali = 1
            End If
        End If
    Next i%
    If hasPair = 1 And hasPali = 1 Then
        isWordNicePt2 = NICE
    Else
        isWordNicePt2 = NAUGHTY
    End If
End Function

Function niceOrNaughty$ (which)
    If which = NAUGHTY Then
        niceOrNaughty$ = "naughty"
    Else
        niceOrNaughty$ = "nice"
    End If
End Function

Sub runTest (expected%, inp$, part)
    testCounter% = testCounter% + 1
    Dim result, p$
    If part = 1 Then
        result = isWordNicePt1(inp$)
    Else
        result = isWordNicePt2(inp$)
    End If
    p$ = "Test " + Str$(testCounter%) + ": '" + inp$ + "'"
    If result = expected% Then
        p$ = p$ + " passed as " + niceOrNaughty$(result)
    Else
        p$ = p$ + " FAILED. Expected " + niceOrNaughty$(expected%) + ", got " + niceOrNaughty$(result)
    End If
    Print p$
End Sub

