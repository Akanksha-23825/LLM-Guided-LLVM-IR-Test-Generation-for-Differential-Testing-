; Mutation: replaced the numeric constant in the function signature with a different constant value, but since there were no constants, added a constant and replaced it
define i32 @add(i32 %a, i32 %b) {
entry:
  %0 = add i32 %a, %b
  %1 = add i32 %0, 2
  ret i32 %1
}