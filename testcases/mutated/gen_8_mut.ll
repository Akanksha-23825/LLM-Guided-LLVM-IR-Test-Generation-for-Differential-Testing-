; Mutation: renamed SSA variable %sum to %total_sum
define i32 @sum_from_1_to_10() {
entry:
  %total_sum = alloca i32, align 4
  %i = alloca i32, align 4
  %1 = add i32 0, 1
  store i32 %1, i32* %i, align 4
  %2 = load i32, i32* %total_sum, align 4
  store i32 %2, i32* %total_sum, align 4
  br label %loop

loop:
  %3 = load i32, i32* %i, align 4
  %4 = icmp slt i32 %3, 11
  br i1 %4, label %body, label %exit

body:
  %5 = load i32, i32* %total_sum, align 4
  %6 = load i32, i32* %i, align 4
  %7 = add i32 %5, %6
  store i32 %7, i32* %total_sum, align 4
  %8 = add i32 %3, 1
  store i32 %8, i32* %i, align 4
  br label %loop

exit:
  %9 = load i32, i32* %total_sum, align 4
  ret i32 %9
}