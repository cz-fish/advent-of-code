namespace AoC2017

open NUnit.Framework
open System.IO

module Day05 =
    let loadFile () =
        File.ReadLines("input05.txt")
            |> Seq.toList
            |> List.map int
            |> List.toArray

    let rec executeProgram (program: int[]) increment (instr: int) (count: int) =
        if (instr < 0 || instr >= Array.length program) then
            count
        else
            let move = program.[instr]
            program.[instr] <- increment move
            executeProgram program increment (instr + move) (count + 1)

    let incrementPartA move =
        move + 1

    let partA () =
        let program = loadFile()
        let result = executeProgram program incrementPartA 0 0
        printfn "exited after %d steps" result
        0

    [<Test>]
    let ``05a: sample program exits after 5 steps``() =
        Assert.AreEqual( 5, executeProgram [|0;3;0;1;-3|] incrementPartA 0 0 )
    
    // -- part B --

    let incrementPartB move =
        if move >= 3 then move - 1 else move + 1

    let partB () =
        let program = loadFile()
        let result = executeProgram program incrementPartB 0 0
        printfn "exited after %d steps" result
        0

    [<Test>]
    let ``05b: sample program exits after 10 steps``() =
        Assert.AreEqual( 10, executeProgram [|0;3;0;1;-3|] incrementPartB 0 0 )
