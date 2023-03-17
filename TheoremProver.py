import unification as uni
import copy
a = uni.Unifictaion("unprovable4.cnf")
list_terms = a.read_file()
list_terms2 = copy.deepcopy(list_terms)
idx_first=0
idx_last=len(list_terms2)-1
last_element=list_terms2[-1]
unification_result=[]
unification_result.append(last_element)

len_list_term=len(list_terms2)
flag_res = 0

result_unify=[]
all=a.print_all()
print(all)
count_resolution=0
flag_proof=0
while len(unification_result)>0:

        for element_idx in range(len(list_terms2)-1):
            list_terms, count, unification_result = a.read_clause(list_terms2, element_idx, idx_last)
            if len(unification_result) == 0:
                count_resolution += 1
                flag_res=1
                flag_proof=1
                print(element_idx + 1, "and", idx_last + 1, "gives",":<empty>")
                break
            elif unification_result != "NO similar":
                flag_res = 1
                count_resolution += 1
                list_terms2.append(unification_result)
                print(element_idx + 1, "and", idx_last + 1, "gives",len(list_terms2),":", a.print_unification(unification_result)
                      )
            else:
                continue
        if flag_res==0:

            break
        else:
            len_list_term=len(list_terms2)
            idx_last=idx_last+1
            if idx_last > len(list_terms2)-1:
                if flag_proof==0:
                    print("No proof existen")
                    break
if count_resolution == 0:
    print("No proof existen")
print(count_resolution,"total resolutions")
