# Code interpreter of the IPPcode23 language 

## Project 2 from [IPP](https://www.fit.vut.cz/study/course/IPP/.en) university course 2022/23

The script (interpret.py in Python 3.10) reads the XML representation of the program and the program
interprets it using input according to command line parameters and generates output.

## Requirements

- Python 3.10 installed

## Supported parameters

| Parameter | Description |
| ------------- | ------------- |
| ```--source```  | Parameter with file containing XML representation of source code   |
| ```--input```  | Parameter with file with inputs for the actual interpretation of the specified source code  |
| ```--help \| -h]``` | Displays help message |

At least one of the parameters (--source or --input) must always be specified. If one of them is missing, the missing data is read from the standard input.

## Usage

To run the script, use:
```bash
$ py interpret.py --source=path-to-source-file --input=path-to-input-file
```
Where ```--source``` parameter is the file containing XML representation of the program in **IPPcode23** language.

## Examples
Given file: 
```bash
$ cat example.xml
```
```
<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode23">
    <instruction order="1" opcode="DEFVAR">
        <arg1 type="var">GF@counter</arg1>
    </instruction>
    <instruction order="2" opcode="MOVE">
        <arg1 type="var">GF@counter</arg1>
        <arg2 type="string"></arg2>
    </instruction>
    <instruction order="3" opcode="LABEL">
        <arg1 type="label">while</arg1>
    </instruction>
    <instruction order="4" opcode="JUMPIFEQ">
        <arg1 type="label">end</arg1>
        <arg2 type="var">GF@counter</arg2>
        <arg3 type="string">aaa</arg3>
    </instruction>
    <instruction order="5" opcode="WRITE">
        <arg1 type="string">Proměnná\032GF@counter\032obsahuje\032</arg1>
    </instruction>
    <instruction order="6" opcode="WRITE">
        <arg1 type="var">GF@counter</arg1>
    </instruction>
    <instruction order="7" opcode="WRITE">
        <arg1 type="string">\010</arg1>
    </instruction>
    <instruction order="8" opcode="CONCAT">
        <arg1 type="var">GF@counter</arg1>
        <arg2 type="var">GF@counter</arg2>
        <arg3 type="string">a</arg3>
    </instruction>
    <instruction order="9" opcode="JUMP">
        <arg1 type="label">while</arg1>
    </instruction>
    <instruction order="10" opcode="LABEL">
        <arg1 type="label">end</arg1>
    </instruction>
</program>
```
Then running:
```bash
$ py interpret.py --source=example.xml
```
Output:
```
Proměnná\032GF@counter\032obsahuje\032\010Proměnná\032GF@counter\032obsahuje\032a\010Proměnná\032GF@counter\032obsahuje\032aa\010
```
## Final evaluation:
- Lexical analysis: **100%**
- Syntactic analysis: **100%**
- Semantic analysis: **100%**
- Running errors (detection): **72%**
- Interpretation of instructions: **80%**
- Command line options: **70%**
- Interpretation of non-trivial programs: **4%((


### Total Score: 5.89/9.00 (**90%**)
2.65/3.00 for implementation documentation

## Final: 8.54/12.00
