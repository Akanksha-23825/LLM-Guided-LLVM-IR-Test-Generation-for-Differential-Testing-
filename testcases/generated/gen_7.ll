define i32 @greater_than_100(i32 %x) {
entry:
  %1 = icmp sgt i32 %x, 100
  ret i32 %1
}