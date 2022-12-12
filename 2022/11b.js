const fs = require("fs");
const assert = require("assert");

/*
  Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
	*/

// optype:
//  1 - old * old
//  2 - old * val
//  3 - old + val

class Monkey{
	constructor(items, optype, opval, test, trueMonkey, falseMonkey) {
     this.items = items;
     this.optype = optype;
     this.opval = opval;
     this.test = test;
     this.trueMonkey = trueMonkey;
     this.falseMonkey = falseMonkey;
     this.inspCount = 0;
	}
}

function parseOp(opstr) {
  var parts = opstr.split(' ');
  assert(parts.length === 5);
  assert(parts[2] === 'old');
  var optype = 0;
  var opvalue = 0;
  if (parts[3] === '*') {
  	  optype = 2;
  	} else if (parts[3] === '+'){
  	   optype = 3;
  	} else{
  	   assert(false);
  	}
  	if (parts[4] === 'old') {
  	   assert(optype === 2);
  	   optype = 1;
  	} else {
  		opvalue = parseInt(parts[4]);
  	}
   return {type: optype, value: opvalue};
}

function parseMonkey(monkeyData) {
  var items = [];
  var op = null;
  var div = 0;
  var trueMonkey = -1;
  var falseMonkey = -1;
  for (var ln of monkeyData.split('\n')) {
  	  if (ln.match(/Starting items:/)) {
  	  	  items = ln.substr(18).split(', ').map(x => parseInt(x));
  	  	  //console.log(`starting items ${items}`);
  	  	}
  	  	else if (ln.match(/Operation:/)) {
  	  		op = parseOp(ln.substr(13).trim());
  	  	}
  	  	else if (ln.match(/Test: divisible by/)) {
  	  	   div = parseInt(ln.substr(20));
  	  	}
  	  	else if (ln.match(/If true/)) {
  	  	   trueMonkey = parseInt(ln.substr(28));
  	  	}
  	  	else if (ln.match(/If false/)) {
  	  		falseMonkey = parseInt(ln.substr(29));
  	  	}
  	}
 
  console.log(`monkey: ${items}, ${JSON.stringify(op)}, ${div}, ${trueMonkey}, ${falseMonkey}`);
  return new Monkey(items, op.type, op.value, div, trueMonkey, falseMonkey);
}

function parseMonkeys(data)
{
	// \n\r\n for the test
	return data.split('\n\n').map(m => parseMonkey(m));
	//return data.split('\n\r\n').map(m => parseMonkey(m));
}

function applyOp(value, optype, opval, mod) {
  var newval = undefined;
  if (optype === 1) {
  	  newval = value * value;
  } else if (optype === 2) {
  	  newval = value * opval;
  } else if (optype === 3) {
  	  newval = value + opval;
  }
  return newval % mod;	
}

function monkeyTurn(monkey, monkeys, mod) {
  for (var item of monkey.items) {
    var value = applyOp(item, monkey.optype, monkey.opval, mod);
    // Part1 only:
    //var value = Math.floor(firstValue / 3);
    //console.log(`item ${item} -> ${monkey.op} -> ${firstValue} -> /3 -> ${value}`);
    if (value % monkey.test == 0) {
    	 monkeys[monkey.trueMonkey].items.push(value);
    } else {
    	 monkeys[monkey.falseMonkey].items.push(value);
    }
    monkey.inspCount++;
  }
  monkey.items = [];
}

function part1(monkeys)
{
	const rounds = 20;
	//const rounds = 2;
	for (var round = 0; round < rounds; ++round) {
	  for (var monkey of monkeys) {
	    monkeyTurn(monkey, monkeys);
	  }
	  //console.log(`round ${round}`);
	  //for (var monkey of monkeys) {
	  	//  console.log(`  ${JSON.stringify(monkey.items)}`);
	  	//}
	}
	var counts = monkeys.map(m => m.inspCount);
	counts = counts.sort((a, b) => (b - a));
	console.log(counts);
	return counts[0] * counts[1];
}

function part2(monkeys)
{
	var mod = monkeys.map(m => m.test).reduce((a, b) => a*b);
	console.log(`using modulus ${mod}`);
	//FIXME
	const rounds = 10000;
	const checkpoints = [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000];
	//const rounds = 2;
	for (var round = 0; round < rounds; ++round) {
	  if (checkpoints.indexOf(round) >= 0) {
	    console.log(`round ${round}`);
	    console.log(JSON.stringify([...monkeys.map(m =>m.inspCount)]));
	  }
	  for (var monkey of monkeys) {
	    monkeyTurn(monkey, monkeys, mod);
	  }
	  //console.log(`round ${round}`);
	  //for (var monkey of monkeys) {
	  	//  console.log(`  ${JSON.stringify(monkey.items)}`);
	  	//}
	}
	var counts = monkeys.map(m => m.inspCount);
	counts = counts.sort((a, b) => (b - a));
	console.log(counts);
	return counts[0] * counts[1];
}

function cassert(actual, expected) {
	console.log(`${actual} =?= ${expected}`);
	assert(actual === expected);
}

const useTestInput = false;
let fname = '/storage/emulated/0/Download/input2022-11.txt';
if (useTestInput){
	fname = '/storage/emulated/0/Download/input-t-2022-11.txt';
}
fs.readFile(fname, 'utf8' , (err, data) => {
    if (err) {
      console.error(err);
      return;
    }

  var monkeys = parseMonkeys(data);
  /*
  const p1result = part1(monkeys);
  console.log(`part1: ${p1result}`);
  if (useTestInput) {
    cassert(p1result, 10605);
  }
  */
  
  const p2result = part2(monkeys);
  console.log(`part2: ${p2result}`);
  if (useTestInput) {
    cassert(p2result, 2713310158);
  }

});
