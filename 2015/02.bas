Dim Shared testCounter%
testCounter% = 0

' Part 1
Call runTest1(58, "2x3x4")
Call runTest1(43, "1x1x10")

Let totalFabric& = 0
Open "input02.txt" For Input As #1
Do Until EOF(1)
    Input #1, package$
    totalFabric& = totalFabric& + wrapOne(package$)
Loop
Close #1

Print "Day 2 Part 1: " + Str$(totalFabric&)

' Part 2
Call runTest2(34, "2x3x4")
Call runTest2(14, "1x1x10")

Let totalRibbon& = 0
Open "input02.txt" For Input As #1
Do Until EOF(1)
    Input #1, package$
    totalRibbon& = totalRibbon& + ribbonOne(package$)
Loop
Close #1

Print "Day 2 Part 2: " + Str$(totalRibbon&)

End

Function parseLine (inp$, d_ptr%, w_ptr%, h_ptr%, d_seg%)
    parseLine = 0
    x% = InStr(1, inp$, "x")
    If x% = 0 Then Exit Function
    d% = Val(Mid$(inp$, 1, x%))
    y% = InStr(x% + 1, inp$, "x")
    If y% = 0 Then Exit Function
    w% = Val(Mid$(inp$, x% + 1, y%))
    h% = Val(Mid$(inp$, y% + 1))
    ' we have the three dimensions %d, %w, %h
    ' sort from smallest to largest
    If d% > w% Then Swap d%, w%
    If w% > h% Then Swap w%, h%
    If d% > w% Then Swap d%, w%
    Def Seg = d_seg%
    ' This only copies one byte to each 2-byte variable
    ' but it is enough, given that the numbers in the input file are small.
    ' It also assumes that all 3 variables are in the same segment
    Poke d_ptr%, d%
    Poke w_ptr%, w%
    Poke h_ptr%, h%
    Def Seg
    parseLine = 1
End Function


Function wrapOne (inp$)
    wrapOne = 0
    d% = 0
    w% = 0
    h% = 0
    r = parseLine(inp$, VarPtr(d%), VarPtr(w%), VarPtr(h%), VarSeg(d%))
    If r = 0 Then Exit Function
    wrapOne = 3 * d% * w% + 2 * d% * h% + 2 * w% * h%
End Function


Sub runTest1 (expected%, inp$)
    Let res% = wrapOne(inp$)
    testCounter% = testCounter% + 1
    If res% = expected% Then
        Print "Test " + Str$(testCounter%) + " passed: " + Str$(res%)
    Else
        Print "Test " + Str$(testCounter%) + " failed: expected " + Str$(expected%) + " got " + Str$(res%)
    End If
End Sub


Function ribbonOne (inp$)
    ribbonOne = 0
    d% = 0
    w% = 0
    h% = 0
    r = parseLine(inp$, VarPtr(d%), VarPtr(w%), VarPtr(h%), VarSeg(d%))
    If r = 0 Then Exit Function
    ribbonOne = 2 * d% + 2 * w% + d% * w% * h%
End Function


Sub runTest2 (expected%, inp$)
    Let res% = ribbonOne(inp$)
    testCounter% = testCounter% + 1
    If res% = expected% Then
        Print "Test " + Str$(testCounter%) + " passed: " + Str$(res%)
    Else
        Print "Test " + Str$(testCounter%) + " failed: expected " + Str$(expected%) + " got " + Str$(res%)
    End If
End Sub
