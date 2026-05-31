; Mutation: added dead computation with unused result
define i32 @add(i32 %a, i32 %b) {
entry:
  %sum = add i32 %a, %b
  %unused = mul i32 %a, %b
  ret i32 %sum
}