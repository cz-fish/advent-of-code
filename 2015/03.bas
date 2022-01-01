Option _Explicit
Dim Shared testCounter As Integer
testCounter = 0

Dim actual_inp$

Open "input03.txt" For Input As #1
Input #1, actual_inp$
Close #1

Dim ans1&, ans2&

' Part 1

Call runTest1(2, ">")
Call runTest1(4, "^>v<")
Call runTest1(2, "^v^v^v^v^v")

ans1& = moveUnique(actual_inp$, 1)
Print "Day 3 Part 1: " + Str$(ans1&)

' Part 2
Call runTest2(3, "^v")
Call runTest2(3, "^>v<")
Call runTest2(11, "^v^v^v^v^v")

ans2& = moveUnique(actual_inp$, 2)
Print "Day 3 Part 2: " + Str$(ans2&)

End


Function moveUnique (inp$, santas%)
    Const minmax% = 300
    Dim grid%(-minmax% To minmax%, -minmax% To minmax%)
    grid%(0, 0) = santas% ' mark the starting position
    Dim x%(1 To santas%)
    Dim y%(1 To santas%)
    Dim currentSanta
    currentSanta = 1
    Dim unique&, l%, i%, c, nx%, ny%

    For i% = 1 To santas%
        x%(i%) = 0
        y%(i%) = 0
    Next i%

    unique& = 1 ' count the starting position
    l% = Len(inp$)
    For i% = 1 To l%
        c = Asc(inp$, i%)
        nx% = x%(currentSanta)
        ny% = y%(currentSanta)
        Select Case c
            Case 60: ' <
                nx% = x%(currentSanta) - 1
            Case 62: ' >
                nx% = x%(currentSanta) + 1
            Case 94: ' ^
                ny% = y%(currentSanta) - 1
            Case 118: ' v
                ny% = y%(currentSanta) + 1
            Case Else:
                Error 1
        End Select
        If nx% < -minmax% Or nx% > minmax% Or ny% < -minmax% Or ny% > minmax% Then
            Print "Out of bounds! " + Str$(nx%) + ", " + Str$(ny%)
            Error 2
        End If
        If grid%(nx%, ny%) = 0 Then
            unique& = unique& + 1
        End If
        grid%(nx%, ny%) = grid%(nx%, ny%) + 1
        x%(currentSanta) = nx%
        y%(currentSanta) = ny%
        currentSanta = currentSanta Mod santas% + 1
    Next i%
    moveUnique = unique&
End Function

Sub runTest1 (expected&, inp$)
    testCounter = testCounter + 1
    Dim actual&, res$
    actual& = moveUnique(inp$, 1)
    res$ = "Test " + Str$(testCounter) + ": "
    If actual& = expected& Then
        res$ = res$ + "passed. result " + Str$(actual&)
    Else
        res$ = res$ + "failed. Expected " + Str$(expected&) + ", got " + Str$(actual&)
    End If
    Print res$
End Sub

Sub runTest2 (expected&, inp$)
    testCounter = testCounter + 1
    Dim actual&, res$
    actual& = moveUnique(inp$, 2)
    res$ = "Test " + Str$(testCounter) + ": "
    If actual& = expected& Then
        res$ = res$ + "passed. result " + Str$(actual&)
    Else
        res$ = res$ + "failed. Expected " + Str$(expected&) + ", got " + Str$(actual&)
    End If
    Print res$
End Sub

