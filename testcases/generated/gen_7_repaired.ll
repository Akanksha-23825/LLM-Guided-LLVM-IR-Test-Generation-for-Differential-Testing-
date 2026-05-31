define i32 @gt_100(i32 %x) {
entry:
  %0 = icmp sgt i32 %x, 100
  %1 = zext i1 %0 to i32
  ret i32 %1
}