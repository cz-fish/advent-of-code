public static class Aoc2022
{
    public static void Main(string[] args)
    {
        var inputText = File.ReadAllText("input16.txt");
        var day16 = new Day16(inputText);
        Console.WriteLine($"Day 16: part1 = {day16.part1()}, part2 = {day16.part2()}");
        // expected part 1: 1944
        // expected part 2: 2679
    }
}