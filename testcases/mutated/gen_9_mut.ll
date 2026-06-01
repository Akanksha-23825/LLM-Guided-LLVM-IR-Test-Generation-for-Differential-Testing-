; Mutation: replaced %b with a constant 5 in the icmp instruction
define i32 @min(i32 %a, i32 %b) {
entry:
  %cmp = icmp slt i32 %a, i32 5
  %select = select i1 %cmp, i32 %a, i32 %b
  ret i32 %select
}