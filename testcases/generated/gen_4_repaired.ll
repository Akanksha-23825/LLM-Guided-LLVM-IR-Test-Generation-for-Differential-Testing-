define i32 @abs(i32 %x) {
  %1 = icmp sgt i32 %x, 0
  %2 = select i1 %1, i32 %x, i32 -%x
  ret i32 %2
}