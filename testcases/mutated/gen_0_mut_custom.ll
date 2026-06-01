; Mutation: changed add to mul
define i32 @add(i32 %a, i32 %b) {
entry:
  %sum = mul i32 %a, %b
  ret i32 %sum
}