load harness

@test "custom-1" {
  check 'if true then x := 5 else x := 0' '⇒ x := 5, {}
⇒ skip, {x → 5}'
}

@test "custom-2" {
  check 'while x + 1 = 3 + 4 ∧ z - -1 = -2 * z do z := -5000' '⇒ skip, {}'
}

@test "custom-3" {
  check 'while ¬ true do x := 1 ; y := 1' '⇒ skip; y := 1, {}
⇒ y := 1, {}
⇒ skip, {y → 1}'
}

@test "custom-4" {
  check 'if ( ¬ false ) then x := 5 else octa := 2' '⇒ x := 5, {}
⇒ skip, {x → 5}'
}

@test "custom-5" {
  check 'skip; skip' '⇒ skip, {}'
}