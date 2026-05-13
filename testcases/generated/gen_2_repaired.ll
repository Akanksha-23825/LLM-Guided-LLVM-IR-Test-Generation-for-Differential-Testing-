define i32 @is_even(i32 %x) {
entry:
  %rem = urem i32 %x, 2
  ret i32 (or i32 %rem, i32 0)
}