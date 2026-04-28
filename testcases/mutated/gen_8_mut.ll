; Mutation: changed add to mul in %new_acc calculation
define i32 @sum_loop(i32 %n) {
entry:
  %acc = add i32 0, 0
  %i = add i32 1, 0
  br label %loop

loop:
  %cond = icmp slt i32 %i, %n
  br i1 %cond, label %loop_body, label %loop_after

loop_body:
  %new_acc = mul i32 %acc, %i
  %new_i = add i32 %i, 1
  br label %loop

loop_after:
  %final_acc = add i32 %acc, %i
  ret i32 %final_acc
}