#!/usr/bin/env python

import node as N


"""
This module creates a test tree for us to run our code on.
Function Fact(n):
  Compound:
    if
      n == 1
      Compound
        return 1
      Compound
        return n * Fact(n-1)

When printed it represents:

(define-function Factorial 
  ((define-variable n))
  (compound 
    (if 
      (eq n 
        (constant 0))
      (compound 
        (compound 
          (return 
            (constant ))))
      (compound 
        (compound 
          (return 
            (* n 
              (apply Factorial 
                ((- n 
                  (constant 1)))))))))))

"""


if_true = N.Compound(
    position = None,
    compound_items = [
      N.Return(
        position = None,
        return_expression = N.Constant(
          position = None,
          value = 1))])

fact_arguments = N.FunctionArguments(
    position = None,
    arguments = [
      N.Expression(
        position = None,
        operator = 'MINUS',
        children = [
          N.ReferVariable(
            position = None,
            name = 'n'),
          N.Constant(
            position = None,
            value = '1')])])



if_false = N.Compound(
    position = None,
    compound_items = [
      N.Return(
        position = None,
        return_expression = N.Expression(
          position = None,
          operator = 'MULTIPLY',
          children = [
            N.ReferVariable(
              position = None,
              name = 'n'),
            N.CallFunction(position = None,
              function = N.ReferVariable(
                position = None,
                name = 'Factorial'),
              arguments = fact_arguments)]))])

ifelse = N.IfElse(
    position = None,
    condition = N.Expression(
        position = None,
        operator = 'EQ',
        children = [
            N.ReferVariable(
               position = None,
               name = 'n'),
            N.Constant(
               position = None,
               value = '0')]),
    if_true = N.Compound(
        position = None,
        compound_items = [if_true]),
    if_false = N.Compound(
        position = None,
        compound_items = [if_false]))


factorial_tree = N.DefineFunction(
     position = None,
     name = 'Factorial',
     arguments = N.FunctionArguments(
          position = None,
          arguments = [
              N.DefineVariable(
                   position = None
                   ,name = 'n')]),
     body = N.Compound(
          position = None,
          compound_items = [ifelse]))

tree = factorial_tree

if __name__ == '__main__':
  print factorial_tree.ToStr()
