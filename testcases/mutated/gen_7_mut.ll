; Mutation: added dead computation with unused result
define i32 @entry(i32 %x) {
entry:
  %1 = icmp sgt i32 %x, 100
  %2 = zext i1 %1 to i32
  %3 = add i32 %x, 200
  ret i32 %2
}