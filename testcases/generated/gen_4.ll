define i32 @abs(i32 %x) {
  %0 = icmp sgt i32 %x, 0
  %1 = select i1 %0, i32 %x, i32 -%x
  ret i32 %1
}