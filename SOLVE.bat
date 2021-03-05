:: 	Starten der stationaeren EDSPN Analyse unter Windows

@echo on

set startTime=%time%
set currentdir=%cd%\


GOTO END_USAGE

# show usage for help
:USAGE
  echo.
  echo Usage:
  echo SOLVE_win netname -E [-s^|-p] [-d^|-i maxiter] [-a bits] [epsilon] [truncerror]
  echo SOLVE_win netname -I maxiter [-s^|-p] [-u^|-l^|-r seedval] [-v] [-a bits] [epsilon] [truncerror]
  echo.
  echo E: EMC explicit solution method   I: fill-in avoidance solution method
  echo s: sequential execution           p: distributed execution
  echo d: direct solve of LGS            i: iterative solve of LGS
  echo u: uniform initial vector         r: random initial vector
  echo l: load initial vector from file  v: save stationary vector
  echo a: use arbitrary precision      
  echo.
  GOTO END_SOLVE
:END_USAGE

if "%1" == "" (
  echo %usage%
  GOTO END_SCRIPT
) else (
  set NETNAME=%1
)
set MODELDIR=%currentdir%%netname%.dir
set TNETHOME=C:\Program Files (x86)\TimeNET
set BIN_DIR=C:\Program Files (x86)\TimeNET\TimeNET\EDSPN\StatAnalysis\bin
set SHARED_BIN_DIR=C:\Program Files (x86)\TimeNET\TimeNET\EDSPN\Shared\bin
set NET=%currentdir%%NETNAME%

if NOT EXIST "%NET%.TN" (
  echo %NET%.TN: No such net
  GOTO USAGE
)  

if "%2" == "-E" (
  set SOL_METHOD=EMC_explicit
  GOTO EMC_PARSE
)

if "%2" == "-I" (
  set SOL_METHOD=FI_avoidance
  GOTO FI_PARSE
)
  
echo ERROR: use one of [-E^|-I] for solution method  
GOTO USAGE
  
:EMC_PARSE

if "%3" == "-s" (
  set EXEC_MODE=sequential
) else if "%3" == "-p" (
  set EXEC_MODE=parallel
) else (
  echo ERROR: use one of [-s^|-p] for execution mode
  GOTO USAGE 
)

if "%4" == "-d" (
  set SOL_MODE=-a
  set MAX_ITER=5000
) else if "%4" == "-i" (
  set SOL_MODE=-i
  set MAX_ITER=%5
  shift
) else (
  echo ERROR: use one of [-d^|-i maxiter] for solve LGS
  GOTO USAGE 
)

if "%5" == "-a" (
  set ARB_BITS=%6
  shift
  shift
) else (
  set ARB_BITS=0
)

if "%5" == "" (
  set EPSILON=1e-07
) else (
  set EPSILON=%5
)

if "%6" == "" (
  set TRUNC_ERROR=1e-07
) else (
  set TRUNC_ERROR=%6
)

GOTO END_PARSE

:FI_PARSE

shift

set MAX_ITER=%2
shift
if "%2" == "-s" (  
  set EXEC_MODE=sequential
) else (
  set EXEC_MODE=parallel
)

if "%3" == "-l" (
  set INIT_VEC=load
  set SEED_VAL=0
) else if "%3" == "-u" (
  set INIT_VEC=uniform
  set SEED_VAL=0
) else if "%3" == "-r" (
  set INIT_VEC=random
  set SEED_VAL=%4
  shift
) else (
  echo ERROR: use one of [-u^|-l^|-r seedval] for fill-in avoidance SM
  GOTO USAGE 
)

if "%4%" == "-v" (
  set SAVE_VEC=yes
  shift
) else (
  set SAVE_VEC=no
)

if "%4%" == "-a" (
  shift
  set ARB_BITS=%4
  shift
) else (
  set ARB_BITS=0
)


if "%4" == "" (
  set EPSILON=1e-07
) else (
  set EPSILON=%4
)

if "%5" == "" (
  set TRUNC_ERROR=1e-07
) else (
  set TRUNC_ERROR=%5
)

:END_PARSE

:: write to AUX file


set AUX="%NET%.AUX"

echo SOLUTION METHOD steady-state > %AUX%
echo MODEL %NET% >> %AUX%
echo SOLUTION METHOD %SOL_METHOD% >> %AUX%

echo TRANSIENT ANALYSIS %EXEC_MODE% >> %AUX%

echo ARBITRARY BITS %ARB_BITS% >> %AUX%
echo EPSILON %EPSILON% >> %AUX%
echo TRUNCATION ERROR %TRUNC_ERROR% >> %AUX%
:: start stationary analysis ...

echo.
echo STEADY STATE SOLUTION OF NET %NETNAME%
echo.

:: remove old results
if EXIST "%NET%.RESULTS" (
echo Removing previous results "%NET%.RESULTS"
del "%NET%.RESULTS"
)
if EXIST "%NET%.dir\%NETNAME%.RESULTS" (
echo Removing previous results "%NET%.dir\%NETNAME%.RESULTS"
del "%NET%.dir\%NETNAME%.RESULTS"
)
echo.

:: execute 'proc_TN'

"%SHARED_BIN_DIR%\proc_tn.exe" %NETNAME%

if ERRORLEVEL 1 (
  echo.
  echo ERROR occurred while proc_TN execution.
  echo SOLUTION OF MODEL %NETNAME% FAILED.
  echo.
  GOTO END_SCRIPT
)

:: execute 'struct_tn'

"%SHARED_BIN_DIR%\struct_tn.exe" -i %NETNAME%

if ERRORLEVEL 1 (
  echo.
  echo ERROR occurred while struct_tn execution.
  echo SOLUTION OF MODEL %NETNAME% FAILED.
  echo.
  GOTO END_SCRIPT
)

:: build 'derive_SMC.exe'

gcc -c "%NET%.dir\%NETNAME%_MDF.c" -o "%NET%.dir\%NETNAME%_MDF.obj"
g++ -o "%NET%_derive_SMC.exe" "%NET%.dir\%NETNAME%_MDF.obj" "%BIN_DIR%\libderive_SMC_win.a" -lstdc++ -L"%BIN_DIR%" -lsolve_Factors_win -lparse_definition_win -lrand_procs_win -lmem_win -L"%SHARED_BIN_DIR%" -lsysdep_win -larbPrec_win -lws2_32

if ERRORLEVEL 1 (
  echo.
  echo ERROR occurred while building derive_SMC.exe.
  echo SOLUTION OF MODEL %NETNAME% FAILED.
  echo.
  GOTO END_SCRIPT
)

if "%SOL_METHOD%" == "EMC_explicit" (
"%NET%_derive_SMC.exe" -f %NETNAME% %SOL_METHOD% %EXEC_MODE% %ARB_BITS% %EPSILON% %TRUNC_ERROR%
) else (
"%NET%_derive_SMC.exe" -f %NETNAME% %SOL_METHOD% %EXEC_MODE% %ARB_BITS% %EPSILON% %TRUNC_ERROR% %MAX_ITER% %INIT_VEC% %SEED_VAL% %SAVE_VEC%
)

if ERRORLEVEL 1 (
  echo.
  echo ERROR occurred while derive_SMC execution.
  echo SOLUTION OF MODEL %NETNAME% FAILED.
  echo.
  GOTO END_SCRIPT
)

:: execute 'solve_LGS' in case of EMC explicit solution method

if "%SOL_METHOD%" == "EMC_explicit" (
  "%BIN_DIR%\solve_LGS.exe" %SOL_MODE% %NETNAME% %MAX_ITER% %EPSILON%

  if ERRORLEVEL 2 (
	set NO_CONVERSION=1
	GOTO SKIP_IF_1
  )
  if ERRORLEVEL 1 (
    echo.
    echo ERROR occurred while solve_LGS execution.
    echo SOLUTION OF MODEL %NETNAME% FAILED.
    echo.
    GOTO END_SCRIPT
  )
)
:SKIP_IF_1


:: build 'derive_RES.exe'
gcc -c "%NET%.dir\%NETNAME%_ERC.c" -o "%NET%.dir\%NETNAME%_ERC.obj"
g++ -o "%NET%_derive_RES.exe" "%NET%.dir\%NETNAME%_ERC.obj" "%BIN_DIR%\libderive_RES_win.a" -L"%SHARED_BIN_DIR%" -lsysdep_win -lws2_32

if ERRORLEVEL 1 (
  echo.
  echo ERROR occurred while building derive_RES.exe.
  echo SOLUTION OF MODEL %NETNAME% FAILED.
  echo.
  GOTO END_SCRIPT
)

:: derive results
"%NET%_derive_RES.exe" %NETNAME% %EPSILON% 

if ERRORLEVEL 1 (
  echo.
  echo ERROR occurred while derive_RES execution.
  echo SOLUTION OF MODEL %NETNAME% FAILED.
  echo.
  GOTO END_SCRIPT
)

:: echo INITIAL VECTOR %INIT_VEC% >> %AUX%
:: echo SEED VALUE %SEED_VAL% >> %AUX%
:: echo SAVE VECTOR %SAVE_VEC% >> %AUX%

 
:END_SCRIPT
echo Removing temporary files.

if "%NO_CONVERSION%" == 1 (
echo WARNING: Solution obtained but with NO CONVERGENCE, try to increase: Max. iterations linear system solution, or use direct solver.
)
	
if EXIST "%NET%.graph" (
del /Q "%NET%.graph" >NUL 2>&1
)
if EXIST "%NET%_MDF.c" (
del /Q "%NET%_MDF.c" >NUL 2>&1
)
if EXIST "%NET%_MDF.obj" (
del /Q "%NET%_MDF.obj" >NUL 2>&1
)

if EXIST "%NET%.gst" (
del /Q "%NET%.gst" >NUL 2>&1
)
if EXIST "%NET%_ERC.c" (
del /Q "%NET%_ERC.c" >NUL 2>&1
)
if EXIST "%NET%_ERC.obj" (
del /Q "%NET%_ERC.obj" >NUL 2>&1
)

for %%K in ("%NET%.*.time") do del /Q "%%K"
for %%K in ("%NET%.*.mem") do del /Q "%%K"

if EXIST "%NET%.DEFINFO" (
del /Q "%NET%.DEFINFO" >NUL 2>&1
)
if EXIST "%NET%.RES" (
del /Q "%NET%.RES" >NUL 2>&1
)

if EXIST %AUX% (
del /Q %AUX% >NUL 2>&1
)

for %%K in ("%NET%.EMC*") do del /Q "%%K"
for %%K in ("%NET%.CONV*") do del /Q "%%K"

if EXIST "%NET%.RATES" (
del /Q "%NET%.RATES" >NUL 2>&1
)
if EXIST "%NET%.PROBMARK" (
del /Q "%NET%.PROBMARK" >NUL 2>&1
)
if EXIST "%NET%.pmf" (
del /Q "%NET%.pmf" >NUL 2>&1
)
if EXIST "%NET%.FIREFREQ" (
del /Q "%NET%.FIREFREQ" >NUL 2>&1
)

if EXIST "%NET%_derive_RES.exe" (
del /Q "%NET%_derive_RES.exe" >NUL 2>&1
)
if EXIST "%NET%_derive_SMC.exe" (
del /Q "%NET%_derive_SMC.exe" >NUL 2>&1
)

if NOT EXIST "%NET%.dir" (
  md "%NET%.dir"
)

if EXIST "%NET%.dir\%NETNAME%.vg" (
del /Q "%NET%.dir\%NETNAME%.vg" >NUL 2>&1
)
if EXIST "%NET%.dir\%NETNAME%_reach_graph.pdf" (
del /Q "%NET%.dir\%NETNAME%_reach_graph.pdf" >NUL 2>&1
)
if EXIST "%NET%.dir\%NETNAME%_reach_graph.gif" (
del /Q "%NET%.dir\%NETNAME%_reach_graph.gif" >NUL 2>&1
)
if EXIST "%NET%.dir\%NETNAME%_reach_graph.svg" (
del /Q "%NET%.dir\%NETNAME%_reach_graph.svg" >NUL 2>&1
)
if EXIST "%NET%.dir\%NETNAME%_reach_graph.png" (
del /Q "%NET%.dir\%NETNAME%_reach_graph.png" >NUL 2>&1
)
if EXIST "%NET%.dir\%NETNAME%_reach_graph.html" (
del /Q "%NET%.dir\%NETNAME%_reach_graph.html" >NUL 2>&1
)

if EXIST "%NET%.RG" (
move "%NET%.RG" "%NET%.dir" >NUL 2>&1
)
if EXIST "%NET%.MDET_*" ( 
move "%NET%.MDET_*" "%NET%.dir" >NUL 
)
if EXIST "%NET%.DELTA_*" ( 
move "%NET%.DELTA_*" "%NET%.dir" >NUL 
)
if EXIST "%NET%.RESULTS" (
move "%NET%.RESULTS" "%NET%.dir" >NUL 2>&1
)
if EXIST "%NET%.STRUCT" (
move "%NET%.STRUCT" "%NET%.dir" >NUL 2>&1
)
if EXIST "%NET%.INV" (
move "%NET%.INV" "%NET%.dir" >NUL 2>&1
)
if EXIST "%NET%.ECS" (
move "%NET%.ECS" "%NET%.dir" >NUL 2>&1
)
if EXIST "%NET%.TN" (
move "%NET%.TN" "%NET%.dir" >NUL 2>&1
)
if EXIST "%NET%.PROBTOK" (
move "%NET%.PROBTOK" "%NET%.dir" >NUL 2>&1
)

echo Start Time: %startTime%
echo Finish Time: %time%

cd %currentdir%
