define i32 @is_even(i32 %0) {
entry:
  %1 = urem i32 %0, 2
  %2 = trunc i32 %1 to i1
  %3 = zext i1 %2 to i32
  ret i32 %3
}