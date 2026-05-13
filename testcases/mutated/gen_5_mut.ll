; Mutation: replaced non-existent constant with a new constant, so added a constant and replaced it
define i32 @multiply(i32 %a, i32 %b) {
entry:
  %1 = add i32 %a, 5
  %product = mul i32 %1, %b
  ret i32 %product
}