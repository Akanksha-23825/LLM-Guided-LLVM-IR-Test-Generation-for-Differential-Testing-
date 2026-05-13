define i32 @abs(i32 %x) {
entry:
  %cmp = icmp sgt i32 %x, 0
  %select = select i1 %cmp, i32 %x, i32 %neg_x
  ret i32 %select
}