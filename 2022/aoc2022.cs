namespace AoC2022
{
    public static class Aoc2022
    {
        public static void Main(string[] args)
        {
            // RunDay16();
            RunDay19();
        }

        private static void RunDay16()
        {
            var inputText = File.ReadAllText("input16.txt");
            var day16 = new Day16(inputText);

            /*
                    Console.WriteLine("20 elephants:");
                    day16.solve(20, 26);

                    const int MaxElephants = 5;
                    for (int time = 30; time >= 18; time -= 4)
                    {
                        Console.WriteLine($"Total time {time}");
                        day16.solve(MaxElephants, time);
                    }
                    Console.WriteLine("----------------------");
            */

            Console.WriteLine($"Day 16: part1 = {day16.part1()}, part2 = {day16.part2()}");
            // expected part 1: 1944
            // expected part 2: 2679
        }

        private static void RunDay19()
        {
            var inputText = File.ReadAllText("input19.txt");
            var day19 = new Day19(inputText);

            Console.WriteLine($"part1: {day19.part1()}");
            Console.WriteLine($"part2: {day19.part2()}");

            //Console.WriteLine($"Day 19: part1 = {day19.part1()}, part2 = {day19.part2()}");
            // expected part 1: 1081
            // expected part 2: 2415
        }

    }
}