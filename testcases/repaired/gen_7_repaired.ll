define i32 @cmp_gt_100(i32 %1) {
entry:
  %2 = icmp sgt i32 %1, 100
  ret i32 %2
}