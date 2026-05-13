define i32 @min(i32 %x, i32 %y) {
entry:
  %cmp = icmp slt i32 %x, %y
  %select = select i1 %cmp, i32 %x, i32 %y
  ret i32 %select
}