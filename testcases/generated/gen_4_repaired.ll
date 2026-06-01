define i32 @abs(i32 %1) {
entry:
  %2 = icmp sgt i32 %1, 0
  %3 = icmp slt i32 %1, 0
  %4 = select i1 %2, i32 %1, i32 sub (i32 0, i32 %1)
  ret i32 %4
}