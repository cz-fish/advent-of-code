// Learn more about F# at http://fsharp.org

open System
open AoC2017

[<EntryPoint>]
let main argv =
    printfn "AoC 2017"
    
    let days = dict [
        ("01a", Day01.partA);
        ("01b", Day01.partB);
        ("02a", Day02.partA);
        ("02b", Day02.partB);
        ("03a", Day03.partA);
    ]

    let mutable dayFunction = fun() -> 1

    let found =
        if argv.Length = 0 then
            printfn "Required parameter - day"
            false
        else
            days.TryGetValue(argv.[0], &dayFunction)

    if found then
        dayFunction()
    else
        printfn "Available parameters: %A" days.Keys
        1

    (* printfn "Press enter to close"
       System.Console.ReadLine() |> ignore *)
       
