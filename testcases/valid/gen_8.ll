define i32 @sum_to_10() {
entry:
  %sum = alloca i32, align 4
  %i = alloca i32, align 4
  store i32 0, i32* %sum, align 4
  store i32 1, i32* %i, align 4
  br label %loop

loop:
  %i_val = load i32, i32* %i, align 4
  %cond = icmp slt i32 %i_val, 11
  br i1 %cond, label %body, label %exit

body:
  %i_val1 = load i32, i32* %i, align 4
  %sum_val = load i32, i32* %sum, align 4
  %new_sum = add i32 %sum_val, %i_val1
  store i32 %new_sum, i32* %sum, align 4
  %i_val2 = load i32, i32* %i, align 4
  %new_i = add i32 %i_val2, 1
  store i32 %new_i, i32* %i, align 4
  br label %loop

exit:
  %sum_val1 = load i32, i32* %sum, align 4
  ret i32 %sum_val1
}