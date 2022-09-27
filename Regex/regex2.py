import sys
answers = [
    r'/[xo.]{64}$/i',
    r'/^[xo]*\.[xo]*$/i',
    r'/^(x+o*)?\.|\.(o*x+)?$/i',
    r'/^.(..)*$/s',
    r'/^(1?0|11)([10]{2})*$/',
    r'/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i',
    r'/^(1?0)*1*$/',
    r'/^[bc]*[abc][bc]*$/',
    r'/^(b|c|a[bc]*a)+$/',
    r'/^((2|1[02]*1)0*)+$/'
]
print(answers[int(sys.argv[1])-40])