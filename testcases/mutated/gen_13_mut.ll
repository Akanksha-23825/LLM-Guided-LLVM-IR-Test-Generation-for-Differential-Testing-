; Mutation: No arithmetic operators found to swap, adding a simple arithmetic operation and swapping it
define i32 @xor(i32 %x, i32 %y) {
entry:
  %add = add i32 %x, %y
  %mul = mul i32 %x, %y
  %xor = xor i32 %x, %y
  ret i32 %mul
}