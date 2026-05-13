define i32 @entry(i32 %x) {
entry:
  %1 = icmp sgt i32 %x, 100
  %2 = zext i1 %1 to i32
  ret i32 %2
}