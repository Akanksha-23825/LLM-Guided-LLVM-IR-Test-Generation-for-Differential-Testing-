define i32 @multiply(i32 %x, i32 %y) {
entry:
  %product = mul i32 %x, %y
  ret i32 %product
}