from core.abst import cAST
cast = cAST('/Users/kirk/homework/spring2019/cse637/class_project/cmdDetect/examples/c_files/exam1.c', line_number=16, function_name='exec')
ast = cast.ast
print(cast.check_func_called())
# for c in ast.ext:
    # print(type(c))

