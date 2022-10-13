use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::Read;

#[derive(Clone, Debug, PartialEq)]
enum Thing {
    Generator(String),
    Microchip(String),
}

fn parse_line(text: &str) -> (u32, Vec<Thing>) {
    let mut floor = 0u32;
    let mut adjective: String = String::new();
    let mut things: Vec<Thing> = vec![];
    
    // remove punctuation
    let mut line = String::from(text);
    line.retain(|c| c != '.' && c != ',');

    for part in line.split(" ") {
        match part {
            // Floor numbers
            "first" => floor = 1,
            "second" => floor = 2,
            "third" => floor = 3,
            "fourth" => floor = 4,
            // Uninteresting sauce
            "The" | "floor" | "a" | "contains" | "nothing" | "relevant" | "and" => (),
            // Keywords
            "generator" => {
                assert!(!adjective.is_empty());
                things.push(Thing::Generator(adjective));
                adjective = String::new();
            },
            "microchip" => {
                assert!(!adjective.is_empty());
                // Remove the "-compatible" suffix
                // TODO: remove_matches - as of rustc 1.53.0, it's an experimental feature
                //adjective.remove_matches("-compatible");
                let suffix = adjective.find("-compatible").unwrap();
                adjective.truncate(suffix);
                things.push(Thing::Microchip(adjective));
                adjective = String::new();
            },
            // Adjectives
            &_ => adjective = part.to_string(),
        };
    }
    (floor, things)
}

fn parse_input(text: &str) -> HashMap<u32, Vec<Thing>> {
    let mut floors: HashMap<u32, Vec<Thing>> = HashMap::new();
    for line in text.lines() {
        let (num, contents) = parse_line(&line);
        println!("Floor {}, contents {:?}", num, contents);
        assert!(num >= 1 && num <= 4);
        assert!(!floors.contains_key(&num));
        floors.insert(num, contents);
    }
    floors
}

#[derive(Clone, Default)]
struct State {
    floors: [Vec<Thing>; 4],
    current: usize,
}

fn make_state(floor_map: HashMap<u32, Vec<Thing>>) -> State {
    let mut state: State = Default::default();
    floor_map.into_iter().for_each(|(k, v)| -> () {
        assert!(k >= 1 && k <= 4);
        state.floors[(k-1) as usize] = v;
    });
    state
}

// Shorten Thing to just 'G' (for generator) or 'M' (for microchip)
// and the kind.
fn print_thing(thing: &Thing) -> String {
    match thing {
        Thing::Generator(x) => "G".to_string() + x,
        Thing::Microchip(x) => "M".to_string() + x,
    }
}

impl State {
    // Serialize the State into a String. The strings can be compared
    // to check if two states are equal
    pub fn as_string(&self) -> String {
        self.floors.iter()
                   .map(|floor| {
                        let mut items = floor.iter()
                             .map(|thing| print_thing(thing))
                             .collect::<Vec<_>>();
                        items.sort();
                        items.join(",")
                   })
                   .collect::<Vec<_>>()
                   .join("::")
            + " " + &self.current.to_string()
    }

    pub fn is_final(&self) -> bool {
        self.floors[0].len() == 0
        && self.floors[1].len() == 0
        && self.floors[2].len() == 0
    }
}

fn pick_one_or_two(items: &Vec<Thing>) -> Vec<(Vec<Thing>, Vec<Thing>)> {
    let mut result: Vec<(Vec<Thing>, Vec<Thing>)> = Vec::new();
    for i in 0 .. items.len() {
        // Pick 1 item
        result.push((
            vec![items[i].clone()],
            items.iter()
                 .enumerate()
                 .filter(|(idx, _x)| *idx != i)
                 .map(|(_idx, x)| x.clone())
                 .collect::<Vec<Thing>>()
        ));

        // Pick 2 items
        for j in i+1 .. items.len() {
            result.push((
                vec![items[i].clone(), items[j].clone()],
                items.iter()
                    .enumerate()
                    .filter(|(idx, _x)| *idx != i && *idx != j)
                    .map(|(_idx, x)| x.clone())
                    .collect::<Vec<Thing>>()
            ));
        }
    }
    result
}

// If microchip A and any generator, then have to have generator A
fn is_acceptable(things: &Vec<Thing>) -> bool {
    let any_generator = things.iter().any(|thing| matches!(thing, Thing::Generator(_)));
    /*
    if !any_generator {
        return true;
    }
    */
    ! any_generator
    || things.iter().all(|thing| {
        match thing {
            Thing::Generator(_) => true,
            Thing::Microchip(chip_type) => things.contains(&Thing::Generator(chip_type.clone())),
        }
    })
    /*
    for thing in things {
        if let Thing::Microchip(thing_type) = thing {
            if !things.contains(Things::Generator(thing_type)) {
                return false;
            }
        }
    }
    true
    */
}

// Rules:
// At least 1, at most 2 things in the elevator in each turn
// If microchip A and any generator, then have to have generator A
fn move_to_fourth(start_state: &State) -> u32 {
    // queue of (step counter, state), for BFS
    let mut q: VecDeque<(u32, State)> = VecDeque::new();
    let mut visited: HashSet<String> = HashSet::new();
    q.push_back((0, start_state.clone()));
    while !q.is_empty() {
        let (steps, state) = q.pop_front().unwrap();
        if State::is_final(&state) {
            return steps;
        }
        // Reject state if already visited
        let state_str = state.as_string();
        //print!("steps {} state {}\n", steps, state_str);
        if visited.contains(&state_str) {
            continue;
        }
        visited.insert(state_str);
        // Pick any 1 or 2 items from the current floor.
        // There always has to be at least one item on the current
        // floor, otherwise we wouldn't be able to use the lift.
        let current_items = &state.floors[state.current];
        assert!(current_items.len() >= 1);
        for (choice, remain) in pick_one_or_two(current_items) {
            if !is_acceptable(&choice) || !is_acceptable(&remain) {
                continue;
            }
            // Move 1 floor up or down
            for change in [1, -1] {
                let new_floor = (state.current as i32) + change;
                // Verify that the state would still be valid
                if new_floor < 0 || new_floor > 3 {
                    continue;
                }
                let mut floor_after_move = state.floors[new_floor as usize].clone();
                let mut moved_items = choice.clone();
                floor_after_move.append(&mut moved_items);
                if is_acceptable(&floor_after_move) {
                    // Push new state to the back of the queue
                    let mut new_state = state.clone();
                    new_state.current = new_floor as usize;
                    new_state.floors[state.current] = remain.clone();
                    new_state.floors[new_floor as usize] = floor_after_move;
                    q.push_back((steps + 1, new_state));
                }
            }
        }
    }

    panic!("Solution not found");
}

fn main() {
    let mut file = File::open("input11.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    let state = make_state(parse_input(&text));
    let num_steps = move_to_fourth(&state);
    println!("Part 1, steps={}", num_steps);
}

#[cfg(test)]
mod tests {
    use super::*;

    // 1: HM LM
    // 2: HG
    // 3: LG
    // 4:
    static TEST_INPUT: &str =
        "The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.\n\
        The second floor contains a hydrogen generator.\n\
        The third floor contains a lithium generator.\n\
        The fourth floor contains nothing relevant.\n";
    
    #[test]
    fn test_parsing() {
        let floors = parse_input(TEST_INPUT);
        assert_eq!(floors.len(), 4);
        assert!(floors.contains_key(&1));
        assert!(floors.contains_key(&2));
        assert!(floors.contains_key(&3));
        assert!(floors.contains_key(&4));
        assert_eq!(floors[&1], vec![Thing::Microchip("hydrogen".to_string()), Thing::Microchip("lithium".to_string())]);
        assert_eq!(floors[&2], vec![Thing::Generator("hydrogen".to_string())]);
        assert_eq!(floors[&3], vec![Thing::Generator("lithium".to_string())]);
        assert_eq!(floors[&4], vec![]);
    }
    
    #[test]
    fn test_state_as_string() {
        let state = State {
            floors: [
                vec![Thing::Generator("F".to_string()), Thing::Microchip("F".to_string())],
                vec![Thing::Microchip("A".to_string())],
                vec![Thing::Generator("A".to_string())],
                vec![]
            ],
            current: 0,
        };
        let state_string = State::as_string(&state);
        assert_eq!(state_string, "GF,MF::MA::GA:: 0".to_string());
    }
    
    #[test]
    fn test_state_as_string_sorting() {
        let state = State {
            floors: [
                vec![Thing::Microchip("A".to_string()), Thing::Generator("F".to_string()), Thing::Generator("A".to_string())],
                vec![],
                vec![],
                vec![],
            ],
            current: 0,
        };
        let state_string = State::as_string(&state);
        assert_eq!(state_string, "GA,GF,MA:::::: 0".to_string());
    }

    #[test]
    fn test_final_state() {
        let state = State {
            floors: [
                vec![Thing::Microchip("A".to_string())],
                vec![],
                vec![],
                vec![Thing::Generator("A".to_string())],
            ],
            current: 3,
        };
        assert!(!State::is_final(&state));

        let final_state = State {
            floors: [
                vec![],
                vec![],
                vec![],
                vec![Thing::Microchip("A".to_string()),Thing::Generator("A".to_string())],
            ],
            current: 3,
        };
        assert!(State::is_final(&final_state));
    }

    #[test]
    fn test_pick_one_or_two() {
        let m_a = Thing::Microchip("A".to_string());
        let m_b = Thing::Microchip("B".to_string());
        let g_a = Thing::Generator("A".to_string());

        let items = vec![
            m_a.clone(),
            m_b.clone(),
            g_a.clone(),
        ];
        let choices = pick_one_or_two(&items);
        assert_eq!(choices.len(), 6);  // 3 single choices and 3 double choices
        assert_eq!(choices[0], (vec![m_a.clone()], vec![m_b.clone(), g_a.clone()]));
        assert_eq!(choices[1], (vec![m_a.clone(), m_b.clone()], vec![g_a.clone()]));
        assert_eq!(choices[2], (vec![m_a.clone(), g_a.clone()], vec![m_b.clone()]));
        assert_eq!(choices[3], (vec![m_b.clone()], vec![m_a.clone(), g_a.clone()]));
        assert_eq!(choices[4], (vec![m_b.clone(), g_a.clone()], vec![m_a.clone()]));
        assert_eq!(choices[5], (vec![g_a.clone()], vec![m_a.clone(), m_b.clone()]));
    }

    #[test]
    fn test_is_acceptable() {
        let m_a = Thing::Microchip("A".to_string());
        let m_b = Thing::Microchip("B".to_string());
        let g_a = Thing::Generator("A".to_string());
        let g_b = Thing::Generator("B".to_string());

        // acceptable combinations
        assert!(is_acceptable(&vec![]));
        assert!(is_acceptable(&vec![m_a.clone()]));
        assert!(is_acceptable(&vec![g_a.clone()]));
        assert!(is_acceptable(&vec![m_a.clone(), g_a.clone()]));
        assert!(is_acceptable(&vec![m_a.clone(), m_b.clone()]));
        assert!(is_acceptable(&vec![g_a.clone(), g_b.clone()]));
        assert!(is_acceptable(&vec![m_a.clone(), g_a.clone(), g_b.clone()]));
        // not acceptable combinations
        assert!(!is_acceptable(&vec![m_a.clone(), g_a.clone(), m_b.clone()]));
        assert!(!is_acceptable(&vec![m_a.clone(), g_b.clone()]));
    }

    #[test]
    fn test_move_to_fourth() {
        let state = make_state(parse_input(TEST_INPUT));
        let step_count = move_to_fourth(&state);
        assert_eq!(step_count, 11);
    }

}