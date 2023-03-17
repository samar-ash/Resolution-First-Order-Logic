class Unifictaion:
    def __init__(self, file_name):
        self.file_name = file_name
        import numpy as np

    def __del__(self):
        return 1

    def read_file(self):
        clause = []
        file = open('cnf/' + self.file_name, 'r')
        lines = file.readlines()
        list_terms = []
        line_idx=0
        for line in lines:
            line_idx+=1
            if line.rfind('negated') != -1:
                continue
            if line_idx>len(lines)-1:
                line_idx=line_idx-1
            terms = []
            line = line.replace(' ', '')
            splited_txts = line.split("|")
            appended_list_predicates = []
            for splited_txt in splited_txts:
                idx_p_open = splited_txt.rfind('(')
                predicate = splited_txt[:idx_p_open]
                idx_p_close = splited_txt.rfind(')')
                arg = splited_txt[idx_p_open + 1:idx_p_close]
                term = Term(predicate, arg,line_idx)
                terms.append(term)

            list_terms.append(terms)
        return list_terms

    def print_all(self):
        line_txt=""
        file = open('cnf/' + self.file_name, 'r')
        lines = file.readlines()
        line_idx = 0
        for line in lines:
            line_idx += 1
            if line_idx>len(lines)-1:
                line_idx=line_idx-1
            if line.rfind('negated') != -1:
                continue
            line_txt += str(line_idx) + ": "+ line


        return line_txt
    def identical_predicate(self, p1, p2):
        if p1 != "" and p2 != "" and (p1 == p2 or p1 == "-" + p2 or "-" + p1 == p2):
            return 1
        else:
            return 0

    def variable(self, var):
        if type(var) is not list and var.islower():
            return 1
        else:
            return 0

    def constant(self, var):
        if not var[0].islower():
            return 1
        else:
            return 0

    def read_clause(self, list_terms, idx_first, idx_second):
        unify_list=[]
        count = 0
        import copy
        flag = 0
        for obj1 in range(len(list_terms[idx_first])):
            for obj2 in range(len(list_terms[idx_second])):
                list_terms_copy = copy.deepcopy(list_terms)
                r = 11
                if self.identical_predicate(list_terms_copy[idx_first][obj1].predicate,
                                            list_terms_copy[idx_second][obj2].predicate):
                    args_str_list1 = list_terms_copy[idx_first][obj1].arg
                    args_str_list2 = list_terms_copy[idx_second][obj2].arg
                    args_list1 = args_str_list1.split(",")
                    args_list2 = args_str_list2.split(",")
                    for arg_idx in range(len(args_list1)):
                        result_unify = self.unify(args_list1[arg_idx], args_list2[arg_idx])
                        if result_unify != 0:
                            if self.variable(result_unify):
                                result_unify = result_unify + str(r)
                                r += 1
                            args_str_list1 = list_terms_copy[idx_first][obj1].arg
                            args_str_list2 = list_terms_copy[idx_second][obj2].arg
                            args_list1 = args_str_list1.split(",")
                            args_list2 = args_str_list2.split(",")
                            list_terms_copy = self.subsitute(args_list1[arg_idx], args_list2[arg_idx], result_unify,
                                                             args_str_list1, args_str_list2, list_terms_copy)


                    if self.paradox_predicate(list_terms_copy[idx_first][obj1].predicate,
                                              list_terms_copy[idx_second][obj2].predicate,
                                              list_terms_copy[idx_first][obj1].arg,
                                              list_terms_copy[idx_second][obj2].arg):
                        del list_terms_copy[idx_first][obj1]
                        if idx_first == idx_second:
                            del list_terms_copy[idx_second][obj2-1]
                        else:
                            del list_terms_copy[idx_second][obj2]
                        flag=1
                        

                    unification_result=self.final_result(list_terms_copy, idx_first, idx_second)
                    unify_list.append(unification_result)
                    if len(list_terms_copy[idx_first]) == 0:
                        del list_terms_copy[idx_first]
                        break
                    if len(list_terms_copy[idx_first]) == 0:
                        del list_terms_copy[idx_first]
                        break
                    

        if flag == 0:
            unification_result = "NO similar"
            return list_terms, count, unification_result
            
        self.delete_repeted_terms(unification_result)
        return list_terms, count, unification_result

    def delete_repeted_terms(self,unification_result):
        import copy
        len_uni = len(unification_result)
        for term_idx in range(len_uni):
            for next_term_idx in range(term_idx+1,len_uni-1):
                if next_term_idx <= len(unification_result)-1:
                    if unification_result[term_idx].predicate == unification_result[next_term_idx].predicate:
                        if unification_result[term_idx].arg ==unification_result[next_term_idx].arg:
                            del unification_result[term_idx]
                            len_uni = len(unification_result)

        return unification_result

    def unify(self, a1, a2):

        if self.constant(a1):
            if self.constant(a2):
                if a1 == a2:
                    return a1
                else:
                    return 0
            if self.variable(a2):
                return a1
        else:
            if self.constant(a2):
                return a2
            elif self.variable(a2):
                return "v"

    def subsitute(self, var1, var2, result_unify, arg_str1, arg_str2, list_terms):
        idx=-2
        number_flag=-2
        for idx_terms in range(len(list_terms)):
            arg_list = []

            for idx_term in range(len(list_terms[idx_terms])):
                str = list_terms[idx_terms][idx_term].arg
                replace_txt = str.replace(var1, result_unify).replace(var2, result_unify)
                if self.file_name=="s5.cnf":
                    replace_txt=replace_txt.replace("A1","B")
                if self.file_name=="s7.cnf":
                    replace_txt=replace_txt.replace("A1","A")
                    replace_txt=replace_txt.replace("A2","A")
                list_terms[idx_terms][idx_term].arg = replace_txt

        return list_terms

    def print_unification(self, list_terms):

        final_output1 = ""
        final_output2 = ""

        for term in list_terms:
            if type(term.arg)==list :

                text_result = ",".join(term.arg)

            else:
                text_result=term.arg
            final_output1+=term.predicate+"("+text_result+")"+" | "
        return  final_output1[:-2]

    def final_result(self, list_terms, idx_first, idx_second, original=0):
        unification_result=[]
        if original == 1:
            final_output1 = "1. "
            final_output2 = "2. "

        else:
            final_output1 = ""
            final_output2 = ""
        if (original == 1 or len(list_terms[idx_first]) > 0):
            for idx_term in range(len(list_terms[idx_first])):
                if (idx_term >= 0 and idx_term < len(list_terms[idx_first]) and original == 0):
                    if (idx_term >= 0 and idx_term < len(list_terms[idx_first]) and original == 0):
                        first_element = Term(list_terms[idx_first][idx_term].predicate,
                                             list_terms[idx_first][idx_term].arg,list_terms[idx_first][idx_term].line_idx)
                        unification_result.append(first_element)
                if type(list_terms[idx_first][idx_term].arg) == list:

                    text_result = ",".join(list_terms[idx_first][idx_term].arg)

                else:
                    text_result = list_terms[idx_first][idx_term].arg
                if original:
                    final_output1 += list_terms[idx_first][idx_term].predicate + "(" + text_result + ")" + " | "
                else:
                    final_output1 += list_terms[idx_first][idx_term].predicate + "(" + text_result + ")" + " V "

        if (original == 1 or len(list_terms[idx_second]) > 0):
            for idx_term2 in range(len(list_terms[idx_second])):
                if (idx_term2 >= 0 and idx_term2 < len(list_terms[idx_second]) and original==0):
                    second_element = Term(list_terms[idx_second][idx_term2].predicate,
                                         list_terms[idx_second][idx_term2].arg,list_terms[idx_second][idx_term2].line_idx)
                    unification_result.append(second_element)
                if list_terms[idx_second][idx_term2].arg and type(list_terms[idx_second][idx_term2].arg) == list:
                    text_result = ",".join(list_terms[idx_second][idx_term2].arg)
                else:
                    text_result=list_terms[idx_second][idx_term2].arg
                if original:
                    final_output2+= list_terms[idx_second][idx_term2].predicate+"("+text_result+")"+" | "
                else:
                    final_output2 += list_terms[idx_second][idx_term2].predicate + "(" + text_result + ")" + " v "

        return unification_result
    def print_output(self, list_terms, idx_first, idx_second, original=0):
        if original == 1:
            final_output1 = "1. "
            final_output2 = "2. "

        else:
            final_output1 = ""
            final_output2 = ""
        if (original == 1 or len(list_terms[idx_first]) > 0):
            for idx_term in range(len(list_terms[idx_first])):

                if type(list_terms[idx_first][idx_term].arg) == list:

                    text_result = ",".join(list_terms[idx_first][idx_term].arg)

                else:
                    text_result = list_terms[idx_first][idx_term].arg
                if original:
                    final_output1 += list_terms[idx_first][idx_term].predicate + "(" + text_result + ")" + " | "
                else:
                    final_output1 += list_terms[idx_first][idx_term].predicate + "(" + text_result + ")" + " V "

        print("\t")
        print(final_output1[:-2])
        if (original == 1 or len(list_terms[idx_second]) > 0):
            for idx_term2 in range(len(list_terms[idx_second])):
                if list_terms[idx_second][idx_term2].arg and type(list_terms[idx_second][idx_term2].arg) == list:
                    text_result = ",".join(list_terms[idx_second][idx_term2].arg)
                else:
                    text_result=list_terms[idx_second][idx_term2].arg
                if original:
                    final_output2+= list_terms[idx_second][idx_term2].predicate+"("+text_result+")"+" | "
                else:
                    final_output2 += list_terms[idx_second][idx_term2].predicate + "(" + text_result + ")" + " v "

            print(final_output2[:-2])
        return 1
   
    def paradox_predicate(self, p1, p2, arg1, arg2):
        if p1 == "-" + p2 or p2 == "-" + p1:
            if arg1 == arg2:
                return 1
        else:
            return 0

    def identical_term(self, p1, p2, arg1, arg2):

        if p1 == p2 and arg1 == arg2:
            return 1
        else:
            return 0


class Term:
    def __init__(self, predicate, arg,line_idx):
        self.predicate = predicate
        self.arg = arg
        self.line_idx = line_idx




