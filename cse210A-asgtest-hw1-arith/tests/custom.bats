load harness

@test "custom-1" {
  check '2 + 3 * 4' '14'
}

@test "custom-2" {
  check '-2 + 3 * -4 + 6 * 2 * 0' '-14'
}

@test "custom-3" {
  check '3 * 8 + 9 * 10' '114'
}

@test "custom-4" {
  check '5 * 6 + 9' '39'
}

@test "custom-5" {
  check '5 * 8 + 6 * 4 + -2' '62'
}
