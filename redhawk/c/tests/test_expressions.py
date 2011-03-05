#!/usr/bin/env python

""" Test Expressions """

import test_utils

def GetNthExpressionInFirstFunction(n, filename="expressions.c"):
  t = test_utils.SetUp("expressions.c")
  return test_utils.ConvertTree(t.children()[0].body.block_items[n-1])

def TestExpression1():
  """ Test 2 + 3 * 5; """
  return GetNthExpressionInFirstFunction(1)

def TestExpression2():
  """ Test a + b * c; """
  return GetNthExpressionInFirstFunction(2)

def TestExpression3():
  """ Test a << 2; """
  return GetNthExpressionInFirstFunction(3)

def TestExpression4():
  """ Test (a - 2) * (b + c) / d; """ 
  return GetNthExpressionInFirstFunction(4)

def TestExpression5():
  """ Test a%b; """
  return GetNthExpressionInFirstFunction(5)

def TestExpression6():
  """ Test (c >> 3) * d;"""
  return GetNthExpressionInFirstFunction(6)

def TestExpression7():
  """ Test (a | b) ^ (c & d);"""
  return GetNthExpressionInFirstFunction(7)

def TestExpression8():
  """ Test (a && b) || (c && d);"""
  return GetNthExpressionInFirstFunction(8)

def TestExpression9():
  """ Test (a < b) && (c <= d) || (e > f) && (g > h);"""
  return GetNthExpressionInFirstFunction(9)

def TestExpression10():
  """ Test a == b;"""
  return GetNthExpressionInFirstFunction(10)

def TestExpression11():
  """ Test a != b; """
  return GetNthExpressionInFirstFunction(11)

def TestExpression12():
  """ Test Unary Expression !(a == b); """
  return GetNthExpressionInFirstFunction(12)


# ------------- Test Unary Operators.

def TestUnaryMinus():
  """ Test Unary Expression (-a);"""
  return GetNthExpressionInFirstFunction(13)

def TestUnaryPlus():
  """ Test Unary Expression (+a);"""
  return GetNthExpressionInFirstFunction(14)

def TestAddressOf():
  """ Test Unary Expression &a;"""
  return GetNthExpressionInFirstFunction(15)

def TestDereference():
  """ Test Unary Expression *ptr;"""
  return GetNthExpressionInFirstFunction(16)

def TestPreIncrement():
  """ Test Unary Expression ++a;"""
  return GetNthExpressionInFirstFunction(17)

def TestPostIncrement():
  """ Test Unary Expression a++;"""
  return GetNthExpressionInFirstFunction(18)

def TestPreDecrement():
  """ Test Unary Expression --a;"""
  return GetNthExpressionInFirstFunction(19)

def TestPostDecrement():
  """ Test Unary Expression a--;"""
  return GetNthExpressionInFirstFunction(20)

def TestSizeOf():
  """ Test sizeof(char); """
  return GetNthExpressionInFirstFunction(21)

def TestBitwiseNegate():
  """ Test ~a; """
  return GetNthExpressionInFirstFunction(22)


# -------------- Test Some Combinations.
def TestMiscCombination1():
  """ Test (a++) * (*(ptr + 4)); """
  return GetNthExpressionInFirstFunction(23)

