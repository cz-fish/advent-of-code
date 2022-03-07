const assert = require("assert");

const PWD_LENGTH = 8;
const Z_CODE = 'z'.charCodeAt(0);
const BANNED_CODES = [
  'i'.charCodeAt(0),
  'l'.charCodeAt(0),
  'o'.charCodeAt(0),
];


function next_valid_password(old_pwd) {
  let new_pwd = increment_password(old_pwd);
  while (!is_valid_password(new_pwd)) {
    new_pwd = increment_password(new_pwd);
  }
  return new_pwd;
}

function increment_password(pwd) {
  // increment the character at increment_pos, and set the rest of the password to 'a'
  // first search for any banned characters, and find the first one
  let increment_pos = pwd.search(/[iol]/);
  // if there is no banned character, then find the last index < 'z'
  if (increment_pos === -1) {
    // increment the last character
    increment_pos = PWD_LENGTH - 1;
    while (pwd.charCodeAt(increment_pos >= 0 && increment_pos) === Z_CODE) {
      increment_pos--;
    }
    assert(increment_pos >= 0); // there's no next password of length 8!
  }
  let c = pwd.charCodeAt(increment_pos) + 1; // it's guaranteed that this won't go past 'z'
  if (BANNED_CODES.includes(c)) {
    // skip over banned char. This is also guaranteed to not go past 'z',
    // plus we also know that the next 'c' will not be banned
    c++;
  }
  let new_pwd = pwd.substr(0, increment_pos) + String.fromCharCode(c);
  return new_pwd.padEnd(PWD_LENGTH, 'a');
}

function is_valid_password(pwd) {
  let pairs = new Set();
  let trip = 0;
  for (let i = 1; i < PWD_LENGTH; i++) {
    if (i > 1) {
      const a = pwd.charCodeAt(i-2);
      const b = pwd.charCodeAt(i-1);
      const c = pwd.charCodeAt(i);
      if (a === b - 1 && b === c - 1) {
        trip++;
      }
    }
    const d = pwd.charCodeAt(i-1);
    const e = pwd.charCodeAt(i);
    if (d === e && !pairs.has(i-2)) {
      pairs.add(i-1);
    }
  }
  return trip > 0 && pairs.size > 1;
}

exports.increment_password = increment_password;
exports.next_valid_password = next_valid_password;
exports.is_valid_password = is_valid_password;

if (require.main === module) {
  // The main is this module, i.e. this module was ran directly (as opposed to
  // running through require).

  // Real puzzle input
  const input = "vzbxkghb";

  const part1_res = next_valid_password(input);
  console.log(`Part 1: ${part1_res}`);
 
  const part2_res = next_valid_password(part1_res);
  console.log(`Part 2: ${part2_res}`);
}
