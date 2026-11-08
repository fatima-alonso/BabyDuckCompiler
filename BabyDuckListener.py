# Generated from BabyDuck.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BabyDuckParser import BabyDuckParser
else:
    from BabyDuckParser import BabyDuckParser

# This class defines a complete listener for a parse tree produced by BabyDuckParser.
class BabyDuckListener(ParseTreeListener):

    # Enter a parse tree produced by BabyDuckParser#programa.
    def enterPrograma(self, ctx:BabyDuckParser.ProgramaContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#programa.
    def exitPrograma(self, ctx:BabyDuckParser.ProgramaContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#vars.
    def enterVars(self, ctx:BabyDuckParser.VarsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#vars.
    def exitVars(self, ctx:BabyDuckParser.VarsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#funcs.
    def enterFuncs(self, ctx:BabyDuckParser.FuncsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#funcs.
    def exitFuncs(self, ctx:BabyDuckParser.FuncsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#funcion.
    def enterFuncion(self, ctx:BabyDuckParser.FuncionContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#funcion.
    def exitFuncion(self, ctx:BabyDuckParser.FuncionContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#retorno.
    def enterRetorno(self, ctx:BabyDuckParser.RetornoContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#retorno.
    def exitRetorno(self, ctx:BabyDuckParser.RetornoContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#parametros_opt.
    def enterParametros_opt(self, ctx:BabyDuckParser.Parametros_optContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#parametros_opt.
    def exitParametros_opt(self, ctx:BabyDuckParser.Parametros_optContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#parametros.
    def enterParametros(self, ctx:BabyDuckParser.ParametrosContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#parametros.
    def exitParametros(self, ctx:BabyDuckParser.ParametrosContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#lista_id.
    def enterLista_id(self, ctx:BabyDuckParser.Lista_idContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#lista_id.
    def exitLista_id(self, ctx:BabyDuckParser.Lista_idContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#type.
    def enterType(self, ctx:BabyDuckParser.TypeContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#type.
    def exitType(self, ctx:BabyDuckParser.TypeContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#body.
    def enterBody(self, ctx:BabyDuckParser.BodyContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#body.
    def exitBody(self, ctx:BabyDuckParser.BodyContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#statement.
    def enterStatement(self, ctx:BabyDuckParser.StatementContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#statement.
    def exitStatement(self, ctx:BabyDuckParser.StatementContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#return_stmt.
    def enterReturn_stmt(self, ctx:BabyDuckParser.Return_stmtContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#return_stmt.
    def exitReturn_stmt(self, ctx:BabyDuckParser.Return_stmtContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#expresion.
    def enterExpresion(self, ctx:BabyDuckParser.ExpresionContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#expresion.
    def exitExpresion(self, ctx:BabyDuckParser.ExpresionContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#rel_op.
    def enterRel_op(self, ctx:BabyDuckParser.Rel_opContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#rel_op.
    def exitRel_op(self, ctx:BabyDuckParser.Rel_opContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#exp.
    def enterExp(self, ctx:BabyDuckParser.ExpContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#exp.
    def exitExp(self, ctx:BabyDuckParser.ExpContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#termino.
    def enterTermino(self, ctx:BabyDuckParser.TerminoContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#termino.
    def exitTermino(self, ctx:BabyDuckParser.TerminoContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#factor.
    def enterFactor(self, ctx:BabyDuckParser.FactorContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#factor.
    def exitFactor(self, ctx:BabyDuckParser.FactorContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#cte.
    def enterCte(self, ctx:BabyDuckParser.CteContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#cte.
    def exitCte(self, ctx:BabyDuckParser.CteContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#assign.
    def enterAssign(self, ctx:BabyDuckParser.AssignContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#assign.
    def exitAssign(self, ctx:BabyDuckParser.AssignContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#print_stmt.
    def enterPrint_stmt(self, ctx:BabyDuckParser.Print_stmtContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#print_stmt.
    def exitPrint_stmt(self, ctx:BabyDuckParser.Print_stmtContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#arg_print.
    def enterArg_print(self, ctx:BabyDuckParser.Arg_printContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#arg_print.
    def exitArg_print(self, ctx:BabyDuckParser.Arg_printContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#read_stmt.
    def enterRead_stmt(self, ctx:BabyDuckParser.Read_stmtContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#read_stmt.
    def exitRead_stmt(self, ctx:BabyDuckParser.Read_stmtContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#condition.
    def enterCondition(self, ctx:BabyDuckParser.ConditionContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#condition.
    def exitCondition(self, ctx:BabyDuckParser.ConditionContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#cycle.
    def enterCycle(self, ctx:BabyDuckParser.CycleContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#cycle.
    def exitCycle(self, ctx:BabyDuckParser.CycleContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#f_call.
    def enterF_call(self, ctx:BabyDuckParser.F_callContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#f_call.
    def exitF_call(self, ctx:BabyDuckParser.F_callContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#argumentos_opt.
    def enterArgumentos_opt(self, ctx:BabyDuckParser.Argumentos_optContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#argumentos_opt.
    def exitArgumentos_opt(self, ctx:BabyDuckParser.Argumentos_optContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#argumentos.
    def enterArgumentos(self, ctx:BabyDuckParser.ArgumentosContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#argumentos.
    def exitArgumentos(self, ctx:BabyDuckParser.ArgumentosContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#f_call_sin_pyc.
    def enterF_call_sin_pyc(self, ctx:BabyDuckParser.F_call_sin_pycContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#f_call_sin_pyc.
    def exitF_call_sin_pyc(self, ctx:BabyDuckParser.F_call_sin_pycContext):
        pass



del BabyDuckParser