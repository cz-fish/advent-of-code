namespace AoC2017
open System.IO

module Day06 =
    let loadFile () =
        File.ReadAllText("input06.txt").Split('\t')
            |> Array.map int

    let oneStep config =
        let maxBlock = config |> Array.max
        let maxIndex = config |> Array.findIndex (fun x -> x = maxBlock)
        let redist = config.[maxIndex]
        let each = (redist + config.Length - 1) / config.Length
        let additions' = [|
            for i in 1 .. config.Length -> if i * each <= redist then each else 0
        |]
        let additions = Array.zeroCreate config.Length
        Array.blit additions' (config.Length - maxIndex - 1) additions 0 (maxIndex + 1)
        Array.blit additions' 0 additions (maxIndex + 1) (config.Length - maxIndex - 1)
        config.[maxIndex] <- 0
        Array.map2 (+) config additions

    let key state = String.concat "," (Array.map string state)

    let rec partA' state encountered length =
        let nextState = oneStep state
        let nextStateStr = key nextState
        //printfn "%d %A" length nextState
        if Map.containsKey nextStateStr encountered then
            length, length - encountered.[nextStateStr]
        else
            partA' nextState (encountered.Add(nextStateStr, length)) (length + 1)

    let day06 () =
        let config = loadFile()
        let encountered = Map.ofList [key config, 0]
        let loopAfter, loopSize = partA' config encountered 1
        printfn "loop after %d, loop size %d" loopAfter loopSize
        0
