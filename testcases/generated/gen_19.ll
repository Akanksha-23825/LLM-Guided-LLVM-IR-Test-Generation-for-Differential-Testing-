define i32 @fizzbuzz(i32 %n, i32 %i) {
entry:
  %zero = icmp eq i32 %i, 0
  br i1 %zero, label %end, label %inc

inc:
  %nxt = add i32 %i, 1
  %nxt_zero = icmp eq i32 %nxt, 0
  br i1 %nxt_zero, label %end, label %loop

loop:
  %fizzbuzz = phi i32 [ %nxt, %inc ], [ 0, %entry ]
  %fizz = icmp eq i32 %fizzbuzz, 15
  %buzz = icmp eq i32 %fizzbuzz, 3
  %fizzbuzz_str = select i1 %fizz, i32 0, i32 select i1 %buzz, i32 0, i32 %fizzbuzz
  %result = add i32 %fizzbuzz_str, %fizzbuzz
  store i32 %result, i32* @result_array, align 4
  %new_i = add i32 %fizzbuzz, 1
  %loop_cond = icmp eq i32 %new_i, %n
  br i1 %loop_cond, label %end, label %inc

end:
  ret i32 0
}