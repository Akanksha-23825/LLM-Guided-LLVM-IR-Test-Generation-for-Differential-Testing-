; Mutation: replaced the function with a new one that adds 5 instead of %b
define i32 @add(i32 %a) {
entry:
  %add = add i32 %a, 5
  ret i32 %add
}