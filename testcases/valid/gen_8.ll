define i32 @sum_to_ten() {
entry:
  %i = alloca i32
  store i32 0, i32* %i
  br label %loop

loop:
  %i1 = load i32, i32* %i
  %i2 = icmp slt i32 %i1, 11
  br i1 %i2, label %loop_body, label %exit

loop_body:
  %i3 = load i32, i32* %i
  %i4 = add i32 %i3, 1
  store i32 %i4, i32* %i
  br label %loop

exit:
  %i5 = load i32, i32* %i
  ret i32 %i5
}