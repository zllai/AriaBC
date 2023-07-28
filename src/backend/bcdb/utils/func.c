//#include "bcdb/middleware.h"
//
//Datum
//bcdb_submit_tx(PG_FUNCTION_ARGS)
//{
//    text	   *string = PG_GETARG_TEXT_PP(0);
//    bool	    result;
//
//    if (arg1 < 0)
//        ereport(ERROR,
//                (errcode(ERRCODE_INVALID_ARGUMENT_FOR_POWER_FUNCTION),
//                        errmsg("cannot take square root of a negative number")));
//
//    result = sqrt(arg1);
//
//    check_float8_val(result, isinf(arg1), arg1 == 0);
//    PG_RETURN_BOOL(true);
//}
