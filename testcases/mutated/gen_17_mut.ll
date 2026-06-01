; Mutation: added dead computation %6
define i32 @first_match(i32 %a, i32 %b, i32 %c, i32 %d) {
entry:
  %1 = icmp slt i32 %a, %b
  %2 = icmp slt i32 %c, %d
  %3 = select i1 %1, i32 %a, i32 %c
  %4 = icmp slt i32 %3, %c
  %5 = select i1 %4, i32 %3, i32 %c
  %6 = add i32 %a, %b
  ret i32 %5
}