Dim Shared testCounter%

testCounter% = 0

Call runTest1(0, "(())")
Call runTest1(0, "()()")
Call runTest1(3, "(((")
Call runTest1(3, "(()(()(")
Call runTest1(3, "))(((((")
Call runTest1(-1, "())")
Call runTest1(-1, "))(")
Call runTest1(-3, ")))")
Call runTest1(-3, ")())())")

' now the actual problem input
Open "input01.txt" For Input As #1
Input #1, problem$
Close 1

Let res = countFloors(problem$)
Print "Day 1 Part 1: " + Str$(res)

Call runTest2(1, ")")
Call runTest2(5, "()())")

res = findBasement(problem$)
Print "Day 1 Part 2: " + Str$(res)

End


Function countFloors (inp$)
    Let floor% = 0
    Let inputLen% = Len(inp$)
    For i% = 1 To inputLen%
        Let c = Asc(inp$, i%)
        Select Case c
            Case 40 '40 = (
                floor% = floor% + 1
            Case 41 '41 = )
                floor% = floor% - 1
        End Select
    Next i%

    countFloors = floor%
End Function

Function findBasement (inp$)
    Let floor% = 0
    Let inputLen% = Len(inp$)
    For i% = 1 To inputLen%
        Let c = Asc(inp$, i%)
        Select Case c
            Case 40 '40 = (
                floor% = floor% + 1
            Case 41 '41 = )
                floor% = floor% - 1
        End Select
        If floor% = -1 Then
            findBasement = i%
            Exit For
        End If
    Next i%
End Function

Sub runTest1 (expected%, inp$)
    Let res = countFloors(inp$)
    testCounter% = testCounter% + 1
    If res = expected% Then
        Print "Test " + Str$(testCounter%) + " passed: " + Str$(res)
    Else
        Print "Test " + Str$(testCounter%) + " failed: expected " + Str$(expected%) + ", got " + Str$(res)
    End If
End Sub

Sub runTest2 (expected%, inp$)
    Let res = findBasement(inp$)
    testCounter% = testCounter% + 1
    If res = expected% Then
        Print "Test " + Str$(testCounter%) + " passed: " + Str$(res)
    Else
        Print "Test " + Str$(testCounter%) + " failed: expected " + Str$(expected%) + ", got " + Str$(res)
    End If
End Sub

