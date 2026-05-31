define i32 @max3(i32 %a, i32 %b, i32 %c) {
entry:
  %compare_ab = icmp sgt i32 %a, %b
  %ab_max = select i1 %compare_ab, i32 %a, i32 %b
  %compare_ab_c = icmp sgt i32 %ab_max, %c
  %compare_ac = icmp sgt i32 %a, %c
  %max3 = select i1 %compare_ab_c, i32 %ab_max, i32 (select i1 %compare_ac, i32 %a, i32 %c)
  ret i32 %max3
}