define i32 @mul(i32 %0, i32 %1) {
entry:
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  store i32 %1, i32* %3, align 4
  %4 = load i32, i32* %2, align 4
  %5 = load i32, i32* %3, align 4
  %6 = mul i32 %4, %5
  ret i32 %6
}