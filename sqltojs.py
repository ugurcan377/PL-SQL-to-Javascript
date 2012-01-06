#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

def main():
    equ = { "number;":"var","varchar":"var","date;":"var","boolean;":"var"," =":" ==","<>":"!=","||":"+","--":"//","and":"&&","not ":"!",
            "then":"{","else":"} else {","end if;":"}","loop":"{","end loop;":"}","do":"","for":"for","declare":"","begin":"","end;":"",
            "dbms_output.put_line":"console.log"}
    equlater = { ":=":"=" ,"elsif":"} else if"}
    arg = sys.argv[1:]
    if ("-o" in arg):
        ina = arg[0]
        outa = arg[2]
    else:
        ina = arg[0]
        outa = "output.txt"
    try:
        inf = open(ina,"r")
    except IOError:
        print ina,"No such file exits"
        sys.exit()
    outf = open(outa,"w")
    text  = inf.readlines()
    for key in equ.keys():
        chh = []
        ch0 = []
        ch = []
        if (equ[key] == "var"):
            for line in text:
                if (key == "varchar"):
                    reg = re.compile("varchar2\(.*\);")
                    tline = reg.sub("var",line)
                elif (key in ["boolean;","date;","number;"]):
                    tline = line.replace(key,equ[key])

                if ("var"  in tline and not tline.startwith("var")):
                    temp = tline.split(" ")
                    temp[-1] = temp[-1].rstrip(";\n")
                    temp.reverse()
                    temp[-1] = temp[-1] + ";\n"
                    test = " ".join(temp)
                    text[text.index(line)] = " ".join(temp)
        elif (key == "do"):
            t1 = 0
            t0 = 0
            for line in text:
                i = text.index(line)
                if (line.startswith("loop")):
                    ch0.append(i)
                if ("end loop" in line):
                    ch.append(i)
                if ("exit" in line):
                    chh.append(i)
            for t1 in ch0:
                temp = [i for i in ch if i>t1]
                j=1000
                for i in temp:
                    if i-t1 < j:
                        j=i
                text[t1] = "do {\n"
                text[j] = "} while(true);\n"
            for t0 in chh:
                temp = text[t0].replace("exit when","")
                temp = temp.rstrip(";\n")
                text[t0] = "if (%s) break;\n" %(temp)
        elif (key == "for"):
            lcount = []
            for line in text:
                i = text.index(line)
                if (line.startswith("for")):
                    lcount.append(i)
            for i in lcount:
                temp = text[i].split(" ")
                temp[-1] = temp[-1].rstrip("\n")
                temp.remove("for")
                temp.remove("in")
                temp.remove("loop")
                temp[1] = temp[1].split("..")
                test = "%s=%s;%s<%s;%s++" %(temp[0],temp[1][0],temp[0],temp[1][1],temp[0])
                text[i] = "for(%s) {\n" %test

        else:
            for line in text:
                text[text.index(line)] = line.replace(key,equ[key])

    for key in equlater.keys():
        for line in text:
            text[text.index(line)] = line.replace(key,equlater[key])
    outf.writelines(text)
    print ina,"file has successfully translated to",outa
    inf.close()
    outf.close()

if __name__ == '__main__':
    main()
