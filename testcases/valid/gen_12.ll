define i32 @bitwise_and(i32 %a, i32 %b) {
  entry:
    %and = and i32 %a, %b
    ret i32 %and
}