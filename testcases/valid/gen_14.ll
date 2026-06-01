define i32 @left_shift(i32 %x, i32 %y) {
entry:
  %0 = mul i32 %y, 2
  %1 = shl i32 %x, %0
  ret i32 %1
}