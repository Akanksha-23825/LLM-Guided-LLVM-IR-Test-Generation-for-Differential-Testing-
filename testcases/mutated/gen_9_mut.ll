; Mutation: added dead computation with unused result
define i32 @min(i32 %a, i32 %b) {
entry:
  %cmp = icmp slt i32 %a, %b
  %unused = add i32 %a, %b
  %select = select i1 %cmp, i32 %a, i32 %b
  ret i32 %select
}