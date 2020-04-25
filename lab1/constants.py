fuzzer_filename = "java_files/fuzzer.java"
classes_filename = "java_files/classes.java"
i_filename = "java_files/I.java"

bracket_closeRe = '(^\s*})'  # Regex for close bracket

typeIntRe = '((int)(\[?\]?)\s([\w\d]+))'
typeStringRe = '((String)(\[?\]?)\s([\w\d]+))'
typeBoolRe = '((boolean)(\[?\]?)\s([\w\d]+))'

booleanRe1 = '([\s\[\{\,](true)[\;\}\,])'  # for a354505667.equals("e"
booleanRe2 = '([\s\[\{\,](false)[\;\}\,])'  # for a354505667.equals("e"
stringRe = '([\s\[\{\,](\"\w*\")[\;\}\,])'  # for a354505667.equals("e"
numberRe = '(([\s\[\{\,])(-?\d+)([\;\}\,]))'  # for a354505667.equals("e"

addRe = '((-?[\.\w\d]+)\s*\+\s*(-?[\.\w\d]+))'
delRe = '((-?[\.\w\d]+)\s*\-\s*(-?[\.\w\d]+))'
mulRe = '((-?[\.\w\d]+)\s*\*\s*(-?[\.\w\d]+))'
divRe = '((-?[\.\w\d]+)\s*\/\s*(-?[\.\w\d]+))'
modRe = '((-?[\.\w\d]+)\s*\%\s*(-?[\.\w\d]+))'
indRe = '(([\.\w\d]+)\[([-*\.\w\d]+)\])'
varRe = '(([\[\s\(])\(([\.\w\d]+)\))'

equalsRe = '(([\.\w\d]+)\.equals\(("?[-*\.\w\d]+"?)\))'  # for a354505667.equals("e"
isisRe = '(([-*\.\w\d]+)\s*==\s*([-*\.\w\d]+))'  # for a1542761177 == 2
leRe = '(([-*\.\w\d]+)\s*<\s*([-*\.\w\d]+))'  # for a1542761177 == 2
geRe = '(([-*\.\w\d]+)\s*>\s*([-*\.\w\d]+))'  # for a1542761177 == 2
leqRe = '(([-*\.\w\d]+)\s*<=\s*([-*\.\w\d]+))'  # for a1542761177 == 2
geqRe = '(([-*\.\w\d]+)\s*>=\s*([-*\.\w\d]+))'  # for a1542761177 == 2
andRe = '(([\.\w\d]+)\s*\&\&\s*([\.\w\d]+))'  # for a1542761177 == 2
orRe = '(([\.\w\d]+)\s*\|\|\s*([\.\w\d]+))'  # for a1542761177 == 2
notRe = '(!([\.\w\d]+))'  # for a1542761177 == 2
boolRe = '(([\!\[\s\(])\(([\.\w\d]+)\))'

assignRe = '(([\.\w\d]+)\s*=\s*(\"?[-*\.\w\d]+\"?)\s*;)'  # for a354505667.equals("e"
printRe = '((System.out.println))'  # for a354505667.equals("e"
ifRe = '(if\(([\.\w\d]+)\))'  # for a354505667.equals("e"

mainRe = '(\s(Problem[\d]+))'  # for a354505667.equals("e"

readRe = '((stdin.readLine\(\)))'  # for a354505667.equals("e"

function_declarationRe = '^((\w+)(\s+)?){3,4}\([^!@#$+%^]+?\)\s+?{'
function_callRe = '((\w)+)(\s+)?\((\w+)?(\s*,\s*\w+)*\s*\);'
array_initializationRe = '{\s*("?\w+"?)\s*((,\s*("?\w+"?))+)?\s*}'

debug_graph = False
