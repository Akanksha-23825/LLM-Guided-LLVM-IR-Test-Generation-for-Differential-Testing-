define i32 @add(integers) {
entry:
  %a = alloca i32
  %b = alloca i32
  store i32 %0, i32* %a
  store i32 %1, i32* %b
  %0 = load i32, i32* %a
  %1 = load i32, i32* %b
  %sum = add nsw i32 %0, %1
  ret i32 %sum
}