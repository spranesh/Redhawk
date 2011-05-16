#!/usr/bin/env python

import redhawk.common.node as N
import redhawk.common.tree_converter as T


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
            (constant 1))))
      (compound 
        (compound 
          (return 
            (* n 
              (apply Factorial 
                ((- n 
                  (constant 1)))))))))))

"""


if_true = [
      N.Return(
        position = None,
        return_expression = N.Constant(
          position = None,
          value = '1'))]

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



if_false = [
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
              arguments = fact_arguments)]))]

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
    if_true = if_true,
    if_false = if_false)


factorial_tree = N.DefineFunction(
     position = None,
     name = 'Factorial',
     arguments = N.FunctionArguments(
          position = None,
          arguments = [
              N.DefineVariable(
                   position = None
                   ,name = 'n')]),
     body = [ifelse])


module_tree = N.Module(position=None,
    filename='sample_last.py',
    children=[factorial_tree])

T.TreeConverter().AttachParents(module_tree)

tree = module_tree.GetChildren()[0]

__all__ = ['tree', 'module_tree']

if __name__ == '__main__':
  print module_tree.ToStr()
