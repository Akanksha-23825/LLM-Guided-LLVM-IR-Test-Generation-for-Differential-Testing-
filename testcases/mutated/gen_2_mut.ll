; Mutation: added a dead computation for %unused
define i32 @check_even(i32 %x) {
entry:
  %rem = urem i32 %x, 2
  %cond = icmp eq i32 %rem, 0
  %unused = add i32 %rem, 1
  %ret = zext i1 %cond to i32
  ret i32 %ret
}