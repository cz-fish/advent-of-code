Option _Explicit

Dim Shared QM As String
QM = Chr$(34)

Call testCountChars

Dim line$
Dim code%, actual%, spec%
Dim codeTotal&, actualTotal&, specTotal&

Open "input08.txt" For Input As #1
Do Until EOF(1)
    Line Input #1, line$
    Call countChars(line$, code%, actual%, spec%)
    codeTotal& = codeTotal& + code%
    actualTotal& = actualTotal& + actual%
    specTotal& = specTotal& + spec%
Loop
Close #1

Color 14
Print "Part 1: " + Str$(codeTotal& - actualTotal&)
Print "Part 2: " + Str$(specTotal& - codeTotal&)
Color 15

End

Sub countChars (text$, inCode%, inMemory%, spec%)
    inCode% = Len(text$)
    Dim i%, esc%
    i% = 1
    esc% = 0
    inMemory% = 0
    ' Special character count = Part 2. The count is the plain character count plus two extra
    ' characters for added quotes around the string plus 1 extra char for every " or \ (counted in the loop below)
    spec% = inCode% + 2
    While i% <= inCode%
        Select Case Asc(text$, i%)
            Case 34 ' "
                spec% = spec% + 1
                If esc% = 1 Then
                    ' the previous '\' has already been counted
                    esc% = 0
                Else
                    ' skip over the un-escaped "
                End If
            Case 92 ' \
                spec% = spec% + 1
                If esc% = 1 Then
                    ' the previous '\' has already been counted
                    esc% = 0
                Else
                    ' count the first '\'
                    inMemory% = inMemory% + 1
                    esc% = 1
                End If
            Case 120 'x
                If esc% = 1 Then
                    ' the previous '\' has already been counted
                    ' skip next 2 chars
                    i% = i% + 2
                    esc% = 0
                Else
                    ' just a regular 'x'
                    inMemory% = inMemory% + 1
                End If
            Case Else
                If esc% = 1 Then
                    ' valid escaped cases were handled above. It is invalid to escape any other character
                    Error 2
                End If
                inMemory% = inMemory% + 1
        End Select
        i% = i% + 1
    Wend
End Sub

' --- Test ---

Function testCountCharsOneWord (text$, expInCode%, expInMemory%, expSpec%)
    Dim actInCode%, actInMemory%, actSpec%
    Call countChars(text$, actInCode%, actInMemory%, actSpec%)
    If expInCode% <> actInCode% Or expInMemory% <> actInMemory% Or expSpec% <> actSpec% Then
        Color 12
        Print "testCountChars FAILED. text=" + text$ + " expected " + _
            str$(expInCode%) + "," + str$(expInMemory%) + "," + str$(expSpec%) + "; got " + _
            str$(actInCode%) + "," + str$(actInMemory%) + "," + str$(actSpec%)
        Color 15
        testCountCharsOneWord = 0
    Else
        testCountCharsOneWord = 1
    End If
End Function

Sub testCountChars ()
    Dim correct%
    correct% = 1
    correct% = correct% And testCountCharsOneWord(QM + QM, 2, 0, 6)
    correct% = correct% And testCountCharsOneWord(QM + "abc" + QM, 5, 3, 9)
    correct% = correct% And testCountCharsOneWord(QM + "aaa\" + QM + "aaa" + QM, 10, 7, 16)
    correct% = correct% And testCountCharsOneWord(QM + "\x27" + QM, 6, 1, 11)
    If correct% = 1 Then
        Color 10
        Print "testCountChars PASSED"
        Color 15
    End If
End Sub
