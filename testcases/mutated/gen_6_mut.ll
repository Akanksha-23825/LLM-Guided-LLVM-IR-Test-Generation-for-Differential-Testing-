; Mutation: added dead computation with unused result
define i32 @subtract(i32 %a, i32 %b) {
entry:
  %sub = sub i32 %a, %b
  %dead = mul i32 %a, %b
  ret i32 %sub
}