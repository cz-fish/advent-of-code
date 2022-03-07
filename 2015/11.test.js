const { expect } = require("@jest/globals");
const d11 = require("./11.js");

test('increment_password increments last letter', () => {
    expect(d11.increment_password('abcdefgm')).toBe('abcdefgn');
    expect(d11.increment_password('abcdefgz')).toBe('abcdefha');
    expect(d11.increment_password('abcdefzz')).toBe('abcdegaa');
    expect(d11.increment_password('azzzzzzz')).toBe('baaaaaaa');
});

test('increment_password skips banned letters', () => {
    expect(d11.increment_password('abcdefgh')).toBe('abcdefgj');
    expect(d11.increment_password('abcdefnz')).toBe('abcdefpa');
    expect(d11.increment_password('abcdelzz')).toBe('abcdemaa');
    expect(d11.increment_password('laibocde')).toBe('maaaaaaa');
});

test('next_valid_password is correct', () => {
    const test_part1 = {
        "abcdefgh": "abcdffaa",
        "ghijklmn": "ghjaabcc",
    };

    for (test in test_part1) {
        const test_res = d11.next_valid_password(test);
        const expected = test_part1[test];
        expect(test_res).toBe(expected);
    } 
});

test('is_valid_password is correct', () => {
    expect(d11.is_valid_password('hijklmmn')).toBeFalsy();
    expect(d11.is_valid_password('abbceffg')).toBeFalsy();
    expect(d11.is_valid_password('abbcegjk')).toBeFalsy();
    expect(d11.is_valid_password('abcdffaa')).toBeTruthy();
    expect(d11.is_valid_password('ghjaabcc')).toBeTruthy();
});
