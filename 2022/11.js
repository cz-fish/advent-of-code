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

class Monkey{
	constructor(items, op, test, trueMonkey, falseMonkey) {
     this.items = items;
     this.op = op;
     this.test = test;
     this.trueMonkey = trueMonkey;
     this.falseMonkey = falseMonkey;
     this.inspCount = 0;
	}
}

function parseMonkey(monkeyData) {
  var items = [];
  var op = '';
  var div = 0;
  var trueMonkey = -1;
  var falseMonkey = -1;
  for (var ln of monkeyData.split('\n')) {
  	  if (ln.match(/Starting items:/)) {
  	  	  items = ln.substr(18).split(', ').map(x => parseInt(x));
  	  	  //console.log(`starting items ${items}`);
  	  	}
  	  	else if (ln.match(/Operation:/)) {
  	  		op = ln.substr(13).trim();
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
 
  console.log(`monkey: ${items}, ${op}, ${div}, ${trueMonkey}, ${falseMonkey}`);
  return new Monkey(items, op, div, trueMonkey, falseMonkey);
}

function parseMonkeys(data)
{
	// \n\r\n for the test
	return data.split('\n\n').map(m => parseMonkey(m));
}

function applyOp(value, op) {
  // new = ? ? ?
  var parts = op.split(' ');
  assert(parts.length === 5);
  var v1;
  var v2;
  if (parts[2] === 'old') {
  	  v1 = value;
  } else {
  	  v1 = parseInt(parts[2]);
  }
  
  if (parts[4] === 'old') {
    v2 = value;
  } else {
  	  v2 = parseInt(parts[4]);
  }
  if (parts[3] === '+') {
     return v1 + v2;
  }
  if (parts[3] === '*') {
  	   return v1 * v2;
  	}
  	assert(False);
}

function monkeyTurn(monkey, monkeys) {
  for (var item of monkey.items) {
    var firstValue = applyOp(item, monkey.op);
    var value = Math.floor(firstValue / 3);
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
  const p1result = part1(monkeys);
  console.log(`part1: ${p1result}`);
  if (useTestInput) {
    cassert(p1result, 10605);
  }
  
  //part2(monkeys);

});
