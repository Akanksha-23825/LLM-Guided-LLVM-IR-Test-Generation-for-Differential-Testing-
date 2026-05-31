define i32 @abs(i32 %x) {
entry:
  %0 = icmp sge i32 %x, 0
  %1 = select i1 %0, i32 %x, i32 neg %x
  ret i32 %1
}