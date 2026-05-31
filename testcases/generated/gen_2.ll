define i32 @is_even(i32 %x) {
entry:
  %1 = urem i32 %x, 2
  %2 = zext i1 %1 to i32
  ret i32 %2
}