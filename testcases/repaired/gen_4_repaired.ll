define i32 @abs(i32 %x) {
entry:
  %icmp = icmp sgt i32 %x, 0
  %select = select i1 %icmp, i32 %x, i32 0 - %x
  ret i32 %select
}