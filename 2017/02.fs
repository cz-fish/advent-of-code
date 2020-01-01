namespace AoC2017

open System.IO

module Day02 =

    let loadFile() =
        File.ReadLines("input02.txt")
            |> Seq.toList
            |> List.map (fun (ln: string)
                            -> ln.Split '\t'
                                |> Array.toList
                                |> List.map int
                        )

    let partA() =
        let sheet = loadFile()
        let checksum = sheet |> List.sumBy (fun row -> (List.max row) - (List.min row))
        printfn "Spreadsheet checksum: %A" checksum
        0

    let findDivisionPair row =
        row |> List.sumBy (
            fun elem1 ->
                row |> List.sumBy (
                            fun elem2 ->
                                if elem1 <> elem2 && elem1 % elem2 = 0 then
                                    elem1 / elem2
                                else
                                    0))

    let partB() =
        let sheet = loadFile()
        let divisors = sheet |> List.sumBy findDivisionPair
        printfn "Sum of division pairs: %A" divisors
        0