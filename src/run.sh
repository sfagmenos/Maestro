#!/bin/bash
	filename="tests/test"
    testname="Test"
	ext=".ms"
    red='\x1B[0;31m'
    NC='\x1B[0m'

function err_handle {
    status=$?
    # echo status was $status

    if [[ $status -ne 0 ]]; then
        echo -e "${red}Maestro Program Failed${NC}"
            
        if [[ $status -eq 1 ]]; then
            echo -e "${red}Key/Attribute Error${NC}"
            echo "---------------------------------"
        continue
        elif [[ $status -eq 255 ]]; then
            echo -e "${red}Test File Not Found${NC}"
            echo "---------------------------------"
            continue
        fi
        echo "---------------------------------"
        continue
    elif [[ $status -eq 0 ]]; then
        echo -e "$(tput setaf 2)Maestro Program Passed${NC}"
    fi
}

trap 'err_handle' ERR
echo "---------------------------------"
for VARIABLE in {0..77}
do
echo -e "$(tput setaf 1)$(tput bold)$(tput setab 7)$testname$VARIABLE$ext$(tput sgr 0)"
	echo "---------------------------------"
	output=$(python myacc.py $filename$VARIABLE$ext)

    if [[ -n $output ]]; then
        echo "Output: ""$output"
    else
        echo "Empty Output"
    fi

    if [[ $output == *Illegal* ]]
        then
            echo -e "${red}Test Failed - Illegal token resulting in syntax error${NC}"
    # elif [[ $output == *Syntax* ]]
    #     then
    #         echo -e "${red}Test Failed - Syntax error${NC}"
    else
         echo -e "$(tput setaf 2)Test Passed${NC}"
    fi
    echo "---------------------------------"
done