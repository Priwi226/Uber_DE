celkove_minuty = 180

# Vypočítajte hodiny a minúty
hodiny = celkove_minuty // 60
minuty = celkove_minuty % 60

# Vytvorte reťazec s hodinami a minutami vo formáte "hodiny.minuty"
cas = f"{hodiny}.{minuty:02}"

print(cas)
print(type(cas))