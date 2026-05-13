define i32 @abs(i32 %x) {
entry:
  %1 = icmp sgt i32 %x, 0
  %2 = sub i32 0, %x
  %3 = select i1 %1, i32 %x, i32 %2
  ret i32 %3
}