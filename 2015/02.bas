Dim Shared testCounter%
testCounter% = 0

Call runTest1(58, "2x3x4")
Call runTest1(43, "1x1x10")

' Part 1
Let totalFabric& = 0
Open "input02.txt" For Input As #1
Do Until EOF(1)
    Input #1, package$
    totalFabric& = totalFabric& + wrapOne(package$)
Loop
Close #1

Print "Day 2 Part 1: " + Str$(totalFabric&)



End


Function wrapOne (inp$)
    wrapOne = 0
    x% = InStr(1, inp$, "x")
    If x% = 0 Then Return
    d% = Val(Mid$(inp$, 1, x%))
    y% = InStr(x% + 1, inp$, "x")
    If y% = 0 Then Return
    w% = Val(Mid$(inp$, x% + 1, y%))
    h% = Val(Mid$(inp$, y% + 1))
    ' we have the three dimensions %d, %w, %h
    ' sort from smallest to largest
    If d% > w% Then Swap d%, w%
    If w% > h% Then Swap w%, h%
    If d% > w% Then Swap d%, w%
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
End Function

