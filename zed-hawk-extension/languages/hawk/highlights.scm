(comment) @comment
(string_literal) @string
(number_literal) @number
(boolean_literal) @constant.language
(set_statement
  name: (identifier) @variable.other)
(set_statement
  type: (type_identifier) @type)
(fn_declaration
  name: (identifier) @function)
(call_expression
  function: (identifier) @function)
(parenthesized_expression
  "(" @punctuation.bracket
  ")" @punctuation.bracket)
(matrix_literal
  "[" @punctuation.bracket
  "]" @punctuation.bracket)
(block
  "{" @punctuation.bracket
  "}" @punctuation.bracket)
(for_statement
  "(" @punctuation.bracket
  ")" @punctuation.bracket)
(while_statement
  "(" @punctuation.bracket
  ")" @punctuation.bracket)
(if_statement
  "(" @punctuation.bracket
  ")" @punctuation.bracket)
(fn_declaration
  "(" @punctuation.bracket
  ")" @punctuation.bracket)
(parameters
  ("," @punctuation.delimiter))
(argument_list
  ("," @punctuation.delimiter))
(set_statement
  "set" @keyword)
(print_statement
  "print" @keyword)
(fn_declaration
  "fn" @keyword)
(return_statement
  "return" @keyword)
(if_statement
  "if" @keyword)
(else_clause
  "else" @keyword)
(while_statement
  "while" @keyword)
(for_statement
  "for" @keyword)
(import_statement
  "import" @keyword)
(or_expression
  "or" @keyword.operator.logical)
(and_expression
  "and" @keyword.operator.logical)
(unary_expression
  "not" @keyword.operator.logical)
