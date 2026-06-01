define i32 @max_of_three(i32 %a, i32 %b, i32 %c) {
entry:
  %max_ab = icmp slt i32 %a, %b
  br i1 %max_ab, label %a_less_than_b, label %b_less_than_a

a_less_than_b:
  %max_ac = icmp slt i32 %b, %c
  br i1 %max_ac, label %b_less_than_c, label %c_less_than_b

b_less_than_c:
  ret i32 %c

c_less_than_b:
  ret i32 %b

b_less_than_a:
  %max_ab = icmp slt i32 %c, %a
  br i1 %max_ab, label %c_less_than_a, label %a_less_than_c

a_less_than_c:
  ret i32 %a

c_less_than_a:
  ret i32 %c

unreachable
}