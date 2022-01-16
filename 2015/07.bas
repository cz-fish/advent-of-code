Option _Explicit

Const OP_VALUE = 0
Const OP_NOT = 1
Const OP_AND = 2
Const OP_OR = 3
Const OP_LSL = 4
Const OP_LSR = 5

Const VAL_NUL = 0
Const VAL_IMMEDIATE = 1
Const VAL_WIRE = 2

Const MAX_WIRES = 27 * 26

Type WireType
    outputWire As Integer ' output of the wire (1 or 2 chars encoded integer)
    value As _Unsigned Integer ' output value - 16 bit number
    hasValue As Integer ' if 0, wire doesn't have value yet, 'value' field is undefined
    opType As Integer ' operation type, one of the OP_* constants
    i1type As Integer ' input 1 type, one of the VAL_* constants
    i1value As _Unsigned Integer ' input 1 value, unused if VAL_NUL, immediate integer value if VAL_IMMEDIATE, wire number if VAL_WIRE
    i2type As Integer ' input 2 type, one of the VAL_* constants
    i2value As _Unsigned Integer ' input 2 value, unused if VAL_NUL, immediate integer value if VAL_IMMEDIATE, wire number if VAL_WIRE
End Type

Dim wires(1 To MAX_WIRES) As WireType, wire As WireType
Dim line$, counter%

Call testWireToNumber("a", 1)
Call testWireToNumber("z", 26)
Call testWireToNumber("aa", 27)
Call testWireToNumber("zz", 702)
Call testWireToNumber("gz", 208)
Call testWireToNumber("hd", 212)

Call testInputParsing

Call testWithExample

counter% = 0

Open "input07.txt" For Input As #1
Do Until EOF(1)
    Line Input #1, line$
    Call parseWire(line$, wire)
    wires(wire.outputWire) = wire
    counter% = counter% + 1
Loop
Close #1

Print Str$(counter%) + " wires loaded"

Dim wireA%
wireA% = wireToNumber("a")

Color 14
Print "Part 1 result: " + Str$(getWireValue(wires(), wireA%))
Color 15

' ---- Part 2 ----

' Save old value of wire 'a'
Dim oldValA~%
oldValA~% = wires(wireA%).value

' Reset all wire values
Dim i%
For i% = 1 To MAX_WIRES
    wires(i%).value = 0
    wires(i%).hasValue = 0
Next

' Override wire 'b' value to old 'a' value
Dim wireB%
wireB% = wireToNumber("b")
wires(wireB%).value = oldValA~%
wires(wireB%).hasValue = 1

' Evaluate 'a' again
Color 14
Print "Part 2 result: " + Str$(getWireValue(wires(), wireA%))
Color 15

End

Function wireToNumber (wire$)
    ' Assign numbers to wire names for primitive hashing. We assume that
    ' a wire name is either 1 or 2 lower case characters. Single-character
    ' names are a=1 through z=26. Then come two-letter names aa=27, ab=28, ...
    ' through zz=27*26=702.

    Dim res As Integer
    res = Asc(wire$, 1) - 96
    If Len(wire$) > 1 Then
        res = 26 * res + Asc(wire$, 2) - 96
    End If
    wireToNumber = res
End Function

Sub valueOrWire (token$, outType%, outVal~%)
    ' The given token is either an immediate value, or a wire name.
    ' We figure out which one it is and assign the outType% and outVal~%

    If Asc(token$, 1) >= 97 Then
        ' token$ starts with a letter, so it's a wire, not a value
        outType% = VAL_WIRE
        outVal~% = wireToNumber(token$)
    Else
        ' token$ is a value
        outType% = VAL_IMMEDIATE
        outVal~% = Val(token$)
    End If
End Sub

Sub parseWire (line$, wire As WireType)
    ' tokenize the line by splitting it by spaces. There are at most 5 tokens
    Dim toks$(0 To 4)
    Dim tstart%, tstop%, ntoks%
    tstart% = 0
    ntoks% = 0
    Do
        tstop% = InStr(tstart% + 1, line$, " ")
        If tstop% Then
            toks$(ntoks%) = Mid$(line$, tstart% + 1, tstop% - tstart% - 1)
            tstart% = tstop%
            ntoks% = ntoks% + 1
        End If
    Loop Until tstop% = 0
    toks$(ntoks%) = Mid$(line$, tstart% + 1)
    ntoks% = ntoks% + 1

    ' outputWire is always in the last token. And the wire doesn't have a value yet
    wire.outputWire = wireToNumber(toks$(ntoks% - 1))
    wire.hasValue = 0

    If ntoks% = 3 Then
        ' this has to be the OP_VALUE operation
        wire.opType = OP_VALUE
        wire.i2type = VAL_NUL
        wire.i2value = 0
        Call valueOrWire(toks$(0), wire.i1type, wire.i1value)
    ElseIf ntoks% = 4 Then
        ' this has to be the OP_NOT operation
        wire.opType = OP_NOT
        wire.i2type = VAL_NUL
        wire.i2value = 0
        Call valueOrWire(toks$(1), wire.i1type, wire.i1value)
    Else
        ' this is one of the binary operations
        Select Case toks$(1)
            Case "AND"
                wire.opType = OP_AND
            Case "OR"
                wire.opType = OP_OR
            Case "LSHIFT"
                wire.opType = OP_LSL
            Case "RSHIFT"
                wire.opType = OP_LSR
            Case Else
                Error 2
        End Select
        Call valueOrWire(toks$(0), wire.i1type, wire.i1value)
        Call valueOrWire(toks$(2), wire.i2type, wire.i2value)
    End If
End Sub

Function getWireValue (wires() As WireType, which%)
    If wires(which%).hasValue = 0 Then
        Call evaluate(wires(), which%)
    End If
    getWireValue = wires(which%).value
End Function

Function getOperandValue (wire As WireType, operandNr%, wires() As WireType)
    If operandNr% = 1 Then
        If wire.i1type = VAL_WIRE Then
            getOperandValue = getWireValue(wires(), wire.i1value)
        Else
            getOperandValue = wire.i1value
        End If
    Else
        If wire.i2type = VAL_WIRE Then
            getOperandValue = getWireValue(wires(), wire.i2value)
        Else
            getOperandValue = wire.i2value
        End If
    End If
End Function

Sub evaluate (wires() As WireType, which%)
    If wires(which%).hasValue Then
        ' already evaluated
        Exit Sub
    End If
    Dim op1~%, op2~%
    op1~% = getOperandValue(wires(which%), 1, wires())
    op2~% = getOperandValue(wires(which%), 2, wires())

    Select Case wires(which%).opType
        Case OP_VALUE
            wires(which%).value = op1~%
        Case OP_NOT
            wires(which%).value = Not op1~%
        Case OP_AND
            wires(which%).value = op1~% And op2~%
        Case OP_OR
            wires(which%).value = op1~% Or op2~%
        Case OP_LSL
            wires(which%).value = _SHL(op1~%, op2~%)
        Case OP_LSR
            wires(which%).value = _SHR(op1~%, op2~%)
    End Select
    wires(which%).hasValue = 1
End Sub

' ---- Tests and aux ----

Sub testWireToNumber (wire$, number%)
    Dim res%
    res% = wireToNumber(wire$)
    If res% <> number% Then
        Color 12
        Print "testWireToNumber FAIL. Wire '" + wire$ + "', expected " + Str$(number%) + ", got " + Str$(res%)
        Color 15
    End If
End Sub

Sub printWire (wire As WireType)
    print "Wire[ out=" + str$(wire.outputWire) + _
        + ", value=" + str$(wire.value) + " (valid=" + str$(wire.hasValue) + ")" _
        + ", op=" + str$(wire.opType) + _
        + ", inp1=" + str$(wire.i1value) + " (type=" + str$(wire.i1type) + ")" _
        + ", inp2=" + str$(wire.i2value) + " (type=" + str$(wire.i2type) + ")" _
        + "]"
End Sub

Sub compareParsedWire (line$, expected As WireType)
    Dim wire As WireType
    Call parseWire(line$, wire)

    If  wire.outputWire <> expected.outputWire Or _
        wire.hasValue <> expected.hasValue Or _
        wire.opType <> expected.opType Or _
        wire.i1type <> expected.i1type Or _
        wire.i2type <> expected.i2type Or _
        wire.i1value <> expected.i1value Or _
        wire.i2value <> expected.i2value Then
        Color 12
        Print "testInputParsing FAILED. Line='" + line$ + "'. Expected"
        Call printWire(expected)
        Print "Got"
        Call printWire(wire)
        Color 15
    Else
        Color 10
        Print "testInputPassing PASSED. Line='" + line$ + "'"
        Color 15
    End If
End Sub

Sub testInputParsing ()
    Dim line$
    Dim expected As WireType
    ' Test a binary operation
    line$ = "gz LSHIFT 15 -> hd"
    expected.outputWire = 212
    expected.value = 0
    expected.hasValue = 0
    expected.opType = OP_LSL
    expected.i1type = VAL_WIRE
    expected.i1value = 208
    expected.i2type = VAL_IMMEDIATE
    expected.i2value = 15
    Call compareParsedWire(line$, expected)

    ' Test NOT operation
    line$ = "NOT ff -> jq"
    expected.outputWire = 277
    expected.value = 0
    expected.hasValue = 0
    expected.opType = OP_NOT
    expected.i1type = VAL_WIRE
    expected.i1value = 162
    expected.i2type = VAL_NUL
    expected.i2value = 0
    Call compareParsedWire(line$, expected)

    ' Test value passing
    line$ = "42 -> ab"
    expected.outputWire = 28
    expected.value = 0
    expected.hasValue = 0
    expected.opType = OP_VALUE
    expected.i1type = VAL_IMMEDIATE
    expected.i1value = 42
    expected.i2type = VAL_NUL
    expected.i2value = 0
    Call compareParsedWire(line$, expected)
End Sub

Function checkWireValue (circuit() As WireType, wirenum%, expected~%)
    Dim res~%
    res~% = getWireValue(circuit(), wirenum%)
    If circuit(wirenum%).hasValue = 0 Or res~% <> expected~% Then
        Color 12
        print "testWithExample FAILURE, wire '" + CHR$(wirenum% + 96) + "': expected " + _
            str$(expected~%) + ", got " + _
            str$(res~%) + " (valid=" + str$(circuit(wirenum%).hasValue) + ")"
        Color 15
        checkWireValue = 0
    Else
        checkWireValue = 1
    End If
End Function

Sub testWithExample ()
    Dim testCircuit(1 To MAX_WIRES) As WireType, wire As WireType
    Call parseWire("123 -> x", wire)
    testCircuit(wire.outputWire) = wire
    Call parseWire("456 -> y", wire)
    testCircuit(wire.outputWire) = wire
    Call parseWire("x AND y -> d", wire)
    testCircuit(wire.outputWire) = wire
    Call parseWire("x OR y -> e", wire)
    testCircuit(wire.outputWire) = wire
    Call parseWire("x LSHIFT 2 -> f", wire)
    testCircuit(wire.outputWire) = wire
    Call parseWire("y RSHIFT 2 -> g", wire)
    testCircuit(wire.outputWire) = wire
    Call parseWire("NOT x -> h", wire)
    testCircuit(wire.outputWire) = wire
    Call parseWire("NOT y -> i", wire)
    testCircuit(wire.outputWire) = wire
    Dim correct%
    correct% = checkWireValue(testCircuit(), wireToNumber("d"), 72)
    correct% = correct% And checkWireValue(testCircuit(), wireToNumber("e"), 507)
    correct% = correct% And checkWireValue(testCircuit(), wireToNumber("f"), 492)
    correct% = correct% And checkWireValue(testCircuit(), wireToNumber("g"), 114)
    correct% = correct% And checkWireValue(testCircuit(), wireToNumber("h"), 65412)
    correct% = correct% And checkWireValue(testCircuit(), wireToNumber("i"), 65079)
    correct% = correct% And checkWireValue(testCircuit(), wireToNumber("x"), 123)
    correct% = correct% And checkWireValue(testCircuit(), wireToNumber("y"), 456)
    If correct% = 1 Then
        Color 10
        Print "testWithExample PASSED"
        Color 15
    End If
End Sub

