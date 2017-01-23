with open('input_file.csv', 'rb') as original:
    with open('output2.csv', 'rb') as output:
        original_lines = original.read().splitlines()
        output_lines = output.read().splitlines()
        equal = 0
        not_equal = 0
        for i in range(len(original_lines)):
            original_data = original_lines[i].split(',')
            output_data = output_lines[i].split(',')
            for k in range(len(original_data)):
                equal += 1
                if not original_data[k]==output_data[k]:
                    print "original_data", original_data[k]
                    print "output_data", output_data[k]
                    not_equal += 1
        print "RESULT: equal=", equal, "AND not_equal=", not_equal