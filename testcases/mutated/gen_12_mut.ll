; Mutation: replaced non-existent constant with a new constant value, adding a constant to one of the function arguments
define i32 @bitwise_and(i32 %a, i32 %b) {
  entry:
    %1 = add i32 %a, 5
    %and = and i32 %1, %b
    ret i32 %and
}