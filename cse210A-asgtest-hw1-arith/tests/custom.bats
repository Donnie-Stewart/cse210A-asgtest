load harness

@test "custom-1" {
  check '1 - 1 - 1 - 1 - 1 - - 1' '-2'
}

@test "custom-2" {
  check '1 - 1 * 10 - 5' '-14'
}

@test "custom-3" {
  check '1 - 200 * 10 + 5 - 2' '-1996'
}

@test "custom-4" {
  check '5 + 3 * 2 - 1 * 2 + 6' '15'
}

@test "custom-5" {
  check '1 - 0 - 2 - 3 - 4 * 6' '-28'
}
