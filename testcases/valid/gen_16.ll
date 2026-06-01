define i32 @power(i32 %base, i32 %exponent) {
entry:
  %is_zero = icmp eq i32 %exponent, 0
  br i1 %is_zero, label %return_zero, label %mult

return_zero:
  ret i32 1

mult:
  %is_even = icmp eq i32 %exponent, 1
  br i1 %is_even, label %return_one, label %half_exponent

return_one:
  ret i32 %base

half_exponent:
  %half = sdiv i32 %exponent, 2
  %result = mul i32 %base, %base
  %is_even_now = icmp eq i32 %half, 0
  br i1 %is_even_now, label %double_half_result, label %mult_with_half_result

mult_with_half_result:
  %half_result = mul i32 %base, %result
  br label %return_half_result

double_half_result:
  %double_half = mul i32 %result, %result
  br label %return_half_result

return_half_result:
  %next_exponent = add i32 %half, 1
  %next_power = mul i32 %result, %result
  %is_power_zero = icmp eq i32 %next_exponent, 0
  br i1 %is_power_zero, label %return_power, label %mult

return_power:
  ret i32 %next_power
}