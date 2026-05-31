define i32 @max(i32 %a, i32 %b) {
entry:
  %cmp = icmp ugt i32 %a, %b
  %cond = zext i1 %cmp to i32
  %cond1 = sub i32 %b, %a
  %cond2 = select i1 %cmp, i32 %b, i32 %a
  %max = select i1 %cond, i32 %cond1, i32 %cond2
  ret i32 %max
}