define i32 @max(i32 %0, i32 %1) {
entry:
  %2 = icmp ugt i32 %0, %1
  %3 = sub i32 %1, %0
  %4 = select i1 %2, i32 %1, i32 %0
  %5 = select i1 %2, i32 %3, i32 %4
  ret i32 %5
}