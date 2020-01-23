namespace AoC2017
open System
open System.IO

module Day04 =
    let loadFile() =
        File.ReadLines("input04.txt")
            |> Seq.toList
            |> List.map (fun (ln: string)
                            -> ln.Split ' '
                                |> Array.toList
                        )

    let countGood passphrases =
        passphrases
            |> List.where (fun (pp:string list) -> Set.count (set pp) = pp.Length)
            |> List.length


    let day04 () =
        // part A
        let passphrases = loadFile()
        let validCount = countGood passphrases
        printfn "[04a] Number of valid passphrases: %d" validCount

        // part B
        let sortedPass = passphrases |> List.map (List.map (Seq.sort >> String.Concat))
        let validNonAnagram = countGood sortedPass
        printfn "[04b] Number of valid passphrases without anagrams: %d" validNonAnagram
        0

